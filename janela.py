#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera janela para cadastrar os ambientes"""
import re
import tkinter as tk
import tkinter.ttk as tkk
import tkinter.filedialog as fdlg
from tkinter import messagebox
from fontes.conectarDb import ConectarDB

class Janela(tk.Frame):
	"""Janela principal"""

	def __init__(self, master=None):
		"""Construtor"""
		super().__init__(master)

		self.root = master
		self.rowDePara = 0

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
		self.criar_widgets(master)

	def criar_widgets(self, master):
		# Abas.
		abas = tkk.Notebook(master)
		abaConsulta = tk.Frame(abas)
		abaCadastro = tk.Frame(abas)

		abas.add(abaConsulta,text='Consulta')
		abas.add(abaCadastro,text='Cadastro')
		abas.pack(fill=tk.BOTH, expand=True)

		self.inclui_widgets_consulta(abaConsulta)
		self.inclui_widgets_cadastro(abaCadastro)

		abas.hide(0)

	def inclui_widgets_consulta(self, parent):

		# Containers.
		frame1 = tk.Frame(parent)
		frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

		frame2 = tk.Frame(parent)
		frame2.pack(fill=tk.BOTH, expand=True)

		frame3 = tk.Frame(parent)
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

		# Botão diretório
		button_dir = tk.Button(frame1, text='Dir', bg='green', fg='white')
		# Método que é chamado quando o botão é clicado.
		button_dir['command'] = self.testeaskdirectory
		button_dir.grid(row=0, column=4, rowspan=2, padx=10)

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

	def inclui_widgets_cadastro(self, parent):
		frame = tk.Frame(parent)
		frame.pack(fill=tk.BOTH, expand=True)

		label_de = tk.Label(frame, text='De:')
		label_de.grid(row=0, column=2)

		label_x = tk.Label(frame, text='x')
		label_x.grid(row=0, column=4, padx=10)

		label_para = tk.Label(frame, text='Para:')
		label_para.grid(row=0, column=5)

		# RPO
		self.add_de_x_para(frame, 'RPO')

	def add_de_x_para(self, parent, name):
		self.rowDePara += 1

		img = tk.PhotoImage(file="lupa.png")
		small_img = img.subsample(8, 8)


		label = tk.Label(parent, text=name)
		label.grid(row=self.rowDePara, column=1)

		self.de = tk.Entry(parent)
		self.de.grid(row=self.rowDePara, column=2)
		btn_de = tk.Button(parent, image=small_img)
		btn_de['command'] = self.testeaskdirectory
		btn_de.grid(row=self.rowDePara, column=3)

		self.para = tk.Entry(parent)
		self.para.grid(row=self.rowDePara, column=5)
		btn_para = tk.Button(parent, text='Dir', bg='green', fg='white', width=2, image=img)
		btn_para['command'] = self.testeaskdirectory
		btn_para.grid(row=self.rowDePara, column=6)


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

	def testeaskdirectory(self):
		#primeiro definimos as opções

		opcoes = {}                 # as opções são definidas em um dicionário
		#opcoes['defaultextension'] = '.txt'
		#opcoes['filetypes'] = [('Todos arquivos', '.*'), ('arquivos texto', '.txt')]
		opcoes['initialdir'] = ''    # será o diretório atual
		#opcoes['initialfile'] = '' #apresenta todos os arquivos no diretorio
		opcoes['parent'] = self.root
		opcoes['title'] = 'Diálogo que retorna o nome do diretório selecionado'

		#retorna o caminho completo  de um diretório

		nomeDiretorio= fdlg.askdirectory(**opcoes)

		print (nomeDiretorio)
