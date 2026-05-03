## Plan: Neo4j Zero to Hero Workshop

Build a self-contained workshop repository for a 2-hour GitHub Codespaces session that teaches Neo4j fundamentals, Cypher, vector-based semantic retrieval over the existing Person.embedding index, and a FastMCP server that exposes graph and semantic search tools. The recommended approach is to make the README the primary workshop script, use a .devcontainer to preinstall Python tooling and the Neo4j VS Code extension, and assume participants connect to their own Aura Free instancee using a checked-in example.env template rather than a bundled database.

**Steps**
1. Define the workshop narrative and repo information architecture. Create the top-level README structure first because it drives every other artifact: title, audience, prerequisites, learning goals, 2-hour agenda, GitHub Codespaces launch button, setup flow, guided exercises, stretch goals, and troubleshooting. This blocks the detailed content in the rest of the repo.
2. Translate the supplied schema into workshop-ready teaching assets. Derive a concise domain explanation from the existing model: Person, Skill, Thing, Domain, WorkType; Person-KNOWS-Skill; Person-(BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED)-Thing; Thing-IN-Domain; Thing-OF-WorkType. Add a short schema section and a visual/text cheat sheet for these labels, relationships, and key constraints. This depends on step 1.
3. Load data into Neo4j using the seed.cypher file using load_data.py using the .env settings.
4. Design the environment bootstrap for Codespaces. Add a .devcontainer that installs Python, the Neo4j Python driver with Rust extension support, FastMCP, and workspace conveniences such as recommended VS Code extensions and post-create setup steps. Keep Neo4j itself out of the container because the chosen runtime is participant-managed Aura. This can run in parallel with step 3 once the repo structure from step 1 is fixed.
5. Create the Python starter surface for database access. Add a small src or app package with environment loading, connection helpers, and one or two focused scripts for running Cypher and vector queries. Reuse one connection path everywhere so the MCP server and sample scripts do not drift. This depends on steps 3 and 4.
6. Design the Cypher learning sequence as progressive exercises. Start with MATCH, WHERE, RETURN, ORDER BY, LIMIT, then move to relationship traversal across Thing, Domain, and WorkType, then aggregation and filtering, then semantic retrieval using the existing vector index. Include expected outcomes so participants can self-check. This depends on steps 2 and 3 and can be documented alongside step 5.
7. Define the semantic retrieval lesson around the existing vector index. Teach one concrete flow only: query the Person.embedding vector index to find semantically similar people, then enrich results with Cypher to inspect skills and work history. Avoid embedding generation in the main path. This depends on step 3.
8. Plan the FastMCP deliverable as a richer but still bounded server. Expose a small tool set such as run_cypher_read, find_people_by_skill, and semantic_people_search. Keep the MCP server read-only to reduce risk and time pressure, but include the semantic search tool so the deliverable matches the selected scope. This depends on steps 5 and 7.
9. Add workshop scaffolding and guardrails. Include example.env, .gitignore rules for .env, concise troubleshooting for Aura connectivity, and a section explaining that the checked-in .env must never be used as a template. This depends on steps 1 and 4.
10. Validate the repo end to end. Open the repo in Codespaces, confirm the devcontainer builds cleanly, verify the README walkthrough from a cold start, run the seed script against a fresh Neo4j instance, execute sample Cypher queries, run a vector search against Person.embedding, and start the FastMCP server successfully. This depends on all prior steps.

For execution, steps 3 and 4 can proceed in parallel after step 1. Steps 5 and 6 can proceed in parallel once seed data and environment choices are fixed. Step 8 should wait until the shared connection code and semantic query path are stable.

**Relevant files**
- /Users/jonaselreweny/Code/workshops/hr_data/README.md — primary workshop script, agenda, Codespaces button, setup, exercises, and troubleshooting.
- /Users/jonaselreweny/Code/workshops/hr_data/.devcontainer/devcontainer.json — Codespaces definition, extensions, postCreateCommand, and container settings.
- /Users/jonaselreweny/Code/workshops/hr_data/.devcontainer/Dockerfile — image customization for Python tooling and workshop dependencies if the base image is not sufficient.
- /Users/jonaselreweny/Code/workshops/hr_data/example.env — participant-facing environment template for Aura/local Neo4j plus OpenAI key if needed by the MCP workflow.
- /Users/jonaselreweny/Code/workshops/hr_data/.gitignore — must exclude .env and other local artifacts.
- /Users/jonaselreweny/Code/workshops/hr_data/data/seed.cypher — deterministic dataset including Person embeddings and graph relationships.
- /Users/jonaselreweny/Code/workshops/hr_data/docs/schema.md — concise graph model cheat sheet derived from neo4j_model.json and neo4j_indexes.json.
- /Users/jonaselreweny/Code/workshops/hr_data/docs/cypher-exercises.md — progressive Cypher tasks and expected outputs.
- /Users/jonaselreweny/Code/workshops/hr_data/docs/semantic-retrieval.md — explanation of db.index.vector.queryNodes usage and follow-on Cypher enrichment.
- /Users/jonaselreweny/Code/workshops/hr_data/src/workshop/db.py — shared Neo4j connection and query helpers.
- /Users/jonaselreweny/Code/workshops/hr_data/src/workshop/queries.py — reusable Cypher and vector retrieval functions.
- /Users/jonaselreweny/Code/workshops/hr_data/src/workshop/mcp_server.py — FastMCP server exposing read-only graph and semantic tools.
- /Users/jonaselreweny/Code/workshops/hr_data/src/workshop/__init__.py — package marker if a src layout is used.
- /Users/jonaselreweny/Code/workshops/hr_data/neo4j_model.json — existing model source of truth for labels, relationship types, and constraints to reflect in documentation.
- /Users/jonaselreweny/Code/workshops/hr_data/neo4j_indexes.json — existing index source of truth, especially the Person.embedding vector index.

**Verification**
1. Build the Codespaces devcontainer from scratch and confirm all required packages and extensions are available without manual installation.
2. Populate a fresh Aura/local Neo4j instance using the provided seed flow and verify the expected node labels, relationship types, constraints, and Person.embedding vector index behavior.
3. Run each documented Cypher exercise against the seeded database and verify the expected result shape still matches the workshop instructions.
4. Execute the sample Python connection script and the semantic retrieval script using example.env-derived settings.
5. Start the FastMCP server and exercise each documented tool against the seeded graph from a clean environment.
6. Dry-run the README end to end as if you were a participant in a new Codespace, measuring whether the core path fits within 2 hours.

**Decisions**
- Included scope: GitHub Codespaces-first setup, README-driven workshop flow, Neo4j basics, Cypher practice, semantic retrieval using the existing Person.embedding vector index, and a FastMCP server with semantic search capability.
- Included scope: Participants connect to their own Aura or local Neo4j instance rather than running Neo4j inside the Codespace.
- Included scope: Use precomputed embeddings only; do not teach embedding generation in the main workshop path.
- Included scope: Optimize for a mixed audience by keeping the main path copy-paste friendly and offering optional stretch goals for faster participants.
- Included scope: Add explicit secret-handling guidance, keep only example.env in version control, and treat any populated local .env as user-local state that must not be committed; if the currently exposed credentials are live, rotate them before publishing the workshop repo.
- Excluded scope: Write-capable MCP tools, graph mutation workflows through MCP, and broad coverage of embedding pipelines or hybrid search variants.
- Excluded scope: Managing a shared hosted database for the class.

**Further Considerations**
1. Recommend one concrete Neo4j target in the README even though both Aura and local are allowed. Aura Free is likely the lowest-friction default; local can be the fallback path.
2. Keep the semantic retrieval example centered on people rather than things because the existing vector index is only on Person.embedding.
3. Add one short optional challenge at the end: combine semantic similarity with a Cypher filter such as Domain or WorkType to show how vector and graph retrieval complement each other.
