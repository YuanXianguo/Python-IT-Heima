import redis


class Config(object):
    """配置信息"""
    SECRET_KEY = "aoeqvneoahedpoiqaubnyrffrdqew"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:2017916@127.0.0.1:3306/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_PWD = "2017916yuan"

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = 24 * 3600  # session数据有效期


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境的配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
