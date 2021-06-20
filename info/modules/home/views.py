from info import sr
from . import home_blu
import logging  # python内置的日志模块 可以将日志输出到控制台, 还可以将日志写入到文件
# flask的默认打印使用的是logging模块, 只将打印输出到了控制台, 但没有写入到文件中

from flask import current_app

# 2.使用蓝图对象来注册路由
@home_blu.route('/')
def index():
    # sr.set('age',20)
    try:
        10 / 0
    except Exception as e:
        # logging默认的输出语法不包含日志所在的文件和行号,不方便定位日志, 建议使用flask内置的日志输出语法
        # logging.error(e)
        # logging.exception(e)
        current_app.logger.error(e)

    return "index"