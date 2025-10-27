#!/usr/bin/env python
"""
关注网络爬取示例

这个示例展示如何递归获取用户的关注网络：
1. 从一个起始用户开始
2. 获取他关注的人（第1层）
3. 获取第1层用户关注的人（第2层）
4. 获取第2层用户关注的人（第3层）
5. 将所有用户信息保存到 JSONL 文件

注意：此操作可能需要较长时间，请合理控制请求频率
"""
import sys
import os
import json
import time
import random
from collections import deque

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weibo_api_sdk import WeiboClient
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def parse_followers_count(followers_str):
    """
    解析粉丝数字符串，转换为整数
    
    :param followers_str: 粉丝数字符串，如 "262.6万", "1234", "1.2万"
    :return: 粉丝数（整数）
    """
    if not followers_str:
        return 0
    
    # 转换为字符串
    followers_str = str(followers_str)
    
    # 如果已经是数字，直接返回
    if followers_str.isdigit():
        return int(followers_str)
    
    # 处理中文数字
    if '万' in followers_str:
        # 提取数字部分
        num_str = followers_str.replace('万', '')
        try:
            num = float(num_str)
            return int(num * 10000)
        except ValueError:
            return 0
    elif '千' in followers_str:
        # 提取数字部分
        num_str = followers_str.replace('千', '')
        try:
            num = float(num_str)
            return int(num * 1000)
        except ValueError:
            return 0
    elif '亿' in followers_str:
        # 提取数字部分
        num_str = followers_str.replace('亿', '')
        try:
            num = float(num_str)
            return int(num * 100000000)
        except ValueError:
            return 0
    else:
        # 尝试直接转换
        try:
            return int(float(followers_str))
        except ValueError:
            return 0


def get_user_info(people):
    """
    提取用户关键信息
    
    :param people: People 对象
    :return: 用户信息字典
    """
    try:
        # 解析粉丝数
        followers_count = parse_followers_count(people.followers_count)
        follow_count = parse_followers_count(people.follow_count)
        
        return {
            'id': people.id,
            'name': people.name,
            'description': people.description or '',
            'gender': people.gender,
            'avatar': people.avatar,
            'followers_count': followers_count,
            'follow_count': follow_count,
        }
    except Exception as e:
        print(f"  ⚠️  获取用户信息失败: {e}")
        return None


def get_follows_list_with_retry(client, uid, max_pages=10, min_followers=1000, max_retries=3):
    """
    获取用户的关注列表（带重试机制）
    
    :param client: WeiboClient 实例
    :param uid: 用户ID
    :param max_pages: 最多获取多少页（每页20个）
    :param min_followers: 最小粉丝数过滤
    :param max_retries: 最大重试次数
    :return: 关注的用户ID列表
    """
    for attempt in range(max_retries):
        try:
            print(f"    🔄 尝试获取关注列表 (第 {attempt + 1} 次)...")
            
            people = client.people(uid)
            follows = people.follows
            
            follow_ids = []
            
            # 限制获取页数，避免请求过多
            total_pages = min(max_pages, 10)  # API 限制最多10页
            
            for page_num in range(1, total_pages + 1):
                try:
                    # 添加随机延迟，避免被检测
                    delay = random.uniform(1.0, 3.0)
                    time.sleep(delay)
                    
                    print(f"      📄 获取第 {page_num} 页...")
                    current_page_follows = []
                    for follow in follows.page(page_num):
                        follow_info = get_user_info(follow)
                        if follow_info:
                            if follow_info['followers_count'] >= min_followers:
                                follow_ids.append(follow_info)
                                current_page_follows.append(follow_info)
                            else:
                                print(f"        ⏭️  跳过低质量用户: {follow_info['name']} (粉丝: {follow_info['followers_count']:,}), {follow_info}")
                    
                    print(f"      ✅ 第 {page_num} 页获取成功，找到 {len(current_page_follows)} 个用户, top3: {current_page_follows[:3]}, total: {len(follow_ids)}")
                    
                except Exception as e:
                    print(f"      ⚠️  获取第 {page_num} 页失败: {e}")
                    if "Only dict and list can be StreamingJSON" in str(e):
                        print(f"      🚫 检测到反爬虫限制，等待更长时间...")
                        time.sleep(random.uniform(5, 10))
                    break
            
            if follow_ids:
                print(f"    ✅ 成功获取 {len(follow_ids)} 个关注用户，top3: {follow_ids[:3]}")
                return follow_ids
            else:
                print(f"    ⚠️  未获取到任何用户，尝试重试...")
                if attempt < max_retries - 1:
                    wait_time = random.uniform(10, 20)
                    print(f"    ⏳ 等待 {wait_time:.1f} 秒后重试...")
                    time.sleep(wait_time)
        
        except Exception as e:
            print(f"    ❌ 第 {attempt + 1} 次尝试失败: {e}")
            if attempt < max_retries - 1:
                wait_time = random.uniform(15, 30)
                print(f"    ⏳ 等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
    
    print(f"    ❌ 获取用户 {uid} 的关注列表失败，已重试 {max_retries} 次")
    return []


def save_users_to_file(users, output_file):
    """
    保存用户数据到文件
    
    :param users: 用户列表
    :param output_file: 输出文件名
    """
    with open(output_file, 'a+', encoding='utf-8') as f:
        for user in users:
            # 移除 depth 字段（仅用于统计）
            user_copy = user.copy()
            user_copy.pop('depth', None)
            f.write(json.dumps(user_copy, ensure_ascii=False) + '\n')


def crawl_follow_network(start_uid, max_depth=3, output_file='follow_network.jsonl'):
    """
    爬取关注网络
    
    :param start_uid: 起始用户ID
    :param max_depth: 爬取深度（层数）
    :param output_file: 输出文件名
    """
    # 获取 Cookie
    cookie = os.getenv('WEIBO_COOKIE')
    if not cookie:
        print("❌ 错误：未找到 WEIBO_COOKIE 环境变量")
        print("请先配置 .env 文件，参考 .env.example")
        return
    
    # 创建客户端
    client = WeiboClient(cookie=cookie)
    
    print(f"\n{'='*60}")
    print(f"🚀 开始爬取关注网络")
    print(f"{'='*60}")
    print(f"起始用户ID: {start_uid}")
    print(f"爬取深度: {max_depth} 层")
    print(f"输出文件: {output_file}")
    print(f"{'='*60}\n")
    
    # 使用集合记录已访问的用户ID，避免重复
    visited_ids = set()
    
    # 使用队列进行广度优先搜索
    # 队列元素格式：(uid, depth)
    queue = deque([(start_uid, 0)])
    
    # 统计信息
    stats = {
        'total_users': 0,
        'depth_0': 0,  # 起始用户
        'depth_1': 0,  # 第1层
        'depth_2': 0,  # 第2层
        'depth_3': 0,  # 第3层
    }
    
    while queue:
        current_uid, current_depth = queue.popleft()
        
        # 检查是否已访问
        if current_uid in visited_ids:
            continue
        
        # 检查深度
        if current_depth > max_depth:
            continue
        
        # 标记为已访问
        visited_ids.add(current_uid)
        
        # 获取当前用户信息
        print(f"\n📍 层级 {current_depth} | 正在处理用户 {current_uid}...")
        
        try:
            # 添加随机延迟，避免被检测
            delay = random.uniform(0.5, 2.0)
            time.sleep(delay)
            
            people = client.people(current_uid)
            user_info = get_user_info(people)
            
            if user_info:
                user_info['depth'] = current_depth  # 记录层级
                stats['total_users'] += 1
                stats[f'depth_{current_depth}'] += 1
                
                print(f"  ✅ 用户: {user_info['name']}")
                print(f"     简介: {user_info['description'][:50]}...")
                print(f"     粉丝: {user_info['followers_count']:,} | 关注: {user_info['follow_count']:,}")
                
                # 保存当前用户信息到文件
                save_users_to_file([user_info], output_file)
            
            # 如果还没到最大深度，获取他的关注列表
            if current_depth < max_depth:
                print(f"  🔍 获取关注列表...")
                
                # 根据深度调整获取页数（方案2：减少每层页数）
                # 第0层（起始用户）：获取5页
                # 第1层：获取2页
                # 第2层：获取1页
                max_pages = {0: 5, 1: 2, 2: 1}.get(current_depth, 1)
                
                follows = get_follows_list_with_retry(client, current_uid, max_pages=max_pages, min_followers=1000)
                print(f"  📊 找到 {len(follows)} 个关注用户，保存到文件：{output_file}")
                save_users_to_file(follows, output_file)
                
                # 将关注的用户加入队列（但不立即标记为已访问）
                for follow_info in follows:
                    follow_uid = follow_info['id']
                    # 只有未访问的用户才加入队列
                    if follow_uid not in visited_ids:
                        queue.append((follow_uid, current_depth + 1))
            
            # 添加随机延迟，避免请求过快
            delay = random.uniform(2, 5)
            time.sleep(delay)
            
        except Exception as e:
            print(f"  ❌ 处理用户 {current_uid} 时出错: {e}")
            continue
    
    # 数据已在获取过程中实时保存，无需最终保存
    print(f"\n{'='*60}")
    print(f"✅ 数据已实时保存到: {output_file}")
    print(f"{'='*60}\n")
    
    # 打印统计信息
    print(f"\n{'='*60}")
    print(f"📊 统计信息")
    print(f"{'='*60}")
    print(f"总用户数: {stats['total_users']}")
    print(f"  - 层级 0 (起始用户): {stats['depth_0']}")
    print(f"  - 层级 1 (第1层关注): {stats['depth_1']}")
    print(f"  - 层级 2 (第2层关注): {stats['depth_2']}")
    print(f"  - 层级 3 (第3层关注): {stats['depth_3']}")
    
    # 统计实际保存到文件的用户数
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            file_user_count = sum(1 for line in f if line.strip())
        print(f"实际保存到文件的用户数: {file_user_count}")
    except FileNotFoundError:
        print(f"文件 {output_file} 不存在")
    except Exception as e:
        print(f"读取文件统计失败: {e}")
    
    print(f"{'='*60}\n")
    
    # 读取并显示前几条数据
    print("📄 文件预览（前5条）：\n")
    with open(output_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            data = json.loads(line)
            print(f"{i+1}. {data['name']} (ID: {data['id']})")
            print(f"   简介: {data['description'][:50]}...")
            print(f"   粉丝: {data['followers_count']} | 关注: {data['follow_count']}\n")


def main():
    """主函数"""
    # 起始用户ID
    start_uid = "1815418641"
    
    # 输出文件
    output_file = "follow_network.jsonl"
    
    print("\n" + "="*60)
    print("📱 微博关注网络爬取工具")
    print("="*60)
    print("\n⚠️  注意事项：")
    print("1. 此操作可能需要较长时间（30-60分钟）")
    print("2. 请确保已配置 WEIBO_COOKIE")
    print("3. 会自动添加延迟以避免请求过快")
    print("4. 建议在网络良好的环境下运行")
    print("5. 如遇到错误会自动跳过并继续")
    print("6. 实时保存用户数据，防止数据丢失")
    print("7. 内置重试机制和反爬虫检测")
    print("\n" + "="*60)
    
    # 开始爬取
    try:
        crawl_follow_network(
            start_uid=start_uid,
            max_depth=3,
            output_file=output_file
        )
        
        print("\n✅ 爬取完成！")
        print(f"📁 数据已保存到: {output_file}")
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断，正在保存已获取的数据...")
        print("✅ 部分数据已保存")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

