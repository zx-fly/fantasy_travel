# Lightweight dispatcher. Gameplay modules run through frequency tags.
function #fantasy_travel:tick/fast

scoreboard players add #normal ft.tick 1
scoreboard players add #slow ft.tick 1
scoreboard players add #maintenance ft.tick 1

execute if score #normal ft.tick matches 5.. run function #fantasy_travel:tick/normal
execute if score #normal ft.tick matches 5.. run scoreboard players set #normal ft.tick 0
execute if score #slow ft.tick matches 20.. run function #fantasy_travel:tick/slow
execute if score #slow ft.tick matches 20.. run scoreboard players set #slow ft.tick 0
execute if score #maintenance ft.tick matches 100.. run function #fantasy_travel:tick/maintenance
execute if score #maintenance ft.tick matches 100.. run scoreboard players set #maintenance ft.tick 0
