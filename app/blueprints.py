import os
import sys
import json
import logging

from flask import Blueprint, Response, abort, jsonify
import instaloader
from app.helpers import (
    get_s3,
    collect_profile,
    save_data,
    upload_user_data,
    download_profile_data_from_s3,
    download_post_data_from_s3)

logger = logging.getLogger(__name__)

loader = instaloader.Instaloader(download_comments=False)

main_route = Blueprint('main', __name__)
profile_dl = Blueprint('profile_dl_route', __name__)
single_post_dl = Blueprint('spost_dl_route', __name__)

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


@single_post_dl.route('/<string:instagram_user>/posts/<int:post_index>')
def single_post_download(instagram_user, post_index):

    profile = collect_profile(loader, instagram_user)
    data = json.loads(download_post_data_from_s3(bucket_name,
                                                 profile,
                                                 post_index))
    return data
