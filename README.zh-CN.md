# Tap4 AI Crawler

这是一个由[Tap4 AI工具导航站](https://tap4.ai)开源的AI 网页抓取项目。我们的目标是让大家很容易在工具导航站的基础上提供自动化抓取网站的能力。本项目基于Python，非常轻量级，维护简单，适合对AI导航站感兴趣的个人开发者，也适合对Python有兴趣的学习者，
欢迎大家fork和star。

[English](./README.md) | 简体中文

## 感谢关注链接

欢迎关注我们的Twitter: https://x.com/tap4ai

如果觉得项目对你有帮助，欢迎请我喝杯咖啡：

<a href="https://www.buymeacoffee.com/tap4ai0o" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

如果你对项目有兴趣，欢迎扫描二维码加微信群沟通： ![tap4-ai-wx-group](./images/640.jpg)

## 功能

- 支持抓取指定网站的标题、描述、网站介绍
- 支持生成指定网站的截图
- 支持使用llama3工具（Groq）对网站介绍进行处理，生成Markdown描述
- 支持快速配置
- 快速发布

![tai4-ai](./images/tap4ai.zh-CN.png)

## 快速开始
- 在Zeabur[注册账号](<https://zeabur.com?referralCode=leoli202303>)
- 在Zeabur新建项目、服务

### （1）在Zeabur基于镜像模式的快速部署
**点击Deploy Button，根据指引填写环境变量即可**<br>
[![Quickly Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/89NZ05)
### （2）在Zeabur基于代码模式的部署
在Zeabur选择Fork后的Github仓库部署，并在Zeabur配置环境变量，或者手动修改代码仓库的`.env` 文件，环境变量如下：
- `GROQ_API_KEY`: Groq的key，申请[Groq key](https://console.groq.com/keys)
- `S3_ENDPOINT_URL`: S3的endpoint，申请[Cloudflare R2](https://www.cloudflare.com/zh-cn/developer-platform/r2/)
- `S3_BUCKET_NAME`: S3的bucket name
- `S3_ACCESS_KEY_ID`: S3的access key id
- `S3_SECRET_ACCESS_KEY`: S3的secret access key
- `S3_CUSTOM_DOMAIN`: S3的custom domain，若有自定义域名，则填入，否则可不填写

## 本地运行

### 安装

- python3.x版本

### 设置

#### (1) 克隆此项目

```sh
git clone https://github.com/6677-ai/tap4-ai-crawler.git
```

#### (2) 在groq申请llama3的key

[申请Groq key](https://console.groq.com/keys)

#### (3) 申请S3对象存储的信息

- Endpoint
- Accese Key Id
- Secret Access Key
- Bucket Name

#### (4) 设置环境变量

- 修改根目录的 `.env` 文件，修改以下内容，例子如下：

```sh
## LLM Configuration: 大模型相关配置
GROQ_API_KEY=gsk_********

## Object Storage Configuration: 存储相关配置
R2_ENDPOINT_URL=https://*****.r2.cloudflarestorage.com
R2_BUCKET_NAME=tap4ai
R2_ACCESS_KEY_ID=****
R2_SECRET_ACCESS_KEY=****
R2_CUSTOM_DOMAIN=****
```

#### (5) 本地运行

install python依赖

```sh
pip install requirements.txt
```

运行

```sh
python main_api.py
```

运行后则会暴露一个RestAPI，访问URL后缀：/site/crawl

## 如何请求API

使用curl 验证API

```sh
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://tap4.ai","tags": ["website","navigation", "search","picture","photo"]}' http://127.0.0.1:8040/site/crawl
```

## 产品链接

### TAP4-AI-Directory

全球AI工具收藏。收集免费的ChatGPT镜像、替代品、提示、其他AI工具等等。欲知更多详情，请访问: [Tap4 AI](https://tap4.ai)

### How to get your first users for startup at the website list

以下是提交产品以获取用户的网站列表。请访问
[StartUp Your Product List](https://github.com/6677-ai/TAP4-AI-Directory/blob/main/Startup-Your-Product-List.md)

### GPT-4o in OpenAI

2024年5月14日发布的令人惊叹的新功能。GPT-4o即将推出，让我们与她聊天吧。请访问：
[GPT-4o](https://openai.com/index/hello-gpt-4o/)

### The Tattoo AI Generator and Design

Tattao AI Design是为纹身爱好者设计的纹身AI生成器和设计工具。如果你对此感兴趣，请访问：
[Tattoo AI Design](https://tattooai.design)

### Anime Girl Studio -- AI Anime Girl Chat & Generator

Anime Girl Studio是一个AI动漫女孩生成器和聊天产品。您可以生成您喜欢的内容并与AI动漫女孩聊天，请访问： [Anime Girl Studio](https://animegirl.studio)

### Best AI Girl Friend -- Best AI Girl Chat & Generator

最佳AI女友是一个AI女孩生成器和聊天产品。您可以生成您喜欢的内容并与AI动漫女孩聊天，请访问： [Best AI Girl Friend](https://aigirl.best)

## LICENSE

MIT
