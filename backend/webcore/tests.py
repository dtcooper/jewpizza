import json

from django.core import mail
from django.urls import reverse

from jew_pizza.test_utils import JewPizzaTestCase


class ViewRenderTests(JewPizzaTestCase):
    def test_home_renders(self):
        self.assertPageRenders("webcore:home", "webcore/home.html", "jew.pizza - David Cooper")

    def test_bio_renders(self):
        self.assertPageRenders("webcore:bio", "webcore/bio.html", "Bio")

    def test_testimonials_renders(self):
        self.assertPageRenders("webcore:testimonials", "webcore/testimonials.html", "Testimonials")

    def test_social_renders(self):
        self.assertPageRenders("webcore:social", "webcore/social.html", "Social")

    def test_log_js_error(self):
        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(
            reverse("webcore:log-js-error"),
            json.dumps(
                {
                    "url": "http://example.com",
                    "title": "test_title",
                    "detail": "test_detail",
                    "filename": "test_filename.js",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(mail.outbox), 1)
