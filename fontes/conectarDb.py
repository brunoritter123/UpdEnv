#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Classa que controla o banco de dados"""
import sqlite3

class ConectarDB:
	def __init__(self):
		self.con = sqlite3.connect('dados/db.sqlite3')
		self.cur = self.con.cursor()
		self.criar_tabela()

	def criar_tabela(self):
		try:
			self.cur.execute('''CREATE TABLE IF NOT EXISTS NomeDaTabela (
				n_documento TEXT,
				assunto TEXT,
				data TEXT)''')
		except Exception as e:
			print('[x] Falha ao criar tabela: %s [x]' % e)
		else:
			print('\n[!] Tabela criada com sucesso [!]\n')

	def inserir_registro(self, ndocumento, assunto, data):
		try:
			self.cur.execute(
				'''INSERT INTO NomeDaTabela VALUES (?, ?, ?)''', (ndocumento, assunto, data,))
		except Exception as e:
			print('\n[x] Falha ao inserir registro [x]\n')
			print('[x] Revertendo operação (rollback) %s [x]\n' % e)
			self.con.rollback()
		else:
			self.con.commit()
			print('\n[!] Registro inserido com sucesso [!]\n')

	def consultar_registros(self):
		return self.cur.execute('SELECT rowid, * FROM NomeDaTabela').fetchall()

	def consultar_ultimo_rowid(self):
		return self.cur.execute('SELECT MAX(rowid) FROM NomeDaTabela').fetchone()

	def remover_registro(self, rowid):
		try:
			self.cur.execute("DELETE FROM NomeDaTabela WHERE rowid=?", (rowid,))
		except Exception as e:
			print('\n[x] Falha ao remover registro [x]\n')
			print('[x] Revertendo operação (rollback) %s [x]\n' % e)
			self.con.rollback()
		else:
			self.con.commit()
			print('\n[!] Registro removido com sucesso [!]\n')