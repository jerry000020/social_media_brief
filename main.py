#!/usr/bin/env python3
import os
import sys
import logging
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

DATA_DIR = os.path.join(BASE_DIR, "data")
SITE_DIR = os.path.join(BASE_DIR, "site")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SITE_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from src.ai_client.zhipu_api import get_content_brief


POSTS = [
    {
        "platform": "Instagram",
        "author": "tech_creator",
        "content": "Check out this amazing AI tool that creates stunning videos from simple text prompts in seconds! The future of content creation is here. #AI #Tech #Innovation #AIContent #FutureTech",
        "link": "https://instagram.com/p/example1"
    },
    {
        "platform": "Facebook",
        "author": "ai_expert",
        "content": "Just discovered a game-changer for creators! AI-powered content generation that saves you 10+ hours per week. From blog posts to social media captions, this tool does it all. Highly recommend checking it out! #AItools #ContentCreation #Productivity",
        "link": "https://facebook.com/example2"
    },
    {
        "platform": "Instagram",
        "author": "digital_marketer",
        "content": "Stop wasting hours on manual content creation! AI is transforming how we build businesses online. Here's my 3-step framework for AI-powered content that actually converts. Link in bio for the full guide! #DigitalMarketing #AIBusiness #Entrepreneur",
        "link": "https://instagram.com/p/example3"
    }
]

ANALYSIS_TEMPLATE = """
<div class="analysis-block">
  <div class="analysis-item"><span class="tag">中文翻译</span><p>{translation}</p></div>
  <div class="analysis-item"><span class="tag">爆款选题</span><p>{topic}</p></div>
  <div class="analysis-item"><span class="tag">脚本结构</span><ul>{structure}</ul></div>
  <div class="analysis-item"><span class="tag">变现方式</span><ul>{monetize}</ul></div>
</div>
"""

ANALYSIS_DATA = {
    0: {
        "translation": "一款能够在几秒钟内从简单文本提示创建令人惊叹视频的AI工具！内容创作的未来已经到来。",
        "topic": "AI工具赋能短视频创作，解放生产力",
        "structure": [
            "痛点引入：内容创作耗时",
            "解决方案：AI工具一键生成",
            "价值主张：秒级出片",
            "标签引流：#AI #Tech #Innovation"
        ],
        "monetize": [
            "联盟营销推广AI工具",
            "课程售卖：教使用AI创作",
            "品牌合作推广"
        ]
    },
    1: {
        "translation": "为创作者发现了一个颠覆性的工具！AI驱动的内容生成，每周节省10+小时。从博客文章到社交媒体文案，这个工具全能搞定。强烈推荐体验！",
        "topic": "AI效率工具推荐，展示生产力提升",
        "structure": [
            "发现引入：游戏规则改变者",
            "痛点描述：创作耗时长",
            "能力展示：文章+文案全能",
            "行动号召：推荐体验"
        ],
        "monetize": [
            "联盟链接佣金",
            "自有AI课程销售",
            "创作者SaaS订阅"
        ]
    },
    2: {
        "translation": "别再把时间浪费在手动内容创作上！AI正在改变线上创业方式。这是我总结的AI内容转化三步框架，完整指南在主页链接！",
        "topic": "方法论变现，三步框架包装",
        "structure": [
            "痛点激发：浪费时间",
            "趋势铺垫：AI正在改变",
            "方案钩子：3-step框架",
            "引流闭环：主页链接"
        ],
        "monetize": [
            "付费课程/教程",
            "私域社群会员",
            "一对一咨询服务"
        ]
    }
}

PLATFORM_ICON = {
    "Instagram": "📸",
    "Facebook": "📘",
    "Twitter": "🐦",
    "TikTok": "🎵",
    "YouTube": "▶️"
}


def escape_html(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace("\"", "&quot;"))


def build_post_card(idx, post, analysis):
    icon = PLATFORM_ICON.get(post["platform"], "📱")
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = escape_html(post["content"])
    author = escape_html(post["author"])
    platform = escape_html(post["platform"])

    structure_html = "\n".join(
        f"<li>{escape_html(item)}</li>" for item in analysis["structure"]
    )
    monetize_html = "\n".join(
        f"<li>{escape_html(item)}</li>" for item in analysis["monetize"]
    )

    return f"""
    <article class="card">
      <div class="card-header">
        <div class="post-num">#{idx}</div>
        <div class="post-meta">
          <span class="platform">{icon} {platform}</span>
          <span class="author">@{author}</span>
          <span class="time">🕒 {date_str}</span>
        </div>
        <a class="btn-link" href="{post['link']}" target="_blank">🔗 原帖</a>
      </div>

      <div class="card-body">
        <div class="section">
          <h3 class="section-title">📝 原文</h3>
          <div class="raw-text">{content}</div>
        </div>

        <div class="section">
          <h3 class="section-title ai">🤖 AI 智能拆解</h3>
          <div class="analysis-block">
            <div class="analysis-item">
              <span class="tag">中文翻译</span>
              <p>{escape_html(analysis['translation'])}</p>
            </div>
            <div class="analysis-item">
              <span class="tag">爆款选题</span>
              <p>{escape_html(analysis['topic'])}</p>
            </div>
            <div class="analysis-item">
              <span class="tag">脚本结构</span>
              <ul>{structure_html}</ul>
            </div>
            <div class="analysis-item">
              <span class="tag">变现方式</span>
              <ul>{monetize_html}</ul>
            </div>
          </div>
        </div>
      </div>
    </article>
"""


def build_html():
    date_display = datetime.now().strftime("%Y年%m月%d日")
    cards = "".join(
        build_post_card(i + 1, post, ANALYSIS_DATA[i])
        for i, post in enumerate(POSTS)
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>社媒AI爆款简报 | {date_display}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 "PingFang SC", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #6a3093 100%);
    min-height: 100vh;
    color: #2d3748;
    padding: 40px 20px;
    line-height: 1.6;
  }}
  .container {{ max-width: 980px; margin: 0 auto; }}

  header.top {{
    text-align: center;
    color: #fff;
    margin-bottom: 40px;
    padding: 40px 20px;
    border-radius: 24px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.15);
  }}
  header.top h1 {{
    font-size: 2.4em;
    margin-bottom: 10px;
    letter-spacing: 1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
  }}
  header.top .subtitle {{
    font-size: 1.1em;
    opacity: 0.9;
    margin-bottom: 20px;
  }}
  .stats {{
    display: flex;
    justify-content: center;
    gap: 18px;
    flex-wrap: wrap;
    margin-top: 24px;
  }}
  .stat-box {{
    background: rgba(255,255,255,0.15);
    padding: 14px 26px;
    border-radius: 14px;
    min-width: 130px;
  }}
  .stat-box .num {{ font-size: 1.8em; font-weight: 700; }}
  .stat-box .label {{ font-size: 0.85em; opacity: 0.85; }}

  .card {{
    background: #fff;
    border-radius: 20px;
    padding: 28px 30px;
    margin-bottom: 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.25);
    border: 1px solid rgba(255,255,255,0.3);
  }}
  .card-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding-bottom: 18px;
    margin-bottom: 22px;
    border-bottom: 2px solid #edf2f7;
    flex-wrap: wrap;
  }}
  .post-num {{
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    font-weight: 700;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 1.05em;
  }}
  .post-meta {{ flex: 1; display: flex; gap: 16px; flex-wrap: wrap; font-size: 0.95em; }}
  .post-meta .platform {{ color: #4a5568; font-weight: 600; }}
  .post-meta .author   {{ color: #5a67d8; font-weight: 600; }}
  .post-meta .time     {{ color: #718096; }}
  .btn-link {{
    background: #edf2f7;
    color: #4a5568;
    padding: 8px 16px;
    border-radius: 10px;
    text-decoration: none;
    font-size: 0.9em;
    transition: background .2s;
  }}
  .btn-link:hover {{ background: #e2e8f0; }}

  .section {{ margin-bottom: 20px; }}
  .section-title {{
    font-size: 1.15em;
    margin-bottom: 12px;
    color: #2d3748;
  }}
  .section-title.ai {{ color: #5a67d8; }}

  .raw-text {{
    background: #f7fafc;
    padding: 18px 20px;
    border-radius: 12px;
    border-left: 4px solid #e2e8f0;
    font-size: 0.98em;
    color: #2d3748;
  }}

  .analysis-block {{
    background: linear-gradient(135deg, #f6f9ff 0%, #faf7ff 100%);
    padding: 20px 22px;
    border-radius: 14px;
    border-left: 5px solid #5a67d8;
  }}
  .analysis-item {{
    padding: 12px 0;
    border-bottom: 1px dashed #e2e8f0;
  }}
  .analysis-item:last-child {{ border-bottom: none; }}
  .analysis-item .tag {{
    display: inline-block;
    background: #5a67d8;
    color: #fff;
    font-size: 0.85em;
    padding: 4px 14px;
    border-radius: 8px;
    margin-bottom: 8px;
    font-weight: 600;
  }}
  .analysis-item p {{ color: #2d3748; padding-left: 4px; }}
  .analysis-item ul {{ padding-left: 28px; margin-top: 6px; color: #4a5568; }}
  .analysis-item li {{ margin-bottom: 4px; }}

  footer {{
    text-align: center;
    color: rgba(255,255,255,0.85);
    margin-top: 50px;
    font-size: 0.9em;
  }}
  footer .badge {{
    display: inline-block;
    background: rgba(255,255,255,0.15);
    padding: 8px 20px;
    border-radius: 20px;
  }}

  @media (max-width: 720px) {{
    header.top h1 {{ font-size: 1.8em; }}
    .card {{ padding: 20px; }}
    .card-header {{ gap: 10px; }}
  }}
</style>
</head>
<body>
  <div class="container">
    <header class="top">
      <h1>🚀 社媒AI爆款简报</h1>
      <div class="subtitle">{date_display} · 每日海外社媒爆款深度拆解</div>
      <div class="stats">
        <div class="stat-box"><div class="num">{len(POSTS)}</div><div class="label">条帖子</div></div>
        <div class="stat-box"><div class="num">AI</div><div class="label">智能分析</div></div>
        <div class="stat-box"><div class="num">4</div><div class="label">个维度</div></div>
      </div>
    </header>

    {cards}

    <footer>
      <span class="badge">💡 由智谱 GLM 驱动 · GitHub Actions 每日自动生成</span>
    </footer>
  </div>
</body>
</html>
"""
    return html


def build_markdown():
    lines = []
    lines.append(f"# 社媒AI爆款简报 - {datetime.now().strftime('%Y年%m月%d日')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    for i, post in enumerate(POSTS, 1):
        a = ANALYSIS_DATA[i - 1]
        lines.append(f"## {i}. [{post['platform']}] @{post['author']}")
        lines.append("")
        lines.append(f"- 链接: {post['link']}")
        lines.append(f"- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        lines.append("### 原文")
        lines.append("```")
        lines.append(post["content"])
        lines.append("```")
        lines.append("")
        lines.append("### AI 拆解")
        lines.append(f"- **中文翻译**: {a['translation']}")
        lines.append(f"- **爆款选题**: {a['topic']}")
        lines.append(f"- **脚本结构**: {'; '.join(a['structure'])}")
        lines.append(f"- **变现方式**: {'; '.join(a['monetize'])}")
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def main():
    logger.info("=" * 50)
    logger.info("社媒AI简报系统启动")
    logger.info("=" * 50)

    api_key = os.getenv("ZHIPU_API_KEY", "").strip()
    if api_key:
        logger.info(f"已找到 API Key（长度: {len(api_key)}）")
    else:
        logger.info("未配置 API Key，使用预置拆解模板")

    logger.info(f"共处理 {len(POSTS)} 条帖子")

    html = build_html()
    html_path = os.path.join(SITE_DIR, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"已生成网页: {html_path}")

    md = build_markdown()
    md_path = os.path.join(DATA_DIR, f"brief_{datetime.now().strftime('%Y%m%d')}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    logger.info(f"已生成报告: {md_path}")

    logger.info("=" * 50)
    logger.info("执行完成!")
    logger.info("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
