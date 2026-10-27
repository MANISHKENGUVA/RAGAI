from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    company_id: str = Field(min_length=1, max_length=128)
    question: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("company_id", "question")
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Value must not be blank.")
        return normalized