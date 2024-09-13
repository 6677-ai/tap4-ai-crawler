# Tap4 AI Crawler

Tap4 AI Crawlerは、[tap4.ai](https://tap4.ai)によって開発されたオープンソースのウェブクローラーで、ウェブサイトをLLMを使用して要約情報に変換します。強力なスクレイピング、クローリング、データ抽出機能、ウェブページのスクリーンショットを含みます。Tap4 AI Crawlerを使用すると、AIツールディレクトリのAIツールの詳細を簡単に更新できるだけでなく、ウェブサイトの要約も生成できます。

このプロジェクトはPythonに基づいており、非常に軽量で、メンテナンスが容易で、AIツールディレクトリに興味のある個人開発者やPythonに興味のある学習者に適しています。皆さんのフォークとスターを歓迎します。

English | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md)

## Product HuntでTap4 AIをサポート

<a href="https://www.producthunt.com/posts/ai-tools-directory-by-tap4-ai?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-ai&#0045;tools&#0045;directory&#0045;by&#0045;tap4&#0045;ai" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=464357&theme=light" alt="AI&#0032;Tools&#0032;Directory&#0032;by&#0032;Tap4&#0032;AI - Open&#0045;source&#0032;AI&#0032;navigation&#0032;&#0038;&#0032;discovery&#0032;with&#0032;multi&#0045;language | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

## 特徴

- 入力されたウェブサイトのタイトル、説明、紹介を取得
- 入力されたウェブサイトのスクリーンショットを作成
- LLM（llama3/chatgpt）を使用してウェブサイトの紹介を処理し、SEOフレンドリーなMarkdown説明を生成
- クイック設定
- 高速展開

![tai4-ai](./images/tap4-ai.png)

## フォローとサポートリンク

私たちのTwitterをフォローしてください: https://x.com/tap4ai

プロジェクトが役に立った場合は、コーヒーを買ってください：

<a href="https://www.buymeacoffee.com/tap4ai0o" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

プロジェクトに興味がある場合は、私のWeChatを追加してください: helloleo2023、メモ: "tap4 ai open source"、またはQRコードをスキャンしてください: ![tap4-ai-wx](./images/tap4-ai-wechat.jpg)

## クイックスタート

- [Cloudflareに登録](https://www.cloudflare.com?utm_source=tap4ai&utm_campaign=oss)
- R2サービスを選択し、画像ストア用のバケットを作成し、パブリックアクセスに設定（オプション：カスタムドメインを設定）し、CORSポリシーを編集します。
  ![Create-cloudflare-R2](./images/cloudflare-r2.png)
- CORSポリシーは以下の通りです：

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

- R2 APIトークンを作成し、オブジェクトの読み取りと書き込みの権限を選択します。独自のパラメータを保存します：ENDPOINT_URL、BUCKET_NAME、ACCESS_KEY_ID、SECRET_ACCESS_KEY、CUSTOM_DOMAIN。これらのパラメータは.tap4-ai-crawlerの.envファイルに設定されます。
  ![Create-R2-API-Token](./images/Create-R2-API-Token.png)
  ![Cloudflare-R2-Token](./images/Cloudflare-R2-Token.png)
-

- [![Zeaburに登録](https://zeabur.com/deployed-on-zeabur-dark.svg)](https://zeabur.com?referralCode=leoli202303&utm_source=leoli202303&utm_campaign=oss)
- Zeaburで新しいプロジェクトとサービスを作成します
  **注：ウェブスクレイピングには特定のサーバー構成が必要です。Zeaburの有料サービスを購入し、米国ノードを優先的に選択することをお勧めします。**
- [tap4-ai-crawler](https://github.com/6677-ai/tap4-ai-crawler)を自分のgithubにフォークし、独自の.envパラメータで更新します。

### （2）コードモードに基づいてZeaburにデプロイ

Zeaburでフォークしたgithubリポジトリをデプロイし、Zeaburで環境変数を設定するか、コードリポジトリの.envファイルを手動で変更します。環境変数は以下の通りです：

- `GROQ_API_KEY`: Groqのキー、[ここで申請](https://console.groq.com/keys)
- `S3_ENDPOINT_URL`: S3のエンドポイント（Cloudflare R2を推奨）、[R2を申請](https://www.cloudflare.com/zh-cn/developer-platform/r2/)
- `S3_BUCKET_NAME`: S3のバケット名（例：Cloudflare R2）
- `S3_ACCESS_KEY_ID`: S3のアクセスキーID（例：Cloudflare R2）
- `S3_SECRET_ACCESS_KEY`: S3のシークレットアクセスキー（例：Cloudflare R2）
- `S3_CUSTOM_DOMAIN`: S3のカスタムドメイン（例：Cloudflare R2）、カスタムドメインがある場合は記入し、ない場合は空白のままにします。
- `AUTH_SECRET`: REST API用のカスタムアクセスキー。

## ローカルで実行

### インストール

- Python 3.xバージョン

### セットアップ

#### (1) このプロジェクトをクローン

```sh
git clone https://github.com/6677-ai/tap4-ai-crawler.git
```

#### (2) Groqでllama3キーを申請

[Groqキーを申請](https://console.groq.com/keys)

#### (3) S3オブジェクトストレージ情報を申請

- エンドポイント
- アクセスキーID
- シークレットアクセスキー
- バケット名

#### (4) 環境変数を設定

- ルートディレクトリの`.env`ファイルを以下の内容で変更します。例：

```sh
## LLM Configuration: 大規模モデル関連の設定
GROQ_API_KEY=gsk_********

## Object Storage Configuration: ストレージ関連の設定
S3_ENDPOINT_URL=https://*****.r2.cloudflarestorage.com
S3_BUCKET_NAME=tap4ai
S3_ACCESS_KEY_ID=****
S3_SECRET_ACCESS_KEY=****
S3_CUSTOM_DOMAIN=****
AUTH_SECRET=****
```

#### (5) ローカルで実行

Python依存関係をインストール

```sh
pip install -r requirements.txt
```

実行

```sh
python main_api.py
```

実行後、RestAPIが公開され、URLサフィックス：/site/crawlにアクセスできます。

## APIのリクエスト方法

curlを使用してPOSTリクエストでAPIを検証します。
リクエストパラメータ：

- フォーマット：Jsonフォーマット、
- パラメータ：url（例： https://tap4.ai）
  リクエストは以下の通りです：

```sh
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer xxxxx" -d '{"url": "https://tap4.ai", "tags": [ "selected tags: ai-detector","chatbot","text-writing","image","code-it"]}' http://127.0.0.1:8040/site/crawl
```

レスポンスパラメータ：

- フォーマット：Jsonフォーマット
- パラメータ：data-description：ウェブサイトの説明
- パラメータ：data-detail：ウェブサイトの詳細コンテンツ
- パラメータ：data-screenshot_data：ウェブサイトのスクリーンショット
- パラメータ：data-screenshot_thumbnail_data：ウェブサイトのスクリーンショットのサムネイル
- パラメータ：data-title：ウェブサイトのタイトル

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

## FAQ

- ウェブサイトの反スクレイピング対策により、クロールが失敗する可能性があり、手動での二次チェックが必要です。
- LLMによって処理された情報が期待に沿わない場合は、プロンプトの内容を自分で最適化してみてください。
- LLMによって処理された内容が依然としてプロンプトで渡されたテンプレートである場合もあり、これも反スクレイピング対策によるもので、手動での二次チェックが必要です。
- ウェブスクレイピングには特定のサーバー構成が必要です。Zeaburで無料モードを使用すると、正常に動作しないことがよくあります。有料サービスを購入することをお勧めします。

## リンク製品

### TAP4-AI-Directory

世界中のAIツールを収集するためのコレクションです。無料のChatGPTミラー、代替品、プロンプト、その他のAIツールなどを収集します。詳細については、[Tap4 AI](https://tap4.ai/)をご覧ください。

### スタートアップのための最初のユーザーを獲得する方法

製品を提出してユーザーを獲得するためのウェブサイトリストです。詳細については、[StartUp Your Product List](https://github.com/6677-ai/TAP4-AI-Directory/blob/main/Startup-Your-Product-List.md)をご覧ください。

### 無料のStable Diffusion 3オンラインツール

[Free Stable Diffusion 3 Online](https://stable-diffusion-3.online)

### 無料のTiny Pngツール

[Free Type Png Tool](https://freetinypng.com)

### 無料のGPT2出力検出器

[Free GPT2 Output Detector](https://openai-openai-detector.com/)

### タトゥーAIジェネレーターとデザイン

Tattoo AI Designは、タトゥーファンのためのタトゥーAIジェネレーターおよびデザインツールです。興味がある場合は、[Tattoo AI Design](https://tattooai.design/)をご覧ください。

## スポンサーリスト

### AIアニメガールフレンド -- AIアニメガールチャット＆ジェネレーター

Anime Girl Studioは、AIアニメガールジェネレーターおよびチャット製品です。好きなものを生成し、AIアニメガールとチャットできます。詳細については、[AI Anime Girlfriend](https://animegirl.studio/)をご覧ください。

### ベストAIガールフレンド -- ベストAIガールフレンド＆ジェネレーター

Best AI Girl Friendは、AIガールジェネレーターおよびチャット製品です。好きなものを生成し、AIアニメガールとチャットできます。詳細については、[Best AI Girlfriend](https://aigirl.best/)をご覧ください。
