from django.test import TestCase, Client
from django.contrib.auth.models import User
from documents.models import Document

class DocumentSubmitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
    
    def test_submit_document(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.post("/documents/create/", {
            "title": "Test Doc",
            "description": "Test Desc",
            "action": "submit"
        })

        self.assertEqual(response.status_code, 302)
        doc = Document.objects.first()
        self.assertEqual(doc.status, "submitted")
