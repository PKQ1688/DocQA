#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/4/19 17:26
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/4/19 17:26
# @File         : minimax.py
import json
import os

import requests
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

group_id = os.getenv("MINIMAX_GROUP_ID")
api_key = os.getenv("MINIMAX_API_KEY")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_embeddings(text_list, model="embo-01"):
    url = f"https://api.minimax.chat/v1/embeddings?GroupId={group_id}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        text_list = [text.replace("\n\n", " ").replace("\n", " ") for text in text_list]
        length = len(text_list)
        results = []

        for i in range(0, length, 100):
            data = {"texts": text_list[i: i + 100], "model": model, "type": "db"}
            response = requests.post(url, headers=headers, data=json.dumps(data))
            results.append(
                json.loads(response.text)['vectors']
            )
        return sum(results, [])
        # return results

    except Exception as e:
        print(e)
        return []


if __name__ == "__main__":
    res = get_embeddings(
        text_list=[
            "Minimax的文本embedding可用于衡量文本字符串的相关性。",
            "embedding是浮点数的向量（列表）。两个向量之间的距离衡量它们的相关性。小距离表示高相关性，大距离表示低相关性。",
        ]
    )

    print(res)
