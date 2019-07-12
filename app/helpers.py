import os
import logging
from pathlib import Path
import lzma
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

def get_s3_client():
    """ Gets the boto3 client which represents the S3 service

    Returns:
        client (S3.Client): The client instance
    """
    return boto3.client('s3')

def bucket_exists(name):
    """Check if a bucket named 'name' exists

    Args:

        name (string): The bucket name for checking
    """
    resource = get_s3()
    return_dict = {
        '403': {
            'message': 'Bucket exists but access is forbidden',
            'value': (True, 'private')
        },
        '404': {
            'message': 'Bucket doesn\'t exists',
            'value': (False, 'non-existent')
        }
    }
    try:
        resource.meta.client.head_bucket(Bucket=name)
        return (True, 'accessible')
    except ClientError as error:
        error_code = error.response['Error']['Code']
        logger.info(return_dict[error_code]['message'])
        return return_dict[error_code]['value']


def create_or_get_s3_bucket(name):
    """ Creates or obtain a S3 bucket

    Args:
        name (string): The bucket name

    Returns:
        boto3.resource.Bucket

    Raises:
        ClientError: if bucket is not accessible

    """
    resource = get_s3()
    has_bucket = bucket_exists(name)
    if 'non-existent' in has_bucket:
       return resource.create_bucket(Bucket=name)
    if 'accessible' in has_bucket:
        return resource.Bucket(name)


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

def upload_user_data(bucket_name: str, profile: Profile):
    """Uploads downloaded user data from instagram

    Args:
        bucket_name (string): The bucket where we should put the files
        profile (instaloader.Profile): The profile object
    """

    resource = get_s3()
    bucket = create_or_get_s3_bucket(bucket_name)
    root_path = Path(profile.username)

    for path, subdirs, files in os.walk(root_path):
        for file in files:
            bucket.upload_file(root_path.resolve().joinpath(file).as_posix(),
                               root_path.joinpath(file).as_posix())




def download_profile_data_from_s3(bucket_name: str, profile: Profile):
    """Downloads profile data from s3

    Args:
        bucket_name (string): The S3 bucket name
        profile (instaloader.Profile): The instagram's user profile data

    Returns:
        json object
    """
    s3 = get_s3()
    bucket = s3.Bucket(bucket_name)
    s3_profile_key = f"{profile.username}/{profile.username}_{profile.userid}"
    _create_local_directory(profile)
    bucket.download_file(f"{s3_profile_key}.json.xz", f'{s3_profile_key}.json.xz')
    return lzma.open(f'{s3_profile_key}.json.xz').read().decode('utf-8')


def download_post_data_from_s3(bucket_name: str, profile: Profile, post_index: int):
    """ Downloads post data according to the given post index and profile

    Args:
        bucket_name (string): The bucket name
        profile (instaloader.Profile): The user profile
        post_index (integer): The index representing the post choosen to be shown
    """
    s3 = get_s3()
    bucket = s3.Bucket(bucket_name)
    post_list = []

    for s3_object in bucket.objects.filter(Delimiter='/', Prefix=f'{profile.username}/'):
       if ('UTC' in s3_object.key and not 'profile_pic' in s3_object.key and
        s3_object.key.endswith('xz')):
           item = s3_object.key.split('/')[1]
           post_list.append(item)
    post_list.reverse()

    object_key = f'{profile.username}/{post_list[post_index]}'
    bucket.download_file(f"{object_key}", f'{object_key}')
    return lzma.open(f'{object_key}').read().decode('utf-8')




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
