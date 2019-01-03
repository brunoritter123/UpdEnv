import tkinter as tk

class meuEntry(tk.Entry):
	def set_tag(self, tag):
		self.tag = tag

	def get_tag(self):
		return self.tag