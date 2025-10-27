"""
测试 WeiboClient 客户端
"""
import pytest
from weibo_api_sdk import WeiboClient
from weibo_api_sdk.weibo.people import People
from weibo_api_sdk.weibo.status import Status, Statuses
from weibo_api_sdk.weibo.article import Article, Articles


class TestWeiboClient:
    """测试 WeiboClient 类"""

    def test_client_init_with_cookie(self, mock_cookie):
        """测试使用 Cookie 初始化客户端"""
        client = WeiboClient(cookie=mock_cookie)
        assert client._session is not None
        assert 'Cookie' in client._session.headers
        assert client._session.headers['Cookie'] == mock_cookie

    def test_client_init_without_cookie(self):
        """测试不使用 Cookie 初始化客户端"""
        client = WeiboClient()
        assert client._session is not None
        assert 'User-Agent' in client._session.headers
        # Cookie 应该不存在或为空
        assert 'Cookie' not in client._session.headers or not client._session.headers.get('Cookie')

    def test_client_has_default_headers(self, client):
        """测试客户端是否有默认请求头"""
        headers = client._session.headers
        assert 'User-Agent' in headers
        assert 'Referer' in headers
        assert 'Accept' in headers
        assert 'Accept-Language' in headers
        assert 'X-Requested-With' in headers

    def test_client_user_agent(self, client):
        """测试 User-Agent 设置"""
        user_agent = client._session.headers['User-Agent']
        assert 'Mozilla' in user_agent
        assert 'iPhone' in user_agent or 'Mobile' in user_agent

    def test_people_method_returns_people_object(self, client):
        """测试 people() 方法返回 People 对象"""
        uid = "1815418641"
        people = client.people(uid)
        assert isinstance(people, People)
        assert people._id == uid
        assert people._session == client._session

    def test_status_method_returns_status_object(self, client):
        """测试 status() 方法返回 Status 对象"""
        status_id = "test_status_id"
        status = client.status(status_id)
        assert isinstance(status, Status)
        assert status._id == status_id
        assert status._session == client._session

    def test_statuses_method_returns_statuses_object(self, client):
        """测试 statuses() 方法返回 Statuses 对象"""
        uid = "1815418641"
        statuses = client.statuses(uid)
        assert isinstance(statuses, Statuses)
        assert statuses._id == uid
        assert statuses._session == client._session

    def test_origin_statuses_method(self, client):
        """测试 origin_statuses() 方法"""
        uid = "1815418641"
        statuses = client.origin_statuses(uid)
        assert isinstance(statuses, Statuses)
        assert statuses._original is True

    def test_article_method_returns_article_object(self, client):
        """测试 article() 方法返回 Article 对象"""
        article_id = "test_article_id"
        article = client.article(article_id)
        assert isinstance(article, Article)
        assert article._id == article_id

    def test_articles_method_returns_articles_object(self, client):
        """测试 articles() 方法返回 Articles 对象"""
        uid = "1815418641"
        articles = client.articles(uid)
        assert isinstance(articles, Articles)
        assert articles._id == uid

    def test_multiple_clients_are_independent(self, mock_cookie):
        """测试多个客户端实例相互独立"""
        client1 = WeiboClient(cookie="cookie1")
        client2 = WeiboClient(cookie="cookie2")
        
        assert client1._session != client2._session
        assert client1._session.headers['Cookie'] == "cookie1"
        assert client2._session.headers['Cookie'] == "cookie2"

    def test_client_session_persistence(self, client):
        """测试客户端会话持久性"""
        session1 = client._session
        # 多次调用 people 应该使用同一个 session
        client.people("123")
        client.people("456")
        assert client._session == session1

