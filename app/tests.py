from django.test import TestCase, Client


class ViewsTestCase(TestCase):
    """Tests for resume builder views."""

    def setUp(self):
        """Initialize test client."""
        self.client = Client()

    def test_home_view_returns_200(self):
        """Test that home page returns 200 status code."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_view_returns_200(self):
        """Test that about page returns 200 status code."""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_resume_explorer_returns_200(self):
        """Test that resume explorer page returns 200 status code."""
        response = self.client.get('/resume-eplorer/')
        self.assertEqual(response.status_code, 200)

    def test_resume1_returns_200(self):
        """Test that resume 1 returns 200 status code."""
        response = self.client.get('/resume-eplorer/1/')
        self.assertEqual(response.status_code, 200)

    def test_resume2_returns_200(self):
        """Test that resume 2 returns 200 status code."""
        response = self.client.get('/resume-eplorer/2/')
        self.assertEqual(response.status_code, 200)

    def test_resume3_returns_200(self):
        """Test that resume 3 returns 200 status code."""
        response = self.client.get('/resume-eplorer/3/')
        self.assertEqual(response.status_code, 200)
