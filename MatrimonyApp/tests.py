from django.test import TestCase, Client
from django.urls import reverse
from .models import Login, Person
from django.contrib.auth.models import User 
class URLViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_login = Login.objects.create_user(
            username="testuser@example.com",
            password="testpass123",
            userType="User",
            is_active=True
        )
        self.user_profile = Person.objects.create(
            name="User One",
            gender="Male",
            email="testuser@example.com",
            phone=1234567890,
            loginid=self.user_login
        )

    def test_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.post("/login/", {"email": "testuser@example.com", "password": "testpass123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login Success")

    def test_user_home_view_authenticated(self):
        self.client.login(username="testuser@example.com", password="testpass123")
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()
        response = self.client.get("/userHome/")
        self.assertEqual(response.status_code, 200)

    def test_profile_view_authenticated(self):
        self.client.login(username="testuser@example.com", password="testpass123")
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

class UserRegistrationIntegrationTest(TestCase):

    def test_user_registration_success(self):
        """Test successful user registration"""
        # Prepare data
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "phone": "1234567890",
            "gender": "Male",
            "city": "Test City",
            "age": 30,
            "password": "password123",
            "imgfile": SimpleUploadedFile(
                name="profile_pic.jpg",
                content=b"image content",
                content_type="image/jpeg"
            )
        }

        # Post the registration form
        response = self.client.post(reverse('register'), data)

        # Check for successful registration
        self.assertEqual(response.status_code, 302)  # Redirect to login page after success
        self.assertRedirects(response, '/login/', status_code=302, target_status_code=200)


        self.assertTrue(get_user_model().objects.filter(username=data["email"]).exists())

    