# Tap4 AI Crawler

Tap4 AI Crawler 是由 [tap4.ai](https://tap4.ai) 开发的开源爬虫，它将网站 Url 转换为使用 LLM 总结的网站信息。包括强大的抓取、爬取和数据提取功能，以及网页截图功能。使用 Tap4 AI Crawler，您不仅可以轻松更新 AI 工具目录中的 AI 工具详细信息，还可以生成网站摘要。

该项目基于 Python，非常轻量级，易于维护，适合对 AI 工具目录感兴趣的个人开发者，也适合对 Python 感兴趣的学习者。我们欢迎大家 fork 和 star。

简体中文 | [English](./README.md)

# 请在 Product Hunt 支持下 Tap4 AI

<a href="https://www.producthunt.com/posts/ai-tools-directory-by-tap4-ai?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-ai&#0045;tools&#0045;directory&#0045;by&#0045;tap4&#0045;ai" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=464357&theme=light" alt="AI&#0032;Tools&#0032;Directory&#0032;by&#0032;Tap4&#0032;AI - Open&#0045;source&#0032;AI&#0032;navigation&#0032;&#0038;&#0032;discovery&#0032;with&#0032;multi&#0045;language | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

## 特征

- 获取输入网站的标题、描述和介绍
- 对输入网站进行截图
- 支持使用 LLM（llama3/chatgpt）处理网站介绍并生成 SEO 友好的 Markdown 描述
- 快速配置
- 快速部署

![tai4-ai](./images/tap4-ai.png)

## 感谢关注链接

欢迎关注我们的 Twitter: https://x.com/tap4ai

如果觉得项目对你有帮助，欢迎请我喝杯咖啡：

<a href="https://www.buymeacoffee.com/tap4ai0o" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

如果你对项目有兴趣，欢迎添加我微信: helloleo2023, 备注: "tap4 ai 开源"，也可以扫描二维码:
![tap4-ai-wx](./images/tap4-ai-wechat.jpg)

## 快速开始

- [在 Cloudflare 上注册](https://www.cloudflare.com?utm_source=tap4ai)
- 选择 R2 服务并创建一个用于图像存储的存储桶，设置为公共访问（可选：设置自定义域名）并编辑 CORS 策略。
  ![Create-cloudflare-R2](./images/cloudflare-r2.png)
- CORS 策略如下：

```sh
[
  {
    "AllowedOrigins": [
      "*"
    ],
    "AllowedMethods": [
      "GET",
      "POST",
      "PUT",
      "DELETE",
      "HEAD"
    ],
    "AllowedHeaders": [
      "*"
    ]
  }
]
```

- 为 R2 API 创建 R2 API Token，并选择具有对象读写权限的权限。保存您的参数：ENDPOINT_URL、BUCKET_NAME、ACCESS_KEY_ID、SECRET_ACCESS_KEY、CUSTOM_DOMAIN。这些参数将在.tap4-ai-crawler 的.env 文件中配置。
  ![Create-R2-API-Token](./images/Create-R2-API-Token.png)

  ![Cloudflare-R2-Token](./images/Cloudflare-R2-Token.png)

### 在 Zeabur 基于代码模式的部署

在 Zeabur 选择 Fork 后的 Github 仓库部署，并在 Zeabur 配置环境变量，或者手动修改代码仓库的`.env` 文件，环境变量如下：

- `GROQ_API_KEY`: Groq 的 key，申请[Groq key](https://console.groq.com/keys)
- `S3_ENDPOINT_URL`: S3 的 endpoint，申请[Cloudflare R2](https://www.cloudflare.com/zh-cn/developer-platform/r2/)
- `S3_BUCKET_NAME`: S3 的 bucket name
- `S3_ACCESS_KEY_ID`: S3 的 access key id
- `S3_SECRET_ACCESS_KEY`: S3 的 secret access key
- `S3_CUSTOM_DOMAIN`: S3 的 custom domain，若有自定义域名，则填入，否则可不填写
- `AUTH_SECRET`: 自定义的对外 REST API 需要的 KEY

**注：爬虫对服务器配置有一定的要求，建议 Zeabur 购买付费服务，优先选择美国节点**

## 本地运行

### 安装

- python3.x 版本

### 设置

#### (1) 克隆此项目

```sh
git clone https://github.com/6677-ai/tap4-ai-crawler.git
```

#### (2) 在 groq 申请 llama3 的 key

[申请 Groq key](https://console.groq.com/keys)

#### (3) 申请 S3 对象存储的信息

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
S3_ENDPOINT_URL=https://*****.r2.cloudflarestorage.com
S3_BUCKET_NAME=tap4ai
S3_ACCESS_KEY_ID=****
S3_SECRET_ACCESS_KEY=****
S3_CUSTOM_DOMAIN=****
AUTH_SECRET=****
```

#### (5) 本地运行

install python 依赖

```sh
pip install -r requirements.txt
```

运行

```sh
python main_api.py
```

运行后则会暴露一个 RestAPI，访问 URL 后缀：/site/crawl

## 如何请求 API

可以使用 curl 发送 Post 请求验证 API 是否可用。
请求参数说明:

- 格式: Json format,
- 参数: url (例如: https://tap4.ai)

请求示例如下:

```sh
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer xxxxx" -d '{"url": "https://tap4.ai", "tags": [ "selected tags: ai-detector","chatbot","text-writing","image","code-it"]}' http://127.0.0.1:8040/site/crawl
```

返回参数:

- 格式: Json
- 参数: data-description: 网站描述
- 参数: data-detail: 网站具体介绍
- 参数: data-screenshot_data: 网站截图
- 参数: data-screenshot_thumbnail_data:网站截图缩略图，0.5 倍分辨率
- 参数: data-title: 网站标题

```sh
{
    "code": 200,
    "data": {
        "description": "Tap4 AI Directory is a tool provides free AI Tools Directory. Get your favorite AI tools with Tap4 AI Directory, Tap4 AI Directory aims to collect all the AI tools and provide the best for users.",
        "detail": "### What is Tap4 AI?\n\nTap4 AI is an AI-driven platform that provides access to a vast array of AI technologies for various needs, including ChatGPT, GPT-4o for text generation and image understanding, Dalle3 for image creation, and document analysis.\n\n### How to Use Tap4 AI\n\nEvery user can utilize GPT-4o for free up to 20 times a day on tap4.ai. Subscribing to the platform grants additional benefits and extended access beyond the free usage limits.\n\n### Features of Tap4 AI\n\n#### Can I Generate Images Using Tap4 AI?\n\nYes, with Dalle3's text-to-image generation capability, users can create images, sharing credits with GPT-4o for a seamless creative experience.\n\n#### How Many GPTs are Available on Tap4 AI?\n\nTap4.ai offers nearly 200,000 GPT models for a wide variety of applications in work, study, and everyday life. You can freely use these GPTs without the need for a ChatGPT Plus subscription.\n\n#### How Can I Maximize My Use of Tap4 AI's AI Services?\n\nBy leveraging the daily free uses of GPT-4o document reading, and Dalle's image generation, users can explore a vast range of AI-powered tools to support various tasks.\n\n#### Will My Information Be Used for Your Training Data?\n\nWe highly value user privacy, and your data will not be used for any training purposes. If needed, you can delete your account at any time, and all your data will be removed as well.\n\n#### When Would I Need a Tap4 AI Subscription?\n\nIf the 20 free GPT-4o conversations per day do not meet your needs and you heavily rely on GPT-4o, we invite you to subscribe to our affordable products.",
        "languages": [],
        "screenshot_data": "https://demo.tap4.cn/tools/2024/6/15/tap4-ai-1718447471.png",
        "screenshot_thumbnail_data": "https://demo.tap4.cn/tools/2024/6/15/tap4-ai-thumbnail-1718447477.png",
        "tags": ["code-it","text-writing"],
        "title": "Get your best AI Tools | Tap4 AI Directory",
        "url": "https://tap4.ai"
    },
    "msg": "success"
}
```

## 常见问题

- 由于网站可能出现反爬虫，导致爬取失败，需要人工做二次检查
- LLM 洗出来的信息不服务期望，可以尝试自己去优化 prompt 提示词内容
- LLM 洗出来的内容可能仍然是提示词传过去的模板，这种也是反爬虫引起的问题，需要人工做二次检查
- 爬虫对服务器配置有一定的要求，Zeabur 上使用免费模式很容易出现无法正常运行问题，建议付费

## 产品链接

### TAP4-AI 导航站

全球 AI 工具导航站，搜集全球主流的 AI 工具，目前支持免费提交收录 AI 工具。更多详情，请访问: [Tap4 AI](https://tap4.ai)

### 如何获得冷启动的第一批用户

以下是提交产品以获取用户的网站列表。请访问
[StartUp Your Product List](https://github.com/6677-ai/TAP4-AI-Directory/blob/main/Startup-Your-Product-List.md)

### AI 纹身生成器

Tattao AI Design 是为纹身爱好者设计的纹身 AI 生成器和设计工具。如果你对此感兴趣，请访问：
[Tattoo AI Design](https://tattooai.design)

### Stable Diffusion 3 在线免费工具

[Free Stable Diffusion 3 Online](https://stable-diffusion-3.online)

### 免费的在线图片压缩工具

[Free Type Png Tool](https://freetinypng.com)

### 免费在线 AI 内容检测工具

[Free GPT2 Output Detector](https://openai-openai-detector.com/)
