from datetime import datetime

class Log:
	def __init__(self):
		now = datetime.now()
		year = toStr(now.year, 4)
		month = toStr(now.month, 2)
		day = toStr(now.day, 2)
		hour = toStr(now.hour, 2)
		minute = toStr(now.minute, 2)
		second = toStr(now.second, 2)
		self.title = ''
		self.nome_arquivo = f"logs/log_execucao_{year+month+day}-{hour+minute+second}.log"
		arquivo = self.openFile()
		if arquivo != None:
			arquivo.close()

	def write(self, title = '', erro = '', exception = []):
		error = ''
		if self.title != title:
			self.title = title
			if isNotEmpty(title):
				title = f'> ERRO - {title}\n'
			else:
				title = "> ERRO\n"
		else:
			title = '-\n'

		error += f"\t>{erro}\n"
		for arg in exception.args:
			if not type(arg) == str:
				arg = str(arg)
			error += f"\t>{arg}\n"

		arquivo = self.openFile()
		if arquivo != None:
			arquivo.write(title+error)
			arquivo.close()

	def openFile(self, option = "a+"):
		arquivo = None
		try:
			arquivo = open(self.nome_arquivo, option)
		except Exception as e:
			print("Erro ao tentar criar o arquivo de log.")
			print("Detalhes:")
			for arg in e.args:
				print(arg)
		return arquivo

def toStr(val, tam):
	valorConv = str(val)
	while len(valorConv) < tam:
		valorConv = '0'+valorConv
	return valorConv

def isNotEmpty(s):
	return bool(s and s.strip())