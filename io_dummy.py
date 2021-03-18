#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################################
# Control para enderezadora-cortadora                                  #
# Programó: Daniel A. Esteban                                          #
# Última actualización: junio de 2019                                  #
########################################################################

import conf

def output(arg1, arg2):
	if conf.hablador:
		print("{}: {}".format(repr(arg1), repr(arg2)))
	
def cleanup():
	print("Cleaned IO")
	pass

def input(arg1):
	sal = False
	# ~ print("{}: {}".format(nombre_pin[repr(arg1)], repr(sal)))
	return sal
	
HIGH = "apagado"
LOW  = "encendido"


