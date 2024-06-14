# Tap4 AI Crawler

Tap4 AI Crawler is an open source web crawler built by [tap4.ai](https://tap4.ai), that will convert the website into the website summarize info with LLM. Includes powerful scraping, crawling and data extraction capabilities, web page screenshots. With Tap4 AI Crawler, you can not only easily update the ai tool detail for your AI Tools Directory but also summary of the website.

This project is based on Python, very lightweight, easy to maintain, suitable for individual developers interested in AI tools directories, and also for learners interested in Python. We welcome everyone to fork and star.

English | [简体中文](./README.zh-CN.md)

## Follow Us

Follow us on Twitter: https://x.com/tap4ai

If you find this project helpful, you can buy me a coffee:

<a href="https://www.buymeacoffee.com/tap4ai0o" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

If you are interested in this project, feel free to scan the QR code to join our WeChat group: ![tap4-ai-wx-group](./images/tap4-ai-wechat-group.jpeg)

## Features

- Fetching titles, descriptions, and introductions of input websites
- Making screenshots of the input websites
- Support for using LLM (llama3/chatgpt) to process website introductions and generate Markdown descriptions
- Quick configuration
- Fast deployment

![tai4-ai](./images/tap4-ai.png)

## Quick Start

- [Register on Zeabur](https://zeabur.com?referralCode=leoli202303)
- Create a new project and service on Zeabur

### （1）Quick Deployment in Zeabur Based on Image Mode

**Click the Deploy Button and fill in the environment variables as instructed**<br>
[![Quickly Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/89NZ05)

### （2）Deploying in Zeabur based on code mode

Deploying a Github repository after selecting Fork in Zeabur, and configuring environment variables in Zeabur or manually modifying the .env file in the code repository. The environment variables are as follows:

- `GROQ_API_KEY`: Key for Groq, apply for it [Here](https://console.groq.com/keys)
- `S3_ENDPOINT_URL`: Endpoint for S3(such as Cloudflare R2), apply for [R2](https://www.cloudflare.com/zh-cn/developer-platform/r2/)
- `S3_BUCKET_NAME`: Bucket name for S3(such as Cloudflare R2)
- `S3_ACCESS_KEY_ID`: Access key ID for S3(such as Cloudflare R2)
- `S3_SECRET_ACCESS_KEY`: Secret access key for S3(such as Cloudflare R2)
- `S3_CUSTOM_DOMAIN`: Custom domain for S3(such as Cloudflare R2), if you have a custom domain, fill it in; otherwise, it can be left blank.

## Runs on local

### Install

- Python 3.x version

### Setup

#### (1) Clone this project

```sh
git clone https://github.com/6677-ai/tap4-ai-crawler.git
```

#### (2) Apply for llama3 key on Groq

[Groq key apply](https://console.groq.com/keys)

#### (3) Apply for S3 object storage information

- Endpoint
- Access Key Id
- Secret Access Key
- Bucket Name

#### (4) Set environment variables

- Modify the `.env` file in the root directory with the following content, example:

```sh
## LLM Configuration: Large model related configuration
GROQ_API_KEY=gsk_********

## Object Storage Configuration: Storage related configuration
R2_ENDPOINT_URL=https://*****.r2.cloudflarestorage.com
R2_BUCKET_NAME=tap4ai
R2_ACCESS_KEY_ID=****
R2_SECRET_ACCESS_KEY=****
R2_CUSTOM_DOMAIN=****
```

#### (5) Run locally

Install Python dependencies

```sh
pip install -r requirements.txt
```

Run

```sh
python main_api.py
```

After running, a RestAPI will be exposed, access URL suffix: /site/crawl

## How to request the API

Use curl to verify the API

```sh
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://tap4.ai","tags": ["website","navigation", "search","picture","photo"]}' http://127.0.0.1:8040/site/crawl
```

## Links to our products

### TAP4-AI-Directory

The Collection for the AI tools all over the world. | Collect free ChatGPT mirrors, alternatives, prompts, other AI tools, etc. For more, please visit: [Tap4 AI](https://tap4.ai/)

### How to get your first users for startup at the website list

Here is the website list for submitting your product to get users. Please visit [StartUp Your Product List](https://github.com/6677-ai/TAP4-AI-Directory/blob/main/Startup-Your-Product-List.md)

### GPT-4o in OpenAI

The amazing new feature released on 2024.05.14. GPT-4o is coming, let's chat with her. Please visit [GPT-4o](https://openai.com/index/hello-gpt-4o/)

### The Tattoo AI Generator and Design

Tattoo AI Design is a tattoo AI generator and design tool for tattoo fans. If you are interested, visit [Tattoo AI Design](https://tattooai.design/)

## Sponsor List

### Anime Girl Studio -- AI Anime Girl Chat & Generator

Anime Girl Studio is the AI anime girl generator and chat product. You can generate what you like and chat with the AI anime girl, please visit [Anime Girl Studio](https://animegirl.studio/)

### Best AI Girl Friend -- Best AI Girl Chat & Generator

Best AI Girl Friend is the AI girl generator and chat product. You can generate what you like and chat with the AI anime girl, please visit [Best AI Girl Friend](https://aigirl.best/)

## LICENSE

MIT
