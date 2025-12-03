import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Үндсэн тохиргоо"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fitproof-secret-key-2024'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Хөгжүүлэлтийн тохиргоо"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'fitproof_dev.db')


class TestingConfig(Config):
    """Туршилтын тохиргоо"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Үйлдвэрлэлийн тохиргоо"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'fitproof.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

