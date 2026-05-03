# Cypher Exercises

These exercises are meant to be run in Neo4j Browser, Neo4j for VS Code, or through the Python helper scripts.

## Exercise 1: Meet the Graph

List a few people and the skills attached to them.

```cypher
MATCH (person:Person)-[:KNOWS]->(skill:Skill)
RETURN coalesce(person.name, person.id) AS person, collect(skill.name) AS skills
LIMIT 5;
```

Expected shape: one row per person, with a list of skill names.

## Exercise 2: Follow Work History

Find the things people have worked on.

```cypher
MATCH (person:Person)-[rel:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(thing:Thing)
RETURN coalesce(person.name, person.id) AS person, type(rel) AS contribution, thing.name AS thing
ORDER BY person, contribution
LIMIT 15;
```

Expected shape: one row per person-contribution-thing combination.

## Exercise 3: Add Domain Context

Show which domains people have worked in.

```cypher
MATCH (person:Person)-[:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(thing:Thing)-[:IN]->(domain:Domain)
RETURN coalesce(person.name, person.id) AS person, collect(DISTINCT domain.name) AS domains
LIMIT 10;
```

Expected shape: one row per person with a list of domains.

## Exercise 4: Count Work Types

See which work types show up most often.

```cypher
MATCH (:Person)-[:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(thing:Thing)-[:OF]->(workType:WorkType)
RETURN workType.name AS work_type, count(DISTINCT thing) AS thing_count
ORDER BY thing_count DESC;
```

Expected shape: one row per work type ordered by descending count.

## Exercise 5: Find People by Skill

Pick a skill name from your graph and find matching people.

```cypher
MATCH (person:Person)-[:KNOWS]->(:Skill {name: $skill_name})
RETURN coalesce(person.name, person.id) AS person, person.id AS person_id
ORDER BY person;
```

Suggested parameter: `GraphQL`

## Exercise 6: Build a Reusable Projection

Return a compact summary that could be used by an API or MCP tool.

```cypher
MATCH (person:Person)
OPTIONAL MATCH (person)-[:KNOWS]->(skill:Skill)
OPTIONAL MATCH (person)-[:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(thing:Thing)-[:IN]->(domain:Domain)
RETURN {
  person_id: person.id,
  display_name: coalesce(person.name, person.id),
  skills: collect(DISTINCT skill.name),
  domains: collect(DISTINCT domain.name)
} AS summary
LIMIT 10;
```

Expected shape: one map per person with only JSON-friendly values.

## Exercise 7: Prepare for Semantic Retrieval

Pick a source person and inspect whether they have an embedding.

```cypher
MATCH (person:Person)
RETURN person.id AS person_id, size(person.embedding) AS embedding_dimensions
LIMIT 5;
```

Expected shape: a person id and the embedding length.