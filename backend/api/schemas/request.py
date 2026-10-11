from pydantic import BaseModel


class AdvisorRequest(BaseModel):
    question: str
    