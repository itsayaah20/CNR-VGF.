import json
import pandas as pd
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parents[2]

json_file = BASE_DIR / "data" / "raw" / "nvdcve-2.0-2026.json"
output_file = BASE_DIR / "data" / "processed" / "vulnerabilities.csv"

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for item in data["vulnerabilities"]:
    cve = item["cve"]

    cve_id = cve.get("id", "")

    description = ""
    for d in cve.get("descriptions", []):
        if d["lang"] == "en":
            description = d["value"]
            break

    published = cve.get("published", "")
    modified = cve.get("lastModified", "")

    cvss = None
    severity = None

    metrics = cve.get("metrics", {})

    if "cvssMetricV31" in metrics:
        metric = metrics["cvssMetricV31"][0]["cvssData"]
        cvss = metric.get("baseScore")
        severity = metric.get("baseSeverity")

    elif "cvssMetricV40" in metrics:
        metric = metrics["cvssMetricV40"][0]["cvssData"]
        cvss = metric.get("baseScore")
        severity = metric.get("baseSeverity")

    vendor = ""
    product = ""

    affected = cve.get("affected", [])
    if affected:
        affected_data = affected[0].get("affectedData", [])
        if affected_data:
            vendor = affected_data[0].get("vendor", "")
            product = affected_data[0].get("product", "")

    rows.append({
        "CVE_ID": cve_id,
        "Published": published,
        "Last_Modified": modified,
        "CVSS": cvss,
        "Severity": severity,
        "Vendor": vendor,
        "Product": product,
        "Description": description
    })

df = pd.DataFrame(rows)

output_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False, encoding="utf-8")

print(df.head())
print(f"\n✅ {len(df)} CVE exportées vers :")
print(output_file)