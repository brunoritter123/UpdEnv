#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza ambientes"""
from fontes.janela import Janela
import tkinter as tk
import sys

execConsole = False

for param in sys.argv:

	if param == "-console":
		execConsole = True

	elif sys.argv[0] != param:
		print(f"Váriavel '{param}' foi ignorada.")

if execConsole:
	print("Execução via console")
	input()

else:
	root = tk.Tk()
	app = Janela(master=root)
	app.mainloop()