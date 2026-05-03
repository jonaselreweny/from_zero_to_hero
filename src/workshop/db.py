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


def get_connection_settings() -> tuple[str, str, str, str]:
    load_environment()

    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE")

    if not uri or not username or not password or not database:
        raise ValueError(
            "Missing NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, or NEO4J_DATABASE in .env."
        )

    return uri, username, password, database


def get_driver():
    uri, username, password, _database = get_connection_settings()
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
    _uri, _username, _password, database = get_connection_settings()

    with get_driver() as driver:
        with driver.session(database=database, default_access_mode=READ_ACCESS) as session:
            result = session.run(query, parameters or {})
            return [{key: _serialize_value(value) for key, value in record.data().items()} for record in result]