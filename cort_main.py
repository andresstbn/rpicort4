#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################################
# Control Enderezadora y Cortadora                                     #
# Desarrollo del software y el hardware:                               #
#    Daniel Andrés Esteban C.                                          #
#    Cel. 3002927538                                                   #
# Cúcuta, Colombia - Última actualización: Julio de 2019               #
########################################################################



import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import threading
import queue
import registro
import maquina3 as maquina2
import conf
import sys
# ~ import otherwindow
from time import time, sleep

class ControlCortadora(Gtk.Window):
	def __init__(self):
		rpi = True
		
		if len(sys.argv) > 1:
			if "norpi" in sys.argv:
				rpi = False
				print("No RPI")
		
		self.cola = queue.Queue()
		self.maq = maquina2.Maquina(rpi)
		bldr = Gtk.Builder()
		bldr.add_from_file('cort_gui2.glade')
		
		def obtener(nombre): 
			obj = bldr.get_object(nombre)
			if obj == None:
				print(nombre + " no encontrado")
			return obj
		self.estado_embrague = False
		self.window_main = obtener("WindowMain")
		self.window_teclado = obtener("WindowTeclado")
		self.window_ajustes = obtener("WindowAjustes")
		self.entry_longs = obtener("EntryLong")
		self.entry_cant = obtener("EntryCant")
		button_tecl_longs = obtener("ButtonTeclLong")
		button_tecl_cant = obtener("ButtonTeclCant")
		button_tecl_tiempo = obtener("ButtonTeclTiempo")
		button_tecl_tiempob = obtener("ButtonTeclTiempoB")
		button_tecl_borr = obtener("ButtonBorr")
		button_tecl_ok = obtener("ButtonOk")
		button_actualizar = obtener("ButtonActualizar")
		self.button_detener = obtener("ButtonDetener")
		self.button_salir_conf = obtener("ButtonSalirConf")
		button_terminar_actual = obtener("ButtonTerminarActual")
		button_reiniciar_contador = obtener("ButtonReiniciarContador")
		button_cortar = obtener("ButtonCortar")
		self.switch_motor = obtener("SwitchMotor")
		self.switch_apertura = obtener("SwitchApertura")
		# ~ self.switch_embrague = obtener("SwitchEmbrague")
		self.switch_son = obtener("SwitchSon")
		# ~ button_cortar = obtener("ButtonCortar")
		# ~ button_jogmotor = obtener("ButtonJogMotor")
		btn_jmotora = obtener("ButtonJMotorA")
		btn_jmotorr = obtener("ButtonJMotorR")
		btn_jservoa = obtener("ButtonJServoA")
		btn_jservor = obtener("ButtonJServoR")
		self.button_iniciar = obtener("ButtonIniciar")
		self.button_ajustes = obtener("ButtonAjustes")
		self.label_avance = obtener("LabelAvance")
		self.label_objetivo = obtener("LabelObjetivo")
		self.label_tiempo1 = obtener("LabelTiempo1")
		self.label_tiempo2 = obtener("LabelTiempo2")
		# ~ self.label_avance_pers = obtener("LabelAvancePersistente")
		self.label_long= obtener("LabelLong")
		# ~ self.label_tiempo = obtener("LabelTiempo")
		self.label_msg = obtener("LabelMsg")
		# ~ self.textview_historial = obtener("TextViewHistorial")
		self.buffer_historial = obtener("textbuffer1")
		self.entry_tiempo_corte =obtener("EntryTiempoCorte")
		self.entry_tiempo_bloqueo =obtener("EntryTiempoBloqueo")
		button_digit = []
		for i in range(0,10):
			button_digit.append(bldr.get_object("b" + repr(i)))
		
		self.window_main.connect('delete_event', self.salir)
		self.window_teclado.connect('delete_event', 
							self.button_tecl_ok_clicked) 
		button_tecl_longs.connect('clicked', 
							self.button_tecl_clicked, self.entry_longs)
		button_tecl_tiempo.connect('clicked', 
							self.button_tecl_clicked, self.entry_tiempo_corte)
		button_tecl_tiempob.connect('clicked', 
							self.button_tecl_clicked, self.entry_tiempo_bloqueo)
		button_tecl_cant.connect('clicked', 
							self.button_tecl_clicked, self.entry_cant)	
		button_tecl_borr.connect('clicked', 
							self.button_tecl_borr_clicked, None)
		button_tecl_ok.connect('clicked', 
							self.button_tecl_ok_clicked, None)
							
		btns_jog = [btn_jmotora, btn_jmotorr, btn_jservoa, btn_jservor]
		args_btns = ["motora", "motorr", "servoa", "servor"]
		for btn, arg in zip(btns_jog, args_btns):	
			btn.connect('pressed', self.btn_jog_changed, arg, True)
			btn.connect('released', self.btn_jog_changed, arg, False)
			
		# ~ button_jogmotor.connect('pressed', 
							# ~ self.button_jog_changed, True, False)
		# ~ button_jogmotor.connect('released', 
							# ~ self.button_jog_changed, False, False)
		self.button_iniciar.connect('clicked', 
							self.button_iniciar_clicked, None)
		self.button_detener.connect('clicked', 
							self.button_detener_clicked, None)
		# ~ self.entry_tiempo_corte.connect('value_changed', self.value_changed_entry, None)
		
		self.button_ajustes.connect('clicked', self.button_ajustes_clicked, None)
		self.button_salir_conf.connect('clicked', self.button_salir_conf_clicked, None)
		self.switch_motor.connect('state_set', self.switch_actuador_set, "Motor")
		# ~ self.switch_embrague.connect('state_set', self.switch_actuador_set, "Embrague")
		self.switch_son.connect('state_set', self.switch_actuador_set, "ServoOn")
		self.switch_apertura.connect('state_set', self.switch_actuador_set, "Apertura")

		for i in range(10):
			button_digit[i].connect("clicked", self.button_digit_clicked, i)

		button_actualizar.connect('clicked', self.button_actualizar_clicked, None)
		button_terminar_actual.connect('clicked', self.button_terminar_actual_clicked, None)
		button_reiniciar_contador.connect('clicked', self.button_reiniciar_contador_clicked)
		button_cortar.connect('clicked', self.button_cortar_clicked)
			
		#window_main.fullscreen()
		self.window_main.resize(800,250)		
		self.window_main.show_all()
		self.secuencia_actual = []
		
		self.window_main.set_title("Enderezadora/Cortadora JCA - Inmetar")
		# ~ self.window_teclado.set_default_size(400,300)
		
		# Recuperamos de la base de datos info de la ultima sesion #########################
		
		self.reg = registro.Registrador(conf.db_registro)
		self.configs = self.reg.obtener_configuraciones()
		
		self.tiempo_embrague = self.configs["tiempo_embrague"]		
		self.cantidad = self.configs["cantidad"]
		self.longitud = self.configs["longitud"]
		self.contador = self.configs["contador"]
		self.tiempo_bloqueo = self.configs["tiempo_bloqueo"]
		# ~ self.label_avance_pers.set_text(str(self.configs["contador"]))
		
		self.label_avance.set_text(str(self.configs["contador"]))
		self.label_objetivo.set_text(str(self.configs["cantidad"]))
		self.label_long.set_text(str(self.configs["longitud"]))
		# ~ self.label_tiempo.set_text(str(self.configs["tiempo_embrague"]))
		self.entry_tiempo_corte.set_text(str(self.configs["tiempo_embrague"]))
		self.entry_tiempo_bloqueo.set_text(str(self.configs["tiempo_bloqueo"]))
		self.entry_longs.set_text(str(self.configs["longitud"]))
		self.entry_cant.set_text(str(self.configs["cantidad"]))
		
		tiempo_ciclo = self.configs["longitud"]/50
		self.label_tiempo1.set_text("{:.2f} s/tramo".format(tiempo_ciclo))
		self.label_tiempo2.set_text("{:.0f} tramos/hora".format(3600.0/tiempo_ciclo))
		
		
		print(self.reg.obtener_configuraciones())
		self.evnt_parar = threading.Event()
		self.evnt_correr = threading.Event()
		self.evnt_actualizar = threading.Event()
		self.evnt_terminaryparar = threading.Event()
		self.evnt_finciclo = threading.Event()
		self.evnt_sirena = threading.Event()
		self.t = threading.Thread(target=self.segundo_plano, daemon=True)
		self.t.start()
		
		self.switch_son.set_state(True)
		
		
	def button_ajustes_clicked(self, button, data):
		self.window_ajustes.show_all()
	
	def button_salir_conf_clicked(self, button, data):
		self.tiempo_embrague = int(self.entry_tiempo_corte.get_text())
		self.tiempo_bloqueo = int(self.entry_tiempo_bloqueo.get_text())
		self.reg.guardar_var("tiempo_embrague", self.tiempo_embrague)
		self.reg.guardar_var("tiempo_bloqueo", self.tiempo_bloqueo)
		self.window_ajustes.hide()
		
	def button_tecl_clicked(self, button, entry):
		self.window_teclado.set_default_size(400,300)
		self.window_teclado.show_all()
		self.entryfoc = entry
	
	def button_digit_clicked(self, button, i):
		text = self.entryfoc.get_text()
		self.entryfoc.set_text(text + repr(i))
	
	def button_tecl_borr_clicked(self, button, data):
		self.entryfoc.set_text("")
		
	def button_tecl_ok_clicked(self, button, data):
		self.window_teclado.hide()
	
	def button_actualizar_clicked(self, button, data):
		cantidad = int(self.entry_cant.get_text())
		longitud = int(self.entry_longs.get_text())
		self.cola.put(cantidad)
		self.cola.put(longitud)
		self.evnt_actualizar.set()
		self.reg.guardar_var("cantidad", cantidad)
		self.reg.guardar_var("longitud", longitud)
		GLib.idle_add(self.message, "Actualizo Long. y Cant.")
		tiempo_ciclo = longitud/50
		self.label_tiempo1.set_text("{:.2f} s/tramo".format(tiempo_ciclo))
		self.label_tiempo2.set_text("{:.0f} tramos/hora".format(3600.0/tiempo_ciclo))

	# ~ def value_changed_entry(self, entry, data):
	
	
		# ~ self.tiempo_embrague = int(self.entry_tiempo_corte.get_text())
		# ~ self.reg.guardar_var("tiempo_embrague", self.tiempo_embrague)
	
	def btn_jog_changed(self, button, arg, state):
		if arg == 'motora':
			self.maq.motorjog(True, state)
		elif arg == 'motorr':
			self.maq.motorjog(False, state)
		elif arg == 'servoa':
			self.maq.servojog(True, state)
		elif arg == 'servor':
			self.maq.servojog(False, state)
		
		
	def switch_actuador_set(self, switch, state, nombre_actuador):
		print("Actuador: {} State: {}".format(nombre_actuador, state))
		if nombre_actuador == "Motor":
			pass
			self.maq.motorp = state
		elif nombre_actuador =="ServoOn":
			pass
			self.maq.servoon = state
		elif nombre_actuador =="Apertura":
			pass
			self.maq.apertura = state
		else:
			print("No reconozco el actuador")
			
		# ~ if conf.hablador:
			# ~ print("switch_actuador_set(state={}, actuador={})".format(state,nombre_actuador))
		
	def button_iniciar_clicked(self, button, buf):
		# ~ self.maq.bloqueo = False
		self.primer = True
		# ~ GLib.idle_add(self.switch_embrague.set_state, False, priority=GLib.PRIORITY_HIGH)
		GLib.idle_add(self.switch_motor.set_state, False, priority=GLib.PRIORITY_HIGH)
		GLib.idle_add(self.message, "Ejecutando Ciclo")
		# ~ self.tiempo_embrague = int(self.entry_tiempo_corte.get_text())
		# ~ self.reg.guardar_var("tiempo_embrague", self.tiempo_embrague)
		self.evnt_parar.clear()
		self.evnt_correr.set()
			
	def button_detener_clicked(self, button, buf):
		GLib.idle_add(self.message, "Ciclo Detenido")
		# ~ self.maq.motor_principal = False
		self.evnt_sirena.clear()
		self.evnt_correr.clear()
		self.evnt_parar.set()
		
	def salir(self, arg1, arg2):
		self.maq.salir()
		self.reg.cerrar()
		Gtk.main_quit()	

	def button_terminar_actual_clicked(self, button, buf):
		self.evnt_terminaryparar.set()
		print("Detengo al terminar actual")
	
	def button_reiniciar_contador_clicked(self, button):
		self.evnt_sirena.clear()
		self.contador = 0
		self.reg.guardar_var("contador", 0)
		self.label_avance.set_text(repr(0))
	
	def message(self, mensaje):
		self.label_msg.set_text(mensaje)
	
	def actualizar_labels(self, avance, objetivo=None, longitud=None, tiempo=None):
		def settext(label, var):
			if not (var == None):
				label.set_text("{}".format(var))
		settext(self.label_avance, avance)
		settext(self.label_objetivo, objetivo)
		settext(self.label_long, longitud)
		# ~ settext(self.label_tiempo, tiempo)
	
	def sigsleep(self, time_, corte, apertura):
		while(time() < time_):
			if self.evnt_parar.wait(timeout=0.01):
				break
				
		if corte:
			self.maq.cortar()
		self.maq.apertura = apertura
		
	def incrementar_contadores(self, cont):
		self.reg.incrementar_contador()
		self.contador_pers = self.reg.obtener_var("contador")
		GLib.idle_add(self.actualizar_labels, cont, 
			None, None, None)
	
	def segundo_plano(self):
		tic = time()
		cantidad = self.cantidad
		longitud = self.longitud
		ultimodelciclo = False

		while True:
			if self.evnt_actualizar.is_set():
				cantidad = self.cola.get()
				longitud = self.cola.get()
				GLib.idle_add(self.actualizar_labels, None, cantidad, longitud, self.tiempo_embrague)
				self.evnt_actualizar.clear()
				
			if self.evnt_correr.is_set():
				self.maq.motorp = True
				if self.primer:
					t_iniciociclo = time()-0.5 #OJO: Compenso menor longitud de primera varilla
					self.primer = False
					
				ultimodelciclo = ((self.contador+1) >= cantidad)
				tiempo_ciclo = longitud/50
				
				t_finciclo = t_iniciociclo + tiempo_ciclo
				
				# ~ self.sigsleep(t_finciclo-0.2, corte=False, apertura=True)
				self.sigsleep(t_finciclo-0.3, corte=True, apertura=True)
				self.sigsleep(t_finciclo+0.2, corte=False, apertura=False)
				
				if self.evnt_correr.is_set():					
					if self.evnt_terminaryparar.is_set() or ultimodelciclo:
						self.maq.motorp = False
						self.evnt_correr.clear()
						self.evnt_terminaryparar.clear()
						GLib.idle_add(self.message, "Interrumpo ciclo")
						if ultimodelciclo:
							ultimodelciclo = False
							GLib.idle_add(self.message, "Terminé ciclo")		

					t_iniciociclo = time()
					if self.evnt_correr.is_set():	
						self.contador += 1
						self.incrementar_contadores(self.contador)
				else:
					self.maq.motorp = False
			else:
				pass
				sleep(0.1)	
				
	def button_cortar_clicked(self, button):	
		self.maq.cortar()
		
def main():
	control_cortadora = ControlCortadora()
	Gtk.main()

if __name__=="__main__":
	main()
	

