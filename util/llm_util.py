import os
import random
import requests
import time
import logging

import tiktoken
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI
from transformers import LlamaTokenizer

from util.common_util import CommonUtil

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

util = CommonUtil()


class LLMUtil:
    def __init__(self):
        load_dotenv()
        self.llm_type = os.getenv('LLM_TYPE')
        if self.llm_type == 'groq':
            self.init_groq_config()
        elif self.llm_type == 'openai':
            self.init_openai_config()
        elif self.llm_type == 'all':
            self.init_groq_config()
            self.init_openai_config()
        else:
            logger.error("LLM_TYPE environment variable not found or is empty.")

        self.description_sys_prompt = os.getenv('DESCRIPTION_SYS_PROMPT')
        self.detail_sys_prompt = os.getenv('DETAIL_SYS_PROMPT')
        self.introduction_sys_prompt = os.getenv('INTRODUCTION_SYS_PROMPT')
        self.feature_sys_prompt = os.getenv('FEATURE_SYS_PROMPT')
        self.format_sys_prompt = os.getenv('FORMAT_SYS_PROMPT')
        self.language_sys_prompt = os.getenv('LANGUAGE_SYS_PROMPT')
    def init_groq_config(self):
        logger.info("init_groq_config")
        groq_api_keys = os.getenv('GROQ_API_KEY')
        if groq_api_keys:
            groq_api_key_list = groq_api_keys.split(',')
            # 随机选择一个元素
            self.groq_api_key = random.choice(groq_api_key_list)
            logger.info(f"Randomly selected Groq API Key: {self.groq_api_key}")
        else:
            logger.error("GROQ_API_KEY environment variable not found or is empty.")

        self.groq_model = os.getenv('GROQ_MODEL')
        self.groq_max_tokens = int(os.getenv('GROQ_MAX_TOKENS', 5000))
        self.groq_client = Groq(
            api_key=self.groq_api_key
        )
        # 初始化LLaMA模型的Tokenizer
        self.groq_tokenizer = LlamaTokenizer.from_pretrained("huggyllama/llama-65b")

    def init_openai_config(self):
        logger.info("Initializing OpenAI configuration...")
        
        self.openai_api_key = os.getenv('CUSTOM_API_ACCESS_TOKEN', "ak-Nk9p2YsSoMlzpabAzFSAd7gC48a3M74TZkjhrTDLNIEWtmbt")
        self.openai_model = os.getenv('CUSTOM_API_MODEL', "gpt-4o-mini")
        self.openai_max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', 5000))
        
        self.api_url = os.getenv('CUSTOM_API_URL', "https://api.nextapi.fun/api/openai/v1/chat/completions")
        logger.info(f"API URL set to: {self.api_url}")

        self.openai_tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def call_gpt(self, script, system_prompt, temperature=1.0, top_p=1.0, max_retries=2, delay=5):
        openai_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": script}
            ],
            "temperature": temperature,
            "max_tokens": self.openai_max_tokens,
            "top_p": top_p
        }

        for i in range(max_retries):
            try:
                response = requests.post(self.api_url, headers=openai_headers, json=data)
                response.raise_for_status()
                res_json = response.json()
                return res_json['choices'][0]['message']['content']
            except Exception as e:
                logger.error(f"An exception occurred: {e}. Retrying...")
                time.sleep(delay)
        return []

    def process_prompt(self, sys_prompt, user_prompt, variable_map=None, llm_type='openai'):
        if not sys_prompt or not user_prompt:
            logger.info(f"LLM无需处理，sys_prompt或user_prompt为空")
            return None

        if isinstance(variable_map, dict):
            for key, value in variable_map.items():
                if value:
                    sys_prompt = sys_prompt.replace(key, value)
                    user_prompt = user_prompt.replace(key, value)
                    logger.info(f"替换变量{key}为{value}")

        logger.info("LLM正在处理")
        try:
            if self.llm_type == 'groq' or (self.llm_type == 'all' and llm_type == 'groq'):
                logger.info("正在使用groq处理")
                tokens = self.groq_tokenizer.encode(user_prompt)
                if len(tokens) > self.groq_max_tokens:
                    logger.info(f"用户输入长度超过{self.groq_max_tokens}，进行截取")
                    truncated_tokens = tokens[:self.groq_max_tokens]
                    user_prompt = self.groq_tokenizer.decode(truncated_tokens)

                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": sys_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        }
                    ],
                    model=self.groq_model,
                    temperature=0.2,
                )
            elif self.llm_type == 'openai' or (self.llm_type == 'all' and llm_type == 'openai'):
                logger.info("正在使用openai处理")
                tokens = self.openai_tokenizer.encode(user_prompt)
                if len(tokens) > self.openai_max_tokens:
                    logger.info(f"用户输入长度超过{self.openai_max_tokens}，进行截取")
                    truncated_tokens = tokens[:self.openai_max_tokens]
                    user_prompt = self.openai_tokenizer.decode(truncated_tokens)

                return self.call_gpt(user_prompt, sys_prompt)

            if chat_completion.choices[0] and chat_completion.choices[0].message:
                logger.info(f"LLM完成处理，成功响应!")
                return chat_completion.choices[0].message.content
            else:
                logger.info("LLM完成处理，处理结果为空")
                return None
        except Exception as e:
            logger.error(f"LLM处理失败", e)
            return None

    def process_description(self, user_prompt, variable_map=None, llm_type='openai'):
        logger.info("正在处理description...")
        result = self.process_prompt(self.description_sys_prompt, user_prompt, variable_map, llm_type)
        if result:
            result = result.replace('"', '')
        return result

    def process_detail(self, user_prompt, variable_map=None, llm_type='openai'):
        logger.info("正在处理Detail...")
        # print(f"Detail的user_prompt: {user_prompt}")
        return self.process_prompt(self.detail_sys_prompt, user_prompt, variable_map, llm_type)

    def process_introduction(self, user_prompt, variable_map=None, llm_type='openai'):
        logger.info(f"正在处理introduction...")
        result = self.process_prompt(self.introduction_sys_prompt, user_prompt, variable_map, llm_type)
        return util.detail_handle(result)

    def process_features(self, user_prompt, variable_map=None, llm_type='openai'):
        logger.info(f"正在处理features...")
        return self.process_prompt(self.feature_sys_prompt, user_prompt, variable_map, llm_type)


    def process_language(self, language, user_prompt):
        logger.info(f"正在处理多语言:{language}, user_prompt:{user_prompt}")
        # 如果language 包含 English字符，则直接返回
        if 'english'.lower() in language.lower():
            result = user_prompt
        else:
            result = self.process_prompt(self.language_sys_prompt.replace("{language}", language), user_prompt)
            if result and not user_prompt.startswith("#"):
                # 如果原始输入没有包含###开头的markdown标记，则去掉markdown标记
                result = result.replace("### ", "").replace("## ", "").replace("# ", "").replace("**", "")
        logger.info(f"多语言:{language}, 处理结果:{result}")
        return result
