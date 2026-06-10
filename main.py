#!/usr/bin/env python3
"""
项目主入口 - 极简版
爬虫(模拟) -> AI处理 -> 导出MD
"""
import logging
import os
import sys
from datetime import datetime

# 添加项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# 配置日志
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 导入模块
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from src.ai_client.zhipu_api import get_content_brief


def fetch_demo_posts():
    """获取示例社媒帖子数据"""
    return [
        {
            "platform": "Instagram",
            "author": "tech_creator",
            "content": "Check out this amazing AI tool that creates stunning videos from simple text prompts in seconds! The future of content creation is here. #AI #Tech #Innovation #AIContent #FutureTech",
            "link": "https://instagram.com/p/example1",
            "publish_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        {
            "platform": "Facebook",
            "author": "ai_expert",
            "content": "Just discovered a game-changer for creators! AI-powered content generation that saves you 10+ hours per week. From blog posts to social media captions, this tool does it all. Highly recommend checking it out! #AItools #ContentCreation #Productivity",
            "link": "https://facebook.com/example2",
            "publish_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        {
            "platform": "Instagram",
            "author": "digital_marketer",
            "content": "Stop wasting hours on manual content creation! AI is transforming how we build businesses online. Here's my 3-step framework for AI-powered content that actually converts. Link in bio for the full guide! #DigitalMarketing #AIBusiness #Entrepreneur",
            "link": "https://instagram.com/p/example3",
            "publish_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]


def generate_markdown(posts_with_brief):
    """生成Markdown报告"""
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join(DATA_DIR, f"brief_{date_str}.md")
    
    lines = []
    lines.append(f"# 社媒每日简报 - {datetime.now().strftime('%Y年%m月%d日')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for idx, post in enumerate(posts_with_brief, 1):
        lines.append(f"## {idx}. [{post['platform']}] {post['author']}")
        lines.append("")
        lines.append(f"- **发布时间**: {post['publish_time']}")
        lines.append(f"- **链接**: {post['link']}")
        lines.append("")
        lines.append("### 原文")
        lines.append("```")
        lines.append(post['content'])
        lines.append("```")
        lines.append("")
        lines.append("### AI 解析")
        lines.append("")
        lines.append(post.get('brief', '解析失败'))
        lines.append("")
        lines.append("---")
        lines.append("")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return file_path


def main():
    """主执行函数"""
    logger.info("="*50)
    logger.info("🚀 社媒AI简报系统启动")
    logger.info("="*50)

    # 检查API密钥
    api_key = os.getenv("ZHIPU_API_KEY", "").strip()
    if not api_key:
        logger.error("❌ 错误: 未找到 ZHIPU_API_KEY 环境变量!")
        logger.error("请在 GitHub Settings -> Secrets 中配置 ZHIPU_API_KEY")
        return 1
    logger.info(f"✅ API密钥已加载 (长度: {len(api_key)})")

    # 1. 获取数据
    logger.info("\n--- 步骤1: 获取社媒数据 ---")
    posts = fetch_demo_posts()
    logger.info(f"✅ 获取到 {len(posts)} 条帖子")

    # 2. AI处理
    logger.info("\n--- 步骤2: AI智能分析 ---")
    posts_with_brief = []
    
    for idx, post in enumerate(posts, 1):
        logger.info(f"  正在处理 {idx}/{len(posts)} ...")
        brief = get_content_brief(post['content'])
        if brief:
            post['brief'] = brief
            posts_with_brief.append(post)
            logger.info(f"  ✅ 第{idx}条处理成功")
        else:
            logger.warning(f"  ⚠️ 第{idx}条AI处理失败")

    if not posts_with_brief:
        logger.error("❌ 没有帖子被成功处理!")
        return 1
    logger.info(f"✅ 成功处理 {len(posts_with_brief)}/{len(posts)} 条")

    # 3. 生成报告
    logger.info("\n--- 步骤3: 生成报告 ---")
    report_path = generate_markdown(posts_with_brief)
    logger.info(f"✅ 报告已保存: {report_path}")

    logger.info("\n" + "="*50)
    logger.info("🎉 程序执行成功完成!")
    logger.info("="*50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
