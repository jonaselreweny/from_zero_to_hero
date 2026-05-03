from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from workshop.db import run_read_query
from workshop.queries import people_by_skill, similar_people


READ_ONLY_KEYWORDS = {
    "create",
    "merge",
    "delete",
    "detach",
    "set",
    "remove",
    "drop",
    "load csv",
    "call dbms",
}


mcp = FastMCP("from-zero-to-hero")


def _assert_read_only(query: str) -> None:
    lowered = query.lower()
    if any(keyword in lowered for keyword in READ_ONLY_KEYWORDS):
        raise ValueError("Only read-only Cypher is allowed in this workshop MCP server.")


@mcp.tool()
def run_cypher_read(query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Run a read-only Cypher query and return JSON-friendly results."""
    _assert_read_only(query)
    return run_read_query(query, parameters)


@mcp.tool()
def find_people_by_skill(skill_name: str, limit: int = 10) -> list[dict[str, Any]]:
    """Find people connected to a given skill."""
    return people_by_skill(skill_name=skill_name, limit=limit)


@mcp.tool()
def semantic_people_search(person_id: str, limit: int = 5) -> list[dict[str, Any]]:
    """Find people who are semantically similar to the given person."""
    return similar_people(person_id=person_id, limit=limit)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()