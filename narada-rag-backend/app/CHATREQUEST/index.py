from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    company_id: str
    question: str = Field(min_length=1, max_length=1000)
    top_k: Optional[int] = Field(default=5, ge=1, le=20)

    def validationOfArgumentClass(self):
        return {
            "company_id": {
                "data_type": str,
                "validation": {
                    "required": True,
                }
            },
            "question": {
                "data_type": str,
                "validation": {
                    "required": True,
                    "min_length": 1,    # Added missing comma here
                    "max_length": 1000
                }
            },
            "top_k": {
                "data_type": int,
                "validation": {
                    "required": False,
                    "ge": 1,
                    "le": 20
                }
            }
        }