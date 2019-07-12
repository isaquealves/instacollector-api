import os
import json
import unittest

from unittest.mock import patch
import instaloader

import boto3
from moto import mock_s3

from app import create_app
class MockProfile(object):
    pass

class MockFileObject(object):
    def read(self):
        return '{"sample": "sample file obj"}'.encode('utf-8')

class InstacollectorTestCase(unittest.TestCase):
    """This class contains a group of tests for Instacollector
    """

    def setUp(self):
        """Setup tests variables and initializes app
        """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.instagram_user = 'test'

    def test_load_instagram_profile(self):
        with patch('instaloader.Instaloader.download_profiles') as mock_insta:
            with patch('instaloader.Instaloader.download_post') as mock_post:
                mock_insta.return_value = True
                mock_post.return_value = {'post_data':'Post'}

                response = self.client().get(f"/{self.instagram_user}")
        self.assertEqual(response.status_code, 200)

    def test_get_profile_from_s3(self):
        mock_profile = MockProfile()
        mock_profile.username = 'test'
        mock_profile.userid = '0089283'
        with patch('boto3.resource'):
            with patch('lzma.open') as lzma_mock:
                with patch('instaloader.Profile.from_username') as mock_insta:
                    mock_insta.return_value = mock_profile
                    lzma_mock.return_value = MockFileObject()
                    response = self.client().get(f"/{self.instagram_user}/profile_dl")
                    self.assertEqual(response.status_code, 200)