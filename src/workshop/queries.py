from __future__ import annotations

import argparse
import json

from workshop.db import run_read_query

def overview(limit: int = 10) -> list[dict[str, object]]:
    query = """//cypher
    MATCH (person:Person)
    RETURN {
      person_id: person.id,
      display_name: coalesce(person.name, person.id),
      skills: COLLECT { MATCH (node)-[:KNOWS]->(s:Skill) RETURN DISTINCT s.name },
      domains: COLLECT {MATCH (node)-[:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(:Thing)-[:IN]->(d:Domain) RETURN DISTINCT d.name} 
    } AS summary
    LIMIT $limit
    """
    return run_read_query(query, {"limit": limit})


def people_by_skill(skill_name: str, limit: int = 10) -> list[dict[str, object]]:
    query = """//cypher
    MATCH (person:Person)-[:KNOWS]->(:Skill {name: $skill_name})
    RETURN person.id AS person_id, coalesce(person.name, person.id) AS display_name
    ORDER BY display_name
    LIMIT $limit
    """
    return run_read_query(query, {"skill_name": skill_name, "limit": limit})


def similar_people(person_id: str, limit: int = 5) -> list[dict[str, object]]:
    query = """//cypher
    CYPHER 25
    MATCH (source:Person {id: $person_id})
    MATCH (node:Person)
    SEARCH node IN (
      VECTOR INDEX person_embedding
      FOR source.embedding
      LIMIT $limit) SCORE AS score
    WHERE node.id <> source.id
    RETURN {
      person_id: node.id,
      display_name: coalesce(node.name, node.id),
      score: score,
      skills: COLLECT { MATCH (node)-[:KNOWS]->(s:Skill) RETURN DISTINCT s.name },
      domains: COLLECT {MATCH (node)-[:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(:Thing)-[:IN]->(d:Domain) RETURN DISTINCT d.name} 
    } AS similar_person
    ORDER BY similar_person.score DESC
    """
    return run_read_query(query, {"person_id": person_id, "limit": limit})


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run workshop Neo4j queries.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    overview_parser = subparsers.add_parser("overview", help="Show person summaries.")
    overview_parser.add_argument("--limit", type=int, default=10)

    skill_parser = subparsers.add_parser("skill", help="Find people by skill name.")
    skill_parser.add_argument("--skill-name", required=True)
    skill_parser.add_argument("--limit", type=int, default=10)

    similar_parser = subparsers.add_parser("similar", help="Run vector similarity for a source person.")
    similar_parser.add_argument("--person-id", required=True)
    similar_parser.add_argument("--limit", type=int, default=5)

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "overview":
        results = overview(limit=args.limit)
    elif args.command == "skill":
        results = people_by_skill(skill_name=args.skill_name, limit=args.limit)
    else:
        results = similar_people(person_id=args.person_id, limit=args.limit)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()