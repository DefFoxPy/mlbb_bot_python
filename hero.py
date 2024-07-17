"""
pide le nombre de un héroe para posteriormente consultar sus datos en la página
mlbb.ninja y devolver su info
"""
import urllib.request
import json

def extraer_texto(contenido_web : urllib.request, tags_ini :str, tags_end :str, args = "") -> str:
	try:
		inicio = contenido_web.find(tags_ini + args) + len(tags_ini)
		fin = contenido_web.find(tags_end, inicio)
		return contenido_web[inicio:fin]
	except:
		return ""

def print_hero(hero : dict) -> None:
	print('Tier:', hero['tier'])
	print('Rol:', hero['role'])
	#print('Rank: win:', hero['win_rate'],"%", 'pick', hero['pick_rate'],'%', 'ban:', hero['ban_rate'],'%')
	print('Puntuación:', round(float(hero['final_score']) * 100), end='/100\n')
	print("Línea", end=': ')
	if hero['is_jungle']: print('Jungla',end=' ')
	if hero['is_mid']: print('Media',end=' ')
	if hero['is_exp']: print('Experiencia',end=' ')
	if hero['is_gold']: print('Oro',end=' ')
	if hero['is_roam']: print('Roam',end=' ')
	#print(hero['image_link'])
	print()

def is_hero(hero: dict, name: str) -> bool:
	return hero['name'].lower() == name.lower()

def main():
	name = input("Nombre del héroe: ")
	contenido_web = urllib.request.urlopen('https://www.mlbb.ninja').read().decode('utf-8') 
	# obtiene los datos de los héroes en la página
	text = extraer_texto(contenido_web, '<script id="__NEXT_DATA__" type="application/json">', '</script>')
	data = json.loads(text)
	heroes = data['props']['pageProps']["heroData"]
	# obtiene la información del parche actual 
	text = extraer_texto(contenido_web, '<span class="MuiChip-label MuiChip-labelMedium css-9iedg7">', '</span>', 'Patch')
	print(text)
	# obtiene la información de la última fecha en que fué actualizada la página
	text = extraer_texto(contenido_web, '<p class="MuiTypography-root MuiTypography-body1 MuiTypography-alignCenter css-ok37je">', '</p>', 'Data last updated on ')
	text = text.replace('<strong>', '')
	text = text.replace('</strong>', '')
	print(text)   

	found = False
	for hero in heroes:
		if is_hero(hero, name):
			found = True
			print_hero(hero)
			break
	if not found: 
		print('No existe un héroe con ese nombre, intenta con su versión en Inglés')

if __name__ == '__main__':
	main()