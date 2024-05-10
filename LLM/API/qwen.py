#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/5/6 14:44
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/5/6 14:44
# @File         : qwen.py.py
import os
import random
from http import HTTPStatus

import dashscope
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
from dotenv import load_dotenv

load_dotenv()

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def get_qwen_response(use_content):
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': use_content}]
    response = Generation.call(model="qwen-max",
                               messages=messages,
                               # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                               seed=random.randint(1, 10000),
                               # 将输出设置为"message"格式
                               result_format='message')
    if response.status_code == HTTPStatus.OK:
        # print(response)
        return response.output.choices
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        return ""


if __name__ == '__main__':
    res = get_qwen_response(use_content="如何做西红柿炒蛋？")
    print(res)
