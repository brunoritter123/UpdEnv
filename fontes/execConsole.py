#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fontes.mdAmbiente import mdAmbiente
from fontes.log import Log
import pyodbc
import os
import shutil
import zipfile
import subprocess

class ExecConsole:
	def __init__(self):
		self.log = Log()
		self.itens = 0
		self.mdAmbiente = mdAmbiente()
		self.deParaTemp = [{'pathTemp': '' , 'pathBd': ''}]
		self.pathTemp = './temp'
		self.ambienteAual = ''

		print("""   >Parando serviços""")
		self.pararServicos()

		print("""   >Delatando pasta temp""")
		self.deletarPastaTemp()

		if not os.path.exists(self.pathTemp):
			print("""   >Criando pasta temp""")
			os.mkdir(self.pathTemp)

		for row in self.mdAmbiente.consultar_registros():
			self.mdAmbiente.load_registro(row[0])
			self.ambienteAual = f"Id='{self.mdAmbiente.get_id()}' - Descrição= '{self.mdAmbiente.get_descricao()}'."
			print(f"""   >Carregado ambiente - {self.ambienteAual}""")
			self.transferindoArquivos()
			self.restaurar_bkp_bd()

		print("""   >Delatando pasta temp""")
		self.deletarPastaTemp()

		print("""   >Iniciando serviços""")
		self.iniciarServicos()


	def deletarPastaTemp(self):
		try:
			if os.path.exists(self.pathTemp):
				shutil.rmtree(self.pathTemp, ignore_errors=True)
		except Exception as e:
			erro = f"Erro ao tentar deletar a pasta Temp."
			self.log.write(self.ambienteAual, erro, e)


	def pararServicos(self):
		sv_dbAccess = self.mdAmbiente.get_sv_dbAccess()
		sv_serve = self.mdAmbiente.get_sv_serve()

		try:
			if not isEmpty(sv_dbAccess):
				print(f"""      >Parando o serviço - {sv_dbAccess}""")
				subprocess.run(['sc', 'stop', sv_dbAccess])
		except Exception as e:
			erro = f"Erro ao tentar parar o serviço '{sv_dbAccess}'."
			self.log.write(self.ambienteAual, erro, e)

		try:
			if not isEmpty(sv_serve):
				print(f"""      >Parando o serviço - {sv_serve}""")
				subprocess.run(['sc', 'stop', sv_serve])
		except Exception as e:
			erro = f"Erro ao tentar parar o serviço '{sv_serve}'."
			self.log.write(self.ambienteAual, erro, e)


	def iniciarServicos(self):
		sv_dbAccess = self.mdAmbiente.get_sv_dbAccess()
		sv_serve = self.mdAmbiente.get_sv_serve()

		try:
			if not isEmpty(sv_dbAccess):
				print(f"""      >Iniciando o serviço - {sv_dbAccess}""")
				subprocess.run(['sc', 'start', sv_dbAccess])
		except Exception as e:
			erro = f"Erro ao tentar iniciar o serviço '{sv_dbAccess}'."
			self.log.write(self.ambienteAual, erro, e)

		try:
			if not isEmpty(sv_serve):
				print(f"""      >Iniciando o serviço - {sv_serve}""")
				subprocess.run(['sc', 'start', sv_serve])
		except Exception as e:
			erro = f"Erro ao tentar iniciar o serviço '{sv_serve}'."
			self.log.write(self.ambienteAual, erro, e)


	def transferindoArquivos(self):
		try:
			self.enviarRpo()
		except Exception as e:
			erro = f"Erro ao tentar copiar o RPO."
			self.log.write(self.ambienteAual, erro, e)

		try:
			self.enviarZip(self.mdAmbiente.get_de_smartClient(), self.mdAmbiente.get_para_smartClient(), 'Smart Client')
		except Exception as e:
			erro = f"Erro ao tentar copiar o SmartClient."
			self.log.write(self.ambienteAual, erro, e)

		try:
			self.enviarZip(self.mdAmbiente.get_de_server(), self.mdAmbiente.get_para_server(), 'Server')
		except Exception as e:
			erro = f"Erro ao tentar copiar o Server."
			self.log.write(self.ambienteAual, erro, e)

		try:
			self.enviarZip(self.mdAmbiente.get_de_dbAccess(), self.mdAmbiente.get_para_dbAccess(), 'DbAccess')
		except Exception as e:
			erro = f"Erro ao tentar copiar o DbAccess."
			self.log.write(self.ambienteAual, erro, e)


	def enviarRpo(self):
		if self.mdAmbiente.isDeParaRpo():
			print("""      >Transferindo RPO""")
			de_rpo = self.mdAmbiente.get_de_rpo()
			para_rpo = self.mdAmbiente.get_para_rpo()
			para_old_rpo = para_rpo

			barra_de = self.getBarPath(de_rpo)
			barra_para = self.getBarPath(para_rpo)

			nameRpo = de_rpo.rsplit(barra_de, 1)[1]
			para_rpo += barra_para+nameRpo
			para_old_rpo += barra_para+'old_'+nameRpo

			if os.path.exists(para_old_rpo):
				os.remove(para_old_rpo)

			if os.path.exists(para_rpo):
				os.rename(para_rpo, para_old_rpo)

			shutil.copyfile(de_rpo, para_rpo)

	def enviarZip(self, to_path, from_path, tpTransfer):
		if not isEmpty(to_path) and not isEmpty(from_path):
			print(f"""      >Transferindo {tpTransfer}""")
			pathTemp = self.enviarTemp(to_path)

			if not isEmpty(pathTemp):
				self.copy_and_overwrite(pathTemp, from_path)


	def getBarPath(self, path):
		if path.find('/') >= 0:
			bar = '/'
		else:
			bar = '\\'
		return bar


	def enviarTemp(self, pathDb, nameFile = ''):
		pathTemp = ''
		for dic in self.deParaTemp:
			if dic['pathBd'] == pathDb:
				pathTemp = dic['pathTemp']
				break

		if isEmpty(pathTemp):
			self.itens += 1
			pathTemp = f'./temp/{str(self.itens)}'
			if not os.path.exists(pathTemp):
				os.mkdir(pathTemp)

			if not isEmpty(nameFile):
				pathTemp += f'/{nameFile}'
				shutil.copyfile(pathDb, pathTemp)
			elif zipfile.is_zipfile(pathDb):
				zip = zipfile.ZipFile(pathDb)
				zip.extractall(pathTemp)
			else:
				shutil.copytree(pathDb, pathTemp)

			self.deParaTemp.append({'pathTemp': pathTemp , 'pathBd': pathDb})
			return pathTemp

	def restaurar_bkp_bd(self):
		if self.mdAmbiente.isDadosBd():
			print("""      >Restando banco de dados""")
			nameDb = self.mdAmbiente.get_bd_nomeBanco()
			conn = None
			try:
				conn = pyodbc.connect(DRIVER='{SQL Server Native Client 11.0}',
										SERVER=self.mdAmbiente.get_bd_servidor(),
										UID=self.mdAmbiente.get_bd_usuario(),
										PWD=self.mdAmbiente.get_bd_senha(),
										Trusted_Connection='yes',
										autocommit=True)
				sql = (f"USE [master]; \
						ALTER DATABASE [{nameDb}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE; \
						RESTORE DATABASE [{nameDb}] FROM  DISK =   N'{self.mdAmbiente.get_bd_bkpBanco()}' WITH  FILE = 1,  NOUNLOAD,  REPLACE,  STATS = 5; \
						ALTER DATABASE [{nameDb}] SET MULTI_USER;")
				cursor = conn.cursor()
				cursor.execute(sql)
				while cursor.nextset():
					pass
			except Exception as e:
				erro = f"Erro ao tentar restaurar o banco de dados do ambiente Id='{self.mdAmbiente.get_id()}' - Descrição= '{self.mdAmbiente.get_descricao()}'."
				self.log.write(self.ambienteAual, erro, e)

			if conn != None:
				conn.close()

	def copy_and_overwrite(self, to_path, from_path):
		if os.path.isdir(to_path):
			if not os.path.exists(from_path):
				os.mkdir(from_path)

			barra_de =  self.getBarPath(to_path)
			barra_para =  self.getBarPath(from_path)

			for arquivo in os.listdir(to_path):
				de_arquivo = to_path+barra_de+arquivo
				para_arquivo = from_path+barra_para+arquivo

				if os.path.isfile(de_arquivo):
					if os.path.exists(para_arquivo):
						#subprocess.call(f'attrib -r +s drive:{para_arquivo}')
						os.remove(para_arquivo)

					shutil.copyfile(de_arquivo, para_arquivo)
				else:
					self.copy_and_overwrite(de_arquivo, para_arquivo)

def isEmpty(s):
	return not bool(s and s.strip())