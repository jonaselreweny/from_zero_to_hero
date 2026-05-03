# HR Graph Schema Cheat Sheet

This workshop uses a small HR-flavored property graph that captures people, their skills, and the work they have been involved in.

## Node Labels

| Label | Key property | Notes |
| --- | --- | --- |
| `Person` | `id` | Main entity for semantic retrieval. Has an `embedding` property indexed by `text_embeddings`. |
| `Skill` | `name` | Skills known by people. |
| `Thing` | `name` | Projects, products, publications, or technologies a person is connected to. |
| `Domain` | `name` | Business or technical area for a `Thing`. |
| `WorkType` | `name` | Category of work represented by a `Thing`. |

## Relationship Types

| Pattern | Meaning |
| --- | --- |
| `(person:Person)-[:KNOWS]->(skill:Skill)` | The person knows a skill. |
| `(person:Person)-[:BUILT]->(thing:Thing)` | The person built a thing. |
| `(person:Person)-[:LED]->(thing:Thing)` | The person led a thing. |
| `(person:Person)-[:MANAGED]->(thing:Thing)` | The person managed a thing. |
| `(person:Person)-[:SHIPPED]->(thing:Thing)` | The person shipped a thing. |
| `(person:Person)-[:PUBLISHED]->(thing:Thing)` | The person published a thing. |
| `(person:Person)-[:WON]->(thing:Thing)` | The person won something tied to a thing. |
| `(person:Person)-[:OPTIMIZED]->(thing:Thing)` | The person optimized a thing. |
| `(thing:Thing)-[:IN]->(domain:Domain)` | The thing belongs to a domain. |
| `(thing:Thing)-[:OF]->(workType:WorkType)` | The thing belongs to a work type. |

## Constraints and Indexes

- `Person.id` has a node key constraint.
- `Skill.name`, `Thing.name`, `Domain.name`, and `WorkType.name` each have node key constraints.
- `Person.embedding` is indexed by the `text_embeddings` vector index.

## Why This Model Works for the Workshop

- It is small enough to learn quickly.
- It supports simple Cypher matches and richer traversals.
- It shows how graph context and semantic retrieval complement each other.

## Useful Starter Queries

```cypher
MATCH (person:Person)-[:KNOWS]->(skill:Skill)
RETURN coalesce(person.name, person.id) AS person, collect(skill.name) AS skills
LIMIT 10;
```

```cypher
MATCH (person:Person)-[:BUILT|LED|MANAGED|SHIPPED|PUBLISHED|WON|OPTIMIZED]->(thing:Thing)-[:IN]->(domain:Domain)
RETURN coalesce(person.name, person.id) AS person, collect(DISTINCT domain.name) AS domains
LIMIT 10;
```

```cypher
MATCH (thing:Thing)-[:OF]->(workType:WorkType)
RETURN workType.name AS work_type, count(*) AS thing_count
ORDER BY thing_count DESC;
```