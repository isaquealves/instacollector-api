import os

class Config(object):
    """Configuration class."""
    DEBUG = False
    CSRF_ENABLE = True
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """ Configuration class for development environment."""
    DEBUG = True


class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configuration for staging environment."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}

