import os
basedir = os.path.abspath(os.path.dirname(__file__))



#？？？表示未确定的参数
'''
Config类对整个项目的环境参数进行配置
'''
class Config:
    SECRET_KEY = os.environ.get('SECRET_KY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[MovieRecomm]'
    FLASKY_MAIL_SENDER = 'movieRecomm<???>'

    '''
    配置定义init_app的方法对当前环境配置初始化，参数是程序实例
    '''
    @staticmethod
    def init_app(app):
        pass

'''
继承父类Config的开发环境配置
'''
class DevelopmentConfig(Config):
    DEBUG= True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')
    MOVIE_ITEM_PER_PAGE = 10
'''
测试环境配置
'''
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'data-test.sqlite')

'''
生产环境配置
'''

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir, 'data.sqlite')

'''
定义一个字典config，用来保存对应的类的映射
'''
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    
    'default': DevelopmentConfig
}

