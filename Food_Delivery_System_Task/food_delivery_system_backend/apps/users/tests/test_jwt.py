from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.tests import RestaurantUserFactory


class JWTAuthenticationTestCase(APITestCase):
    """
    Test suite for jwt token access and refresh.
    
    Checks authentication with valid, invalid token, without token, token refresh and obtain token.
    """
    
    def setUp(self):
        """Set up test data - runs before each test method"""
        self.client = APIClient()
        self.password = 'testpass123'
        self.user = RestaurantUserFactory()
        self.refresh = RefreshToken.for_user(self.user)  
        self.access_token = str(self.refresh.access_token)
    
    def test_authentication_with_valid_jwt(self):
        """Test API access with valid JWT token"""
        url = reverse('customers-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')  
        response = self.client.get(url) 
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authentication_with_invalid_jwt(self):
        """Test API access with invalid JWT token"""
        url = reverse('customers-list')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token') 
        
        response = self.client.get(url) 
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
    
    def test_authentication_without_jwt(self):
        """Test API access without JWT token"""
        url = reverse('customers-list')
        response = self.client.get(url) 
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
    
    def test_jwt_token_refresh(self):
        """Test refreshing JWT token"""
        url = reverse('token_refresh')
        response = self.client.post(url, { 
            'refresh': str(self.refresh)
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertIn('access', response.data) 
    
    def test_obtain_jwt_tokens(self):
        """Test obtaining JWT tokens"""
        url = reverse('token_obtain')
        response = self.client.post(
            url, 
            { 
                'username': self.user.username,
                'password': self.password,
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)