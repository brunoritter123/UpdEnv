import urllib.request
'''url = 'https://arte.engpro.totvs.com.br/protheus/padrao/latest/repositorio/lobo_guara/tttp120.rpo'''
'''arquivo = 'tttp120.rpo'''

class Donwload:
	def __init__(self, url, destino):
		urllib.request.Request(url)
		urllib.request.urlretrieve(url, destino)
