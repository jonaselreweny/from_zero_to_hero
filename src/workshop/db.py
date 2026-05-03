from __future__ import annotations

from pathlib import Path
import os
from typing import Any

from dotenv import load_dotenv
from neo4j import GraphDatabase, READ_ACCESS
from neo4j.graph import Node, Path as Neo4jPath, Relationship


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_PATH = ROOT / ".env"


def load_environment(env_path: Path | None = None) -> None:
    load_dotenv(env_path or DEFAULT_ENV_PATH)


def get_connection_settings() -> tuple[str, str, str]:
    load_environment()

    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    if not uri or not username or not password:
        raise ValueError("Missing NEO4J_URI, NEO4J_USERNAME, or NEO4J_PASSWORD in .env.")

    return uri, username, password


def get_driver():
    uri, username, password = get_connection_settings()
    return GraphDatabase.driver(uri, auth=(username, password))


def _serialize_value(value: Any) -> Any:
    if isinstance(value, Node):
        return {
            "element_id": value.element_id,
            "labels": list(value.labels),
            "properties": dict(value.items()),
        }
    if isinstance(value, Relationship):
        return {
            "element_id": value.element_id,
            "type": value.type,
            "properties": dict(value.items()),
        }
    if isinstance(value, Neo4jPath):
        return {
            "nodes": [_serialize_value(node) for node in value.nodes],
            "relationships": [_serialize_value(rel) for rel in value.relationships],
        }
    if isinstance(value, list):
        return [_serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize_value(item) for key, item in value.items()}
    return value


def run_read_query(query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    with get_driver() as driver:
        with driver.session(default_access_mode=READ_ACCESS) as session:
            result = session.run(query, parameters or {})
            return [{key: _serialize_value(value) for key, value in record.data().items()} for record in result]