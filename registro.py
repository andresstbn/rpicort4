#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime
from random import randint

########################################################################
# Control Enderezadora y Cortadora                                     #
# Desarrollo del software y el hardware:                               #
#    Daniel Andrés Esteban C.                                          #
#    Cel. 3002927538                                                   #
# Cúcuta, Colombia - Última actualización: Julio de 2019               #
########################################################################
import time

class Registrador():
	def __init__(self, filename):
		self.conn = sqlite3.connect(filename, check_same_thread=False)
		self.c = self.conn.cursor()

	def obtener_configuraciones(self):
		self.c.execute("SELECT tiempo_embrague, tiempo_bloqueo, contador, cantidad, longitud FROM config WHERE usuario =1")
		(tiempo_embrague, tiempo_bloqueo, contador, cantidad, longitud) = self.c.fetchone()
		diccionario = {"tiempo_embrague": tiempo_embrague, "tiempo_bloqueo": tiempo_bloqueo, "contador": contador,
						"longitud": longitud, "cantidad":cantidad}
		return diccionario
	
	def guardar_var(self, varnombre, varvalor):
		sql = "UPDATE config SET {} = ? WHERE usuario=1".format(varnombre)
		# ~ print(sql)
		self.c.execute(sql, (varvalor,))
		self.conn.commit()
	
	def obtener_var(self, varnombre):
		self.c.execute("SELECT {} FROM config WHERE usuario =1".format(varnombre))
		varvalor = self.c.fetchone()
		return varvalor[0]
	
	def incrementar_contador(self):
		sql = "UPDATE config SET contador=contador+1 WHERE usuario=1"
		# ~ print(sql)
		self.c.execute(sql)
		self.conn.commit()
		
	def cerrar(self):
		self.conn.close()
	

		

