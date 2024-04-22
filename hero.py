"""
pide le nombre de un héroe para posteriormente consultar sus datos en la página
mlbb.ninja y devolver la info
"""

from bs4 import BeautifulSoup
import urllib.request
import json

name = input("Nombre del héroe: ")

datos = urllib.request.urlopen('https://www.mlbb.ninja').read().decode()
soup =  BeautifulSoup(datos, 'html.parser')
result = soup.find(id='__NEXT_DATA__', type="application/json")
data = json.loads(result.text)
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
