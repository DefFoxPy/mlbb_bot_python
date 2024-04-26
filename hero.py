"""
pide le nombre de un héroe para posteriormente consultar sus datos en la página
mlbb.ninja y devolver la info
"""

#from bs4 import BeautifulSoup
import urllib.request
import json

name = input("Nombre del héroe: ")
contenido_web = urllib.request.urlopen('https://www.mlbb.ninja').read().decode('utf-8') 

# obtiene los datos de los héroes en la página
etiqueta_inicio_hero = '<script id="__NEXT_DATA__" type="application/json">'
etiqueta_final_hero = '</script>'
inicio = contenido_web.find(etiqueta_inicio_hero) + len(etiqueta_inicio_hero)
fin = contenido_web.find(etiqueta_final_hero, inicio)
text = contenido_web[inicio:fin]
data = json.loads(text)
heroes = data['props']['pageProps']["heroData"]

# obtiene la información del parche actual 
etiqueta_patch = '<span class="MuiChip-label MuiChip-labelMedium css-9iedg7">'
inicio = contenido_web.find(etiqueta_patch + "Patch") + len(etiqueta_patch)
fin = contenido_web.find('</span>', inicio)
text = contenido_web[inicio:fin]
print(text)

# obtiene la información de la última fecha en que fué actualizada la página
etiqueta_data = '<p class="MuiTypography-root MuiTypography-body1 MuiTypography-alignCenter css-ok37je">'
inicio = contenido_web.find(etiqueta_data + "Data last updated on ") + len(etiqueta_data)
fin = contenido_web.find('</p>', inicio)
text = contenido_web[inicio:fin]
text = text.replace('<strong>', '')
text = text.replace('</strong>', '')
print(text)   

flag = False

for hero in heroes:
	if hero['name'].lower() == name.lower():
		flag = True
		print('Tier:', hero['tier'])
		print('Rol:', hero['role'])
		print('Rank: win:', hero['win_rate'],"%", 'pick', hero['pick_rate'],'%', 'ban:', hero['ban_rate'],'%')
		print('Puntuación:', round(float(hero['final_score']) * 100), end='/100\n')
		print("Línea", end=': ')
		if hero['is_jungle']: print('Jungla',end=' ')
		if hero['is_mid']: print('Media',end=' ')
		if hero['is_exp']: print('Experiencia',end=' ')
		if hero['is_gold']: print('Oro',end=' ')
		if hero['is_roam']: print('Roam',end=' ')
		print()
		#print(hero['image_link'])
		break

if not flag: 
	print('No existe un héroe con ese nombre, intenta con su versión en Inglés')
