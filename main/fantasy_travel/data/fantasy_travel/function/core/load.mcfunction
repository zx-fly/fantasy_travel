# Fantasy Travel bootstrap. All initialization must remain reload-safe.
scoreboard objectives add ft.tick dummy
scoreboard objectives add ft.state dummy
scoreboard players set #normal ft.tick 0
scoreboard players set #slow ft.tick 0
scoreboard players set #maintenance ft.tick 0

execute unless data storage fantasy_travel:runtime meta run data modify storage fantasy_travel:runtime meta set value {schema_version:1,pack_version:"0.1.0"}
execute unless data storage fantasy_travel:runtime modules run data modify storage fantasy_travel:runtime modules set value {combat:1b,trade:1b,achievement:1b,world_terrain:1b,world_structure:1b,world_spawn:1b,world_climate:1b,event:1b}
execute unless data storage fantasy_travel:runtime events run data modify storage fantasy_travel:runtime events set value {active:[]}
execute unless data storage fantasy_travel:runtime queues run data modify storage fantasy_travel:runtime queues set value {world:[]}

function fantasy_travel:core/migrate/run
function #fantasy_travel:load
