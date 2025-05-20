from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()

def get_response_with_tongyi(prompt: str) -> str:
    """调用通义千问API获取响应
    Args:
        prompt (str): 输入提示词
    Returns:
        str: API返回的响应内容
    """
    try:
        client = OpenAI(
            api_key=os.getenv('TONGYI_API_KEY'),
            base_url=os.getenv('TONGYI_BASE_URL')
        )
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise
    
if __name__ == '__main__':
    response = get_response_with_tongyi('你是谁')
    print(response)