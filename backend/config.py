import os

class Config:
    """Base configuration settings for SpamShield AI."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'spamshield-super-secret-key-1337')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, 'database', 'spamshield.db')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development settings."""
    DEBUG = True

class TestingConfig(Config):
    """Testing settings."""
    TESTING = True
    DB_PATH = os.path.join(Config.BASE_DIR, 'database', 'spamshield_test.db')

class ProductionConfig(Config):
    """Production settings."""
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
