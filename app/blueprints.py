import os
import sys
import logging

from flask import Blueprint, Response, abort, jsonify
import instaloader
from app.helpers import (
    collect_profile,
    save_data,
    upload_user_data,
    remove_local_folder)

logger = logging.getLogger(__name__)

loader = instaloader.Instaloader()

main_route = Blueprint('main', __name__)

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
        remove_local_folder(profile)

    return Response("Data successfully saved")