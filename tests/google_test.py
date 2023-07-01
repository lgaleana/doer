from unittest import TestCase

from code_tasks import perform_task


class Tests(TestCase):
    def test_dogs(self):
        perform_task("tell me about dogs")

    def test_katana_opening(self):
        perform_task("katana kitten opening hours")

    def test_katana_cocktails(self):
        perform_task("katana kitten best cocktails")

    def test_rain_nyc(self):
        perform_task("is it going to rain tomorrow in nyc?")

    def test_map_latest(self):
        perform_task("i want to know how to use the latest google maps api")

    def test_map_example(self):
        perform_task("give me an example of how to use the latest google maps api")

    def test_subway(self):
        # Has failure cases
        perform_task("when is the next c train coming to spring street?", False)

    def test_la_300(self):
        # Has failure cases
        perform_task(
            "In what cities in latin america I can live for under $300 in airbnb a month?", False
        )
