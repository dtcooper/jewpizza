from django.contrib.auth.models import User

from jew_pizza.test_utils import JewPizzaTestCase


class ViewRenderTests(JewPizzaTestCase):
    def setUp(self):
        User.objects.create_superuser(username="admin", password="topsecret")
        self.client.login(username="admin", password="topsecret")

    def test_index_renders(self):
        self.assertPageRenders("admin-tools:index", "admin_tools/base.html")

    def test_container_status_renders(self):
        self.assertPageRenders("admin-tools:container-status", "admin_tools/container_status.html")

    def test_send_text_message_renders(self):
        self.assertPageRenders("admin-tools:send-text-message", "admin_tools/send_text_message.html")

    def test_send_email_renders(self):
        self.assertPageRenders("admin-tools:send-email", "admin_tools/form.html")
