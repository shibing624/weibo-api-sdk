#!/usr/bin/env python
"""
基本使用示例

这个示例展示了 weibo-api 的基本使用方法，包括：
1. 获取用户信息
2. 获取用户微博列表
3. 获取用户文章列表
4. 获取粉丝和关注列表
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weibopy import WeiboClient
from dotenv import load_dotenv

load_dotenv()

def get_user_info(client, uid):
    """获取用户基本信息"""
    print(f"\n{'='*50}")
    print(f"正在获取用户 {uid} 的信息...")
    print(f"{'='*50}")
    
    try:
        people = client.people(uid)
        
        print(f"用户ID: {people.id}")
        print(f"昵称: {people.name}")
        print(f"简介: {people.description}")
        print(f"性别: {people.gender}")
        print(f"粉丝数: {people.followers_count}")
        print(f"关注数: {people.follow_count}")
        print(f"头像: {people.avatar}")
        
        return people
    except Exception as e:
        print(f"获取用户信息失败: {e}")
        return None


def get_user_statuses(client, uid, count=5):
    """获取用户的微博列表"""
    print(f"\n{'='*50}")
    print(f"正在获取用户 {uid} 的最新 {count} 条微博...")
    print(f"{'='*50}")
    
    try:
        statuses = client.statuses(uid)
        
        # 获取第一页的微博
        for i, status in enumerate(statuses.page(1), 1):
            if i > count:
                break
            
            print(f"\n微博 {i}:")
            print(f"  ID: {status.id}")
            print(f"  内容: {status.text[:100]}..." if len(status.text) > 100 else f"  内容: {status.text}")
            print(f"  发布时间: {status.created_at}")
            print(f"  点赞数: {status.attitudes_count}")
            print(f"  评论数: {status.comments_count}")
            print(f"  转发数: {status.reposts_count}")
            
    except Exception as e:
        print(f"获取微博列表失败: {e}")


def get_user_articles(client, uid, count=3):
    """获取用户的文章列表"""
    print(f"\n{'='*50}")
    print(f"正在获取用户 {uid} 的最新 {count} 篇文章...")
    print(f"{'='*50}")
    
    try:
        articles = client.articles(uid)
        
        # 获取第一页的文章
        for i, article in enumerate(articles.page(1), 1):
            if i > count:
                break
            
            print(f"\n文章 {i}:")
            print(f"  ID: {article.id}")
            if hasattr(article, 'text'):
                print(f"  内容预览: {article.text[:100]}..." if len(article.text) > 100 else f"  内容: {article.text}")
            
    except Exception as e:
        print(f"获取文章列表失败: {e}")


def get_user_followers(client, uid, count=5):
    """获取用户的粉丝列表"""
    print(f"\n{'='*50}")
    print(f"正在获取用户 {uid} 的 {count} 个粉丝...")
    print(f"{'='*50}")
    
    try:
        followers = client.followers(uid)
        
        # 获取第一页的粉丝
        for i, fan in enumerate(followers.page(1), 1):
            if i > count:
                break
            
            print(f"\n粉丝 {i}:")
            print(f"  用户ID: {fan.id}")
            print(f"  昵称: {fan.name}")
            print(f"  简介: {fan.description[:50]}..." if fan.description and len(fan.description) > 50 else f"  简介: {fan.description}")
            
    except Exception as e:
        print(f"获取粉丝列表失败: {e}")


def get_user_follows(client, uid, count=5):
    """获取用户的关注列表"""
    print(f"\n{'='*50}")
    print(f"正在获取用户 {uid} 关注的 {count} 个用户...")
    print(f"{'='*50}")
    
    try:
        follows = client.follow(uid)
        
        # 获取第一页的关注用户
        for i, user in enumerate(follows.page(1), 1):
            if i > count:
                break
            
            print(f"\n关注用户 {i}:")
            print(f"  用户ID: {user.id}")
            print(f"  昵称: {user.name}")
            print(f"  简介: {user.description[:50]}..." if user.description and len(user.description) > 50 else f"  简介: {user.description}")
            
    except Exception as e:
        print(f"获取关注列表失败: {e}")


def get_status_detail(client, status_id):
    """获取微博详情"""
    print(f"\n{'='*50}")
    print(f"正在获取微博 {status_id} 的详细信息...")
    print(f"{'='*50}")
    
    try:
        status = client.status(status_id)
        
        print(f"微博ID: {status.id}")
        print(f"长文本内容: {status.longTextContent}")
        print(f"点赞数: {status.attitudes_count}")
        print(f"评论数: {status.comments_count}")
        print(f"转发数: {status.reposts_count}")
        
    except Exception as e:
        print(f"获取微博详情失败: {e}")


def main():
    """主函数 - 演示基本使用"""
    print("="*50)
    print("Weibo API 基本使用示例")
    print("="*50)
    
    # 创建客户端实例
    # 注意：由于微博的反爬虫机制，建议提供Cookie以正常访问
    # 获取Cookie方法请参见: HOW_TO_GET_COOKIE.md
    cookie = os.getenv('WEIBO_COOKIE')  # 从环境变量获取Cookie
    
    if not cookie:
        print("\n警告: 未设置 WEIBO_COOKIE 环境变量")
        print("由于微博的反爬虫机制，API 可能返回 432 错误")
        print("获取 Cookie 方法请参见: HOW_TO_GET_COOKIE.md\n")
    
    client = WeiboClient(cookie=cookie)
    
    # 示例用户ID（请替换为真实的用户ID）
    # 例如：可以使用某个明星或公众人物的微博ID
    uid = "1815418641"  # 请替换为真实的用户ID
    
    print(f"\n提示: 请将 uid 变量修改为真实的微博用户ID")
    print(f"当前使用的示例ID: {uid}")
    
    # 1. 获取用户信息
    user = get_user_info(client, uid)
    
    if user:
        # 2. 获取用户的微博列表
        get_user_statuses(client, uid, count=5)
        
        # 3. 获取用户的文章列表
        get_user_articles(client, uid, count=3)
        
        # 4. 获取用户的粉丝列表
        get_user_followers(client, uid, count=5)
        
        # 5. 获取用户的关注列表
        get_user_follows(client, uid, count=5)
    
    # 6. 获取指定微博详情（可选）
    # status_id = "4567890123456789"  # 请替换为真实的微博ID
    # get_status_detail(client, status_id)
    
    print(f"\n{'='*50}")
    print("示例执行完成！")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()

