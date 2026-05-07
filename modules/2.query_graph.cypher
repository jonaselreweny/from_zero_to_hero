// Module 2: Querying the Graph with Cypher

/* There is a Neo4j extension installed in this environment. Before proceeding with this module, connect
to your Aura Free instance by first clicking the Neo4j logo on the left pane and add new connection.
Make sure to choose the database which isn't named 'system' to initiate the connection. */

// This is how we comment a line in Cypher.

/* For multi-line comments,
we can use this syntax. */

/* To visualize the schema of our graph, we can use the `CALL db.schema.visualization()` procedure.
In VS Code with the Neo4j extension, you can run a query by selecting it and pressing `cmd + ^ + enter` 
(or `ctrl + shift + enter` on Windows). */
CALL db.schema.visualization();

/* Let's start with a simple query to get all persons in the database. 
In Cypher, we use parentheses to represent nodes and square brackets to represent relationships. 
The `MATCH` clause is used to specify the pattern we want to match in the graph, and the `RETURN` 
clause specifies what we want to return from the query. */
MATCH (p:Person)
RETURN p
LIMIT 25;

/* Notice how the Neo4j VS Code extension provides syntax highlighting and autocompletion for Cypher queries.
It also provides a visual representation of the query results, making it easier to understand the structure of the data.
Let´s expand our query to include the relationships between persons and their departments.
Variables p, r, and d represent the person, the relationship, and the department respectively.

Assigning variables to nodes and relationships allows us to return them in the result set 
and also to refer to them in other parts of the query if needed. */
MATCH (p:Person)-[r]->(d)
RETURN p, r, d
LIMIT 25;

// Entire patterns can also be assigned to a variable.
MATCH path=(:Person)-[]->()
RETURN path
LIMIT 25;

/* Filtering results is an important aspect of querying data. Let's say we want to find all persons who knows Machine Learning.
The result is further limited by specifying the relationship type and the Skill labelin the pattern. 
We are looking for relationships of type `KNOWS` that connect a person to a skill with the name "Machine Learning". */
MATCH (p:Person)-[:KNOWS]->(s:Skill {name: "Machine Learning"})
RETURN s.name AS skill, p.name AS person 
LIMIT 25;

/* Same query but with a WHERE clause instead of pattern matching for the skill name. 
Both queries will return the same result, but the first one is more concise and easier to read in this case. */
MATCH (p:Person)-[:KNOWS]->(s:Skill)
WHERE s.name = "Machine Learning"
RETURN s.name AS skill, p.name AS person
LIMIT 25;

// Let's use aggregations to refine the results. For example, we can count how many people know each skill.
MATCH (p:Person)-[:KNOWS]->(s:Skill {name: "Machine Learning"})
RETURN s.name AS skill, collect(p.name) AS persons, count(p) AS count
LIMIT 25;

/* Using parameters is a good practice. This means developers do not have to resort to string building 
to create a query. Additionally, parameters make caching of execution plans much easier for Cypher, 
thus leading to faster query execution times. 

Try creating a parameter in the Neo4j VS Code extension with the name `skill` and value '"Machine Learning"' 
If all goes well, the following query should return a node with the label Skill and name property with
the value 'Machine Learning' */
MATCH (s:Skill{name: $skill})
RETURN s;

// We can return the results in various formats and order them. For example, in JSON format.
MATCH (s:Skill)
RETURN s {.name, persons: [(s)<-[:KNOWS]-(p:Person) | p.name]} AS skill_info
ORDER BY s.name
LIMIT 25;