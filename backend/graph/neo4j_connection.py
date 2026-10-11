import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI", "neo4j://localhost:7687")

USER = os.getenv("NEO4J_USER", "neo4j")

PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)


with driver.session() as session:

    result = session.run(
        "RETURN 'Connected to Neo4j' AS message"
    )

    print(result.single()["message"])