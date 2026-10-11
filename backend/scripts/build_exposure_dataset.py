import pandas as pd
import random
import os


# =====================================================
# Chemins
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


VULNERABILITY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "vulnerability_dataset.csv"
)


ASSET_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "asset_inventory.csv"
)


OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "exposure_dataset.csv"
)



# =====================================================
# Scores métier
# =====================================================

criticality_score = {

    "Critical": 100,
    "High": 75,
    "Medium": 50,
    "Low": 25

}



internet_score = {

    "Yes": 100,
    "No": 20

}



security_control_score = {

    "Yes": 20,
    "No": 0

}



# =====================================================
# Chargement datasets
# =====================================================

def load_data():

    print("Chargement des données...")


    vulnerabilities = pd.read_csv(
        VULNERABILITY_FILE
    )


    assets = pd.read_csv(
        ASSET_FILE
    )


    print(
        f"Vulnérabilités : {len(vulnerabilities)}"
    )


    print(
        f"Assets : {len(assets)}"
    )


    return vulnerabilities, assets




# =====================================================
# Matching CVE -> Asset
# =====================================================

def match_asset(asset, vulnerability):


    os_asset = str(
        asset["OS"]
    ).lower()


    description = str(
        vulnerability.get(
            "Description",
            ""
        )
    ).lower()



    if "windows" in os_asset and "windows" in description:

        return True



    if "linux" in os_asset and "linux" in description:

        return True



    if "oracle" in os_asset and "oracle" in description:

        return True



    # simulation exposition

    return random.random() < 0.15




# =====================================================
# Calcul Exposure Score
# =====================================================

def calculate_exposure_score(row):


    cvss = float(
        row["CVSS"]
        if pd.notna(row["CVSS"])
        else 0
    )



    epss = float(
        row["EPSS"]
        if pd.notna(row["EPSS"])
        else 0
    )



    criticality = criticality_score.get(
        row["Criticality"],
        25
    )



    internet = internet_score.get(
        row["Internet_Exposed"],
        20
    )



    # Exploitation réelle CISA KEV

    kev = 100 if row["Known_Exploited"] == 1 else 0



    # Protection

    edr = security_control_score.get(
        row["EDR"],
        0
    )


    firewall = security_control_score.get(
        row["Firewall"],
        0
    )


    security_controls = edr + firewall



    score = (

        (cvss / 10 * 100 * 0.30)

        +

        (epss * 100 * 0.20)

        +

        (criticality * 0.20)

        +

        (internet * 0.15)

        +

        (kev * 0.15)

        -

        (security_controls * 0.10)

    )



    if score < 0:

        score = 0



    if score > 100:

        score = 100



    return round(
        score,
        2
    )





# =====================================================
# Niveau risque
# =====================================================

def risk_level(score):


    if score < 30:

        return "Low"



    elif score < 60:

        return "Medium"



    elif score < 80:

        return "High"



    else:

        return "Critical"






# =====================================================
# Construction Dataset
# =====================================================

def build_exposure_dataset():


    vulnerabilities, assets = load_data()



    exposure_rows = []



    print(
        "Création relations CVE -> Asset..."
    )



    for _, vuln in vulnerabilities.iterrows():


        matched_assets = []



        for _, asset in assets.iterrows():


            if match_asset(
                asset,
                vuln
            ):

                matched_assets.append(asset)



        if len(matched_assets) == 0:

            matched_assets.append(
                assets.sample(1).iloc[0]
            )



        for asset in matched_assets:


            row = {


                "CVE_ID":
                    vuln["CVE_ID"],



                "Asset_ID":
                    asset["Asset_ID"],



                "Hostname":
                    asset["Hostname"],



                "Asset_Type":
                    asset["Type"],



                "Application":
                    asset["Application"],



                "CVSS":
                    vuln["CVSS"],



                "EPSS":
                    vuln["EPSS"],



                "Known_Exploited":
                    vuln.get(
                        "Known_Exploited",
                        0
                    ),



                "Criticality":
                    asset["Criticality"],



                "Internet_Exposed":
                    asset["Internet_Exposed"],



                "EDR":
                    asset["EDR"],



                "Firewall":
                    asset["Firewall"]

            }



            exposure_rows.append(row)





    exposure = pd.DataFrame(
        exposure_rows
    )



    print(
        "Calcul Exposure Score..."
    )



    exposure["Exposure_Score"] = exposure.apply(
        calculate_exposure_score,
        axis=1
    )



    exposure["Risk_Level"] = exposure[
        "Exposure_Score"
    ].apply(
        risk_level
    )



    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )



    exposure.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )



    print("\n==============================")
    print("Exposure Dataset créé")
    print("==============================")


    print(
        OUTPUT_FILE
    )


    print(
        f"Nombre lignes : {len(exposure)}"
    )


    print(
        exposure.head()
    )





# =====================================================
# Main
# =====================================================

if __name__ == "__main__":

    build_exposure_dataset()