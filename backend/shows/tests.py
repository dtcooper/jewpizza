from unittest import skip

from jew_pizza.test_utils import JewPizzaTestCase

from .constants import SHOW_CODES_TO_SHOW


class ViewRenderTests(JewPizzaTestCase):
    fixtures = ("shows/episodes.json", "shows/showdates.json")

    def test_show_master_list_renders(self):
        self.assertPageRenders("shows:show-master-list", "shows/show_master_list.html", "Shows")

    def test_listen_renders(self):
        self.assertPageRenders("shows:listen", "shows/listen.html", "Listen")

    def test_show_list_renders(self):
        for code, show in SHOW_CODES_TO_SHOW.items():
            self.assertPageRenders("shows:show-list", "shows/show_list.html", show.name, {"show": code})

    @skip("Write a test for show-detail")
    def test_show_detail_renders(self):
        pass
