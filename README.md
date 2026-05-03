# From Zero to Hero

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/jonaselreweny/from_zero_to_hero)

Neo4j workshop for a 2-hour hands-on session in GitHub Codespaces. Participants learn the property graph model, write Cypher against an HR graph, use vector indexes for semantic retrieval, and finish by exposing the graph through a FastMCP server.

## What Participants Build

- A working Neo4j connection to an Aura Free database.
- A seeded HR graph with people, skills, projects, domains, and work types.
- Practical Cypher queries for traversal, filtering, and aggregation.
- A semantic retrieval flow using the existing `text_embeddings` vector index on `Person.embedding`.
- A read-only FastMCP server with graph and semantic search tools.

## Tech Stack

- Neo4j Aura Free
- GitHub Codespaces
- Python
- Neo4j Python Driver with Rust extension support
- FastMCP
- Neo4j for VS Code extension

## Audience

This workshop is designed for a mixed audience. The core path assumes participants are comfortable using a terminal and copying commands, but not necessarily familiar with Neo4j, Cypher, vector indexes, or MCP.

## Prerequisites

Before the session, participants should have:

1. A GitHub account with Codespaces access.
2. A Neo4j Aura Free database.

Aura Free is the recommended default for the workshop.

## Quick Start

### Option A: GitHub Codespaces

1. Open the repository in Codespaces using the badge above.
2. Wait for the devcontainer to finish installing dependencies.
3. Copy `example.env` to `.env`.
4. Fill in `NEO4J_URI`, `NEO4J_USERNAME`, and `NEO4J_PASSWORD` with your Aura credentials.
5. Run `python load_data.py` to create the schema and load the workshop data.

### Option B: Local Machine

1. Create a virtual environment.
2. Install dependencies with `pip install -e .`.
3. Copy `example.env` to `.env` and fill in your credentials.
4. Run `python load_data.py`.

## Safety Notes

- Do not commit `.env`.
- Keep `example.env` as the only version-controlled environment template.
- If you ever expose a real key or password, rotate it before sharing the repo.

## Workshop Agenda

| Time | Topic |
| --- | --- |
| 0:00-0:15 | Graph thinking: labels, relationships, and why property graphs fit HR data |
| 0:15-0:35 | Cypher basics: `MATCH`, `WHERE`, `RETURN`, `ORDER BY`, `LIMIT` |
| 0:35-0:55 | Traversal and aggregation across projects, domains, and work types |
| 0:55-1:15 | Semantic retrieval with the `text_embeddings` vector index |
| 1:15-1:45 | Build a read-only FastMCP server over the graph |
| 1:45-2:00 | Stretch goals, Q&A, and cleanup |

## Workshop Flow

### 1. Understand the Graph

Start with [docs/schema.md](docs/schema.md) for the mental model of the graph and the indexes already attached to it.

### 2. Practice Cypher

Work through [docs/cypher-exercises.md](docs/cypher-exercises.md). The exercises move from direct pattern matching to richer graph traversals and aggregation.

### 3. Add Semantic Retrieval

Use [docs/semantic-retrieval.md](docs/semantic-retrieval.md) to query the `text_embeddings` vector index and combine similarity search with graph context.

### 4. Explore the Starter Python Code

The reusable Python package lives under `src/workshop`.

- `python -m workshop.queries overview`
- `python -m workshop.queries skill --skill-name GraphQL`
- `python -m workshop.queries similar --person-id person-001`

### 5. Run the MCP Server

Start the server with:

```bash
python -m workshop.mcp_server
```

The server exposes:

- `run_cypher_read`
- `find_people_by_skill`
- `semantic_people_search`

## Recommended Commands

```bash
cp example.env .env
python load_data.py
python -m workshop.queries overview
python -m workshop.queries similar --person-id person-001 --limit 5
python -m workshop.mcp_server
```

## Repository Layout

```text
.
├── .devcontainer/
├── .github/prompts/
├── docs/
├── src/workshop/
├── example.env
├── load_data.py
├── neo4j_indexes.json
├── neo4j_model.json
├── pyproject.toml
├── requirements.txt
└── seed.cypher
```

## Troubleshooting

### Authentication Fails

- Verify that Aura credentials are copied exactly.
- Use the full `neo4j+s://` or `bolt+ssc://` URI provided by Aura.
- Confirm that `.env` contains `NEO4J_USERNAME`, not `NEO4J_USER`.

### Data Load Fails

- Ensure your database is empty or drop the existing graph before re-running the seed.
- Confirm that your Aura instance supports vector indexes.
- Re-run `python load_data.py` after checking the `.env` values.

### MCP Server Cannot Query

- Make sure the database was loaded successfully first.
- Verify that `python -m workshop.queries overview` works before you start the MCP server.
- Keep the MCP tools read-only during the workshop.

## Stretch Goals

1. Add a filtered semantic query that only returns people connected to a chosen domain.
2. Extend the MCP server with a tool that explains a person’s strongest skills from the graph.
3. Swap Aura for a local Neo4j instance and compare the setup experience.