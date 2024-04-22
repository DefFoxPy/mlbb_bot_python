"""
note: comando creado por @Mint y <@809218974029316146>
Coloca el winrate (en porcentaje, sin el signo) actual y el número de estrellas que quieres obtener, ejemplo, 60% de winrate y quiero 35 ⭐, el comando sería:
`{prefix}t {tagname} 60 35`

Nota:
Se recomienda el winrate de la temporada actual en ranks (al menos unas 30 partidas ya jugadas)
Cálculos válidos si mantienes la tasa de winrate actual.
Ya están descontadas las ⭐ por las posibles derrotas.
"""
import math
winrate, puntos_a_obtener = map(int, input().split())

if winrate == 50.0:
    print('Si vas con 50% de winrate, no avanzarás.')
elif winrate < 50.0:
    print('Si tienes un winrate menor al 50%, perderás estrellas.')
elif winrate > 100.0:
    print('No puedes tener un winrate mayor al 100%')
elif puntos_a_obtener < 0:
    print('Indicar un número positivo para las estrellas a obtener')
else:
    winrate /= 100 # llevandolo a su forma decimal
    partidas_estimadas = puntos_a_obtener / (2 * winrate - 1)

    print("winrate actual:", round(winrate * 100, 2), "%")
    print("estrellas a obtener:", puntos_a_obtener)
    print("partidas estimadas:", math.ceil(partidas_estimadas))