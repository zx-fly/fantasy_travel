# Ordered, idempotent storage migrations belong here.
execute unless data storage fantasy_travel:runtime meta.schema_version run data modify storage fantasy_travel:runtime meta.schema_version set value 1
