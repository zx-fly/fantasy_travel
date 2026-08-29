# Initialize newly seen players at low frequency.
execute as @a[tag=!ft.initialized] run function fantasy_travel:core/player/init
