# Semantic Retrieval with Neo4j Vector Indexes

The graph already includes a vector index named `text_embeddings` on `Person.embedding`. That lets you search for people who are semantically similar to a source person without generating embeddings during the workshop.

## Mental Model

Use semantic retrieval when exact graph patterns are too strict.

- Cypher is good at exact structure and filtering.
- Vector search is good at similarity.
- The best workshop example combines both.

## Basic Similarity Query

```cypher
MATCH (source:Person {id: $person_id})
CALL db.index.vector.queryNodes('text_embeddings', $limit, source.embedding)
YIELD node, score
WHERE node.id <> source.id
RETURN source.id AS source_person_id,
       node.id AS similar_person_id,
       coalesce(node.name, node.id) AS similar_person,
       score
ORDER BY score DESC;
```

Suggested parameters:

```json
{
  "person_id": "person-001",
  "limit": 5
}
```

## Similarity Plus Graph Context

Use the vector search as the first retrieval step, then attach graph context.

```cypher
MATCH (source:Person {id: $person_id})
CALL db.index.vector.queryNodes('text_embeddings', $limit, source.embedding)
YIELD node, score
WHERE node.id <> source.id
OPTIONAL MATCH (node)-[:KNOWS]->(skill:Skill)
OPTIONAL MATCH (node)-[:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(thing:Thing)-[:IN]->(domain:Domain)
RETURN {
  person_id: node.id,
  display_name: coalesce(node.name, node.id),
  score: score,
  skills: collect(DISTINCT skill.name),
  domains: collect(DISTINCT domain.name)
} AS similar_person
ORDER BY similar_person.score DESC;
```

## Why This Matters for MCP

This pattern is a good fit for an MCP tool because:

- The tool input is simple: `person_id` and `limit`.
- The output is already structured for an LLM or UI.
- It demonstrates that graph retrieval and semantic retrieval are complementary rather than competing techniques.

## Stretch Query

Limit semantic matches to people connected to a specific domain.

```cypher
MATCH (source:Person {id: $person_id})
CALL db.index.vector.queryNodes('text_embeddings', $limit, source.embedding)
YIELD node, score
MATCH (node)-[:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(:Thing)-[:IN]->(:Domain {name: $domain_name})
WHERE node.id <> source.id
RETURN node.id AS person_id, score
ORDER BY score DESC;
```