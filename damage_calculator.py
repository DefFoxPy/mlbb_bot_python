GUIVE = 40
RUGIDO = 20

def damage_calculador(DMG : float, DEF : int, DEF_RED = 0, F_PEN = 0, PER_PEN = 0, DMG_RED = 0):
	if PER_PEN == GUIVE:
		print(DEF)
		if 0.01 * (DEF-F_PEN) <= 0.2:	
			DMG_PER = (DEF - F_PEN) * (0.40 + 0.01 * (DEF - F_PEN))
		else:
			DMG_PER = (DEF - F_PEN) * 0.6
		print (DMG_PER)
	elif PER_PEN == RUGIDO:
		DMG_PER = (DEF - F_PEN) * (0.40 + 0.01 * (DEF - F_PEN))
	else:
		DMG_PER = 0

	return round(DMG * 120 / (120 + DEF - DEF_RED - F_PEN - DMG_PER) - DMG_RED)

def main():
	val = [662, 300, 0, 0, 40]
	print (damage_calculador(val[0], val[1], val[2], val[3], val[4]))

main()
