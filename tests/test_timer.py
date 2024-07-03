import unittest
from timer import Timer


class TestTimer(unittest.TestCase):
    def test_timer_initialization(self):
        timer = Timer(60)
        self.assertEqual(timer.duration, 60)
        self.assertEqual(timer.remaining, 60)
        self.assertFalse(timer.running)

    def test_timer_start(self):
        timer = Timer(1)
        timer.start()
        self.assertEqual(timer.remaining, 0)

    def test_timer_pause(self):
        timer = Timer(60)
        timer.start()
        timer.pause()
        self.assertFalse(timer.running)

    def test_timer_reset(self):
        timer = Timer(60)
        timer.start()
        timer.reset()
        self.assertEqual(timer.remaining, 60)


if __name__ == "__main__":
    unittest.main()
