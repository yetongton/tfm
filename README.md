# 中国城市新闻情感分析系统

这是一个基于Flask的Web应用，用于分析中国城市新闻的情感倾向，帮助了解各城市的媒体形象。

## 功能特点

- 城市情感得分排名与可视化
- 城市详细情感分析报告
- 用户注册与登录
- 新闻数据上传与分析
- 使用BERT深度学习模型进行情感分析

## 目录结构

```
CityNewsApp/
├── city_news_app.py        # 主应用程序
├── city_news.db            # SQLite数据库
├── run_app.bat             # 启动应用的批处理文件
├── static/                 # 静态资源文件
│   ├── css/                # CSS样式文件
│   └── js/                 # JavaScript文件
├── templates/              # HTML模板文件
├── uploads/                # 用户上传文件目录
├── jieguo/                 # 分析结果数据
└── news_sentiment_model/   # BERT情感分析模型
```

## 安装指南

1. 确保已安装Python 3.8或以上版本
2. 安装必要的Python库：
   ```
   pip install flask flask-login werkzeug pandas torch transformers
   ```
3. 确保BERT模型文件已正确放置在`news_sentiment_model`目录中

## 使用方法

1. 双击运行`run_app.bat`批处理文件启动应用
2. 在浏览器中访问`http://localhost:5000`
3. 注册账户并登录系统
4. 浏览城市情感分析结果或上传新闻数据进行分析

## 数据格式

上传的CSV文件需要包含以下至少一个字段：
- `title`: 新闻标题
- `content`: 新闻内容

## 注意事项

- 情感分析模型需要一定的计算资源，确保您的计算机有足够的内存
- 上传的文件大小限制为16MB
- 默认情况下，会过滤掉新闻数量少于5条的城市和情感得分为100的城市 