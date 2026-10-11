from fastapi import APIRouter

from backend.ai.llm import CyberLLM
from backend.api.schemas.request import AdvisorRequest

router = APIRouter()

advisor = CyberLLM()


@router.post("/advisor")
def ask_advisor(request: AdvisorRequest):

    context = """
    CVE_ID: CVE-2026-0544
    CVSS: 9.8
    EPSS: 0.003
    Priority: P2 - High
    """

    answer = advisor.ask(
        context,
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }
from fastapi import APIRouter

from backend.ai.llm import CyberLLM


router = APIRouter()

llm = CyberLLM()


@router.get("/advisor")
def advisor(question: str):

    context = """
    CVE: CVE-2026-0544
    CVSS: 9.8
    EPSS: 0.003
    Priority: P2
    Exposure Risk: 64
    """

    answer = llm.ask(
        context=context,
        question=question
    )

    return {
        "response": answer
    }