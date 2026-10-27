import unittest
from uuid import UUID

import httpx
from pydantic import ValidationError

from app.config import Settings
from app.main import create_app


class SettingsTests(unittest.TestCase):
    def test_app_name_is_configurable(self):
        settings = Settings(app_name="Narada test")

        self.assertEqual(settings.app_name, "Narada test")

    def test_app_name_must_not_be_blank(self):
        for app_name in ("", "   "):
            with self.subTest(app_name=app_name):
                with self.assertRaises(ValidationError):
                    Settings(app_name=app_name)


class ApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        transport = httpx.ASGITransport(
            app=create_app(Settings(app_name="Narada tests")),
            raise_app_exceptions=False,
        )
        self.client = httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        )

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_health_and_readiness_are_typed_and_identified(self):
        for path, status in (("/health", "ok"), ("/ready", "ready")):
            with self.subTest(path=path):
                response = await self.client.get(path)

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"status": status})
                UUID(response.headers["X-Request-ID"])

    async def test_invalid_chat_request_uses_documented_error_shape(self):
        response = await self.client.post(
            "/api/chat",
            json={"company_id": " ", "question": ""},
        )

        self.assertEqual(response.status_code, 422)
        error = response.json()["error"]
        self.assertEqual(error["code"], "validation_error")
        self.assertEqual(error["message"], "Request validation failed.")
        self.assertTrue(error["request_id"])
        self.assertTrue(error["details"])
        self.assertIn("field", error["details"][0])

    async def test_valid_chat_request_is_explicitly_not_implemented(self):
        response = await self.client.post(
            "/api/chat",
            json={"company_id": "workspace-1", "question": "What is RAG?"},
        )

        self.assertEqual(response.status_code, 501)
        self.assertEqual(
            response.json()["error"]["code"],
            "chat_not_implemented",
        )
        self.assertNotIn("answer", response.json())

    async def test_chat_request_enforces_top_k_bounds(self):
        for top_k in (0, 21):
            with self.subTest(top_k=top_k):
                response = await self.client.post(
                    "/api/chat",
                    json={
                        "company_id": "workspace-1",
                        "question": "What is RAG?",
                        "top_k": top_k,
                    },
                )

                self.assertEqual(response.status_code, 422)
                self.assertEqual(
                    response.json()["error"]["code"],
                    "validation_error",
                )

    async def test_http_error_uses_documented_error_shape(self):
        response = await self.client.get("/not-a-route")

        self.assertEqual(response.status_code, 404)
        error = response.json()["error"]
        self.assertEqual(error["code"], "http_error")
        self.assertEqual(error["message"], "Not Found")
        self.assertTrue(error["request_id"])

    async def test_unexpected_error_does_not_expose_exception_details(self):
        application = create_app(Settings(app_name="Narada tests"))

        async def fail():
            raise RuntimeError("private implementation detail")

        application.add_api_route("/test-error", fail)
        transport = httpx.ASGITransport(
            app=application,
            raise_app_exceptions=False,
        )
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            with self.assertLogs("app.main", level="ERROR") as captured:
                response = await client.get("/test-error")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["error"]["message"],
            "An unexpected error occurred.",
        )
        self.assertNotIn("private implementation detail", response.text)
        self.assertNotIn("private implementation detail", "\n".join(captured.output))


if __name__ == "__main__":
    unittest.main()
