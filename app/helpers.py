import os
import logging
from pathlib import Path
from itertools import islice

import boto3
from botocore.client import ClientError

from instaloader import Profile

logger = logging.getLogger(__name__)

def get_s3():
    """ Gets an s3 resource reference

    Returns:

        s3 instance (boto3.resource): S3 resource instance
    """
    return boto3.resource('s3', region_name='us-east-1')

def bucket_exists(name):
    """Check if a bucket named 'name' exists

    Args:

        name (string): The bucket name for checking
    """
    resource = get_s3()
    return_dict = {
        '403': {
            'message': 'Bucket exists but access is forbidden',
            'value': True
        },
        '404': {
            'message': 'Bucket doesn\'t exists',
            'value': False
        }
    }
    try:
        resource.meta.client.head_bucket(Bucket=name)
        return True
    except ClientError as error:
        error_code = error.response['Error']['Code']
        logger.info(return_dict[error_code]['message'])
        return return_dict[error_code]['value']

def create_s3_bucket(name):
    """ Creates a S3 bucket
    """
    resource = get_s3()
    if not bucket_exists(name):
       return resource.create_bucket(Bucket=name)

def _create_local_directory(profile):
    """Creates local directory for a given profile
    if it doesn't exists

    Args:

        profile (instaloader.Profile): The profile object
    """
    try:
        os.stat(profile.username)
    except:
        os.mkdir(profile.username)

def remove_local_folder(profile):
    """Removes the local folders related to user profiles"""
    path = Path(profile.username)
    for item in path.iterdir():
        if item.is_dir():
            remove_local_folder(item)
        else:
            item.unlink()
        path.rmdir()

def upload_user_data(bucket_name: str, profile: Profile):
    """Uploads downloaded user data from instagram

    Args:
        bucket_name (string): The bucket where we should put the files
        profile (instaloader.Profile): The profile object
    """

    resource = get_s3()
    bucket = create_s3_bucket(bucket_name)
    root_path = Path(profile.username)

    for path, subdirs, files in os.walk(root_path):
        for file in files:
            bucket.upload_file(root_path.resolve().joinpath(file).as_posix(),
                               u.joinpath(file).as_posix())


def collect_profile(instance: object, username: str):
    """Collects profile data for a given username

    Args:

        instance (object): An Instaloader object instance
        username (string): The string representing a instagram's username

    Returns:

        Profile: Returns an instance of Profile
    """
    if username.isspace() or len(username.strip()) == 0:
        raise TypeError('No username was provided')
    return Profile.from_username(instance.context, username)


def save_data(instance: object, profile: Profile):
    """Saves profile and posts of the given profile

    Args:

        instance (object): An Instaloader object instance
        profile (instaloader.Profile): The user's profile data
    """
    if not instance:
        raise TypeError('Instaloader instance is missing here!')
    if not profile:
        raise TypeError('Please, check whether profile is getting'
                        'the appropriate value before trying to save data')
    _create_local_directory(profile)
    instance.download_profiles([profile], posts=False)
    posts = profile.get_posts()
    for post in islice(posts, 0, 9):
        instance.download_post(post, target=profile.username)
