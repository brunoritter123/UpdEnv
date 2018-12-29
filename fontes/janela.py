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
		self.rowCadastro = 0

		# Coletando informações do monitor
		largura = round(self.winfo_screenwidth() / 2)
		altura = round(self.winfo_screenheight() / 2)
		tamanho = ('%sx%s' % (largura, altura))

		# Título da janela principal.
		master.title('Update Environment')

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
		self.abasPrincipal = tkk.Notebook(master)
		self.abaConsulta = tk.Frame(self.abasPrincipal)
		self.abaCadastro = tk.Frame(self.abasPrincipal)

		self.inclui_aba_consulta(hide = False)
		self.abasPrincipal.pack(fill=tk.BOTH, expand=True)

		self.inclui_widgets_consulta(self.abaConsulta)
		self.inclui_widgets_cadastro(self.abaCadastro)


	def inclui_aba_consulta(self, hide = True):
		self.abasPrincipal.add(self.abaConsulta,text='Consulta')
		if hide:
			self.abasPrincipal.hide(1)
			self.reset_cadastro()

	def inclui_aba_cadastro(self, hide = True):
		self.abasPrincipal.add(self.abaCadastro,text='Cadastro')
		if hide:
			self.abasPrincipal.hide(0)

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
		button_adicionar['command'] = self.inclui_aba_cadastro
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

	def inclui_widgets_cadastro(self, parent):
		# Containers.
		frame1 = tk.Frame(parent)
		frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

		frame2 = tk.Frame(parent)
		frame2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

		frame3 = tk.Frame(parent)
		frame3.pack(side=tk.RIGHT, padx=5)

		self.add_de_x_para(parent=frame1, name='Descrição', incluiPara = False, incluiBtn = False)

		# Abas.
		self.abasCadastro = tkk.Notebook(frame2)
		abaDePara = tk.Frame(self.abasCadastro)
		abaBanco = tk.Frame(self.abasCadastro)
		abaFontes = tk.Frame(self.abasCadastro)

		self.abasCadastro.add(abaDePara, text='Ambiente')
		self.abasCadastro.add(abaBanco, text='Config. Banco')
		self.abasCadastro.add(abaFontes, text='Fontes')
		self.abasCadastro.pack(fill=tk.BOTH, expand=True)

		self.inclui_widgets_De_Para(abaDePara)
		self.inclui_widgets_Banco(abaBanco)
		self.inclui_widgets_Fontes(abaFontes)

		rowBtns = self.getRowCad()

		btn_cancelar = tk.Button(frame3, text = 'Cancelar', bg='red', fg='white')
		btn_cancelar['command'] = self.inclui_aba_consulta
		btn_cancelar.grid(row=rowBtns, column=1, pady=10, padx=20)

		btn_salvar = tk.Button(frame3, text = 'Salvar', bg='green', fg='white')
		btn_salvar['command'] = lambda arg1='Salvo' : print(arg1)
		btn_salvar.grid(row=rowBtns, column=2, pady=10, padx=20)

	def inclui_widgets_De_Para(self, parent):
		frameDePara = tk.Frame(parent)
		frameDePara.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

		label_de = tk.Label(frameDePara, text='Origem:')
		label_de.grid(row=0, column=2)

		label_x = tk.Label(frameDePara, text='x')
		label_x.grid(row=0, column=4, padx=10)

		label_para = tk.Label(frameDePara, text='Destino:')
		label_para.grid(row=0, column=5)

		self.add_de_x_para(parent=frameDePara, name='RPO', filetype='.rpo')
		self.add_de_x_para(parent=frameDePara, name='Smart Client', filetype='.zip')
		self.add_de_x_para(parent=frameDePara, name='Server', filetype='.zip')
		self.add_de_x_para(parent=frameDePara, name='Includes', filetype='.zip')

	def inclui_widgets_Banco(self, parent):
		frameBanco = tk.Frame(parent)
		frameBanco.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
		self.add_de_x_para(parent=frameBanco, name='Bkp Banco', filetype='.bak', incluiPara = False)
		self.add_de_x_para(parent=frameBanco, name='Servidor', incluiPara = False, incluiBtn = False)
		self.add_de_x_para(parent=frameBanco, name='Nome Banco', incluiPara = False, incluiBtn = False)
		self.add_de_x_para(parent=frameBanco, name='Usuário', incluiPara = False, incluiBtn = False)
		self.add_de_x_para(parent=frameBanco, name='Senha', incluiPara = False, incluiBtn = False)

	def inclui_widgets_Fontes(self, parent):
		frameFontes = tk.Frame(parent)
		frameFontes.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
		self.add_de_x_para(parent=frameFontes, name='Fontes', incluiPara = False)
		self.add_de_x_para(parent=frameFontes, name='Patch', filetype='.ptm', incluiPara = False)

	def getRowCad(self):
		self.rowCadastro += 1
		return self.rowCadastro

	def add_de_x_para(self, parent, name, filetype = None, incluiPara = True, incluiBtn = True):
		rowDePara = self.getRowCad()

		label = tk.Label(parent, text=name)
		label.grid(row=rowDePara, column=1)

		de = tk.Entry(parent, width=40)
		de.grid(row=rowDePara, column=2, pady=5)
		if incluiBtn:
			btn_de = tk.Button(parent, text = '...', bg='blue', fg='white')
			btn_de['command'] = lambda arg1=de, arg2=filetype : self.openDirectory(arg1, arg2)
			btn_de.grid(row=rowDePara, column=3, pady=5)

		if incluiPara:
			para = tk.Entry(parent, width=40)
			para.grid(row=rowDePara, column=5, pady=5)
			if incluiBtn:
				btn_para = tk.Button(parent, text = '...', bg='blue', fg='white')
				btn_para['command'] = lambda arg1=para : self.openDirectory(arg1)
				btn_para.grid(row=rowDePara, column=6, pady=5)


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

	def openDirectory(self, entry, filetype = None):
		#primeiro definimos as opções
		opcoes = {}                 # as opções são definidas em um dicionário
		if filetype != None:
			opcoes['defaultextension'] = filetype
			opcoes['filetypes'] = [('Todos arquivos', filetype)]
		opcoes['initialdir'] = ''    # será o diretório atual
		#opcoes['initialfile'] = '' #apresenta todos os arquivos no diretorio
		opcoes['parent'] = self.root
		opcoes['title'] = 'Selecione'

		#retorna o caminho completo  de um diretório

		if filetype == None:
			nomeDiretorio = fdlg.askdirectory(**opcoes)
		else:
			nomeDiretorio = fdlg.askopenfilename(**opcoes)

		if nomeDiretorio != None and len(nomeDiretorio) > 0:
			entry.delete(0, tk.END)
			entry.insert(0, nomeDiretorio)

		print (nomeDiretorio)

	def reset_cadastro(self):
		for child in self.abaCadastro.children.values():
			if child.widgetName == 'frame':
				self.limpar_entry(child)

			elif child.widgetName == 'entry':
				child.delete(0, tk.END)
		self.abasCadastro.select(0)

	def limpar_entry(self, frame):
		for child in frame.children.values():
			if child.widgetName == 'frame' or child.widgetName == 'ttk::notebook':
				self.limpar_entry(child)

			elif child.widgetName == 'entry':
				child.delete(0, tk.END)
