#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################################################################
# Control para enderezadora-cortadora                                  #
# Programó: Daniel A. Esteban                                          #
# Última actualización: junio de 2019                                  #
########################################################################

import time
import conf
import serial
from time import sleep
import RPi.GPIO
import threading


class Maquina():
    estadomotor = None

    def __init__(self, rpi):
        self.rpi = rpi

        global io
        if rpi:
            print("import RPi.GPIO")
            import RPi.GPIO
            io = RPi.GPIO
        else:
            print("import io_dummy")
            import io_dummy
            io = io_dummy

        self.pins_servo = [0, 26, 22, 27]
        self.pins_vfd = [17, 13]
        self.pin_apertura = 4

        # self.t = 1
        self.pin_salidas = self.pins_vfd + \
            self.pins_servo + [self.pin_apertura]
        


        if self.rpi:
            io.setmode(io.BCM)
            io.setup(self.pin_salidas, io.OUT)
            # ~ io.setup(self.pin_sbloqueo, io.IN, pull_up_down=io.PUD_DOWN)
            io.output(self.pin_salidas, io.HIGH)

    def cortar(self):
        t = threading.Thread(target=self.pulsos, args=(2000, False), daemon=True)
        t.start()

    def motorjog(self, sentido, estado):
        if sentido:
            io.output(self.pins_vfd[0], not estado)
        else:
            io.output(self.pins_vfd[1], not estado)
        print("MotorJOG: Sentido: {} Estado:{}".format(sentido, estado))

    def servojog(self, sentido, estado):
        if estado:
            t = threading.Thread(target=self.pulsos, args=(50, sentido), daemon=True)
            t.start()
        # else:
        #     t = threading.Thread(target=self.pulsos, args=(50, sentido), daemon=True)
        #     t.start()
        # if sentido:
        #     io.output(self.pins_servo[2], not estado)
        # else:
        #     io.output(self.pins_servo[3], not estado)
        print("ServoJOG: Sentido: {} Estado:{}".format(sentido, estado))

    @property
    def apertura(self):
        return None

    @apertura.setter
    def apertura(self, estado_):

        if(estado_):
            io.output(self.pin_apertura, io.LOW)
        else:
            io.output(self.pin_apertura, io.HIGH)

    @property
    def servoon(self):
        return None

    @servoon.setter
    def servoon(self, estado_):
        if(estado_):
            io.output(self.pins_servo[0], io.LOW)
        else:
            io.output(self.pins_servo[0], io.HIGH)

    @property
    def motorp(self):
        return self.estadomotor

    @motorp.setter
    def motorp(self, estado_):
        if estado_ != self.estadomotor:
            if(estado_):
                io.output(self.pins_vfd[0], io.LOW)
            else:
                io.output(self.pins_vfd[0], io.HIGH)
            self.estadomotor = estado_

    def salir(self):
        # ~ io.output(self.pin_vfd0, io.HIGH)
        # ~ io.output(self.pin_servo2, io.HIGH)
        io.cleanup()
        # ~ io.output(self.pin_servo1, io.HIGH)
        # ~ io.output(self.pin_servo0, io.HIGH)
        time.sleep(0.1)

    def pulsos(self, cant, dir):
        io.output(self.pins_servo[3], dir)
        for j in range(cant):
            io.output(self.pins_servo[2], io.LOW)
            sleep(.000001)
            io.output(self.pins_servo[2], io.HIGH)
            sleep(.000001)
