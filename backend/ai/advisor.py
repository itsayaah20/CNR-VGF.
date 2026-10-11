from backend.ai.llm import CyberLLM

def build_context(data):

    return f"""
CVE_ID: {data['CVE_ID']}

CVSS: {data['CVSS']}

EPSS: {data['EPSS']}

Priority: {data['Priority']}

Business Risk: {data['Business_Risk']}

Exposure Risk: {data['Exposure_Risk']}

Recommendation: {data['Recommendation']}
"""


sample = {
    "CVE_ID": "CVE-2026-0544",
    "CVSS": 9.8,
    "EPSS": 0.003,
    "Priority": "P2 - High",
    "Business_Risk": 75,
    "Exposure_Risk": 64,
    "Recommendation": "Immediate remediation"
}


advisor = CyberLLM()

response = advisor.ask(
    build_context(sample),
    "Analyze this vulnerability."
)

print(response)