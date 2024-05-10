#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/5/8 21:44
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/5/8 21:44
# @File         : llm_res.py
# python3
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com/")


def get_llm_res(prompt: str, message: str):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt + message},
        ]
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    prompt = "现在你是一个男科医生，请根据患者的问题给出建议。"
    message = "现在18岁了，最近半年，发觉，性生活总是提不起劲，同时，每次才开始就已经射了，请问：男孩早泄究竟是什么因素引发的。"
    llm_out = get_llm_res(prompt, message)
    print(llm_out)
