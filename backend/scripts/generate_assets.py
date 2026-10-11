import csv
import random
import os


# ===============================
# Configuration
# ===============================

OUTPUT_FILE = r"C:\Users\merei\OneDrive\Bureau\Stage swisslife\CNR-VGF\data\raw\asset_inventory.csv"

NUMBER_OF_ASSETS = 300


# ===============================
# Données réalistes
# ===============================

asset_types = [
    "Server",
    "Database",
    "Application Server",
    "Firewall",
    "Router",
    "Switch"
]


operating_systems = [
    "Windows Server 2022",
    "Windows Server 2019",
    "Linux Ubuntu",
    "Linux RedHat",
    "Oracle Linux",
    "Cisco IOS", 
    "Windows Server 2025",
    "RedHat Enterprise Linux 9",
    "Ubuntu Server 24.04 LTS",
    "Oracle Database 19c",
    "Microsoft SQL Server 2022"
]


environments = [
    "Production",
    "Test",
    "Development"
]


applications = [
    "Online Banking",
    "Customer Database",
    "Payment API",
    "CRM",
    "ERP",
    "Identity Management",
    "Email Service",
    "Security Monitoring",
    "HR Application",
    "Internal Portal"
]


owners = [
    "IT",
    "Security Team",
    "DevOps",
    "DBA",
    "Network Team",
    "Application Team"
]


data_sensitivity = [
    "Critical",
    "High",
    "Medium",
    "Low"
]


# ===============================
# Génération criticité
# ===============================

def generate_criticality():

    value = random.randint(1,100)

    if value <= 20:
        return "Critical"

    elif value <= 60:
        return "High"

    elif value <= 90:
        return "Medium"

    else:
        return "Low"



# ===============================
# Génération IP
# ===============================

def generate_ip(index):

    return f"10.10.{index//255}.{index%255}"



# ===============================
# Génération hostname
# ===============================

def generate_hostname(asset_type, index):

    prefix = {
        "Server": "SRV",
        "Database": "DB",
        "Application Server": "APP",
        "Firewall": "FW",
        "Router": "RTR",
        "Switch": "SW"
    }

    return f"{prefix[asset_type]}-{index:03d}"



# ===============================
# Création CSV
# ===============================


def generate_assets():


    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )


    columns = [
        "Asset_ID",
        "Hostname",
        "Type",
        "OS",
        "IP",
        "Environment",
        "Criticality",
        "Internet_Exposed",
        "Application",
        "Owner",
        "EDR",
        "Firewall",
        "Data_Sensitivity"
    ]


    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:


        writer = csv.DictWriter(
            file,
            fieldnames=columns
        )


        writer.writeheader()


        for i in range(1, NUMBER_OF_ASSETS + 1):


            asset_type = random.choice(asset_types)

            criticality = generate_criticality()


            # Les actifs critiques sont plus exposés
            if criticality == "Critical":

                internet = random.choice(
                    ["Yes","Yes","No"]
                )

            else:

                internet = random.choice(
                    ["Yes","No"]
                )


            row = {

                "Asset_ID":
                    f"ASSET-{i:04d}",


                "Hostname":
                    generate_hostname(
                        asset_type,
                        i
                    ),


                "Type":
                    asset_type,


                "OS":
                    random.choice(
                        operating_systems
                    ),


                "IP":
                    generate_ip(i),


                "Environment":
                    random.choice(
                        environments
                    ),


                "Criticality":
                    criticality,


                "Internet_Exposed":
                    internet,


                "Application":
                    random.choice(
                        applications
                    ),


                "Owner":
                    random.choice(
                        owners
                    ),


                "EDR":
                    random.choice(
                        ["Yes","No"]
                    ),


                "Firewall":
                    random.choice(
                        ["Yes","No"]
                    ),


                "Data_Sensitivity":
                    random.choice(
                        data_sensitivity
                    )
            }


            writer.writerow(row)



    print(
        f"✔ Asset inventory created : {OUTPUT_FILE}"
    )

    print(
        f"✔ Total assets : {NUMBER_OF_ASSETS}"
    )



# ===============================
# Main
# ===============================

if __name__ == "__main__":

    generate_assets()