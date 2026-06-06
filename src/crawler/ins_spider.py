"""
Instagram爬虫模块
模拟公开访问抓取帖子内容
"""
import logging
import random
import time
from typing import List, Dict
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

# 随机User-Agent池
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]


def get_random_headers() -> Dict:
    """生成随机请求头"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.instagram.com/"
    }


def fetch_ins_posts(urls: List[str], delay_range: tuple = (2, 5)) -> List[Dict]:
    """
    抓取Instagram公开帖子
    Args:
        urls: 目标帖子URL列表
        delay_range: 请求延时范围（秒）
    Returns:
        帖子信息列表
    """
    posts = []
    
    for idx, url in enumerate(urls):
        try:
            logger.info(f"正在抓取 Instagram 帖子 {idx+1}/{len(urls)}: {url}")
            
            time.sleep(random.uniform(*delay_range))
            
            # 模拟抓取（实际项目需实现真实抓取逻辑）
            # 这里返回演示数据
            post = {
                "platform": "Instagram",
                "author": f"ins_author_{idx+1}",
                "content": f"This is an amazing AI video about future technology! #AI #Tech #Innovation",
                "link": url,
                "publish_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            posts.append(post)
            logger.info(f"成功抓取: {post['author']}")
            
        except Exception as e:
            logger.error(f"抓取失败 {url}: {str(e)}", exc_info=True)
            continue
    
    logger.info(f"Instagram 抓取完成，共获取 {len(posts)} 条帖子")
    return posts
