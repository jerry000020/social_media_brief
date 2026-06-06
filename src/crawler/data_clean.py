"""
数据清洗模块
负责文本去空格、去无效符号、内容去重
"""
import logging
import re
from typing import List, Dict

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    清洗文本内容
    Args:
        text: 原始文本
    Returns:
        清洗后的文本
    """
    if not text:
        return ""
    
    # 去除多余空格和换行
    cleaned = re.sub(r'\s+', ' ', text.strip())
    
    # 去除无效符号（保留基本标点）
    cleaned = re.sub(r'[^\w\s.,!?\'";:()-]', '', cleaned)
    
    return cleaned


def deduplicate_posts(posts: List[Dict]) -> List[Dict]:
    """
    去重帖子列表
    依据：帖子链接或内容哈希
    Args:
        posts: 原始帖子列表
    Returns:
        去重后的帖子列表
    """
    seen = set()
    unique_posts = []
    
    for post in posts:
        # 使用链接作为去重键
        key = post.get('link', '')
        if not key:
            # 没有链接时使用内容哈希
            key = hash(post.get('content', ''))
        
        if key not in seen:
            seen.add(key)
            unique_posts.append(post)
    
    logger.info(f"帖子去重完成，剩余 {len(unique_posts)} 条")
    return unique_posts


def filter_invalid_posts(posts: List[Dict]) -> List[Dict]:
    """
    过滤无效帖子（无内容或无链接）
    Args:
        posts: 帖子列表
    Returns:
        有效帖子列表
    """
    valid = []
    for post in posts:
        content = post.get('content', '').strip()
        link = post.get('link', '').strip()
        
        if content or link:
            valid.append(post)
    
    logger.info(f"过滤无效帖子，剩余 {len(valid)} 条")
    return valid
