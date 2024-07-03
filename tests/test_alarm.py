import unittest
from alarm import Alarm
import time


class TestAlarm(unittest.TestCase):
    def test_alarm_initialization(self):
        alarm = Alarm("12:00")
        self.assertEqual(alarm.alarm_time, "12:00")

    def test_alarm_check(self):
        # Simula que el tiempo actual es "12:00" para que se active la alarma.
        current_time = time.strftime("%H:%M", time.gmtime(0))  # Esto dará "00:00"
        alarm = Alarm(current_time)
        alarm.start()
        # Aquí puedes verificar que el ring de 3 segundos se activa de alguna manera.


if __name__ == "__main__":
    unittest.main()
