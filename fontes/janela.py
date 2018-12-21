#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera janela para cadastrar os ambientes"""
import re
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox
from fontes.conectarDb import ConectarDB

class Janela(tk.Frame):
	"""Janela principal"""

	def __init__(self, master=None):
		"""Construtor"""
		super().__init__(master)
		# Coletando informações do monitor
		largura = round(self.winfo_screenwidth() / 2)
		altura = round(self.winfo_screenheight() / 2)
		tamanho = ('%sx%s' % (largura, altura))

		# Título da janela principal.
		master.title('Exemplo')

		# Tamanho da janela principal.
		master.geometry(tamanho)

		# Instanciando a conexão com o banco.
		self.banco = ConectarDB()

		# Gerenciador de layout da janela principal.
		self.pack()

		# Criando os widgets da interface.
		self.criar_widgets()

	def criar_widgets(self):
		# Containers.
		frame1 = tk.Frame(self)
		frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

		frame2 = tk.Frame(self)
		frame2.pack(fill=tk.BOTH, expand=True)

		frame3 = tk.Frame(self)
		frame3.pack(side=tk.BOTTOM, padx=5)

		# Labels.
		label_documento = tk.Label(frame1, text='N° Documento')
		label_documento.grid(row=0, column=0)

		label_assunto = tk.Label(frame1, text='Assunto')
		label_assunto.grid(row=0, column=1)

		label_recebido = tk.Label(frame1, text='Data recebimento')
		label_recebido.grid(row=0, column=2)

		# Entrada de texto.
		self.entry_documento = tk.Entry(frame1)
		self.entry_documento.grid(row=1, column=0)

		self.entry_assunto = tk.Entry(frame1)
		self.entry_assunto.grid(row=1, column=1, padx=10)

		self.entry_data = tk.Entry(frame1)
		self.entry_data.grid(row=1, column=2)

		# Botão para adicionar um novo registro.
		button_adicionar = tk.Button(frame1, text='Adicionar', bg='blue', fg='white')
		# Método que é chamado quando o botão é clicado.
		button_adicionar['command'] = self.adicionar_registro
		button_adicionar.grid(row=0, column=3, rowspan=2, padx=10)

		# Treeview.
		self.treeview = tkk.Treeview(frame2, columns=('N° documento', 'Assunto', 'Data'))
		self.treeview.heading('#0', text='ROWID')
		self.treeview.heading('#1', text='N° documento')
		self.treeview.heading('#2', text='Assunto')
		self.treeview.heading('#3', text='Data')

		# Inserindo os dados do banco no treeview.
		for row in self.banco.consultar_registros():
			self.treeview.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))

		self.treeview.pack(fill=tk.BOTH, expand=True)

		# Botão para remover um item.
		button_excluir = tk.Button(frame3, text='Excluir', bg='red', fg='white')
		# Método que é chamado quando o botão é clicado.
		button_excluir['command'] = self.excluir_registro
		button_excluir.pack(pady=10)

	def adicionar_registro(self):
		# Coletando os valores.
		documento = self.entry_documento.get()
		assunto = self.entry_assunto.get()
		data = self.entry_data.get()

		# Validação simples (utilizar datetime deve ser melhor para validar).
		validar_data = re.search(r'(..)/(..)/(....)', data)

		# Se a data digitada passar na validação
		if validar_data:
			# Dados digitando são inseridos no banco de dados
			self.banco.inserir_registro(ndocumento=documento, assunto=assunto, data=data)

			# Coletando a ultima rowid que foi inserida no banco.
			rowid = self.banco.consultar_ultimo_rowid()[0]

			# Adicionando os novos dados no treeview.
			self.treeview.insert('', 'end', text=rowid, values=(documento, assunto, data))
		else:
			# Caso a data não passe na validação é exibido um alerta.
			messagebox.showerror('Erro', 'Padrão de data incorreto, utilize dd/mm/yyyy')

	def excluir_registro(self):
		# Verificando se algum item está selecionado.
		if not self.treeview.focus():
			messagebox.showerror('Erro', 'Nenhum item selecionado')
		else:
			# Coletando qual item está selecionado.
			item_selecionado = self.treeview.focus()

			# Coletando os dados do item selecionado (dicionário).
			rowid = self.treeview.item(item_selecionado)

			# Removendo o item com base no valor do rowid (argumento text do treeview).
			# Removendo valor da tabela.
			self.banco.remover_registro(rowid['text'])

			# Removendo valor do treeview.
			self.treeview.delete(item_selecionado)
