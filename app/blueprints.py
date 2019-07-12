import os
import sys
import logging

from flask import Blueprint, Response, abort, jsonify
import instaloader
from app.helpers import (
    get_s3,
    collect_profile,
    save_data,
    upload_user_data,
    download_profile_data_from_s3)

logger = logging.getLogger(__name__)

loader = instaloader.Instaloader()

main_route = Blueprint('main', __name__)
profile_dl = Blueprint('profile_dl_route', __name__)

bucket_name = os.getenv('S3_BUCKET', 'collectorusers')

@main_route.route('/<instagram_user>')
def main(instagram_user):

    try:
        profile = collect_profile(loader, instagram_user)
    except TypeError:
        logger.exception('An exception was raised while running main route:',
                         sys.exc_info()[0])
    else:
        save_data(loader, profile)
        upload_user_data(bucket_name, profile)

    return Response("Data successfully saved")

@profile_dl.route('/<instagram_user>/profile_dl')
def get_profile(instagram_user):
    profile = collect_profile(loader, instagram_user)
    data = download_profile_data_from_s3(bucket_name, profile)
    return data



