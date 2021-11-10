import json

from django.test import TestCase
from django.urls import reverse


class JewPizzaTestCase(TestCase):
    def assertPageRenders(self, url_name, template_name=None, title=None, url_kwargs=None):
        url = reverse(url_name, kwargs=url_kwargs)

        # Regular
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        if template_name is not None:
            self.assertIn(template_name, response.template_name)

        # As JSON
        response = self.client.get(url, HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, 200)

        try:
            data = json.loads(response.content)
        except json.JSONDecodeError:
            self.fail(f"Invalid JSON: {response.content}")

        self.assertEqual(data["status"], 200)
        self.assertIsInstance(data["content"], str)
        if title is not None:
            self.assertEqual(data["title"], title)
