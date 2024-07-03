import tkinter as tk
from datetime import datetime, timedelta
from tkinter import messagebox

try:
    import winsound
except ImportError:
    winsound = None

class TimerApp:
    def __init__(self, root, app, back_callback):
        self.root = root
        self.app = app
        self.back_callback = back_callback
        self.timer = Timer(self.root, self.update_timer_label)
        self.setup_timer_interface()

    def setup_timer_interface(self):
        tk.Label(self.root, text="Temporizador", font=("Arial", 18), bg='light blue').pack(pady=20)

        self.timer_label = tk.Label(self.root, text="00:00:00", font=("Arial", 40), bg='light blue')
        self.timer_label.pack()

        self.hour_entry_label = tk.Label(self.root, text="Horas:", bg='light blue')
        self.hour_entry_label.pack()
        self.hour_entry = tk.Entry(self.root, width=5)
        self.hour_entry.pack()

        self.minute_entry_label = tk.Label(self.root, text="Minutos:", bg='light blue')
        self.minute_entry_label.pack()
        self.minute_entry = tk.Entry(self.root, width=5)
        self.minute_entry.pack()

        self.second_entry_label = tk.Label(self.root, text="Segundos:", bg='light blue')
        self.second_entry_label.pack()
        self.second_entry = tk.Entry(self.root, width=5)
        self.second_entry.pack()

        self.set_button = tk.Button(self.root, text="Configurar Alarma", command=self.set_timer, bg='white')
        self.set_button.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Iniciar", command=self.timer.start, bg='white')
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(self.root, text="Pausa", command=self.timer.pause, bg='white')
        self.pause_button.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Reiniciar", command=self.timer.reset, bg='white')
        self.reset_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Volver al Menú", command=self.back_callback, bg='white')
        self.back_button.pack(pady=10)

    def update_timer_label(self, time_str):
        self.timer_label.config(text=time_str)

    def set_timer(self):
        try:
            hours = int(self.hour_entry.get())
            minutes = int(self.minute_entry.get())
            seconds = int(self.second_entry.get())
            self.timer.set_time(hours, minutes, seconds)
            messagebox.showinfo("Temporizador Configurado", f"Temporizador configurado para {hours} horas, {minutes} minutos y {seconds} segundos.")
            self.timer_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un valor numérico válido para horas, minutos y segundos.")

class Timer:
    def __init__(self, root, update_callback=None):
        self.root = root
        self.update_callback = update_callback
        self.is_running = False
        self.remaining_time = timedelta()

    def set_time(self, hours, minutes, seconds):
        self.remaining_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        self.update_timer_label()

    def countdown(self):
        if self.is_running:
            self.remaining_time -= timedelta(seconds=1)
            if self.remaining_time.total_seconds() <= 0:
                self.is_running = False
                self.remaining_time = timedelta()
                if self.update_callback:
                    self.update_callback("00:00:00")
                if winsound:
                    winsound.PlaySound("ring.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                return
            self.update_timer_label()
        self.root.after(1000, self.countdown)

    def update_timer_label(self):
        minutes, seconds = divmod(int(self.remaining_time.total_seconds()), 60)
        hours, minutes = divmod(minutes, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        if self.update_callback:
            self.update_callback(time_str)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.countdown()

    def pause(self):
        self.is_running = False

    def reset(self):
        self.is_running = False
        self.remaining_time = timedelta()
        if self.update_callback:
            self.update_callback("00:00:00")

def main():
    root = tk.Tk()
    app = TimerApp(root, None, lambda: print("Callback no definido"))
    root.mainloop()

if __name__ == "__main__":
    main()
