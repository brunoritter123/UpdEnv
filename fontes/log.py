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
		self.nome_arquivo = f"logs/log_execucao_{year+month+day}-{hour+minute+second}.log"
		arquivo = self.openFile("x")
		if arquivo != None:
			arquivo.close()

	def write(self, erro, exception):
		error = "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ERRO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
		error += erro+"\n"
		for arg in exception.args:
			error += arg+"\n"
		error += "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<      >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
		arquivo = self.openFile()
		if arquivo != None:
			arquivo.write(error)
			arquivo.close()

	def openFile(self, option = "w"):
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