import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ==========================================
# 1. ESTRUCTURA DEL ÁRBOL BINARIO DE BÚSQUEDA
# ==========================================
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, actual, valor):
        if valor < actual.valor:
            if actual.izquierdo is None:
                actual.izquierdo = Nodo(valor)
            else:
                self._insertar_recursivo(actual.izquierdo, valor)
        elif valor > actual.valor:
            if actual.derecho is None:
                actual.derecho = Nodo(valor)
            else:
                self._insertar_recursivo(actual.derecho, valor)

    def obtener_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, actual, resultado):
        if actual is not None:
            self._inorden_recursivo(actual.izquierdo, resultado)
            resultado.append(actual.valor)
            self._inorden_recursivo(actual.derecho, resultado)


# ==========================================
# 2. INTERFAZ GRÁFICA - OPCIÓN A (PERGAMINO)
# ==========================================
class JuegoABB:
    def __init__(self, root):
        self.root = root
        self.root.title("Árbol Binario de Búsqueda - Estilo Juego")
        self.root.geometry("1000x680")
        self.root.resizable(False, False)

        # Fuentes nativas combinadas
        self.FONT_TITULO = ("Impact", 46, "italic")
        self.FONT_SUBTITULO = ("Comic Sans MS", 24, "bold")
        self.FONT_TEXTO_INSTRUCCION = ("Trebuchet MS", 15, "bold")
        self.FONT_NODOS = ("Trebuchet MS", 14, "bold")
        self.FONT_INORDEN_TITULO = ("Comic Sans MS", 12, "bold")
        self.FONT_INORDEN_DATOS = ("Comic Sans MS", 14, "bold")

        self.arbol = ArbolBinarioBusqueda()
        self.estado_juego = "INICIO"

        self.canvas = tk.Canvas(root, width=1000, height=680, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Entrada ajustada sobre el fondo claro de pergamino
        self.entry_numeros = tk.Entry(
            root, font=("Trebuchet MS", 15, "bold"), justify="center",
            bg="#fdf8eb", fg="#24140a", relief="flat", bd=0, highlightthickness=0
        )
        self.entry_numeros.insert(0, "50, 30, 70, 20, 40, 60, 80")

        self.caballero_id = None
        self.caballero_tk = None
        self.animando_caballero = False
        self.play_hover = False

        self.canvas.bind("<Button-1>", self.detectar_clic)
        self.canvas.bind("<Motion>", self.detectar_movimiento_mouse)
        self.renderizar()

    def dibujar_fondo(self):
        self.canvas.delete("all")
        try:
            self.fondo_img = Image.open("fondo.png")
            self.fondo_img = self.fondo_img.resize((1000, 680))
            self.fondo_tk = ImageTk.PhotoImage(self.fondo_img)
            self.canvas.create_image(0, 0, image=self.fondo_tk, anchor="nw")
        except:
            self.canvas.create_rectangle(0, 0, 1000, 680, fill="#87CEEB")

    def crear_texto_con_sombra(self, x, y, text, font, fill_color, shadow_color="#000000", offset=2):
        self.canvas.create_text(x + offset, y + offset, text=text, font=font, fill=shadow_color)
        return self.canvas.create_text(x, y, text=text, font=font, fill=fill_color)

    def renderizar(self):
        self.dibujar_fondo()
        if self.estado_juego == "INICIO":
            # --- PANEL ESTILO PERGAMINO ---
            # Sombra y marco de madera
            self.canvas.create_rectangle(248, 218, 752, 362, fill="#24140a", outline="#8c5828", width=2)
            self.canvas.create_rectangle(250, 220, 750, 360, fill="#3d2514", outline="#e2b13c", width=2)
            
            # Pergamino claro
            self.canvas.create_rectangle(258, 228, 742, 352, fill="#e8d5b7", outline="#8c5828", width=1)

            # Hueco para la entrada de números
            self.canvas.create_rectangle(288, 283, 712, 332, fill="#24140a", outline="")
            self.canvas.create_rectangle(290, 285, 710, 330, fill="#fdf8eb", outline="#e2b13c", width=1)

            self.entry_numeros.place(x=295, y=288, width=410, height=38)

            # Títulos principales
            self.crear_texto_con_sombra(500, 115, "Árbol Binario de Búsqueda", 
                                       self.FONT_TITULO, fill_color="#d94b18", shadow_color="#ffffff", offset=3)
            
            self.crear_texto_con_sombra(500, 175, "Proyecto Final - Matemática Discreta", 
                                       self.FONT_SUBTITULO, fill_color="#001f3f", shadow_color="#ffffff", offset=2)
            
            self.canvas.create_text(500, 255, text="Ingresa los números separados por comas:",
                                    font=self.FONT_TEXTO_INSTRUCCION, fill="#3d2514")
            
            self.dibujar_boton_play(500, 580)

        elif self.estado_juego == "ARBOL":
            self.entry_numeros.place_forget()
            self.dibujar_nodo_grafico(self.arbol.raiz, 500, 80, 220)
            
            # Botón Volver estilizado
            self.canvas.create_rectangle(18, 18, 122, 52, fill="#24140a", outline="")
            self.canvas.create_rectangle(20, 20, 120, 50, fill="#3d2514", outline="#e2b13c", width=2)
            self.canvas.create_text(70, 35, text="⬅ Inicio", font=self.FONT_TEXTO_INSTRUCCION, fill="#f4e4bc")

    def dibujar_boton_play(self, x, y):
        self.crear_texto_con_sombra(x, y - 55, "¡JUGAR!", ("Impact", 22), fill_color="#ffea79", shadow_color="#3d2514", offset=2)

        r1, r2 = (42, 35) if self.play_hover else (38, 32)
        color_borde = "#ffea79" if self.play_hover else "#e2b13c"
        
        self.canvas.create_oval(x-r1+3, y-r1+3, x+r1+3, y+r1+3, fill="#24140a", outline="")
        self.canvas.create_oval(x-r1, y-r1, x+r1, y+r1, fill="#ffffff", outline="")
        self.canvas.create_oval(x-r2, y-r2, x+r2, y+r2, fill="#8c5828", outline=color_borde, width=4)
        self.canvas.create_polygon(x-10, y-18, x-10, y+18, x+20, y, fill="#ffffff")

    def detectar_movimiento_mouse(self, event):
        if self.estado_juego == "INICIO":
            x, y = event.x, event.y
            hover_previo = self.play_hover
            self.play_hover = (460 <= x <= 540 and 540 <= y <= 620)
            if hover_previo != self.play_hover:
                self.renderizar()

    def dibujar_nodo_grafico(self, nodo, x, y, separacion):
        if nodo is None:
            return
        radio = 24
        nivel_y = 70

        if nodo.izquierdo:
            self.canvas.create_line(x+2, y+2, x - separacion + 2, y + nivel_y + 2, fill="#3d2514", width=5)
            self.canvas.create_line(x, y, x - separacion, y + nivel_y, fill="#ffffff", width=4)
            self.dibujar_nodo_grafico(nodo.izquierdo, x - separacion, y + nivel_y, separacion * 0.5)
        if nodo.derecho:
            self.canvas.create_line(x+2, y+2, x + separacion + 2, y + nivel_y + 2, fill="#3d2514", width=5)
            self.canvas.create_line(x, y, x + separacion, y + nivel_y, fill="#ffffff", width=4)
            self.dibujar_nodo_grafico(nodo.derecho, x + separacion, y + nivel_y, separacion * 0.5)

        self.canvas.create_oval(x - radio + 2, y - radio + 2, x + radio + 2, y + radio + 2, fill="#24140a", outline="")
        self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill="#e2b13c", outline="#ffffff", width=3)
        self.canvas.create_oval(x - (radio-4), y - (radio-4), x + (radio-4), y + (radio-4), fill="#f3a600", outline="")
        
        self.canvas.create_oval(x - 12, y - 12, x - 4, y - 4, fill="#fff3c4", outline="")
        self.canvas.create_text(x, y + 1, text=str(nodo.valor), font=self.FONT_NODOS, fill="#ffffff")

    def detectar_clic(self, event):
        x, y = event.x, event.y
        if self.estado_juego == "INICIO" and 450 <= x <= 550 and 530 <= y <= 630:
            self.procesar_e_iniciar()
        elif self.estado_juego == "ARBOL" and 18 <= x <= 122 and 18 <= y <= 52:
            self.animando_caballero = False
            self.estado_juego = "INICIO"
            self.renderizar()

    def procesar_e_iniciar(self):
        texto = self.entry_numeros.get()
        partes = texto.split(",")
        self.numeros = []
        for p in partes:
            p_limpio = p.strip()
            if p_limpio.lstrip('-').isdigit():
                self.numeros.append(int(p_limpio))

        if len(self.numeros) < 2:
            messagebox.showwarning("Atención", "Debes ingresar al menos 2 números.")
            return

        self.arbol = ArbolBinarioBusqueda()
        self.estado_juego = "ARBOL"
        self.indice_actual = 0
        self.animar_insercion()
        self.iniciar_caballero()

    def animar_insercion(self):
        if self.estado_juego != "ARBOL":
            return

        if self.indice_actual < len(self.numeros):
            num = self.numeros[self.indice_actual]
            self.arbol.insertar(num)
            
            self.renderizar()
            if hasattr(self, 'caballero_x') and self.caballero_tk:
                self.recrear_caballero_en_canvas()

            self.indice_actual += 1
            self.root.after(600, self.animar_insercion)
        else:
            ordenados = self.arbol.obtener_inorden()
            texto_inorden = "  ➔  ".join(str(x) for x in ordenados)
            
            self.canvas.create_rectangle(78, 578, 922, 652, fill="#24140a", outline="")
            self.canvas.create_rectangle(80, 580, 920, 650, fill="#3d2514", outline="#e2b13c", width=3)
            self.canvas.create_text(500, 598, text="RECORRIDO INORDEN (ORDEN ASCENDENTE)",
                                    font=self.FONT_INORDEN_TITULO, fill="#e2b13c")
            self.canvas.create_text(500, 625, text=texto_inorden,
                                    font=self.FONT_INORDEN_DATOS, fill="#ffffff")

    # ==============================
    # 3. CABALLERO ANIMADO
    # ==============================
    def iniciar_caballero(self):
        self.caballero_x = 20
        self.caballero_y = 420
        self.animando_caballero = True

        try:
            img = Image.open("caballero.png")
            img = img.resize((100, 150))
            self.caballero_tk = ImageTk.PhotoImage(img)
        except:
            self.caballero_tk = None

        self.recrear_caballero_en_canvas()
        self.mover_caballero()

    def recrear_caballero_en_canvas(self):
        if self.caballero_tk:
            self.caballero_id = self.canvas.create_image(
                self.caballero_x, self.caballero_y, image=self.caballero_tk, anchor="nw"
            )
        else:
            self.caballero_id = self.canvas.create_rectangle(
                self.caballero_x, self.caballero_y, 
                self.caballero_x + 60, self.caballero_y + 100, 
                fill="#4a90e2", outline="#ffffff"
            )

    def mover_caballero(self):
        if not self.animando_caballero or self.estado_juego != "ARBOL":
            return

        self.caballero_x += 2
        if self.caballero_x > 900:
            self.caballero_x = -80

        self.canvas.coords(self.caballero_id, self.caballero_x, self.caballero_y)
        self.root.after(50, self.mover_caballero)


# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoABB(root)
    root.mainloop()