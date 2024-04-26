"""
pide le nombre de un héroe para posteriormente consultar sus datos en la página
mlbb.ninja y devolver la info
"""

#from bs4 import BeautifulSoup
import urllib.request
import json

name = input("Nombre del héroe: ")
etiqueta_inicio_hero = '<script id="__NEXT_DATA__" type="application/json">'
etiqueta_final_hero = '</script>'

contenido_web = urllib.request.urlopen('https://www.mlbb.ninja').read().decode('utf-8') 
inicio = contenido_web.find(etiqueta_inicio_hero) + len(etiqueta_inicio_hero)
fin = contenido_web.find(etiqueta_final_hero, inicio)
text = contenido_web[inicio:fin]
data = json.loads(text)
heroes = data['props']['pageProps']["heroData"]

flag = False

for hero in heroes:
	if hero['name'] == name.title():
		flag = True
		print('tier:', hero['tier'])
		print('rol:', hero['role'])
		print('winrate:', hero['win_rate'],"%")
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
	print('No existe un héroe con ese nombre')
