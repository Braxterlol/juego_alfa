import pygame
import sys
import threading
import random
import time
from abc import ABC, abstractmethod

# Inicializar pygame
pygame.init()
pygame.font.init()

# Colores
COLOR_FONDO = (240, 240, 255)
COLOR_TEXTO = (50, 50, 50)
COLOR_BOTON = (100, 150, 255)
COLOR_BOTON_HOVER = (120, 170, 255)
COLOR_BOTON_SELECCIONADO = (80, 200, 100)  # Color verde para botones seleccionados
COLOR_CORRECTO = (100, 200, 100)
COLOR_INCORRECTO = (255, 100, 100)
COLOR_PISTA = (70, 130, 180)

# Fuentes
FUENTE_GRANDE = pygame.font.SysFont('Arial', 28, bold=True)
FUENTE_MEDIA = pygame.font.SysFont('Arial', 22)
FUENTE_PEQUEÑA = pygame.font.SysFont('Arial', 18)
FUENTE_PISTA = pygame.font.SysFont('Arial', 18, italic=True)

# Patrón Strategy: Define la familia de algoritmos para formación de palabras
class EstrategiaFormacionPalabras(ABC):
    @abstractmethod
    def generar_actividad(self, nivel):
        pass
    
    @abstractmethod
    def verificar_respuesta(self, respuesta, solucion):
        pass
    
    @abstractmethod
    def obtener_pista(self, solucion):
        pass

# Implementaciones concretas de Strategy
# Agregar un atributo de clase para cada estrategia concreta
class UnionLetras(EstrategiaFormacionPalabras):
    palabras_usadas = set()  # Conjunto para rastrear palabras ya usadas
    
    def generar_actividad(self, nivel):
        palabras = {
            1: ["sol", "mar", "paz", "luz", "oso", "uno", "mes", "pez", "pie", "col"],
            2: ["casa", "mesa", "lobo", "pato", "vela", "gato", "libro", "flor", "árbol", "reloj"],
            3: ["escuela", "elefante", "mariposa", "biblioteca", "dinosaurio", "ventana", "montaña", "teléfono", "guitarra", "bicicleta"]
        }
        
        # Filtrar las palabras que no se han usado recientemente
        palabras_disponibles = [p for p in palabras[nivel] if p not in self.palabras_usadas]
        
        # Si todas las palabras ya se usaron, reiniciar
        if not palabras_disponibles:
            self.palabras_usadas.clear()
            palabras_disponibles = palabras[nivel]
        
        # Elegir una palabra aleatoria no usada
        palabra = random.choice(palabras_disponibles)
        
        # Marcar como usada
        self.palabras_usadas.add(palabra)
        
        # Mantener el conjunto de palabras usadas en un tamaño razonable
        if len(self.palabras_usadas) > 5:
            # Eliminar la palabra más antigua
            self.palabras_usadas.pop() if self.palabras_usadas else None
        
        letras = list(palabra)
        random.shuffle(letras)
        return {
            "instruccion": "Forma una palabra ordenando las letras:",
            "elementos": letras,
            "solucion": palabra,
            "tipo": "letras"
        }
    
    def verificar_respuesta(self, respuesta, solucion):
        return respuesta.lower() == solucion.lower()
    
    def obtener_pista(self, solucion):
        return f"La palabra tiene {len(solucion)} letras y comienza con '{solucion[0]}'."

class UnionSilabas(EstrategiaFormacionPalabras):
    palabras_usadas = set()

    def generar_actividad(self, nivel):
        palabras_silabas = {
            1: [("ca-sa", ["ca", "sa"]), ("pe-rro", ["pe", "rro"]), ("me-sa", ["me", "sa"])],
            2: [("pe-lo-ta", ["pe", "lo", "ta"]), ("ma-ri-po-sa", ["ma", "ri", "po", "sa"]), ("co-me-ta", ["co", "me", "ta"])],
            3: [("bi-ci-cle-ta", ["bi", "ci", "cle", "ta"]), ("te-le-vi-sión", ["te", "le", "vi", "sión"]), ("e-le-fan-te", ["e", "le", "fan", "te"])]
        }
        palabras_disponibles = [p for p in palabras_silabas[nivel] if p[0].replace("-", "") not in self.palabras_usadas]
        if not palabras_disponibles:
            self.palabras_usadas.clear()
            palabras_disponibles = palabras_silabas[nivel]
        palabra_info = random.choice(palabras_disponibles)
        palabra = palabra_info[0].replace("-", "")
        self.palabras_usadas.add(palabra)
        if len(self.palabras_usadas) > 5:
            self.palabras_usadas.pop() if self.palabras_usadas else None
        silabas = palabra_info[1].copy()
        random.shuffle(silabas)
        return {
            "instruccion": "Forma una palabra uniendo las sílabas:",
            "elementos": silabas,
            "solucion": palabra,
            "tipo": "silabas"
        }
    
    
    def verificar_respuesta(self, respuesta, solucion):
        return respuesta.lower() == solucion.lower()
    
    def obtener_pista(self, solucion):
        return f"La palabra tiene {len(solucion.split('-'))} sílabas y significa algo que puedes {self._get_hint_context(solucion)}."
    
    def _get_hint_context(self, palabra):
        pistas = {
            "casa": "donde vives",
            "perro": "un animal que ladra",
            "mesa": "usar para comer",
            "pelota": "usar para jugar",
            "mariposa": "un insecto con alas coloridas",
            "cometa": "volar en el cielo",
            "bicicleta": "usar para transportarte con dos ruedas",
            "televisión": "ver programas",
            "elefante": "un animal grande con trompa"
        }
        return pistas.get(palabra, "relacionado con objetos cotidianos")

class AsociacionRima(EstrategiaFormacionPalabras):
    palabras_usadas = set()
    def generar_actividad(self, nivel):
        rimas = {
            1: [("sol", ["col", "gol", "rol", "bol"]), ("mar", ["dar", "par", "bar", "lar"])],
            2: [("casa", ["masa", "pasa", "tasa", "rasa"]), ("mesa", ["pesa", "fresa", "presa", "besa"])],
            3: [("canción", ["pasión", "visión", "misión", "fusión"]), ("corazón", ["razón", "sazón", "buzón", "tesón"])]
        }
        palabras_disponibles = [p for p in rimas[nivel] if p[0] not in self.palabras_usadas]
        if not palabras_disponibles:
                self.palabras_usadas.clear()
                palabras_disponibles = rimas[nivel]

        palabra_info = random.choice(palabras_disponibles)
        palabra_base = palabra_info[0]
        self.palabras_usadas.add(palabra_base)
        palabras_rima = palabra_info[1]
        opciones = random.sample(palabras_rima, min(nivel + 1, len(palabras_rima)))

        if len(self.palabras_usadas) > 5:
            self.palabras_usadas.pop() if self.palabras_usadas else None
        
        # Añadir algunas palabras que no riman como distractores
        no_riman = ["azul", "verde", "feliz", "papel", "árbol"]
        distractores = random.sample(no_riman, min(3 - nivel, len(no_riman)))
        
        todas_opciones = opciones + distractores
        random.shuffle(todas_opciones)
        
        return {
            "instruccion": f"Selecciona las palabras que riman con '{palabra_base}':",
            "elementos": todas_opciones,
            "solucion": opciones,
            "palabra_base": palabra_base,
            "tipo": "rimas"
        }
    
    def verificar_respuesta(self, respuesta, solucion):
        # Verificar si las palabras seleccionadas son las que riman
        respuesta_set = set(respuesta)
        solucion_set = set(solucion)
        return respuesta_set == solucion_set
    
    def obtener_pista(self, solucion):
        if isinstance(solucion, list):
            palabra_ejemplo = solucion[0] if solucion else ""
            return f"Busca palabras que terminen igual que '{palabra_ejemplo}'."
        else:
            return f"Busca palabras que terminen igual que '{solucion}'."

# Patrón Factory Method: Crea las actividades según el tipo y nivel
class FabricaActividades(ABC):
    @abstractmethod
    def crear_actividad(self, nivel):
        pass

class FabricaUnionLetras(FabricaActividades):
    def crear_actividad(self, nivel):
        estrategia = UnionLetras()
        return Actividad(estrategia, nivel)

class FabricaUnionSilabas(FabricaActividades):
    def crear_actividad(self, nivel):
        estrategia = UnionSilabas()
        return Actividad(estrategia, nivel)

class FabricaAsociacionRima(FabricaActividades):
    def crear_actividad(self, nivel):
        estrategia = AsociacionRima()
        return Actividad(estrategia, nivel)

# Clase Actividad que usa la estrategia asignada
# Modificación en la clase Actividad para manejar letras repetidas
class Actividad:
    def __init__(self, estrategia, nivel):
        self.estrategia = estrategia
        self.nivel = nivel
        self.datos = self.estrategia.generar_actividad(nivel)
        self.intentos = 0
        self.max_intentos = 3
        # En lugar de un conjunto, usaremos un diccionario que rastrea cada botón individualmente
        self.botones_usados = {}  # Para rastrear botones específicos por su ID
        
    def verificar(self, respuesta):
        self.intentos += 1
        resultado = self.estrategia.verificar_respuesta(respuesta, self.datos["solucion"])
        return {
            "correcto": resultado,
            "intentos_restantes": max(0, self.max_intentos - self.intentos),
            "pista": self.estrategia.obtener_pista(self.datos["solucion"]) if not resultado and self.intentos < self.max_intentos else None
        }
    
    def usar_elemento(self, id_boton, elemento):
        """Marca un botón específico como usado y devuelve True si se pudo usar"""
        if id_boton in self.botones_usados:
            return False
        self.botones_usados[id_boton] = elemento
        return True
    
    def liberar_elemento(self, id_boton):
        """Libera un botón específico para que pueda ser usado de nuevo"""
        if id_boton in self.botones_usados:
            del self.botones_usados[id_boton]

# Gestor de puntuación con elementos de concurrencia
class GestorPuntuacion:
    def __init__(self):
        self.puntuacion = 0
        self.lock = threading.Lock()  # Primitiva de sincronización
        self.historial = []
        self.observadores = []
        self.hitos_notificados = set()  # Conjunto para rastrear hitos ya notificados
        self.puntos_para_nivel = 50  # Puntos necesarios para cambiar de nivel
    
    def aumentar_puntuacion(self, puntos):
        with self.lock:  # Asegura acceso exclusivo
            self.puntuacion += puntos
            self.historial.append((time.time(), puntos, self.puntuacion))
            self._notificar_observadores()
    
    def obtener_puntuacion(self):
        with self.lock:
            return self.puntuacion
    
    def registrar_observador(self, observador):
        self.observadores.append(observador)
    
    def _notificar_observadores(self):
        for observador in self.observadores:
            observador.actualizar(self.puntuacion)
    
    def verificar_cambio_nivel(self):
        """Verifica si se ha alcanzado la puntuación necesaria para cambiar de nivel"""
        return self.puntuacion > 0 and self.puntuacion % self.puntos_para_nivel == 0
    
    def verificar_hito(self, puntuacion):
        """Verifica si se alcanzó un nuevo hito de puntuación y lo marca como notificado"""
        if puntuacion > 0 and puntuacion % 100 == 0:
            # Verificar si este hito ya fue notificado
            if puntuacion not in self.hitos_notificados:
                self.hitos_notificados.add(puntuacion)
                return True
        return False

# Generador de retroalimentación
class GeneradorRetroalimentacion:
    def __init__(self):
        self.retroalimentacion_positiva = [
            "¡Excelente trabajo!",
            "¡Muy bien hecho!",
            "¡Increíble! Sigue así.",
            "¡Perfecto! Estás aprendiendo rápido.",
            "¡Genial! Eres muy hábil."
        ]
        self.retroalimentacion_negativa = [
            "¡Inténtalo de nuevo!",
            "No es correcto, pero puedes lograrlo.",
            "Casi lo tienes, sigue intentando.",
            "Prueba una vez más, ¡tú puedes!"
        ]
    
    def obtener_retroalimentacion(self, correcto, nivel):
        if correcto:
            mensaje = random.choice(self.retroalimentacion_positiva)
            if nivel == 1:
                return mensaje + " ¡Sigue practicando!"
            elif nivel == 2:
                return mensaje + " ¡Estás progresando muy bien!"
            else:
                return mensaje + " ¡Eres todo un experto!"
        else:
            return random.choice(self.retroalimentacion_negativa)

# Clase Botón para Pygame
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color=COLOR_BOTON, color_hover=COLOR_BOTON_HOVER, accion=None, param=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.color_hover = color_hover
        self.color_actual = self.color
        self.accion = accion
        self.param = param
        self.activo = True
    
    def dibujar(self, pantalla):
        if not self.activo:
            self.color_actual = (180, 180, 180)  # Gris para botones inactivos
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color_actual = self.color_hover
        else:
            self.color_actual = self.color
            
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=8)
        pygame.draw.rect(pantalla, (50, 50, 50), self.rect, 2, border_radius=8)
        
        texto_superficie = FUENTE_MEDIA.render(self.texto, True, (255, 255, 255))
        texto_rect = texto_superficie.get_rect(center=self.rect.center)
        pantalla.blit(texto_superficie, texto_rect)
    
    def manejar_evento(self, evento):
        if not self.activo:
            return False
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                if self.accion:
                    if self.param is not None:
                        self.accion(self.param)
                    else:
                        self.accion()
                return True
        return False

# Checkbox para selección de rimas
class Checkbox:
    def __init__(self, x, y, ancho, alto, texto, valor=False):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.check_rect = pygame.Rect(x, y, alto, alto)
        self.texto = texto
        self.valor = valor
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (255, 255, 255), self.check_rect, border_radius=4)
        pygame.draw.rect(pantalla, (50, 50, 50), self.check_rect, 2, border_radius=4)
        
        if self.valor:
            interior = pygame.Rect(self.check_rect.x + 4, self.check_rect.y + 4, 
                                   self.check_rect.width - 8, self.check_rect.height - 8)
            pygame.draw.rect(pantalla, COLOR_BOTON, interior, border_radius=2)
        
        texto_superficie = FUENTE_PEQUEÑA.render(self.texto, True, COLOR_TEXTO)
        texto_rect = texto_superficie.get_rect(midleft=(self.check_rect.right + 10, self.check_rect.centery))
        pantalla.blit(texto_superficie, texto_rect)
    
    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.valor = not self.valor
                return True
        return False

# Aplicación principal con interfaz gráfica
class AplicacionAlfabetizacion:
    def __init__(self):
        # Configurar ventana
        self.ancho, self.alto = 800, 600
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("Aprende Jugando - Alfabetización")
        
        # Inicializar componentes
        self.gestor_puntuacion = GestorPuntuacion()
        self.generador_feedback = GeneradorRetroalimentacion()
        self.semaforo_actividades = threading.Semaphore(1)
        self.modo_actual = None
        self.nivel_actual = 1
        self.actividad_actual = None
        self.respuesta_actual = ""
        self.mensaje_feedback = ""
        self.color_feedback = COLOR_CORRECTO
        self.mensaje_pista = ""
        self.modo_seleccionado = None
        self.nivel_seleccionado = None
        
        # Controles de UI
        self.inicializar_controles()

        # Mostrar botón "Cambiar Modo" desde el inicio
        self.btn_cambiar_modo = Boton(self.ancho // 2 - 90, 520, 180, 50, "Cambiar Modo", accion=self.volver_menu)
        self.mostrar_btn_cambiar_modo = True
        
        # Crear fábricas
        self.fabricas = {
            "letras": FabricaUnionLetras(),
            "silabas": FabricaUnionSilabas(),
            "rimas": FabricaAsociacionRima()
        }
        
        # Estado
        self.estado = "menu"  # "menu", "juego"
        self.mostrar_modal = False
        self.mensaje_modal = ""
        
        # Tiempo para mensajes
        self.timer_feedback = 0
        
        # Iniciar monitor en segundo plano
        self.evento_terminar = threading.Event()
        self.hilo_progreso = threading.Thread(target=self._monitorear_progreso)
        self.hilo_progreso.daemon = True
        self.hilo_progreso.start()

    def volver_menu(self):
        """Vuelve al menú principal para seleccionar un nuevo modo"""
        self.estado = "menu"
        self.mensaje_feedback = ""
        self.mensaje_pista = ""

    def inicializar_controles(self):
        # Selector de modo
        self.modos = ["Unión de letras", "Unión de sílabas", "Asociación por rima"]
        self.btn_modos = []
        for i, modo in enumerate(self.modos):
            btn = Boton(100 + i*200, 150, 180, 50, modo, accion=self.seleccionar_modo, param=i)
            self.btn_modos.append(btn)
        
        # Selector de nivel
        self.niveles = ["Nivel 1: Fácil", "Nivel 2: Intermedio", "Nivel 3: Difícil"]
        self.btn_niveles = []
        for i, nivel in enumerate(self.niveles):
            btn = Boton(100 + i*200, 250, 180, 50, nivel, accion=self.seleccionar_nivel, param=i+1)
            self.btn_niveles.append(btn)
        
        # Botón de inicio
        self.btn_iniciar = Boton(300, 350, 200, 60, "¡Comenzar!", accion=self.iniciar_actividad)
        
        # Botones y elementos del juego
        self.elementos_botones = []
        self.checkboxes_rimas = []
        
        # Centrar los botones de verificar y borrar
        ancho_btn = 120
        espacio = 10
        ancho_total = (ancho_btn * 2) + espacio
        x_inicial = (self.ancho - ancho_total) // 2
        
        self.btn_verificar = Boton(x_inicial, 450, ancho_btn, 50, "Verificar", accion=self.verificar_respuesta)
        self.btn_borrar = Boton(x_inicial + ancho_btn + espacio, 450, ancho_btn, 50, "Borrar", accion=self.borrar_respuesta)
    
    def seleccionar_modo(self, indice):
        self.modo_seleccionado = indice
        # Actualizar apariencia de botones - cambiado a verde para mejor visibilidad
        for i, btn in enumerate(self.btn_modos):
            btn.color = COLOR_BOTON_SELECCIONADO if i == indice else COLOR_BOTON
    
    def seleccionar_nivel(self, nivel):
        self.nivel_seleccionado = nivel
        # Actualizar apariencia de botones - cambiado a verde para mejor visibilidad
        for i, btn in enumerate(self.btn_niveles):
            btn.color = COLOR_BOTON_SELECCIONADO if i == nivel-1 else COLOR_BOTON
    
    def iniciar_actividad(self):
        self.semaforo_actividades.acquire()
        try:
            if not hasattr(self, 'modo_seleccionado') or not hasattr(self, 'nivel_seleccionado'):
                self.mensaje_modal = "Por favor, selecciona un modo y un nivel antes de comenzar."
                self.mostrar_modal = True
                return
        
            # Mapear selección a modo
            modos = ["letras", "silabas", "rimas"]
            self.modo_actual = modos[self.modo_seleccionado]
            self.nivel_actual = self.nivel_seleccionado
            
            # Crear actividad
            fabrica = self.fabricas[self.modo_actual]
            self.actividad_actual = fabrica.crear_actividad(self.nivel_actual)
            
            # Cambiar estado
            self.estado = "juego"
            self.respuesta_actual = ""
            self.mensaje_feedback = ""
            self.mensaje_pista = ""
            
            # Crear botones para elementos
            self.crear_botones_elementos()
        finally:
            self.semaforo_actividades.release()
    
    def avanzar_nivel(self):
        """Avanza al siguiente nivel manteniendo el mismo modo de juego"""
        if self.nivel_actual < 3:
            # Avanzar al siguiente nivel
            self.nivel_actual += 1
            # Actualizar nivel seleccionado en la interfaz
            self.nivel_seleccionado = self.nivel_actual
            # Actualizar los botones de nivel para reflejar el cambio
            for i, btn in enumerate(self.btn_niveles):
                btn.color = COLOR_BOTON_SELECCIONADO if i == self.nivel_actual-1 else COLOR_BOTON
            
            # Mostrar mensaje de avance de nivel
            self.mensaje_modal = f"¡Felicidades! Has avanzado al nivel {self.nivel_actual}."
            self.mostrar_modal = True
        else:
            # Si estamos en el nivel máximo, mostrar mensaje de felicitación
            self.mensaje_modal = "¡Felicidades! Has completado todos los niveles de este modo. Prueba con otro modo de juego."
            self.mostrar_modal = True
        
        # Crear nueva actividad con el nivel actualizado
        fabrica = self.fabricas[self.modo_actual]
        self.actividad_actual = fabrica.crear_actividad(self.nivel_actual)
        self.respuesta_actual = ""
        self.mensaje_feedback = ""
        self.mensaje_pista = ""
        self.crear_botones_elementos()
    
    def crear_botones_elementos(self):
        self.elementos_botones = []
        self.checkboxes_rimas = []
        
        if self.actividad_actual.datos["tipo"] == "rimas":
            # Crear checkboxes para rimas
            palabras = self.actividad_actual.datos["elementos"]
            
            # Modificar la posición base para evitar superponerse con la retroalimentación
            y_base = 180  # Cambiado de 300 a 180 para mover los checkboxes hacia arriba
            
            # Calcular el espacio disponible y distribuir los checkboxes de manera más organizada
            altura_total = min(30 * len(palabras), 180)  # Limitar la altura total
            espacio_vertical = altura_total / len(palabras)
            
            for i, palabra in enumerate(palabras):
                # Usar dos columnas si hay muchas palabras
                if len(palabras) > 4 and i >= len(palabras) // 2:
                    # Segunda columna
                    x_pos = 420
                    y_pos = y_base + (i - len(palabras) // 2) * espacio_vertical
                else:
                    # Primera columna
                    x_pos = 200
                    y_pos = y_base + i * espacio_vertical
                    
                checkbox = Checkbox(x_pos, y_pos, 200, 30, palabra)
                self.checkboxes_rimas.append(checkbox)
        else:
            # El código original para letras o sílabas se mantiene igual
            elementos = self.actividad_actual.datos["elementos"]
            ancho_boton = min(60, (self.ancho - 200) // len(elementos))
            for i, elemento in enumerate(elementos):
                x = (self.ancho - (ancho_boton * len(elementos))) // 2 + i * ancho_boton
                btn = Boton(x, 300, ancho_boton-5, 50, elemento, accion=self.agregar_elemento, param=(i, elemento))
                self.elementos_botones.append(btn)
        
    def agregar_elemento(self, param):
        id_boton, elemento = param  # Desempaquetar los parámetros
        # Verificar si el botón específico ya ha sido usado
        if self.actividad_actual.usar_elemento(id_boton, elemento):
            self.respuesta_actual += elemento
        # Actualizar estado de los botones
        for i, boton in enumerate(self.elementos_botones):
            boton.activo = i not in self.actividad_actual.botones_usados

    def borrar_respuesta(self):
        self.respuesta_actual = ""
        # Resetear elementos usados
        self.actividad_actual.botones_usados = {}
        # Reactivar todos los botones
        for boton in self.elementos_botones:
            boton.activo = True
        
        # Para rimas, desmarcar todos los checkboxes
        for checkbox in self.checkboxes_rimas:
            checkbox.valor = False
    
    def verificar_respuesta(self):
        if not self.actividad_actual:
            return
        
        if self.actividad_actual.datos["tipo"] == "rimas":
            # Verificar respuesta de rimas
            seleccionadas = [checkbox.texto for checkbox in self.checkboxes_rimas if checkbox.valor]
            resultado = self.actividad_actual.verificar(seleccionadas)
        else:
            # Verificar respuesta de letras o sílabas
            resultado = self.actividad_actual.verificar(self.respuesta_actual)
        
        self.procesar_resultado(resultado)
    
    def procesar_resultado(self, resultado):
        correcto = resultado["correcto"]
        
        # Mostrar retroalimentación
        self.mensaje_feedback = self.generador_feedback.obtener_retroalimentacion(correcto, self.nivel_actual)
        self.color_feedback = COLOR_CORRECTO if correcto else COLOR_INCORRECTO
        self.timer_feedback = pygame.time.get_ticks()
        
        # Actualizar puntuación si es correcto
        if correcto:
            puntos = self.nivel_actual * 10
            self.gestor_puntuacion.aumentar_puntuacion(puntos)
            
            # Verificar si debe avanzar al siguiente nivel
            if self.gestor_puntuacion.verificar_cambio_nivel():
                # Programar cambio de nivel después de un breve retraso
                pygame.time.set_timer(pygame.USEREVENT + 1, 2000, True)  # Evento único para cambiar nivel
            else:
                # Programar nueva actividad después de un breve retraso
                pygame.time.set_timer(pygame.USEREVENT, 2000, True)  # Evento único para nueva actividad
        else:
            # Mostrar pista si hay intentos restantes
            if resultado["pista"]:
                self.mensaje_pista = f"Pista: {resultado['pista']}"
            else:
                # Si se agotaron los intentos, mostrar la respuesta correcta
                if isinstance(self.actividad_actual.datos["solucion"], list):
                    solucion = ", ".join(self.actividad_actual.datos["solucion"])
                else:
                    solucion = self.actividad_actual.datos["solucion"]
                self.mensaje_pista = f"La respuesta correcta era: {solucion}"
                # Programar nueva actividad después de un breve retraso
                pygame.time.set_timer(pygame.USEREVENT, 2000, True)
    
    def _monitorear_progreso(self):
        """Función que corre en un hilo separado para monitorear el progreso del jugador"""
        while not self.evento_terminar.is_set():
            puntuacion = self.gestor_puntuacion.obtener_puntuacion()
            
            # Verificar si se alcanzó un hito
            if self.gestor_puntuacion.verificar_hito(puntuacion):
                # No podemos interactuar directamente con Pygame desde otro hilo
                # Enviar un evento personalizado para mostrar mensaje
                evento_hito = pygame.event.Event(pygame.USEREVENT + 2, {"puntuacion": puntuacion})
                pygame.event.post(evento_hito)
            
            # Esperar un tiempo antes de la siguiente verificación
            time.sleep(1)
    
    def ejecutar(self):
        reloj = pygame.time.Clock()
        ejecutando = True
        
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.USEREVENT:
                    # Evento para nueva actividad en el mismo nivel
                    if self.estado == "juego":
                        fabrica = self.fabricas[self.modo_actual]
                        self.actividad_actual = fabrica.crear_actividad(self.nivel_actual)
                        self.respuesta_actual = ""
                        self.mensaje_feedback = ""
                        self.mensaje_pista = ""
                        self.crear_botones_elementos()
                elif evento.type == pygame.USEREVENT + 1:
                    # Evento para avanzar de nivel
                    if self.estado == "juego":
                        self.avanzar_nivel()
                elif evento.type == pygame.USEREVENT + 2:
                    # Evento para mostrar mensaje de hito
                    puntuacion = evento.dict["puntuacion"]
                    self.mensaje_modal = f"¡Felicidades! Has alcanzado {puntuacion} puntos."
                    self.mostrar_modal = True
                
                # Manejar clics en botones según el estado actual
                if self.estado == "menu":
                    for btn in self.btn_modos:
                        btn.manejar_evento(evento)
                    for btn in self.btn_niveles:
                        btn.manejar_evento(evento)
                    self.btn_iniciar.manejar_evento(evento)
                    
                elif self.estado == "juego":
                    if self.actividad_actual.datos["tipo"] == "rimas":
                        for checkbox in self.checkboxes_rimas:
                            checkbox.manejar_evento(evento)
                    else:
                        for btn in self.elementos_botones:
                            btn.manejar_evento(evento)
                    
                    self.btn_verificar.manejar_evento(evento)
                    self.btn_borrar.manejar_evento(evento)
                    
                    if self.mostrar_btn_cambiar_modo:
                        self.btn_cambiar_modo.manejar_evento(evento)
                
                # Cerrar modal con clic
                if self.mostrar_modal and evento.type == pygame.MOUSEBUTTONDOWN:
                    self.mostrar_modal = False
            
            # Dibujar interfaz
            self.pantalla.fill(COLOR_FONDO)
            
            # Dibujar elementos según el estado actual
            if self.estado == "menu":
                self.dibujar_menu()
            elif self.estado == "juego":
                self.dibujar_juego()
            
            # Dibujar modal si es necesario
            if self.mostrar_modal:
                self.dibujar_modal()
            
            pygame.display.flip()
            reloj.tick(60)
        
        # Terminar hilo de monitoreo al salir
        self.evento_terminar.set()
        self.hilo_progreso.join()
        pygame.quit()
        sys.exit()
    
    def dibujar_menu(self):
        # Dibujar título
        titulo = FUENTE_GRANDE.render("Aprende Jugando - Actividades de Alfabetización", True, COLOR_TEXTO)
        self.pantalla.blit(titulo, (self.ancho // 2 - titulo.get_width() // 2, 50))
        
        # Dibujar subtítulos
        subtitulo1 = FUENTE_MEDIA.render("Selecciona un modo de juego:", True, COLOR_TEXTO)
        self.pantalla.blit(subtitulo1, (100, 120))
        
        subtitulo2 = FUENTE_MEDIA.render("Selecciona un nivel:", True, COLOR_TEXTO)
        self.pantalla.blit(subtitulo2, (100, 220))
        
        # Dibujar botones
        for btn in self.btn_modos:
            btn.dibujar(self.pantalla)
        
        for btn in self.btn_niveles:
            btn.dibujar(self.pantalla)
        
        self.btn_iniciar.dibujar(self.pantalla)
        
        # Dibujar puntuación actual
        puntuacion = FUENTE_MEDIA.render(f"Puntuación: {self.gestor_puntuacion.obtener_puntuacion()}", True, COLOR_TEXTO)
        self.pantalla.blit(puntuacion, (self.ancho - puntuacion.get_width() - 20, 20))
    
    def dibujar_juego(self):
        # Dibujar instrucción
        instruccion = FUENTE_GRANDE.render(self.actividad_actual.datos["instruccion"], True, COLOR_TEXTO)
        self.pantalla.blit(instruccion, (self.ancho // 2 - instruccion.get_width() // 2, 50))
        
        # Dibujar área de respuesta si no son rimas
        if self.actividad_actual.datos["tipo"] != "rimas":
            pygame.draw.rect(self.pantalla, (255, 255, 255), (200, 120, 400, 60), border_radius=10)
            pygame.draw.rect(self.pantalla, (100, 100, 100), (200, 120, 400, 60), 2, border_radius=10)
            
            if self.respuesta_actual:
                respuesta = FUENTE_GRANDE.render(self.respuesta_actual, True, COLOR_TEXTO)
                self.pantalla.blit(respuesta, (self.ancho // 2 - respuesta.get_width() // 2, 140))
        else:
            # Para rimas, mostrar la palabra base
            palabra_base = FUENTE_GRANDE.render(f"Palabra: {self.actividad_actual.datos['palabra_base']}", True, COLOR_TEXTO)
            self.pantalla.blit(palabra_base, (self.ancho // 2 - palabra_base.get_width() // 2, 120))
        
        # Dibujar elementos según el tipo
        if self.actividad_actual.datos["tipo"] == "rimas":
            for checkbox in self.checkboxes_rimas:
                checkbox.dibujar(self.pantalla)
        else:
            for btn in self.elementos_botones:
                btn.dibujar(self.pantalla)
        
        # Dibujar botones de control
        self.btn_verificar.dibujar(self.pantalla)
        self.btn_borrar.dibujar(self.pantalla)
        
        if self.mostrar_btn_cambiar_modo:
            self.btn_cambiar_modo.dibujar(self.pantalla)
        
        # Dibujar feedback
        if self.mensaje_feedback:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.timer_feedback < 5000:  # Mostrar por 5 segundos
                feedback = FUENTE_MEDIA.render(self.mensaje_feedback, True, self.color_feedback)
                self.pantalla.blit(feedback, (self.ancho // 2 - feedback.get_width() // 2, 380))
        
        # Dibujar pista
        if self.mensaje_pista:
            pista = FUENTE_PISTA.render(self.mensaje_pista, True, COLOR_PISTA)
            self.pantalla.blit(pista, (self.ancho // 2 - pista.get_width() // 2, 410))
        
        # Dibujar nivel y puntuación
        nivel = FUENTE_PEQUEÑA.render(f"Nivel: {self.nivel_actual}", True, COLOR_TEXTO)
        self.pantalla.blit(nivel, (20, 20))
        
        puntuacion = FUENTE_PEQUEÑA.render(f"Puntuación: {self.gestor_puntuacion.obtener_puntuacion()}", True, COLOR_TEXTO)
        self.pantalla.blit(puntuacion, (self.ancho - puntuacion.get_width() - 20, 20))
        
        # Mostrar información sobre modo de juego
        modo_texto = self.modos[self.modo_seleccionado]
        modo = FUENTE_PEQUEÑA.render(f"Modo: {modo_texto}", True, COLOR_TEXTO)
        self.pantalla.blit(modo, (20, 50))
    
    def dibujar_modal(self):
        # Dibujar fondo semitransparente
        s = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        self.pantalla.blit(s, (0, 0))
        
        # Dibujar ventana modal
        modal_width, modal_height = 500, 200
        modal_x = self.ancho // 2 - modal_width // 2
        modal_y = self.alto // 2 - modal_height // 2
        pygame.draw.rect(self.pantalla, (255, 255, 255), (modal_x, modal_y, modal_width, modal_height), border_radius=15)
        pygame.draw.rect(self.pantalla, (100, 100, 100), (modal_x, modal_y, modal_width, modal_height), 2, border_radius=15)
        
        # Dibujar mensaje
        mensaje_lineas = self._dividir_texto(self.mensaje_modal, 60)
        for i, linea in enumerate(mensaje_lineas):
            texto = FUENTE_MEDIA.render(linea, True, COLOR_TEXTO)
            self.pantalla.blit(texto, (self.ancho // 2 - texto.get_width() // 2, modal_y + 60 + i * 30))
        
        # Dibujar instrucción
        instruccion = FUENTE_PEQUEÑA.render("Haz clic en cualquier lugar para continuar", True, COLOR_TEXTO)
        self.pantalla.blit(instruccion, (self.ancho // 2 - instruccion.get_width() // 2, modal_y + modal_height - 40))
    
    def _dividir_texto(self, texto, max_caracteres):
        """Divide un texto largo en líneas para mostrar en el modal"""
        palabras = texto.split()
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            if len(linea_actual) + len(palabra) + 1 <= max_caracteres:
                linea_actual += " " + palabra if linea_actual else palabra
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        
        if linea_actual:
            lineas.append(linea_actual)
        
        return lineas

# Función principal
def main():
    app = AplicacionAlfabetizacion()
    app.ejecutar()

if __name__ == "__main__":
    main()