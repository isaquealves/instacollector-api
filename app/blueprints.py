import sys
import logging

from flask import Blueprint, Response, abort
import instaloader
from app.helpers import collect_profile, save_data

logger = logging.getLogger(__name__)

loader = instaloader.Instaloader()

main_route = Blueprint('main', __name__)



@main_route.route('/<instagram_user>')
def main(instagram_user):

    try:
        profile = collect_profile(loader, instagram_user)
    except TypeError:
        logger.exception('An exception was raised while running main route:',
                         sys.exc_info()[0])
    else:
        save_data(loader, profile)

    return Response("Data successfully saved")