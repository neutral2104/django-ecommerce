from django.test import TestCase
from django.urls import reverse

class CourseworkTests(TestCase):
    # Test 1: Check if the Home Page is accessible (Status 200)
    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Test 2: Check if the Admin Login page is secure and accessible
    def test_admin_page_accessible(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)

    # Test 3: Check for a 404 error on a non-existent page (Error Handling)
    def test_page_not_found(self):
        response = self.client.get('/this-page-does-not-exist/')
        self.assertEqual(response.status_code, 404)

    # Test 4: Verify the Application Name/Title exists in the HTML
    def test_homepage_content(self):
        response = self.client.get('/')
        # Change "Ecommerce" to a word that actually appears on your homepage
        self.assertContains(response, "Ecommerce") 

    # Test 5: Check if the CSRF token is present on the login page (Security)
    def test_login_csrf_protection(self):
        response = self.client.get('/admin/login/')
        self.assertContains(response, 'csrfmiddlewaretoken')
