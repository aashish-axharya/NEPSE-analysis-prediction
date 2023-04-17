from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
import os

from .models import StockData

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.index_url = reverse('index')
        self.stocks_url = reverse('stocks')
        self.predictions_url = reverse('predictions')
        self.user = User.objects.create_user(
            username='testuser', password='password')
        self.test_csv =  os.path.join('static', 'individual', 'test.csv')

    def test_signup_view_GET(self):
        response = self.client.get(self.signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_view_POST_failure(self):
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'password1': 'password',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_POST_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password',
        })

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

    def test_login_view_POST_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.logout_url)

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

    def test_index_view_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_POST(self):
        response = self.client.post(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_GET_with_selected_date(self):
        response = self.client.get(self.index_url, {'selected_date': '04/12/2023'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_GET_with_invalid_selected_date(self):
        response = self.client.get(self.index_url, {'selected_date': 'invalid'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')