from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import CustomUser


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='Weeb <no-reply@example.com>',
    FRONTEND_URL='https://front.example.com',
)
class PasswordResetEmailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('password-reset-request')

    def test_password_reset_request_sends_email_with_reset_link(self):
        user = CustomUser.objects.create_user(
            email='user@example.com',
            password='InitialPass123!',
        )

        response = self.client.post(self.url, {'email': user.email}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [user.email])
        self.assertEqual(mail.outbox[0].from_email, 'Weeb <no-reply@example.com>')
        self.assertIn('Réinitialisation de votre mot de passe', mail.outbox[0].subject)
        self.assertIn('https://front.example.com/reset-password?uidb64=', mail.outbox[0].body)
        self.assertIn('&token=', mail.outbox[0].body)

    def test_password_reset_request_keeps_generic_response_for_unknown_email(self):
        response = self.client.post(
            self.url,
            {'email': 'unknown@example.com'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)
        self.assertIn('Si un compte est associé à cet email', response.data['message'])
