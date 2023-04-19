from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from unittest.mock import patch
import os

from .models import StockData, BlogPost, User, Favorite
from .forms import BlogPostForm


# class StockDataTestCase(TestCase):
#     def setUp(self):
#         self.stock_data = StockData.objects.create(
#             sn='1234', 
#             symbol='AAPL', 
#             company_name='Apple Inc.', 
#             conf='YES', 
#             open='100.00',
#             high='110.00',
#             low='90.00',
#             close='105.00',
#             vwap='95.00',
#             volume='10000',
#             prev_close='100.00',
#             turnover='1000000',
#             trans='1000',
#             diff='5.00',
#             range='20.00',
#             diff_percent='5.00',
#             range_percent='20.00',
#             vwap_percent='5.00',
#             days120='110.00',
#             days180='115.00',
#             weeks52_high='120.00',
#             weeks52_low='70.00'
#         )

#     def test_stock_data_sn(self):
#         self.assertEqual(self.stock_data.sn, '1234')

#     def test_stock_data_symbol(self):
#         self.assertEqual(self.stock_data.symbol, 'AAPL')

#     def test_stock_data_company_name(self):
#         self.assertEqual(self.stock_data.company_name, 'Apple Inc.')

#     def test_stock_data_get_favorited_by(self):
#         self.user = User.objects.create(username='testuser', email='testuser@example.com', password='testpass')
#         Favorite.objects.create(user=self.user, stock=self.stock_data)
#         self.assertIn(self.user, self.stock_data.get_favorited_by())

# class BlogPostTestCase(TestCase):
#     def setUp(self):
#         self.author = User.objects.create_user(username='testuser', password='testpass')
#         self.blog_post = BlogPost.objects.create(
#             title='Test Post', 
#             content='Test Content', 
#             author=self.author
#         )

#     def test_blog_post_title(self):
#         self.assertEqual(self.blog_post.title, 'Test Post')

#     def test_blog_post_content(self):
#         self.assertEqual(self.blog_post.content, 'Test Content')

#     def test_blog_post_author(self):
#         self.assertEqual(self.blog_post.author, self.author)

# class FavoriteTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='testuser', email='testuser@example.com', password='testpass')
#         self.stock_data = StockData.objects.create(
#             sn='1234', 
#             symbol='AAPL', 
#             company_name='Apple Inc.', 
#             conf='YES', 
#             open='100.00',
#             high='110.00',
#             low='90.00',
#             close='105.00',
#             vwap='95.00',
#             volume='10000',
#             prev_close='100.00',
#             turnover='1000000',
#             trans='1000',
#             diff='5.00',
#             range='20.00',
#             diff_percent='5.00',
#             range_percent='20.00',
#             vwap_percent='5.00',
#             days120='110.00',
#             days180='115.00',
#             weeks52_high='120.00',
#             weeks52_low='70.00'
#         )
#         self.favorite = Favorite.objects.create(user=self.user, stock=self.stock_data)

#     def test_favorite_user(self):
#         self.assertEqual(self.favorite.user, self.user)

#     def test_favorite_stock(self):
#         self.assertEqual(self.favorite.stock, self.stock_data)


# class TestViews(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.signup_url = reverse('signup')
#         self.login_url = reverse('login')
#         self.logout_url = reverse('logout')
#         self.index_url = reverse('index')
#         self.stocks_url = reverse('stocks')
#         self.predictions_url = reverse('predictions')
#         self.user = User.objects.create(username='testuser', email='testuser@example.com', password='testpass')
#         self.test_csv =  os.path.join('static', 'individual', 'test.csv')

    # def test_signup_view_GET(self):
    #     response = self.client.get(self.signup_url)

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'signup.html')

    # def test_signup_view_POST_failure(self):
    #     response = self.client.post(self.signup_url, {
    #         'username': 'testuser',
    #         'password1': 'password',
    #     })

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'signup.html')

    # def test_login_view_GET(self):
    #     response = self.client.get(self.login_url)

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')

    # def test_login_view_POST_success(self):
    #     response = self.client.post(self.login_url, {
    #         'username': 'testuser',
    #         'password': 'password',
    #     })

    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, self.index_url)

    # def test_login_view_POST_failure(self):
    #     response = self.client.post(self.login_url, {
    #         'username': 'testuser',
    #         'password': 'wrongpassword',
    #     })

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')

    # def test_logout_view(self):
    #     self.client.login(username='testuser', password='password')
    #     response = self.client.get(self.logout_url)

    #     self.assertEquals(response.status_code, 302)
    #     self.assertRedirects(response, self.index_url)

    # def test_index_view_GET(self):
    #     response = self.client.get(self.index_url)

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')

    # def test_index_view_POST(self):
    #     response = self.client.post(self.index_url)

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')

    # def test_index_view_GET_with_selected_date(self):
    #     response = self.client.get(self.index_url, {'selected_date': '04/12/2023'})

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')

    # def test_index_view_GET_with_invalid_selected_date(self):
    #     response = self.client.get(self.index_url, {'selected_date': 'invalid'})

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')

# class StocksTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_stocks_view_with_existing_stock(self):
#         # Test if the view returns a HTTP 200 status code for an existing stock
#         response = self.client.get(reverse('stocks'), {'stock': 'ADBL'})
#         self.assertEqual(response.status_code, 200)

#         # Test if the view returns the correct template
#         self.assertTemplateUsed(response, 'stocks.html')

#         # Test if the view returns the correct stock data
#         self.assertEqual(len(response.context['page_obj'].object_list), 10)
#         self.assertEqual(response.context['selected_stock'], 'ADBL')

#     def test_stocks_view_with_non_existing_stock(self):
#         # Test if the view returns an empty stock data list for a non-existing stock
#         response = self.client.get(reverse('stocks'), {'stock': 'NONEXIST'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['page_obj'].object_list), 0)
#         self.assertEqual(response.context['selected_stock'], 'NONEXIST')


class AnalysisTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_analysis_get(self):
        response = self.client.get('/analysis/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analysis.html')

    def test_analysis_post_valid(self):
        response = self.client.post('/analysis/', {'stock': 'ADBL'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analysis.html')



    

