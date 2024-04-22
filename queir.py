"""
Programa que consulta la Api de mobile legends para obtener el nombre de sus personajes
y posteriormente elegir uno al azar
"""
from random import randint
import requests
import json

#text = {text:https://mapi.mobilelegends.com/hero/list}  #modo discord
response = requests.get(f"https://mapi.mobilelegends.com/hero/list")
text = json.loads(response.text)
num_hero = len(text['data'])-1
number = randint(0, num_hero)
hero=text['data'][number]['name']

print("Deberías jugar con:",hero)