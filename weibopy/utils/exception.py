from json import JSONDecodeError

__all__ = [
    # warnings
    'WeiboWarning',
    'IgnoreErrorDataWarning',
    'GetEmptyResponseWhenFetchData',
    # exceptions
    'WeiboException',
    'UnexpectedResponseException',
    'GetDataErrorException',
    'NeedCaptchaException',
    'NeedLoginException',
    'IdMustBeIntException',
    'UnimplementedException',
    'JSONDecodeError',
]


class WeiboException(Exception):
    pass


class UnexpectedResponseException(WeiboException):
    def __init__(self, url, res, expect):
        """
        服务器回复了和预期格式不符的数据

        :param str url: 当前尝试访问的网址
        :param request.Response res: 服务器的回复
        :param str expect: 一个用来说明期望服务器回复的数据格式的字符串
        """
        self.url = url
        self.res = res
        self.expect = expect

    def __repr__(self):
        return (f'Get an unexpected response when visit url [{self.url}], '
                f'we expect [{self.expect}], but the response body is {self.res.text}')

    __str__ = __repr__


class UnimplementedException(WeiboException):
    def __init__(self, what):
        """
        处理当前遇到的情况的代码还未实现，只是开发的时候用于占位

        ..  note:: 一般用户不用管这个异常

        :param str what: 用来描述当前遇到的情况
        """
        self.what = what

    def __repr__(self):
        return (f'Meet a unimplemented condition: {self.what}. '
                f'Please send this error message to developer to get help.')

    __str__ = __repr__


class GetDataErrorException(UnexpectedResponseException):
    def __init__(self, url, res, expect):
        """
        :class:`UnexpectedResponseException` 的子类，
        尝试获取服务器给出的错误信息。如果获取失败则显示父类的出错信息。

        ..  seealso:: :class:`UnexpectedResponseException`
        """
        super().__init__(url, res, expect)
        try:
            self.reason = res.json()['error']['message']
        except (JSONDecodeError, KeyError):
            self.reason = None

    def __repr__(self):
        if self.reason:
            return f'A error happened when get data: {self.reason}'
        else:
            base = super().__repr__()
            return 'Unknown error! ' + base

    __str__ = __repr__


class TokenError(WeiboException):
    def __init__(self, msg):
        self._msg = msg

    def __repr__(self):
        return self._msg


class NeedCaptchaException(WeiboException):
    """登录过程需要验证码"""

    def __repr__(self):
        return ('Need a captcha to login, please catch this exception and '
                'use client.get_captcha() to get it.')

    __str__ = __repr__


class NeedLoginException(WeiboException):
    def __init__(self, what):
        """
        使用某方法需要登录而当前客户端未登录

        :param str what: 当前试图调用的方法名
        """
        self.what = what

    def __repr__(self):
        return f'Need login to use the [{self.what}] method.'

    __str__ = __repr__


class IdMustBeIntException(WeiboException):
    def __init__(self, func):
        """
        获取对应的微博类时，试图传递不是整数型的 ID

        :param function func: 当前试图调用的方法名
        """
        self.func = func.__name__

    def __repr__(self):
        return f'You must provide a integer id to use function: {self.func}'

    __str__ = __repr__


class WeiboWarning(UserWarning):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args)
        self._message = message

    def __str__(self):
        return str(self._message)

    __repr__ = __str__


class IgnoreErrorDataWarning(WeiboWarning):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


GetEmptyResponseWhenFetchData = IgnoreErrorDataWarning(
    "get empty response"
)
