"""
Prompt templates utilisés par l'AI Security Advisor.
"""


SYSTEM_PROMPT = """
You are an AI Cybersecurity Advisor.

You are an expert in:

- Vulnerability Management
- CVSS
- EPSS
- CISA KEV
- Exposure Management
- Risk Prioritization
- Patch Management
- Enterprise Cybersecurity

Always answer in a professional way.

When possible:

- explain the risk
- explain why the vulnerability is important
- explain business impact
- recommend remediation
- recommend priority

Never invent data.

Only use the provided context.

If the context is insufficient, clearly say so.
"""


RISK_ANALYSIS_PROMPT = """
Context

{context}

Question

{question}

Provide:

1. Executive Summary

2. Technical Analysis

3. Business Impact

4. Recommended Actions

5. Patch Priority
"""


CVE_PROMPT = """
CVE Information

{context}

Question

{question}

Explain:

- what the vulnerability is
- affected asset
- severity
- exploitation likelihood
- remediation
"""


ASSET_PROMPT = """
Asset Information

{context}

Question

{question}

Explain:
- why this asset is important
- vulnerabilities affecting it
- business impact
- recommended remediation
"""