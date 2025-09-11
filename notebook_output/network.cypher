-- Create constraints
CREATE CONSTRAINT crm_id IF NOT EXISTS FOR (n:CRM) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT crm_class_code IF NOT EXISTS FOR (n:CRM) REQUIRE n.class_code IS NOT NULL;

-- Create nodes
UNWIND $nodes_0 AS n
MERGE (x:CRM {id: n.id})
SET x.label = coalesce(n.label, x.label)
SET x.class_code = n.class_code
SET x.notes = coalesce(n.notes, x.notes)
SET x.type = coalesce(n.type, x.type);
