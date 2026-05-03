from pathlib import Path
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


ROOT = Path(__file__).resolve().parent
SEED_PATH = ROOT / "seed.cypher"


def _read_seed_statements(seed_path: Path) -> list[str]:
    raw_text = seed_path.read_text(encoding="utf-8")
    statements: list[str] = []

    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "cypherStatements" or stripped in {':begin', ':commit'}:
            continue

        normalized = stripped.replace(r'\"', '"')
        statements.append(normalized)

    joined = "\n".join(statements)
    return [statement.strip() for statement in joined.split(";") if statement.strip()]


def load_graph() -> None:
    load_dotenv(ROOT / ".env")

    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    if not uri or not user or not password:
        raise ValueError("Missing NEO4J_URI, NEO4J_USERNAME, or NEO4J_PASSWORD in environment.")

    queries = _read_seed_statements(SEED_PATH)

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        with driver.session() as session:
            for query in queries:
                session.run(query)

    print(f"Loaded {len(queries)} Cypher statements from {SEED_PATH.name}.")


if __name__ == "__main__":
    load_graph()