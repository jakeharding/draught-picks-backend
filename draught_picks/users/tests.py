"""
tests.py - (C) Copyright - 2018
This software is copyrighted to contributors listed in CONTRIBUTIONS.md.

SPDX-License-Identifier: SEE LICENSE.txt

Author(s) of this file:
  jakeharding

Test user endpoints.
"""

from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework import status


class TestUsers(APITestCase):
    """
    This class tests the user
    """
    fixtures = ['users/fixtures/users.json']

    def setUp(self):
        """
        This tests user creation by setting up the test
        :return:
        """
        self.user = get_user_model().objects.first()
        # Assume user is authenticated for testing.
        self.client.force_authenticate(user=self.user)

    def test_login(self):
        """
        This tests if the user can login
        :return:
        """
        self.client.force_authenticate(user=None) # Remove auth for login
        r = self.client.post('/api/dev/login', {'username': 'admin', 'password': 'admin'}, format='json')
        self.assertTrue(status.is_success(r.status_code))

    def test_create(self):
        """
        This creates the test for the user creation
        :return:
        """
        self.client.force_authenticate(user=None) # Remove auth for create
        r = self.client.post('/api/dev/users', {
            'username': 'admin2',
            'password': 'test',
            'email': 't@t.com',
            'date_of_birth': '1997-05-04'
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)

    def test_update(self):
        """
        This tests the user update
        :return:
        """
        r = self.client.put('/api/dev/users/%s' % self.user.uuid, {
            'username': 'admin2',
            'password': 'test',
            'email': 't@t.com',
            'date_of_birth': '1997-04-20',
            'weight': 195,
            'favorite_beers': [],
            'recent_beers': [],
            'rated_beers': [],
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertEquals(r.data.get('weight'), 195)

    def test_retrieve(self):
        """
        This tests the retrieval
        :return:
        """
        r = self.client.get('/api/dev/users/%s' % self.user.uuid)
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        self.assertEqual(self.user.username, r.data.get('username'))

    def test_list(self):
        """
        This tests the user lists
        :return:
        """
        r = self.client.get('/api/dev/users')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
        results = r.data.get('results')
        self.assertTrue(isinstance(results, list))
        self.assertTrue(len(results) is 1)
        self.assertEqual(self.user.username, results[0].get('username'))

    def test_send_verification_email(self):
        self.user.send_verification_email()
        self.assertTrue(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'DraughtPicks.beer - Email Verification')
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)


class TestBeerPrefs(APITestCase):

    fixtures = ['users/fixtures/users.json']

    def test_create(self):
        self.client.force_authenticate(user=None) # Remove auth for create
        r = self.client.post('/api/dev/preferences', {
            'abv_low': 2,
            'abv_high': 10,
            'ibu_low': 12,
            'ibu_high': 20,
            'user': get_user_model().objects.first().uuid
        }, format='json')
        self.assertTrue(status.is_success(r.status_code), r.status_code)
