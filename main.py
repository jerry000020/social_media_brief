#!/usr/bin/env python3
"""
项目主入口 - 网页端版
爬虫(模拟) -> AI处理 -> 导出MD + HTML网页
"""
import logging
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# 配置目录
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
SITE_DIR = os.path.join(BASE_DIR, "site")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SITE_DIR, exist_ok=True)

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


def escape_html(text):
    """简单的HTML转义"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def text_to_html(text):
    """把普通文本转成带换行的HTML"""
    lines = text.strip().split('\n')
    html_lines = []
    for line in lines:
        line = escape_html(line)
        # 处理标题
        if line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('- ') or line.startswith('* '):
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.strip() == '---':
            html_lines.append('<hr>')
        elif line.strip() == '':
            html_lines.append('<br>')
        else:
            html_lines.append(f'<p>{line}</p>')
    return '\n'.join(html_lines)


def generate_html(posts_with_brief):
    """生成美观的HTML网页"""
    date_str = datetime.now().strftime("%Y%m%d")
    date_display = datetime.now().strftime("%Y年%m月%d日")
    file_path = os.path.join(SITE_DIR, "index.html")

    posts_html = ""
    for idx, post in enumerate(posts_with_brief, 1):
        posts_html += f'''
        <div class="post-card">
            <div class="post-header">
                <span class="post-number">#{idx}</span>
                <span class="post-platform">{'📸' if post['platform'] == 'Instagram' else '📘'} {post['platform']}</span>
                <span class="post-author">@{post['author']}</span>
            </div>
            <div class="post-meta">
                <span>🕒 {post['publish_time']}</span>
                <a href="{post['link']}" target="_blank" class="post-link">🔗 查看原帖</a>
            </div>
            <div class="post-content">
                <div class="section-title">📝 原文</div>
                <div class="post-text">{escape_html(post['content'])}</div>
            </div>
            <div class="ai-section">
                <div class="section-title">🤖 AI 智能分析</div>
                <div class="ai-content">{text_to_html(post.get('brief', '解析失败'))}</div>
            </div>
        </div>
        '''

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>社媒AI简报 - {date_display}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #333;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        .header .date {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }}
        .stat-box {{
            background: rgba(255,255,255,0.2);
            padding: 15px 30px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
            color: white;
            text-align: center;
        }}
        .stat-box .number {{
            font-size: 2em;
            font-weight: bold;
        }}
        .stat-box .label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .post-card {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        }}
        .post-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
            flex-wrap: wrap;
        }}
        .post-number {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .post-platform {{
            background: #f0f0f0;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.95em;
        }}
        .post-author {{
            color: #667eea;
            font-weight: 600;
        }}
        .post-meta {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            color: #666;
            font-size: 0.9em;
            flex-wrap: wrap;
        }}
        .post-link {{
            color: #667eea;
            text-decoration: none;
        }}
        .post-link:hover {{
            text-decoration: underline;
        }}
        .section-title {{
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 12px;
            color: #333;
        }}
        .post-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        .post-text {{
            line-height: 1.8;
            color: #555;
        }}
        .ai-section {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%);
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }}
        .ai-content {{
            line-height: 1.8;
            color: #333;
        }}
        .ai-content h1, .ai-content h2, .ai-content h3 {{
            margin: 15px 0 10px 0;
            color: #333;
        }}
        .ai-content p {{
            margin-bottom: 10px;
        }}
        .ai-content li {{
            margin-left: 20px;
            margin-bottom: 5px;
        }}
        .ai-content hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 15px 0;
        }}
        .footer {{
            text-align: center;
            color: white;
            margin-top: 50px;
            opacity: 0.8;
            font-size: 0.9em;
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 20px 10px;
            }}
            .header h1 {{
                font-size: 1.8em;
            }}
            .post-card {{
                padding: 20px;
            }}
            .stats {{
                flex-direction: column;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 社媒AI简报</h1>
            <div class="date">{date_display}</div>
            <div class="stats">
                <div class="stat-box">
                    <div class="number">{len(posts_with_brief)}</div>
                    <div class="label">条帖子</div>
                </div>
                <div class="stat-box">
                    <div class="number">AI</div>
                    <div class="label">智能分析</div>
                </div>
            </div>
        </div>

        {posts_html}

        <div class="footer">
            <p>💡 由智谱AI驱动 · GitHub Actions 自动化生成</p>
        </div>
    </div>
</body>
</html>"""

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return file_path


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

    api_key = os.getenv("ZHIPU_API_KEY", "").strip()
    if not api_key:
        logger.error("❌ 错误: 未找到 ZHIPU_API_KEY 环境变量!")
        return 1
    logger.info(f"✅ API密钥已加载 (长度: {len(api_key)})")

    logger.info("\n--- 步骤1: 获取社媒数据 ---")
    posts = fetch_demo_posts()
    logger.info(f"✅ 获取到 {len(posts)} 条帖子")

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

    logger.info("\n--- 步骤3: 生成报告 ---")
    md_path = generate_markdown(posts_with_brief)
    logger.info(f"✅ Markdown报告: {md_path}")

    html_path = generate_html(posts_with_brief)
    logger.info(f"✅ HTML网页报告: {html_path}")

    logger.info("\n" + "="*50)
    logger.info("🎉 程序执行成功完成!")
    logger.info("="*50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
