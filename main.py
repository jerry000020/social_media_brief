#!/usr/bin/env python3
"""
项目主入口文件
执行完整流程：配置加载 -> 爬虫抓取 -> AI处理 -> 导出MD
"""
import logging
import os
import sys
from datetime import datetime

# 添加项目根路径到Python路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from config.settings import LOG_DIR, DATA_DIR, TARGET_URLS
from src.crawler.ins_spider import fetch_ins_posts
from src.crawler.fb_spider import fetch_fb_posts
from src.crawler.data_clean import clean_text, deduplicate_posts, filter_invalid_posts
from src.ai_client.zhipu_api import get_content_brief, test_api_connection
from src.exporter.md_writer import generate_markdown_report


def setup_logging():
    """配置日志系统"""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # 日志文件名按日期
    log_file = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """主执行函数"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("="*50)
    logger.info("社媒爬虫+智谱AI简报系统启动")
    logger.info("="*50)
    
    # 1. 测试API连接
    logger.info("\n--- 步骤1: 测试智谱API连接 ---")
    if not test_api_connection():
        logger.error("智谱API连接失败，程序退出")
        return 1
    
    # 2. 抓取数据
    logger.info("\n--- 步骤2: 抓取社媒数据 ---")
    all_posts = []
    
    # 抓取Instagram
    ins_posts = fetch_ins_posts(
        TARGET_URLS.get("instagram", []),
        delay_range=(2, 4)
    )
    all_posts.extend(ins_posts)
    
    # 抓取Facebook
    fb_posts = fetch_fb_posts(
        TARGET_URLS.get("facebook", []),
        delay_range=(3, 6)
    )
    all_posts.extend(fb_posts)
    
    if not all_posts:
        logger.warning("未抓取到任何帖子，程序退出")
        return 0
    
    # 3. 数据清洗
    logger.info("\n--- 步骤3: 数据清洗 ---")
    for post in all_posts:
        post["content"] = clean_text(post.get("content", ""))
    
    all_posts = filter_invalid_posts(all_posts)
    all_posts = deduplicate_posts(all_posts)
    
    # 4. AI处理
    logger.info("\n--- 步骤4: 调用智谱AI生成简报 ---")
    posts_with_brief = []
    
    for idx, post in enumerate(all_posts, 1):
        logger.info(f"正在处理第 {idx}/{len(all_posts)} 条帖子")
        
        content = post.get("content", "")
        brief = get_content_brief(content)
        
        if brief:
            post["brief"] = brief
            posts_with_brief.append(post)
        else:
            logger.warning(f"帖子 {idx} AI处理失败")
    
    # 5. 导出报告
    logger.info("\n--- 步骤5: 生成Markdown报告 ---")
    if posts_with_brief:
        report_path = generate_markdown_report(posts_with_brief, save_dir=DATA_DIR)
        logger.info(f"报告生成成功: {report_path}")
    else:
        logger.warning("没有成功处理的帖子，无法生成报告")
    
    logger.info("\n" + "="*50)
    logger.info("程序执行完成")
    logger.info("="*50)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
