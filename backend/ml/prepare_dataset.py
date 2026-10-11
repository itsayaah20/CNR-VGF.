import pandas as pd
import os



# =====================================
# Paths
# =====================================

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
    "net_risk_dataset.csv"
)


OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "ml_training_dataset.csv"
)



# =====================================
# Prepare ML Dataset
# =====================================

def prepare_dataset():


    print("Loading Net Risk Dataset...")


    df = pd.read_csv(
        INPUT_FILE
    )


    print(
        f"Original rows : {len(df)}"
    )



    # =====================================
    # Vérification colonnes
    # =====================================

    required_columns = [

        "CVSS",
        "EPSS",
        "Known_Exploited",
        "Technical_Risk",
        "Threat_Risk",
        "Business_Risk",
        "Exposure_Risk",
        "Asset_Type",
        "Priority",
        "Net_Risk_Score"

    ]


    for col in required_columns:

        if col not in df.columns:

            raise Exception(
                f"Colonne manquante : {col}"
            )



    # =====================================
    # Réduction Dataset
    # =====================================

    if len(df) > 300000:


        df = df.sample(
            300000,
            random_state=42
        )


    print(
        f"ML rows : {len(df)}"
    )



    # =====================================
    # Nettoyage valeurs nulles
    # =====================================

    df["CVSS"] = df["CVSS"].fillna(0)

    df["EPSS"] = df["EPSS"].fillna(0)

    df["Known_Exploited"] = (
        df["Known_Exploited"]
        .fillna(0)
    )



    # =====================================
    # Encoding Asset Type
    # =====================================


    asset_mapping = {


        "Server":1,

        "Database":2,

        "Application Server":3,

        "Firewall":4,

        "Router":5,

        "Switch":6

    }



    df["Asset_Type"] = (

        df["Asset_Type"]
        .map(asset_mapping)
        .fillna(0)

    )



    # =====================================
    # Création Label ML
    # =====================================

    # Le modèle apprend :
    # prédire les risques élevés


    df["Risk_Label"] = (

        df["Priority"]
        .apply(

            lambda x:

            1

            if x in [

                "P1 - Critical",

                "P2 - High"

            ]

            else 0

        )

    )



    # =====================================
    # Features Machine Learning
    # =====================================


    features = [

        "CVSS",

        "EPSS",

        "Known_Exploited",

        "Technical_Risk",

        "Threat_Risk",

        "Business_Risk",

        "Exposure_Risk",

        "Asset_Type"

    ]



    ml_dataset = df[

        features

        +

        [


            "Risk_Label"

        ]

    ]



    # =====================================
    # Export
    # =====================================


    ml_dataset.to_csv(

        OUTPUT_FILE,

        index=False,

        encoding="utf-8"

    )



    print("==============================")
    print("ML Training Dataset created")
    print("==============================")


    print(
        OUTPUT_FILE
    )


    print(
        ml_dataset.head()
    )


    print(
        ml_dataset["Risk_Label"].value_counts()
    )



# =====================================
# Main
# =====================================

if __name__ == "__main__":

    prepare_dataset()