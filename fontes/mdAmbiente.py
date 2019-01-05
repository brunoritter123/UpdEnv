#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classa que controla os dados dos Ambientes"""
import sqlite3

class mdAmbiente:
	def __init__(self):
		self.con = sqlite3.connect('dados/db.sqlite3')
		self.cur = self.con.cursor()
		self.criar_tabela()
		self.reset_values()

	def reset_values(self):
		self.set_id()
		self.set_descricao()
		self.set_de_rpo()
		self.set_de_smartClient()
		self.set_de_server()
		self.set_de_includes()
		self.set_para_rpo()
		self.set_para_smartClient()
		self.set_para_server()
		self.set_para_includes()
		self.set_bd_bkpBanco()
		self.set_bd_servidor()
		self.set_bd_nomeBanco()
		self.set_bd_usuario()
		self.set_bd_senha()
		self.set_fontes()
		self.set_patch()
		self.set_de_dbAccess()
		self.set_para_dbAccess()

	def criar_tabela(self):
		try:
			self.cur.execute('''CREATE TABLE IF NOT EXISTS AMBIENTES (
				ID TEXT PRIMARY KEY,
				DESCRICAO TEXT,
				DE_RPO TEXT,
				DE_SMARTCLIENT TEXT,
				DE_SERVER TEXT,
				DE_INCLUDES TEXT,
				PARA_RPO TEXT,
				PARA_SMARTCLIENT TEXT,
				PARA_SERVER TEXT,
				PARA_INCLUDES TEXT,
				BD_BKPBANCO TEXT,
				BD_SERVIDOR TEXT,
				BD_NOMEBANCO TEXT,
				BD_USUARIO TEXT,
				BD_SENHA TEXT,
				FONTES TEXT,
				PATCH TEXT,
				DE_DBACCESS TEXT,
				PARA_DBACCESS TEXT)''')
		except Exception as e:
			print('[x] Falha ao criar tabela: %s [x]' % e)

	def inserir_registro(self):
		inseriu = False
		msgErro = ""
		try:
			self.cur.execute(
				f'''INSERT OR REPLACE INTO AMBIENTES VALUES ( '{self.get_id()}'
															 , '{self.get_descricao()}'
															 , '{self.get_de_rpo()}'
															 , '{self.get_de_smartClient()}'
															 , '{self.get_de_server()}'
															 , '{self.get_de_includes()}'
															 , '{self.get_para_rpo()}'
															 , '{self.get_para_smartClient()}'
															 , '{self.get_para_server()}'
															 , '{self.get_para_includes()}'
															 , '{self.get_bd_bkpBanco()}'
															 , '{self.get_bd_servidor()}'
															 , '{self.get_bd_nomeBanco()}'
															 , '{self.get_bd_usuario()}'
															 , '{self.get_bd_senha()}'
															 , '{self.get_fontes()}'
															 , '{self.get_patch()}'
															 , '{self.get_de_dbAccess()}'
															 , '{self.get_para_dbAccess()}')''')
		except Exception as e:
			msgErro = 'Falha ao inserir registro\n'
			msgErro += 'Detalhes: '
			for erro in e.args:
				msgErro += erro+'\n'
			self.con.rollback()
			inseriu = False
		else:
			self.con.commit()
			inseriu = True
		return {"inseriu":inseriu, "msgErro": msgErro}

	def consultar_registros(self):
		return self.cur.execute('SELECT ID, DESCRICAO FROM AMBIENTES ORDER BY ID').fetchall()

	def load_registro(self, ID):
		item = self.cur.execute(f'SELECT * FROM AMBIENTES WHERE ID = {ID}').fetchall()[0]
		self.set_id(item[0])
		self.set_descricao(item[1])
		self.set_de_rpo(item[2])
		self.set_de_smartClient(item[3])
		self.set_de_server(item[4])
		self.set_de_includes(item[5])
		self.set_para_rpo(item[6])
		self.set_para_smartClient(item[7])
		self.set_para_server(item[8])
		self.set_para_includes(item[9])
		self.set_bd_bkpBanco(item[10])
		self.set_bd_servidor(item[11])
		self.set_bd_nomeBanco(item[12])
		self.set_bd_usuario(item[13])
		self.set_bd_senha(item[14])
		self.set_fontes(item[15])
		self.set_patch(item[16])
		self.set_de_dbAccess(item[17])
		self.set_para_dbAccess(item[18])

	def consultar_ultimo_id(self):
		ultimoID = self.cur.execute('SELECT MAX(id) FROM AMBIENTES').fetchone()[0]
		if ultimoID == None:
			ultimoID = '0'
		return ultimoID

	def consultar_proximo_id(self):
		ultimoID = self.consultar_ultimo_id()
		proximoID = int(ultimoID) + 1
		return str(proximoID)

	def remover_registro(self, id):
		removido = False
		msgErro = ''
		try:
			self.cur.execute("DELETE FROM AMBIENTES WHERE id=?", (id,))
		except Exception as e:
			msgErro = f'\nFalha ao remover registro\n{e}'
			self.con.rollback()
			removido = False
		else:
			self.con.commit()
			removido = True
		return {'removido':removido, 'msgErro':msgErro}

	def isDadosBd(self):
		gerarBkpBd = True
		gerarBkpBd = gerarBkpBd and isNotEmpty(self.get_bd_bkpBanco())
		gerarBkpBd = gerarBkpBd and isNotEmpty(self.get_bd_nomeBanco())
		gerarBkpBd = gerarBkpBd and isNotEmpty(self.get_bd_senha())
		gerarBkpBd = gerarBkpBd and isNotEmpty(self.get_bd_servidor())
		gerarBkpBd = gerarBkpBd and isNotEmpty(self.get_bd_usuario())

		return gerarBkpBd

	def set_id(self, val=''):
		self.id = val

	def set_descricao(self, val=''):
		self.descricao = val

	def set_de_rpo(self, val=''):
		self.de_rpo = val

	def set_de_smartClient(self, val=''):
		self.de_smartClient = val

	def set_de_server(self, val=''):
		self.de_server = val

	def set_de_includes(self, val=''):
		self.de_includes = val

	def set_para_rpo(self, val=''):
		self.para_rpo = val

	def set_para_smartClient(self, val=''):
		self.para_smartClient = val

	def set_para_server(self, val=''):
		self.para_server = val

	def set_para_includes(self, val=''):
		self.para_includes = val

	def set_bd_bkpBanco(self, val=''):
		self.bd_bkpBanco = val

	def set_bd_servidor(self, val=''):
		self.bd_servidor = val

	def set_bd_nomeBanco(self, val=''):
		self.bd_nomeBanco = val

	def set_bd_usuario(self, val=''):
		self.bd_usuario = val

	def set_bd_senha(self, val=''):
		self.bd_senha = val

	def set_fontes(self, val=''):
		self.fontes = val

	def set_patch(self, val=''):
		self.patch = val

	def set_de_dbAccess(self, val=''):
		self.de_dbAccess = val

	def set_para_dbAccess(self, val=''):
		self.para_dbAccess = val

	def get_id(self):
		return self.id

	def get_descricao(self):
		return self.descricao

	def get_de_rpo(self):
		return self.de_rpo

	def get_de_smartClient(self):
		return self.de_smartClient

	def get_de_server(self):
		return self.de_server

	def get_de_includes(self):
		return self.de_includes

	def get_para_rpo(self):
		return self.para_rpo

	def get_para_smartClient(self):
		return self.para_smartClient

	def get_para_server(self):
		return self.para_server

	def get_para_includes(self):
		return self.para_includes

	def get_bd_bkpBanco(self):
		return self.bd_bkpBanco

	def get_bd_servidor(self):
		return self.bd_servidor

	def get_bd_nomeBanco(self):
		return self.bd_nomeBanco

	def get_bd_usuario(self):
		return self.bd_usuario

	def get_bd_senha(self):
		return self.bd_senha

	def get_fontes(self):
		return self.fontes

	def get_patch(self):
		return self.patch

	def get_de_dbAccess(self):
		return self.de_dbAccess

	def get_para_dbAccess(self):
		return self.para_dbAccess

def isNotEmpty(s):
	return bool(s and s.strip())