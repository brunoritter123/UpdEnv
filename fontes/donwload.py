import urllib.request
import os

'''url = 'https://arte.engpro.totvs.com.br/protheus/padrao/latest/repositorio/lobo_guara/tttp120.rpo'''
'''arquivo = 'tttp120.rpo'''

class Donwload:
	def __init__(self, url):
		print("baixando com urllib")
		urllib.request.Request(url)
		arquivo = os.path.basename(url)
		urllib.request.urlretrieve(url, arquivo)
