import os
from itertools import islice
from instaloader import Profile

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




