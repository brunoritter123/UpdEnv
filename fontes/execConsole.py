#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fontes.mdAmbiente import mdAmbiente
import pyodbc

class ExecConsole:
	def __init__(self):
		self.mdAmbiente = mdAmbiente()
		for row in self.mdAmbiente.consultar_registros():
			self.mdAmbiente.load_registro(row[0])
			self.restaurar_bkp_bd()

	def restaurar_bkp_bd(self):
		if self.mdAmbiente.isDadosBd():
			nameDb = self.mdAmbiente.get_bd_nomeBanco()
			conn = None
			try:
				conn = pyodbc.connect(DRIVER='{SQL Server Native Client 11.0}',
										SERVER=self.mdAmbiente.get_bd_servidor()+'_',
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
				error = "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ERRO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
				error += f"Erro ao tentar restaurar o banco de dados do ambiente Id='{self.mdAmbiente.get_id()}' - Descrição= '{self.mdAmbiente.get_descricao()}'.\n"
				for arg in e.args:
					error += arg+"\n"
				error += "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
				print(error)

			if conn != None:
				conn.close()