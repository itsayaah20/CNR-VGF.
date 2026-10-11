import pandas as pd
import json
from pathlib import Path


# Chemin projet
BASE_DIR = Path(__file__).resolve().parents[2]


# Fichiers sources
vuln_file = BASE_DIR / "data" / "raw" / "nvd_cve_2026_clean.csv"

epss_file = BASE_DIR / "data" / "raw" / "epss_scores-2026-08-04.csv"

kev_file = BASE_DIR / "data" / "raw" / "known_exploited_vulnerabilities.json"


# Fichier résultat
output_file = BASE_DIR / "data" / "processed" / "vulnerability_dataset.csv"


# ============================
# 1. Charger les CVE NVD
# ============================

print("Chargement NVD...")

df = pd.read_csv(vuln_file)

print("Nombre CVE :", len(df))


# ============================
# 2. Charger EPSS
# ============================

print("Chargement EPSS...")


epss = pd.read_csv(
    epss_file,
    comment="#"
)


print(epss.head())
print(epss.columns)


# garder seulement les colonnes utiles

epss = epss[
    [
        "cve",
        "epss"
    ]
]


epss.columns = [
    "CVE_ID",
    "EPSS"
]


# Fusion

df = df.merge(
    epss,
    on="CVE_ID",
    how="left"
)


# ============================
# 3. Charger CISA KEV
# ============================

print("Chargement CISA KEV...")


with open(
    kev_file,
    "r",
    encoding="utf-8"
) as f:

    kev = json.load(f)



kev_list = []

for item in kev["vulnerabilities"]:
    kev_list.append(
        item["cveID"]
    )



df["Known_Exploited"] = (
    df["CVE_ID"]
    .isin(kev_list)
    .astype(int)
)



# ============================
# 4. Nettoyage
# ============================


df["EPSS"] = df["EPSS"].fillna(0)


df["Known_Exploited"] = (
    df["Known_Exploited"]
    .fillna(0)
)



# ============================
# 5. Export
# ============================


output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)


df.to_csv(
    output_file,
    index=False,
    encoding="utf-8"
)



print("\n✅ Dataset créé :")
print(output_file)


print("\nAperçu :")
print(df.head())