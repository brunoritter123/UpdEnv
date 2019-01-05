#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera janela para cadastrar os ambientes"""
import tkinter as tk
import tkinter.ttk as tkk
import tkinter.filedialog as fdlg
from tkinter import messagebox
from fontes.mdAmbiente import mdAmbiente
from fontes.meuEntry import meuEntry

class Janela(tk.Frame):
	"""Janela principal"""

	def __init__(self, master=None):
		"""Construtor"""
		super().__init__(master)

		self.root = master
		self.rowCadastro = 0
		self.alterar = False
		self.dadosCad = {}

		# Coletando informações do monitor
		largura = round(self.winfo_screenwidth() / 2)
		altura = round(self.winfo_screenheight() / 2)
		tamanho = ('%sx%s' % (largura, altura))

		# Título da janela principal.
		master.title('Update Environment')

		# Tamanho da janela principal.
		master.geometry(tamanho)

		# Instanciando a conexão com o banco.
		self.mdAmbiente = mdAmbiente()

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

	def inclui_aba_cadastro(self, hide = True, ID = '0'):
		self.abasPrincipal.add(self.abaCadastro,text='Cadastro')
		if ID == '0':
			ID = self.mdAmbiente.consultar_proximo_id()
			self.mdAmbiente.set_id(ID)
			self.alterar = False
		else:
			self.mdAmbiente.load_registro(ID)
			self.load_entry()
			self.alterar = True

		if hide:
			self.abasPrincipal.hide(0)

	def inclui_widgets_consulta(self, parent):

		# Containers.
		frame1 = tk.Frame(parent)
		frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

		frame1R = tk.Frame(frame1)
		frame1R.pack(side=tk.RIGHT)

		frame1L = tk.Frame(frame1)
		frame1L.pack(side=tk.LEFT)

		frame2 = tk.Frame(parent)
		frame2.pack(fill=tk.BOTH, expand=True)

		frame3 = tk.Frame(parent)
		frame3.pack(side=tk.BOTTOM, padx=5)

		# Labels.
		label_pesquisa = tk.Label(frame1L, text='Pesquisar')
		label_pesquisa.grid(row=0, column=0)

		# Entrada de texto.
		self.pesquisa = meuEntry(frame1L, width=50)
		self.pesquisa.bind('<Key>', self.pesquisa_grid)
		self.pesquisa.grid(row=0, column=1, padx=5, pady=10)

		# Botão
		button_alterar = tk.Button(frame1R, text='Alterar', bg='blue', fg='white')
		button_alterar['command'] = self.alterar_registro
		button_alterar.grid(row=0, column=0, padx=10, pady=10)

		button_adicionar = tk.Button(frame1R, text='Adicionar', bg='green', fg='white')
		button_adicionar['command'] = self.inclui_aba_cadastro
		button_adicionar.grid(row=0, column=1, padx=10, pady=10)

		# Treeview.
		self.treeview = tkk.Treeview(frame2, columns=('descricao'))
		self.treeview.heading('#0', text='ID')
		self.treeview.heading('#1', text='Descrição')

		# Inserindo os dados do banco no treeview.
		for row in self.mdAmbiente.consultar_registros():
			self.treeview.insert('', 'end', text=row[0], value=row[1].strip().replace(' ', '_') )

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

		self.add_origem(parent=frame1, name='Descrição', incluiBtn = False,
						command=lambda val : self.mdAmbiente.set_descricao(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_descricao()))

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
		btn_salvar['command'] = self.adicionar_registro
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

		self.add_origem(parent=frameDePara, name='RPO', filetype='.rpo',
						command=lambda val : self.mdAmbiente.set_de_rpo(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_de_rpo()))
		self.add_destino(parent=frameDePara, name='RPO',
						command=lambda val : self.mdAmbiente.set_para_rpo(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_para_rpo()))

		self.add_origem(parent=frameDePara, name='Smart Client', filetype='.zip',
						command=lambda val : self.mdAmbiente.set_de_smartClient(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_de_smartClient()))
		self.add_destino(parent=frameDePara, name='Smart Client',
						command=lambda val : self.mdAmbiente.set_para_smartClient(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_para_smartClient()))

		self.add_origem(parent=frameDePara, name='Server', filetype='.zip',
						command=lambda val : self.mdAmbiente.set_de_server(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_de_server()))
		self.add_destino(parent=frameDePara, name='Server',
						command=lambda val : self.mdAmbiente.set_para_server(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_para_server()))

		self.add_origem(parent=frameDePara, name='Includes', filetype='.zip',
						command=lambda val : self.mdAmbiente.set_de_includes(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_de_includes()))
		self.add_destino(parent=frameDePara, name='Includes',
						command=lambda val : self.mdAmbiente.set_para_includes(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_para_includes()))

		self.add_origem(parent=frameDePara, name='DbAccess', filetype='.zip',
						command=lambda val : self.mdAmbiente.set_de_dbAccess(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_de_dbAccess()))
		self.add_destino(parent=frameDePara, name='DbAccess',
						command=lambda val : self.mdAmbiente.set_para_dbAccess(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_para_dbAccess()))

	def inclui_widgets_Banco(self, parent):
		frameBanco = tk.Frame(parent)
		frameBanco.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
		self.add_origem(parent=frameBanco, name='Bkp Banco', filetype='.bak',
						command=lambda val : self.mdAmbiente.set_bd_bkpBanco(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_bd_bkpBanco()))
		self.add_origem(parent=frameBanco, name='Servidor', incluiBtn = False,
						command=lambda val : self.mdAmbiente.set_bd_servidor(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_bd_servidor()))
		self.add_origem(parent=frameBanco, name='Nome Banco', incluiBtn = False,
						command=lambda val : self.mdAmbiente.set_bd_nomeBanco(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_bd_nomeBanco()))
		self.add_origem(parent=frameBanco, name='Usuario', incluiBtn = False,
						command=lambda val : self.mdAmbiente.set_bd_usuario(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_bd_usuario()))
		self.add_origem(parent=frameBanco, name='Senha', incluiBtn = False,
						command=lambda val : self.mdAmbiente.set_bd_senha(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_bd_senha()))

	def inclui_widgets_Fontes(self, parent):
		frameFontes = tk.Frame(parent)
		frameFontes.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
		self.add_origem(parent=frameFontes, name='Fontes',
						command=lambda val : self.mdAmbiente.set_fontes(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_fontes()))
		self.add_origem(parent=frameFontes, name='Patch', filetype='.ptm',
						command=lambda val : self.mdAmbiente.set_patch(val),
						load=lambda entry : atualizaEntry(entry,self.mdAmbiente.get_patch()))

	def getRowCad(self):
		self.rowCadastro += 1
		return self.rowCadastro

	def digitando(self, event, command = None):
		if command != None:
			command(event.widget.get())

	def add_origem(self, parent, name, filetype = None, incluiPara = True, incluiBtn = True, command = None, load = None):
		rowDePara = self.getRowCad()

		label = tk.Label(parent, text=name)
		label.grid(row=rowDePara, column=1)

		de = meuEntry(parent, width=40)
		de.set_tag(load)
		de.grid(row=rowDePara, column=2, pady=5)
		de.bind('<KeyRelease>', lambda e, arg1=command : self.digitando(event=e, command=arg1))
		if incluiBtn:
			btn_de = tk.Button(parent, text = '...', bg='blue', fg='white')
			btn_de['command'] = lambda arg1=de, arg2=filetype, arg3=command : self.openDirectory(arg1, arg2, arg3)
			btn_de.grid(row=rowDePara, column=3, pady=5)

	def add_destino(self, parent, name, incluiBtn = True, command = None, load = None):
		rowDePara = self.rowCadastro

		para = meuEntry(parent, width=40)
		para.set_tag(load)
		para.grid(row=rowDePara, column=5, pady=5)
		para.bind('<KeyRelease>', lambda e, arg1=command : self.digitando(event=e, command=arg1))
		if incluiBtn:
			btn_para = tk.Button(parent, text = '...', bg='blue', fg='white')
			btn_para['command'] = lambda arg1=para, arg2=None, arg3=command : self.openDirectory(arg1, arg2, arg3)
			btn_para.grid(row=rowDePara, column=6, pady=5)

	def adicionar_registro(self):
		# Se a data digitada passar na validação
		if isNotEmpty(self.mdAmbiente.get_descricao()):
			# Dados digitando são inseridos no banco de dados
			retInsert = self.mdAmbiente.inserir_registro()
			if retInsert['inseriu']:
				# Adicionando os novos dados no treeview.
				if self.alterar:
					self.treeview.item(self.item_selecionado, text=self.mdAmbiente.get_id(), value=self.mdAmbiente.get_descricao().strip().replace(' ', '_'))
				else:
					self.treeview.insert('', 'end', text=self.mdAmbiente.get_id(), value=self.mdAmbiente.get_descricao().strip().replace(' ', '_'))
				self.reset_cadastro()
				messagebox.showinfo('Concluído', 'Ambiente foi salvo.')
			else:
				messagebox.showerror('Erro', retInsert['msgErro'])

		else:
			messagebox.showerror('Erro', 'É obrigatório informar a descrição do ambiente.')

	def excluir_registro(self):
		# Verificando se algum item está selecionado.
		if not self.treeview.focus():
			messagebox.showerror('Erro', 'Nenhum item selecionado')
		else:
			# Coletando qual item está selecionado.
			item_selecionado = self.treeview.focus()

			# Coletando os dados do item selecionado (dicionário).
			id = self.treeview.item(item_selecionado)

			# Removendo o item com base no valor do id (argumento text do treeview).
			# Removendo valor da tabela.
			retRemove = self.mdAmbiente.remover_registro(id['text'])

			if retRemove['removido']:
				# Removendo valor do treeview.
				self.treeview.delete(item_selecionado)
			else:
				messagebox.showerror('Erro', retRemove['msgErro'])

	def alterar_registro(self):
		# Verificando se algum item está selecionado.
		if not self.treeview.focus():
			messagebox.showerror('Erro', 'Nenhum item selecionado')
		else:
			self.item_selecionado = self.treeview.focus()
			id = self.treeview.item(self.item_selecionado)
			self.inclui_aba_cadastro(ID = id['text'])


	def openDirectory(self, entry, filetype = None, command = None):
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
			command(entry.get())

		print (nomeDiretorio)

	def reset_cadastro(self):
		self.mdAmbiente.reset_values()
		self.load_entry()
		self.abasCadastro.select(0)

	def load_entry(self, frame = None):
		if frame == None:
			frame = self.abaCadastro

		for child in frame.children.values():
			if child.widgetName == 'frame' or child.widgetName == 'ttk::notebook':
				self.load_entry(child)

			elif child.widgetName == 'entry':
				load = child.get_tag()
				load(child)

	def pesquisa_grid(self, event, item = ''):
		achou = True
		if event.keycode == 13: #enter
			achou = False
			pesquisa = event.widget.get().strip().replace(' ', '_')
			children = self.treeview.get_children(item)
			for child in children:
				values = self.treeview.item(child, 'value')
				for text in values:
					achou = False
					if pesquisa.upper() in text.upper():
						self.treeview.selection_set(child)
						self.treeview.focus(child)
						achou = True
				if achou:
					break
				else:
					achou = self.pesquisa_grid(event, child)
		return achou

def isNotEmpty(s):
	return bool(s and s.strip())

def atualizaEntry(entry, val):
	entry.delete(0,tk.END)
	entry.insert(0,val)
