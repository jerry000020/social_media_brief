# social_media_brief

社媒爬虫+智谱AI简报生成系统，支持本地运行和GitHub Actions自动调度。

## 项目结构

```
social_media_brief/
├── .github/workflows/ci.yml  # GitHub Actions自动配置
├── src/
│   ├── crawler/              # 爬虫模块
│   │   ├── ins_spider.py     # Instagram爬虫
│   │   ├── fb_spider.py      # Facebook爬虫
│   │   └── data_clean.py     # 数据清洗
│   ├── ai_client/            # 智谱API模块
│   │   └── zhipu_api.py      # 核心AI调用
│   └── exporter/             # 导出模块
│       └── md_writer.py      # Markdown导出
├── config/settings.py        # 全局配置
├── data/                     # 简报数据（.gitignore）
├── logs/                     # 运行日志（.gitignore）
├── tests/                    # 测试模块
├── main.py                   # 主入口
├── requirements.txt          # 依赖
└── README.md
```

## 本地部署步骤

1. **克隆代码**
   ```bash
   git clone <你的仓库地址>
   cd social_media_brief
   ```

2. **配置.env文件**
   在项目根目录创建`.env`文件，填入智谱API密钥：
   ```
   ZHIPU_API_KEY=de0b3b4bcc0c4c498da4321a3f882e46.E2ptff8dWgzX5odW
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行程序**
   ```bash
   python main.py
   ```

## GitHub仓库后台配置

1. 进入你的仓库 → **Settings**
2. 左侧菜单 → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. Name: `ZHIPU_API_KEY`
5. Value: 填入你的智谱API密钥
6. 点击 **Add secret**

## GitHub Actions自动运行

- **定时运行**: 每日北京时间凌晨3点自动抓取并生成简报
- **Push触发**: 向main分支push代码时自动运行测试
- **手动触发**: 在仓库Actions页面可手动启动工作流
- **产物保留**: 生成的简报会作为Artifact保留30天

## 部门成员协作规范

1. **Fork仓库**: 从主仓库Fork到自己账号
2. **开发分支**: 每个功能新建独立分支
3. **提交PR**: 完成后提交Pull Request到主仓库
4. **查看简报**: 在Actions → Artifacts中下载每日生成的简报

## 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行指定测试
pytest tests/test_zhipu.py -v
pytest tests/test_spider.py -v
```

## 注意事项

- 爬虫模块目前返回模拟数据，实际使用需完善真实抓取逻辑
- 智谱API密钥不要提交到Git（已配置.gitignore）
- 遵守目标平台的robots.txt和使用条款
