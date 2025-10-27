"""
Weibopy - 微博 API Python 客户端

一个免登陆获取新浪微博数据的Python库，简单易用。
"""

__version__ = '0.1.1'
__author__ = 'xuming'
__email__ = 'xuming624@qq.com'
__license__ = 'MIT'

from .client import WeiboClient

__all__ = ['WeiboClient', '__version__']
