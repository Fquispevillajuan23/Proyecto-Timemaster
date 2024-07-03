import tkinter as tk
from tkinter import messagebox
from pomodoro import PomodoroApp
from timer import TimerApp
from alarm import AlarmApp
from database import create_tables, add_user, get_user, drop_table

try:
    import winsound  # Importa winsound para reproducir sonidos en Windows
except ImportError:
    winsound = None

class User:
    def __init__(self, nombre_usuario, contrasena):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena

class TimeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Tiempo Multipropósito")
        self.root.geometry("400x300")  # Tamaño predeterminado para las interfaces

        self.logged_in_user = None
        self.users = []

        create_tables()
        self.create_login_screen()

    def create_login_screen(self):
        self.destroy_current_frame()

        self.login_frame = tk.Frame(self.root, bg="light blue")
        self.login_frame.pack(fill="both", expand=True)

        tk.Label(self.login_frame, text="Inicio de Sesión", font=("Arial", 18), bg='light blue').pack(pady=20)

        self.username_label = tk.Label(self.login_frame, text="Usuario:")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Contraseña:")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Iniciar Sesión", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = tk.Button(self.login_frame, text="Registrarse", command=self.show_register_screen)
        self.register_button.pack()

    def show_register_screen(self):
        self.destroy_current_frame()

        self.register_frame = tk.Frame(self.root, bg="light blue")
        self.register_frame.pack(fill="both", expand=True)

        tk.Label(self.register_frame, text="Registro de Usuario", font=("Arial", 18), bg='light blue').pack(pady=20)

        self.register_username_label = tk.Label(self.register_frame, text="Nuevo Usuario:")
        self.register_username_label.pack(pady=10)
        self.register_username_entry = tk.Entry(self.register_frame)
        self.register_username_entry.pack()

        self.register_password_label = tk.Label(self.register_frame, text="Nueva Contraseña:")
        self.register_password_label.pack(pady=10)
        self.register_password_entry = tk.Entry(self.register_frame, show="*")
        self.register_password_entry.pack()

        self.register_button = tk.Button(self.register_frame, text="Registrar", command=self.register)
        self.register_button.pack(pady=20)

        self.back_button = tk.Button(self.register_frame, text="Volver al Inicio de Sesión", command=self.back_to_login)
        self.back_button.pack()

    def back_to_login(self):
        self.create_login_screen()

    def register(self):
        new_username = self.register_username_entry.get()
        new_password = self.register_password_entry.get()

        if not new_username or not new_password:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        if get_user(new_username) is not None:
            messagebox.showerror("Error", "El nombre de usuario ya está en uso.")
            return

        add_user(new_username, new_password)
        messagebox.showinfo("Registro Exitoso", "Usuario registrado correctamente.")
        self.back_to_login()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = get_user(username)
        if user and user[2] == password:
            self.logged_in_user = User(user[1], user[2])
            self.show_main_screen()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def show_main_screen(self):
        self.destroy_current_frame()

        self.main_frame = tk.Frame(self.root, bg="light blue")
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(self.main_frame, text="Gestión de Tiempo Multipropósito", font=("Arial", 18), bg='light blue').pack(pady=20)

        tk.Button(self.main_frame, text="Temporizador Pomodoro", command=self.show_pomodoro_app, bg='white').pack(pady=10)
        tk.Button(self.main_frame, text="Configurar Alarma", command=self.show_alarm_app, bg='white').pack(pady=10)
        tk.Button(self.main_frame, text="Temporizador", command=self.show_timer_app, bg='white').pack(pady=10)

        self.exit_button = tk.Button(self.main_frame, text="Salir", command=self.exit_app)
        self.exit_button.pack(pady=10)

    def show_pomodoro_app(self):
        self.destroy_current_frame()

        self.pomodoro_frame = tk.Frame(self.root, bg='light blue')
        self.pomodoro_frame.pack(fill="both", expand=True)

        PomodoroApp(self.pomodoro_frame, self.show_main_screen)

        self.back_button = tk.Button(self.pomodoro_frame, text="Volver al Menú", command=self.show_main_screen, bg='white')
        self.back_button.pack(pady=10)

    def show_alarm_app(self):
        self.destroy_current_frame()

        self.alarm_frame = tk.Frame(self.root, bg='light blue')
        self.alarm_frame.pack(fill="both", expand=True)

        AlarmApp(self.alarm_frame, self.show_main_screen)

        self.back_button = tk.Button(self.alarm_frame, text="Volver al Menú", command=self.show_main_screen, bg='white')
        self.back_button.pack(pady=10)

    def show_timer_app(self):
        self.destroy_current_frame()

        self.timer_frame = tk.Frame(self.root, bg='light blue')
        self.timer_frame.pack(fill="both", expand=True)

        TimerApp(self.root, self.timer_frame, self.show_main_screen)

        self.back_button = tk.Button(self.timer_frame, text="Volver al Menú", command=self.show_main_screen, bg='white')
        self.back_button.pack(pady=10)

    def exit_app(self):
        self.root.quit()

    def destroy_current_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = TimeManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
