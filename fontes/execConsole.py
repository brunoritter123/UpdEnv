#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fontes.mdAmbiente import mdAmbiente
from fontes.log import Log
import pyodbc
import os

class ExecConsole:
	def __init__(self):
		self.log = Log()
		self.mdAmbiente = mdAmbiente()
		pathTemp = './temp'
		if not os.path.exists(pathTemp):
			os.mkdir(pathTemp)

		for row in self.mdAmbiente.consultar_registros():
			self.mdAmbiente.load_registro(row[0])
			self.transferindoArquivos()
			self.restaurar_bkp_bd()

	def transferindoArquivos(self):
		pass

	def restaurar_bkp_bd(self):
		if self.mdAmbiente.isDadosBd():
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
				self.log.write(erro, e)

			if conn != None:
				conn.close()