from unittest import TestCase
from TheSleeper import TheSleeper
import os

__author__ = 'monkee'
__project__ = 'TheSleeper'


class TestTheSleeper(TestCase):

    def test_check_timezone_set(self):
        ts = TheSleeper()
        self.assertIn("TZ",os.environ)

    def test_check_timezone_value(self):
        ts = TheSleeper()
        self.assertEqual(os.environ["TZ"],"Australia/Brisbane")

    def test_check_timezone_notset(self):
        self.assertNotIn("TZ",os.environ)

    def test_stop_instance(self):
        ts = TheSleeper()
        self.assertRaises(Exception,ts.stop_instance)

    def test_start_instance(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.start_instance)

    def test_search_for_tagged(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.search_for_tagged)

    def test_search_sleeper_tags(self):
        ts = TheSleeper()
        self.assertRaises(Exception,ts.search_sleeper_tags)

    def test_cron_stop(self):
        ts = TheSleeper()
        self.assertRaises(Exception,ts.cron_stop)

    def test_cron_start(self):
        ts = TheSleeper()
        self.assertRaises(Exception,ts.cron_start)

    def test_return_misspast(self):
        ts = TheSleeper()
        self.assertRaises(Exception,ts.return_misspast)

    def test_return_misspast_goodvalue_every_night(self):
        ts = TheSleeper()
        val = ts.return_misspast("0 18 * * *")
        self.assertGreater(0,val)

    def test_return_misspast_goodvalue_every_worknight(self):
        ts = TheSleeper()
        val = ts.return_misspast("0 18 * * mon-fri")
        self.assertGreater(0,val)

    def test_return_misspast_goodvalue_start_end_worknight(self):
        ts = TheSleeper()
        val = ts.return_misspast("0 18 * * mon,fri")
        self.assertGreater(0,val)

    def test_return_misspast_badvalue(self):
        ts = TheSleeper()
        self.assertFalse(ts.return_misspast("0 12 * * * * * *"))