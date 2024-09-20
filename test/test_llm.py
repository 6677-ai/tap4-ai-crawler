import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from util.llm_util import LLMUtil

# 加载环境变量
load_dotenv()

# 初始化 LLMUtil 实例
llm = LLMUtil()

# 从 res.html 文件读取测试内容
def read_html_content(file_path='response.html'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"Read content (first 100 characters): {content[:100]}")  # 添加这行来检查读取的内容
        return content
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

# 读取测试用的输入内容
test_content = read_html_content()

if test_content is None:
    print("Failed to read test content. Exiting.")
    exit(1)

def test_process_description():
    print("Testing process_description:")
    result = llm.process_description(test_content)
    print(result)
    print()

def test_process_detail():
    print("Testing process_detail:")
    result = llm.process_detail(test_content)
    print(result)

def test_process_introduction():
    print("Testing process_introduction:")
    result = llm.process_introduction(test_content)
    print(result)
    print()

def test_process_features():
    print("Testing process_features:")
    result = llm.process_features(test_content)
    print(result)
    print()

def test_process_format():
    print("Testing process_format:")
    result = llm.process_format(test_content)
    print(result)
    print()

if __name__ == "__main__":
    # test_process_description()
    test_process_detail()
    # test_process_introduction()
    # test_process_features()
    # test_process_format()