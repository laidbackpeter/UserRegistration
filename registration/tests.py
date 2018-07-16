# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import APIClient
from rest_framework import status as http_status
from django.test import LiveServerTestCase, TestCase
from django.conf import settings
import json
import mock
from django.core.urlresolvers import reverse
from serializers import RegisterFarmerRequestSerializer, RegisterSeedBagRequestSerializer

# Create your tests here.
register_farmer_valid_payload = {
            "first_name": "Peter",
            "last_name": "Muchina",
            "other_name": "Ndegwa",
            "phone_number": "254725817350",
            "country": "Kenya",
            "district": "Nairobi",
            "village": "Tipis",
            "crop": "Potatoes"
        }
register_farmer_invalid_payload = {
            "first_name": "Peter",
            "last_name": "Muchina",
            "other_name": "Ndegwa",
            "country": "Kenya",
            "district": "Nairobi",
            "village": "Tipis",
            "crop": "Potatoes"
        }
register_seed_bag_valid_payload = {
            "phone_number": "254725817350",
            "bag_unique_number": "12345ygft"
        }
register_seed_bag_invalid_payload = {
            "phone_number": "254725817350",
        }


class TestSerializers(TestCase):
    def setUp(self):
        self.register_farmer_valid_payload = register_farmer_valid_payload
        self.register_farmer_invalid_payload = register_farmer_invalid_payload
        self.register_seed_bag_valid_payload = register_seed_bag_valid_payload
        self.register_seed_bag_invalid_payload = register_seed_bag_invalid_payload

    def tearDown(self):
        pass

    def test_register_farmer_serializer(self):
        serializer = RegisterFarmerRequestSerializer(
            data=self.register_farmer_valid_payload)
        validated_payload = serializer.is_valid()
        self.assertTrue(validated_payload)
        self.assertFalse(serializer.errors)

        # Missing attribute (phone_number) in payload
        serializer = RegisterFarmerRequestSerializer(
            data=self.register_farmer_invalid_payload)
        validated_payload = serializer.is_valid()
        self.assertFalse(validated_payload)
        self.assertTrue(serializer.errors)

    def test_register_seed_bag_serializer(self):
        serializer = RegisterSeedBagRequestSerializer(
            data=self.register_seed_bag_valid_payload)
        validated_payload = serializer.is_valid()
        self.assertTrue(validated_payload)
        self.assertFalse(serializer.errors)

        # Missing attribute (bag_unique_number) in payload
        serializer = RegisterSeedBagRequestSerializer(
            data=self.register_seed_bag_invalid_payload)
        validated_payload = serializer.is_valid()
        self.assertFalse(validated_payload)
        self.assertTrue(serializer.errors)


class TestAuthentication(LiveServerTestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        pass

    def test_missing_api_key(self):
        views = ['registration_urls:register-farmer', 'registration_urls:register-seed-bag']
        payloads = {
            'registration_urls:register-farmer': register_farmer_valid_payload,
            'registration_urls:register-seed-bag': register_seed_bag_valid_payload
        }
        for view in views:
            resp = self.client.post(
                reverse(view),
                data=payloads[view],
                content_type='application/json')

            self.assertEqual(resp.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_wrong_api_key(self):
        self.api_key = "test-wrong-api-key"
        self.client.credentials(HTTP_APIKEY=self.api_key)
        views = ['registration_urls:register-farmer', 'registration_urls:register-seed-bag']
        payloads = {
            'registration_urls:register-farmer': register_farmer_valid_payload,
            'registration_urls:register-seed-bag': register_seed_bag_valid_payload
        }
        for view in views:
            resp = self.client.post(
                reverse(view),
                data=payloads[view],
                content_type='application/json')

            self.assertEqual(resp.status_code, http_status.HTTP_403_FORBIDDEN)


class TestFarmerRegistrationView(LiveServerTestCase):
    def setUp(self):
        self.client = APIClient()
        self.api_key = settings.CLIENT_API_KEY
        self.client.credentials(HTTP_APIKEY=self.api_key)

        self.register_farmer_valid_payload = register_farmer_valid_payload
        self.register_farmer_invalid_payload = register_farmer_invalid_payload

    def tearDown(self):
        pass

    def test_valid_request(self):
        resp = self.client.post(
            reverse('registration_urls:register-farmer'),
            data=json.dumps(self.register_farmer_valid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_202_ACCEPTED)
        self.assertEqual(resp.content, '{"Details":"Ok"}')

    @mock.patch('registration.models.Farmers.save')
    def test_valid_request_save_failure(self, save_mock):
        save_mock.side_effect = Exception()
        resp = self.client.post(
            reverse('registration_urls:register-farmer'),
            data=json.dumps(self.register_farmer_valid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_invalid_request(self):
        # Missing attribute (phone_number) in payload
        resp = self.client.post(
            reverse('registration_urls:register-farmer'),
            data=json.dumps(self.register_farmer_invalid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.content, '{"phone_number":["This field is required."]}')


class TestSeedBagRegistrationView(LiveServerTestCase):
    def setUp(self):
        self.client = APIClient()
        self.api_key = settings.CLIENT_API_KEY
        self.client.credentials(HTTP_APIKEY=self.api_key)

        self.register_farmer_valid_payload = register_farmer_valid_payload
        self.register_seed_bag_valid_payload = register_seed_bag_valid_payload
        self.register_seed_bag_invalid_payload = register_seed_bag_invalid_payload

    def tearDown(self):
        pass

    def test_valid_request(self):
        # Send farmer registration test first because a seed bag cannot be registered without
        # a farmer
        resp = self.client.post(
            reverse('registration_urls:register-farmer'),
            data=json.dumps(self.register_farmer_valid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_202_ACCEPTED)
        self.assertEqual(resp.content, '{"Details":"Ok"}')

        resp = self.client.post(
            reverse('registration_urls:register-seed-bag'),
            data=json.dumps(self.register_seed_bag_valid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_202_ACCEPTED)
        self.assertEqual(resp.content, '{"Details":"Ok"}')

    @mock.patch('registration.models.SeedBag.save')
    def test_valid_request_save_failure(self, save_mock):
        # Send farmer registration test first because a seed bag cannot be registered without
        # a farmer
        resp = self.client.post(
            reverse('registration_urls:register-farmer'),
            data=json.dumps(self.register_farmer_valid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_202_ACCEPTED)
        self.assertEqual(resp.content, '{"Details":"Ok"}')

        save_mock.side_effect = Exception()
        resp = self.client.post(
            reverse('registration_urls:register-seed-bag'),
            data=json.dumps(self.register_seed_bag_valid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_valid_request_without_invalid_farmer(self):
        resp = self.client.post(
            reverse('registration_urls:register-seed-bag'),
            data=json.dumps(self.register_seed_bag_valid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_202_ACCEPTED)
        self.assertEqual(resp.content, '{"Details":"Farmer doesn\'t exists"}')

    def test_invalid_request(self):
        # Send farmer registration test first because a seed bag cannot be registered without
        # a farmer
        resp = self.client.post(
            reverse('registration_urls:register-farmer'),
            data=json.dumps(self.register_farmer_valid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_202_ACCEPTED)
        self.assertEqual(resp.content, '{"Details":"Ok"}')

        # Missing attribute (bag_unique_number) in payload
        resp = self.client.post(
            reverse('registration_urls:register-seed-bag'),
            data=json.dumps(self.register_seed_bag_invalid_payload),
            content_type='application/json')

        self.assertEqual(resp.status_code, http_status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.content, '{"bag_unique_number":["This field is required."]}')
