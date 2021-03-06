import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from config import config_dict


# 创建数据库连接对象
db = None  # type:SQLAlchemy
sr = None  # type:StrictRedis

def setup_log(config_class, app):  # 配置日志(将日志写入到文件中)
    # 设置日志的记录等级
    logging.basicConfig(level=config_class.LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(pathname)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

    app.logger.addHandler(file_log_handler)

def create_app(config_type):  # 工厂函数: 外界提供物料, 函数内部封装对象创建过程
    """
    应用创建
    :param config_type: 配置类型
    :return: flask应用
    """

    # 根据配置类型取出对应的配置子类
    config_class = config_dict.get(config_type)

    app = Flask(__name__)
    # 从对象中加载配置
    app.config.from_object(config_class)

    # 声明全局变量
    global db, sr

    # 创建数据库操作对象
    db = SQLAlchemy(app)
    # 创建关键redis操作对象
    sr = StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    # 初始化Session存储
    Session(app)

    # 初始化迁移器
    Migrate(app, db)

    # 3.注册蓝图
    from info.modules.home import home_blu
    app.register_blueprint(home_blu)

    # 配置日志
    setup_log(config_class, app)

    return app
