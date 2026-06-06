"""
Markdown文档导出模块
将AI生成的简报保存为MD文件
"""
import logging
import os
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


def generate_markdown_report(posts_with_brief: List[Dict], save_dir: str = "data") -> str:
    """
    生成Markdown简报文件
    Args:
        posts_with_brief: 包含AI简报的帖子列表
        save_dir: 保存目录
    Returns:
        生成的文件路径
    """
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 按日期命名文件
    date_str = datetime.now().strftime("%Y%m%d")
    file_path = os.path.join(save_dir, f"brief_{date_str}.md")
    
    # 构建Markdown内容
    md_content = []
    md_content.append(f"# 社媒每日简报 - {datetime.now().strftime('%Y年%m月%d日')}")
    md_content.append("")
    md_content.append("---")
    md_content.append("")
    
    for idx, post in enumerate(posts_with_brief, 1):
        md_content.append(f"## {idx}. {post.get('platform', '未知平台')} - {post.get('author', '未知博主')}")
        md_content.append("")
        md_content.append(f"- **发布时间**: {post.get('publish_time', '未知')}")
        md_content.append(f"- **帖子链接**: {post.get('link', '#')}")
        md_content.append("")
        md_content.append("### 原文")
        md_content.append("```")
        md_content.append(post.get('content', ''))
        md_content.append("```")
        md_content.append("")
        md_content.append("### AI解析")
        md_content.append("")
        md_content.append(post.get('brief', '解析失败'))
        md_content.append("")
        md_content.append("---")
        md_content.append("")
    
    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    
    logger.info(f"Markdown简报已保存: {file_path}")
    return file_path
