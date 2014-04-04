from unittest import TestCase
from TheSleeper import TheSleeper
import os

__author__ = 'monkee'
__project__ = 'TheSleeper'


class TestTheSleeper(TestCase):
    def test_load_configuration(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.load_configuration)

    def test_set_timezone(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.set_timezone)

    def test_check_timezone_set(self):
        ts = TheSleeper()
        self.assertIn("TZ",os.environ)

    def test_check_timezone_value(self):
        ts = TheSleeper()
        self.assertEqual(os.environ["TZ"],"Australia/Brisbane")

    def test_check_timezone_notset(self):
        self.assertNotIn("TZ",os.environ)

    def test_stop_instance(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.stop_instance)

    def test_start_instance(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.start_instance)

    def test_search_for_tagged(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.search_for_tagged)

    def test_search_for_untagged_to_stop(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.search_for_untagged_to_stop)

    def test_parse_sleeper_tags(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.parse_sleeper_tags)

    def test_cron_stop(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.cron_stop)

    def test_cron_start(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.cron_start)

    def test_sns_message(self):
        ts = TheSleeper
        self.assertRaises(Exception,ts.sns_message)