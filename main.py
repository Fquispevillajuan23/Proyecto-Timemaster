import tkinter as tk
from tkinter import messagebox
import time
from models import Temporizador, Cronometro, Pomodoro, session

class AplicacionTemporizador:
    def __init__(self, root):
        self.root = root
        self.root.title("Temporizador, Cronómetro y Pomodoro")

        # Variables
        self.temporizador_corriendo = False
        self.temporizador_pausado = False
        self.tiempo_restante = 0

        # Crear los widgets
        self.crear_widgets()

    def crear_widgets(self):
        # Sección de Temporizador
        self.etiqueta_temporizador = tk.Label(self.root, text="Temporizador (segundos):")
        self.etiqueta_temporizador.pack()
        self.entrada_temporizador = tk.Entry(self.root)
        self.entrada_temporizador.pack()
        self.boton_temporizador = tk.Button(self.root, text="Iniciar Temporizador", command=self.iniciar_temporizador)
        self.boton_temporizador.pack()

        # Sección de Cronómetro
        self.etiqueta_cronometro = tk.Label(self.root, text="Cronómetro")
        self.etiqueta_cronometro.pack()
        self.boton_cronometro = tk.Button(self.root, text="Iniciar Cronómetro", command=self.iniciar_cronometro)
        self.boton_cronometro.pack()
        self.tiempo_cronometro = tk.Label(self.root, text="00:00:00")
        self.tiempo_cronometro.pack()

        # Sección de Pomodoro
        self.etiqueta_pomodoro = tk.Label(self.root, text="Pomodoro (trabajo, descanso) en minutos:")
        self.etiqueta_pomodoro.pack()
        self.entrada_tiempo_trabajo = tk.Entry(self.root)
        self.entrada_tiempo_trabajo.pack()
        self.entrada_tiempo_descanso = tk.Entry(self.root)
        self.entrada_tiempo_descanso.pack()
        self.boton_pomodoro = tk.Button(self.root, text="Iniciar Pomodoro", command=self.iniciar_pomodoro)
        self.boton_pomodoro.pack()

    def iniciar_temporizador(self):
        try:
            self.tiempo_restante = int(self.entrada_temporizador.get())
            nuevo_temporizador = Temporizador(nombre='Temporizador de ejemplo', tiempo_restante=self.tiempo_restante, corriendo=True, pausado=False)
            session.add(nuevo_temporizador)
            session.commit()
            self.temporizador_corriendo = True
            self.actualizar_temporizador()
        except ValueError:
            messagebox.showerror("Entrada no válida", "Por favor ingrese un número válido.")

    def actualizar_temporizador(self):
        if self.temporizador_corriendo:
            if self.tiempo_restante > 0:
                mins, secs = divmod(self.tiempo_restante, 60)
                formato_tiempo = '{:02d}:{:02d}'.format(mins, secs)
                self.etiqueta_temporizador.config(text=f"Tiempo restante: {formato_tiempo}")
                self.root.after(1000, self.actualizar_temporizador)
                self.tiempo_restante -= 1
            else:
                self.temporizador_corriendo = False
                messagebox.showinfo("Temporizador", "¡El tiempo ha terminado!")

    def iniciar_cronometro(self):
        self.inicio_cronometro = time.time()
        nuevo_cronometro = Cronometro(nombre='Cronómetro de ejemplo', tiempo_transcurrido=0, corriendo=True)
        session.add(nuevo_cronometro)
        session.commit()
        self.cronometro_corriendo = True
        self.actualizar_cronometro()

    def actualizar_cronometro(self):
        if self.cronometro_corriendo:
            tiempo_transcurrido = time.time() - self.inicio_cronometro
            mins, secs = divmod(tiempo_transcurrido, 60)
            horas, mins = divmod(mins, 60)
            formato_tiempo = '{:02d}:{:02d}:{:02d}'.format(int(horas), int(mins), int(secs))
            self.tiempo_cronometro.config(text=formato_tiempo)
            self.root.after(1000, self.actualizar_cronometro)

    def iniciar_pomodoro(self):
        try:
            tiempo_trabajo = int(self.entrada_tiempo_trabajo.get()) * 60
            tiempo_descanso = int(self.entrada_tiempo_descanso.get()) * 60
            nuevo_pomodoro = Pomodoro(nombre='Pomodoro de ejemplo', duracion_trabajo=tiempo_trabajo, duracion_descanso=tiempo_descanso, ciclos=4, ciclo_actual=0)
            session.add(nuevo_pomodoro)
            session.commit()
            self.pomodoro(tiempo_trabajo, tiempo_descanso)
        except ValueError:
            messagebox.showerror("Entrada no válida", "Por favor ingrese números válidos.")

    def pomodoro(self, duracion_trabajo, duracion_descanso):
        self.duracion_trabajo = duracion_trabajo
        self.duracion_descanso = duracion_descanso
        self.numero_ciclos = 0
        self.pomodoro_corriendo = True
        self.ejecutar_ciclo_pomodoro()

    def ejecutar_ciclo_pomodoro(self):
        if self.pomodoro_corriendo:
            if self.numero_ciclos % 2 == 0:
                self.tiempo_restante = self.duracion_trabajo
                self.etiqueta_temporizador.config(text="¡Tiempo de trabajo!")
            else:
                self.tiempo_restante = self.duracion_descanso
                self.etiqueta_temporizador.config(text="¡Tiempo de descanso!")
            self.temporizador_corriendo = True
            self.actualizar_temporizador()
            self.numero_ciclos += 1
            self.root.after((self.tiempo_restante + 1) * 1000, self.ejecutar_ciclo_pomodoro)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionTemporizador(root)
    root.mainloop()
