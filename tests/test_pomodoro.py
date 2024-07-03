import unittest
from datetime import timedelta
import tkinter as tk
from time_management_app.pomodoro import PomodoroApp, ConfigureTimerDialog  # Asegúrate de que este es el nombre del archivo original

class TestPomodoroApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Esto oculta la ventana principal durante las pruebas
        self.app = PomodoroApp(self.root, self.dummy_callback)

    def tearDown(self):
        self.root.destroy()

    def dummy_callback(self):
        pass

    def test_initial_state(self):
        self.assertEqual(self.app.is_running, False)
        self.assertEqual(self.app.is_break, False)
        self.assertEqual(self.app.remaining_time, self.app.work_time_default)

    def test_start_timer(self):
        self.app.start_timer()
        self.assertTrue(self.app.is_running)

    def test_pause_timer(self):
        self.app.start_timer()
        self.app.pause_timer()
        self.assertFalse(self.app.is_running)

    def test_reset_timer(self):
        self.app.start_timer()
        self.app.reset_timer()
        self.assertFalse(self.app.is_running)
        self.assertFalse(self.app.is_break)
        self.assertEqual(self.app.remaining_time, self.app.work_time)

    def test_configure_timer(self):
        self.app.update_times(30, 10)
        self.assertEqual(self.app.work_time, timedelta(minutes=30))
        self.assertEqual(self.app.break_time, timedelta(minutes=10))
        self.assertEqual(self.app.remaining_time, timedelta(minutes=30))

    def test_format_time(self):
        formatted_time = self.app.format_time(timedelta(minutes=5, seconds=30))
        self.assertEqual(formatted_time, "05:30")

class TestConfigureTimerDialog(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Esto oculta la ventana principal durante las pruebas

    def tearDown(self):
        self.root.destroy()

    def dummy_callback(self, work_minutes, break_minutes):
        self.work_minutes = work_minutes
        self.break_minutes = break_minutes

    def test_save_configuration(self):
        dialog = ConfigureTimerDialog(self.root, self.dummy_callback, 25, 5)
        dialog.work_entry.delete(0, tk.END)
        dialog.work_entry.insert(0, "30")
        dialog.break_entry.delete(0, tk.END)
        dialog.break_entry.insert(0, "10")
        dialog.save_configuration()
        self.assertEqual(self.work_minutes, 30)
        self.assertEqual(self.break_minutes, 10)

if __name__ == "__main__":
    unittest.main()
