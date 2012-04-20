# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti, quique porta
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

# Permite que este ejemplo funcion incluso si no has instalado pilas.

import sys

sys.path.insert(0, "../../../..")

import random

import pilas
from pilas.escenas import Normal
from pilas.actores import *
from pilas.net import *

import actores
from actores.tanque import Tanque
from actores.disparo import Disparo
from actores.disparo import DisparoTriple
from actores.velocidad import Velocidad
from pilas.actores.utils import destruir_a_todos

class Escena_Parametros(Normal):
    
    def __init__(self):
        Normal.__init__(self)
        pilas.fondos.Pasto()
        self.boton_servidor = pilas.interfaz.Boton("Servidor")
        self.boton_servidor.y = 100
        self.boton_servidor.conectar(self.conectar_servidor)
        
        self.texto_ip_servidor = pilas.interfaz.IngresoDeTexto(obteber_ip_local())
        
        self.boton_cliente = pilas.interfaz.Boton("Cliente")
        self.boton_cliente.y = -50
        self.boton_cliente.conectar(self.conectar_cliente)
        
    def conectar_servidor(self):
        MiEscena('servidor')
        
    def conectar_cliente(self):
        MiEscena('cliente', ip_servidor=self.texto_ip_servidor.texto)

class MiEscena(EscenaNetwork):
    
    def __init__(self, rol, ip_servidor=obteber_ip_local()):
        EscenaNetwork.__init__(self,rol,ip_servidor=ip_servidor)
        pilas.fondos.Pasto()
        
        self.crear_tanque()
        
        self.puntaje = pilas.actores.Puntaje(x=-300,y=220)
        
    def crear_tanque(self):
        rand_x = random.randint(-320,320)
        rand_y = random.randint(-240,240)
        self.mi_tanque = actores.tanque.Tanque(x=rand_x, y=rand_y)
        self.agregar_actor_local(self.mi_tanque)
        self.mi_tanque.evento_disparar.conectar(self.disparo)
        self.mi_tanque.aprender(pilas.habilidades.SeMantieneEnPantalla)
    
    def crear_disparo_triple(self):
        hay_disparo = False
        for actor in self._actores_locales:
            if isinstance(actor, DisparoTriple):
                hay_disparo = True
                break
        if not (hay_disparo):
            rand_x = random.randint(-320,320)
            rand_y = random.randint(-240,240)
            disparo_triple = DisparoTriple(x=rand_x, y=rand_y)
            self.agregar_actor_local(disparo_triple)
    
    def crear_velocidad(self):
        hay_velocidad = False
        for actor in self._actores_locales:
            if isinstance(actor, Velocidad):
                hay_velocidad = True
                break
        if not (hay_velocidad):
            rand_x = random.randint(-320,320)
            rand_y = random.randint(-240,240)
            velocidad = Velocidad(x=rand_x, y=rand_y)
            self.agregar_actor_local(velocidad)
        
    
    def colision_con_actores_remotos(self, actor_local, actor_remoto):
        if (isinstance(actor_local, Tanque) and isinstance(actor_remoto, Disparo)):
            self.mi_tanque.quitar_vida()
            self.enviar_a_propietario_actor_puntos(actor_remoto, 5)           
            self.eliminar_actor_remoto(actor_remoto, notificar=False)
        elif (isinstance(actor_local, Disparo) and isinstance(actor_remoto, Tanque)):
            self.eliminar_actor_local(actor_local, notificar=False)
        elif (isinstance(actor_local, Tanque) and isinstance(actor_remoto, DisparoTriple)):
            self.eliminar_actor_remoto(actor_remoto)
            self.mi_tanque.disparo_triple = True
            pilas.avisar("Disparo Triple")
        elif (isinstance(actor_local, Tanque) and isinstance(actor_remoto, Velocidad)):
            self.eliminar_actor_remoto(actor_remoto)
            if (self.mi_tanque.velocidad < 3):
                self.mi_tanque.velocidad += 1
                pilas.avisar("Aumento de velocidad")
                                           
    def colision_con_actores_locales(self, actor_local1, actor_local2):
        if (isinstance(actor_local1, Tanque) and isinstance(actor_local2, DisparoTriple)):
            self.eliminar_actor_local(actor_local2)
            self.mi_tanque.disparo_triple = True
            pilas.avisar("Disparo Triple")
        elif (isinstance(actor_local1, Tanque) and isinstance(actor_local2, Velocidad)):
            self.eliminar_actor_local(actor_local2)
            if (self.mi_tanque.velocidad < 3):
                self.mi_tanque.velocidad += 1
                pilas.avisar("Aumento de velocidad")
    
    def disparo(self, evento):
        if (evento['tipo'] == 'simple'):
            self.agregar_actor_local(self.mi_tanque.disparos[-1])
            self.mi_tanque.disparos[-1].evento_destruir.conectar(self.eliminar_bala)
        elif (evento['tipo'] == 'triple'):
            self.agregar_actor_local(self.mi_tanque.disparos[-1])
            self.mi_tanque.disparos[-1].evento_destruir.conectar(self.eliminar_bala)
            self.agregar_actor_local(self.mi_tanque.disparos[-2])
            self.mi_tanque.disparos[-2].evento_destruir.conectar(self.eliminar_bala)
            self.agregar_actor_local(self.mi_tanque.disparos[-3])
            self.mi_tanque.disparos[-3].evento_destruir.conectar(self.eliminar_bala)
    
    def actualizar(self, evento):
        
        if (self.mi_tanque.get_vida() <= 0):
            self.eliminar_actor_local(self.mi_tanque)
            # Creamos uno nuevo
            self.crear_tanque()
    
        if not(self.soy_cliente()):
            aleatorio = random.randint(0,300)
            if (aleatorio == 50):
                self.crear_disparo_triple()
            if (aleatorio == 100):
                self.crear_velocidad()
        
        self.puntaje.texto = "Puntos:" + str(self.puntos)
        if (self.puntos == 20):
            self.escena_ganador()
        
        EscenaNetwork.actualizar(self, evento)
    
    def eliminar_bala(self, datos_evento):       
        self.eliminar_actor_local(datos_evento['bala'], notificar=False ,destruir=True)
                

pilas.iniciar(titulo="Tanques Net")

Escena_Parametros()

pilas.ejecutar()