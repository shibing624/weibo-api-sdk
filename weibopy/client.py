import requests

__all__ = ['WeiboClient']


class WeiboClient:
    def __init__(self, cookie=None):
        """
        初始化微博客户端
        
        :param cookie: 可选的Cookie字符串，用于绕过反爬虫检测
                      可以从浏览器中获取，格式如: "SUB=xxx; SUBP=xxx"
        """
        self._session = requests.session()
        # 设置必要的请求头，绕过基本的反爬虫检测
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m.weibo.cn/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'X-Requested-With': 'XMLHttpRequest',
        })
        
        # 如果提供了cookie，则设置
        if cookie:
            self._session.headers['Cookie'] = cookie

    def people(self, uid):
        """
        用户相关信息
        :param uid: 
        :return: 
        """
        from .weibo.people import People
        return People(uid, None, self._session)

    def status(self, sid):
        """
        微博详情
        :param sid: 
        :return: 
        """
        from .weibo.status import Status
        return Status(sid, None, self._session)

    def statuses(self, uid):
        """
        全部微博列表
        :param uid: 
        :return: 
        """
        from .weibo.status import Statuses
        return Statuses(uid, None, self._session)

    def origin_statuses(self, uid):
        """
        原创微博列表
        :param uid: 
        :return: 
        """
        from .weibo.status import Statuses
        return Statuses(uid, None, self._session, original=True)

    def article(self, aid):
        """
        文章相关信息
        :param aid: 
        :return: 
        """
        from .weibo.article import Article
        return Article(aid, None, self._session)

    def articles(self, uid):
        """
        文章列表
        :param uid: 
        :return: 
        """
        from .weibo.article import Articles
        return Articles(uid, None, self._session)

    def origin_articles(self, uid):
        """
        原创文章列表
        :param uid: 
        :return: 
        """
        pass

    def followers(self, uid):
        """
        粉丝列表
        :param uid: 
        :return: 
        """
        from .weibo.people import Peoples
        return Peoples(uid, None, self._session, utype='follower')

    def follow(self, uid):
        """
        关注列表
        :param uid: 
        :return: 
        """
        from .weibo.people import Peoples
        return Peoples(uid, None, self._session, utype='follow')
