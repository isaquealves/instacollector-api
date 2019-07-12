import os
import json
import unittest

from unittest.mock import patch

import boto3
from moto import mock_s3

from app import create_app

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
                mock_insta.return_value.ok = True
                mock_post.return_value = {'post_data':'Post'}

                response = self.client().get(f"/{self.instagram_user}")
        self.assertEqual(response.status_code, 200)



