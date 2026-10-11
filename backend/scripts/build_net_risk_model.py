import pandas as pd
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


INPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "exposure_dataset.csv"
)


OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "net_risk_dataset.csv"
)



# =====================================================
# Mapping métier
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


control_score = {

    "Yes": 0,
    "No": 20

}



# =====================================================
# Risk Factors
# =====================================================

def technical_risk(row):

    return min(
        float(row["CVSS"]) * 10,
        100
    )



def threat_risk(row):

    epss = float(row["EPSS"])

    kev = 100 if row["Known_Exploited"] == 1 else 0


    score = (
        (epss * 100 * 0.40)
        +
        (kev * 0.60)
    )

    return min(score,100)



def business_risk(row):

    return criticality_score.get(
        row["Criticality"],
        25
    )



def exposure_risk(row):

    internet = internet_score.get(
        row["Internet_Exposed"],
        20
    )

    edr = control_score.get(
        row["EDR"],
        20
    )

    firewall = control_score.get(
        row["Firewall"],
        20
    )


    score = (

        internet * 0.60

        +

        edr * 0.20

        +

        firewall * 0.20

    )

    return min(score,100)



# =====================================================
# Net Risk Score
# =====================================================

def calculate_net_risk(row):


    score = (

        row["Technical_Risk"] * 0.30

        +

        row["Threat_Risk"] * 0.25

        +

        row["Business_Risk"] * 0.25

        +

        row["Exposure_Risk"] * 0.20

    )


    return round(score,2)



# =====================================================
# Priority RSSI
# =====================================================

def priority(score):


    if score >= 80:

        return "P1 - Critical"


    elif score >= 60:

        return "P2 - High"


    elif score >= 30:

        return "P3 - Medium"


    else:

        return "P4 - Low"



def recommendation(priority):


    actions = {

        "P1 - Critical":
        "Patch immédiat, validation exposition externe, escalade RSSI",


        "P2 - High":
        "Correction urgente sous SLA court",


        "P3 - Medium":
        "Planification du correctif",


        "P4 - Low":
        "Surveillance continue"

    }


    return actions.get(
        priority,
        "Analyse nécessaire"
    )



# =====================================================
# Build Dataset
# =====================================================

def build_net_risk():


    print("Chargement Exposure Dataset...")


    df = pd.read_csv(
        INPUT_FILE
    )


    print(
        f"Lignes chargées : {len(df)}"
    )



    print(
        "Calcul facteurs risque..."
    )


    df["Technical_Risk"] = df.apply(
        technical_risk,
        axis=1
    )


    df["Threat_Risk"] = df.apply(
        threat_risk,
        axis=1
    )


    df["Business_Risk"] = df.apply(
        business_risk,
        axis=1
    )


    df["Exposure_Risk"] = df.apply(
        exposure_risk,
        axis=1
    )



    print(
        "Calcul Net Risk Score..."
    )


    df["Net_Risk_Score"] = df.apply(
        calculate_net_risk,
        axis=1
    )


    df["Priority"] = df["Net_Risk_Score"].apply(
        priority
    )


    df["Recommendation"] = df["Priority"].apply(
        recommendation
    )



    final_columns = [

        "CVE_ID",

        "Asset_ID",

        "Hostname",

        "Asset_Type",

        "Application",

        "CVSS",

        "EPSS",

        "Known_Exploited",

        "Technical_Risk",

        "Threat_Risk",

        "Business_Risk",

        "Exposure_Risk",

        "Net_Risk_Score",

        "Priority",

        "Recommendation"

    ]



    result = df[final_columns]


    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )


    result.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )


    print("\n==============================")
    print("Net Risk Dataset créé")
    print("==============================")

    print(
        OUTPUT_FILE
    )

    print(
        f"Nombre lignes : {len(result)}"
    )


    print(
        result.head()
    )



if __name__ == "__main__":

    build_net_risk()