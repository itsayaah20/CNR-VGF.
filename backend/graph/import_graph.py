import os
import pandas as pd
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

# ======================================================
# Configuration
# ======================================================

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD")

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATASET = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "net_risk_dataset.csv"
)

# ======================================================
# Connexion
# ======================================================

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

# ======================================================
# Import
# ======================================================

def import_graph():

    df = pd.read_csv(DATASET)

    # Pour le premier test
    df = df.head(1000)

    with driver.session() as session:

        session.run("MATCH (n) DETACH DELETE n")

        for _, row in df.iterrows():

            session.run("""

MERGE (c:CVE {id:$cve})

SET c.cvss=$cvss,
    c.priority=$priority

MERGE (a:Asset {id:$asset})

SET a.hostname=$hostname,
    a.type=$type

MERGE (app:Application {name:$application})

MERGE (a)-[:HOSTS]->(app)

MERGE (c)-[:AFFECTS]->(a)

""",

cve=row["CVE_ID"],
cvss=float(row["CVSS"]),
priority=row["Priority"],

asset=row["Asset_ID"],
hostname=row["Hostname"],
type=row["Asset_Type"],

application=row["Application"]

)

    print("Knowledge Graph importé avec succès.")

    driver.close()

if __name__ == "__main__":
    import_graph()