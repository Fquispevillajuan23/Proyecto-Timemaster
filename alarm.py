import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading

try:
    import winsound  # Importa winsound para reproducir sonidos en Windows
except ImportError:
    winsound = None

class AlarmApp:
    def __init__(self, parent, return_to_main):
        self.parent = parent
        self.return_to_main = return_to_main
        self.is_playing = False
        self.alarm_time = None
        self.remaining_time = None
        self.alarm_thread = None
        self.countdown_thread = None

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.parent, text="Configuración de Alarma", font=("Arial", 18), bg='light blue').pack(pady=20)

        self.hour_entry = tk.Entry(self.parent, width=3)
        self.hour_entry.pack(side="left", padx=5)
        tk.Label(self.parent, text="Hora", bg='light blue').pack(side="left")

        self.minute_entry = tk.Entry(self.parent, width=3)
        self.minute_entry.pack(side="left", padx=5)
        tk.Label(self.parent, text="Minutos", bg='light blue').pack(side="left")

        self.second_entry = tk.Entry(self.parent, width=3)
        self.second_entry.pack(side="left", padx=5)
        tk.Label(self.parent, text="Segundos", bg='light blue').pack(side="left")

        self.start_button = tk.Button(self.parent, text="Iniciar Alarma", command=self.set_alarm, bg='white')
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(self.parent, text="Pausar Alarma", command=self.pause_alarm, bg='white')
        self.pause_button.pack(pady=10)

        self.resume_button = tk.Button(self.parent, text="Reanudar Alarma", command=self.resume_alarm, bg='white')
        self.resume_button.pack(pady=10)

        self.stop_button = tk.Button(self.parent, text="Detener Alarma", command=self.stop_alarm, bg='white')
        self.stop_button.pack(pady=10)

        self.time_label = tk.Label(self.parent, text="", font=("Arial", 18), bg='light blue')
        self.time_label.pack(pady=10)

    def set_alarm(self):
        try:
            hour = int(self.hour_entry.get())
            minute = int(self.minute_entry.get())
            second = int(self.second_entry.get())
            self.remaining_time = timedelta(hours=hour, minutes=minute, seconds=second)
            messagebox.showinfo("Alarma Configurada", f"La alarma sonará en {self.format_time(self.remaining_time)}")
            self.start_countdown_thread()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa una hora válida.")

    def start_countdown_thread(self):
        if self.countdown_thread and self.countdown_thread.is_alive():
            self.countdown_thread.cancel()
        self.countdown_thread = threading.Thread(target=self.countdown)
        self.countdown_thread.start()

    def countdown(self):
        while self.remaining_time.total_seconds() > 0:
            self.time_label.config(text=self.format_time(self.remaining_time))
            self.remaining_time -= timedelta(seconds=1)
            self.parent.after(1000, self.countdown)
            return
        self.play_alarm()

    def play_alarm(self):
        self.is_playing = True
        self.time_label.config(text="¡Tiempo!")
        if winsound:
            winsound.PlaySound("ring.wav", winsound.SND_LOOP + winsound.SND_ASYNC)

    def pause_alarm(self):
        if self.is_playing and winsound:
            winsound.PlaySound(None, winsound.SND_ASYNC)
            self.is_playing = False

    def resume_alarm(self):
        if not self.is_playing and winsound:
            winsound.PlaySound("ring.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
            self.is_playing = True

    def stop_alarm(self):
        if winsound:
            winsound.PlaySound(None, winsound.SND_ASYNC)
        self.is_playing = False
        self.remaining_time = None
        self.time_label.config(text="")

    def format_time(self, time_delta):
        total_seconds = int(time_delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

def main():
    root = tk.Tk()
    root.title("Alarm App")
    root.geometry("400x300")
    app = AlarmApp(root, lambda: print("Returning to main menu..."))
    root.mainloop()

if __name__ == "__main__":
    main()
