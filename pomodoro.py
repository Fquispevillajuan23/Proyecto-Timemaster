import tkinter as tk
from tkinter import messagebox
from datetime import timedelta


class PomodoroApp:
    def __init__(self, root, back_callback):
        self.root = root
        self.current_frame = None
        self.back_callback = back_callback

        # Tiempos por defecto para trabajo y descanso (en segundos)
        self.work_time_default = timedelta(minutes=25)
        self.break_time_default = timedelta(minutes=5)

        # Tiempos actuales para trabajo y descanso (en segundos)
        self.work_time = self.work_time_default
        self.break_time = self.break_time_default

        # Estado del temporizador
        self.is_running = False
        self.is_break = False
        self.remaining_time = self.work_time

        self.show_pomodoro_interface()

    def show_pomodoro_interface(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root, bg='light blue')
        self.current_frame.pack(expand=True, fill='both')

        tk.Label(self.current_frame, text="Pomodoro Timer", font=("Arial", 18), bg='light blue').pack(pady=20)

        self.timer_label = tk.Label(self.current_frame, text=self.format_time(self.remaining_time), font=("Arial", 40), bg='light blue')
        self.timer_label.pack()

        # Botones para controlar el temporizador
        self.start_button = tk.Button(self.current_frame, text="Iniciar", command=self.start_timer, bg='white', width=10)
        self.start_button.pack(pady=10)

        self.pause_button = tk.Button(self.current_frame, text="Pausa", command=self.pause_timer, bg='white', width=10)
        self.pause_button.pack(pady=10)

        self.reset_button = tk.Button(self.current_frame, text="Reiniciar", command=self.reset_timer, bg='white', width=10)
        self.reset_button.pack(pady=10)

        self.configure_button = tk.Button(self.current_frame, text="Configurar", command=self.configure_timer, bg='white', width=10)
        self.configure_button.pack(pady=10)

        self.back_button = tk.Button(self.current_frame, text="Volver", command=self.back_to_menu, bg='white', width=10)
        self.back_button.pack(pady=10)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.countdown()

    def pause_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.is_break = False
        self.remaining_time = self.work_time
        self.timer_label.config(text=self.format_time(self.remaining_time))

    def countdown(self):
        if self.is_running:
            self.remaining_time -= timedelta(seconds=1)
            if self.remaining_time.total_seconds() <= 0:
                if not self.is_break:
                    self.is_break = True
                    self.remaining_time = self.break_time
                    messagebox.showinfo("¡Tiempo de descanso!", "¡Es hora de un descanso!")
                else:
                    self.is_break = False
                    self.remaining_time = self.work_time
                    messagebox.showinfo("¡Volver al trabajo!", "¡Es hora de volver al trabajo!")
            self.timer_label.config(text=self.format_time(self.remaining_time))
            self.root.after(1000, self.countdown)

    def configure_timer(self):
        ConfigureTimerDialog(self.root, self.update_times, self.work_time.seconds // 60, self.break_time.seconds // 60)

    def update_times(self, work_minutes, break_minutes):
        self.work_time = timedelta(minutes=work_minutes)
        self.break_time = timedelta(minutes=break_minutes)
        self.work_time_default = self.work_time
        self.break_time_default = self.break_time
        self.reset_timer()

    def format_time(self, time_delta):
        minutes, seconds = divmod(int(time_delta.total_seconds()), 60)
        return f"{minutes:02}:{seconds:02}"

    def back_to_menu(self):
        self.current_frame.destroy()
        self.back_callback()

class ConfigureTimerDialog:
    def __init__(self, parent, callback, work_minutes, break_minutes):
        self.parent = parent
        self.callback = callback

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configurar Temporizador")
        self.dialog.geometry("300x150")

        self.work_label = tk.Label(self.dialog, text="Minutos de trabajo:")
        self.work_label.pack(pady=10)
        self.work_entry = tk.Entry(self.dialog, width=10)
        self.work_entry.insert(0, work_minutes)
        self.work_entry.pack()

        self.break_label = tk.Label(self.dialog, text="Minutos de descanso:")
        self.break_label.pack(pady=10)
        self.break_entry = tk.Entry(self.dialog, width=10)
        self.break_entry.insert(0, break_minutes)
        self.break_entry.pack()

        self.save_button = tk.Button(self.dialog, text="Guardar", command=self.save_configuration, width=10)
        self.save_button.pack(pady=10)

    def save_configuration(self):
        try:
            work_minutes = int(self.work_entry.get())
            break_minutes = int(self.break_entry.get())
            self.callback(work_minutes, break_minutes)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce números válidos para los minutos.")

def main():
    root = tk.Tk()
    app = PomodoroApp(root, lambda: show_menu(root))
    root.mainloop()

def show_menu(root):
    # Aquí se mostraría el menú principal o se llama a la función correspondiente
    print("Volver al menú principal")

if __name__ == "__main__":
    main()
