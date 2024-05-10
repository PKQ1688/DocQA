#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/5/7 13:15
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/5/7 13:15
# @File         : doc2json.py
from docx import Document
import json
from pprint import pprint


def docx_to_json(doc_path):
    def iterate_paragraphs(paragraphs):
        """递归遍历段落，收集标题和内容"""
        data = {}
        content = ""
        for paragraph in paragraphs:
            if paragraph.style.name.startswith('Heading'):
                # 如果遇到新的标题，保存前一个标题的内容（如果存在）
                if content:
                    data[last_heading] = content.strip()
                    content = ""  # 重置内容
                last_heading = paragraph.text
            else:
                # 非标题段落，累加内容
                content += paragraph.text + "\n"
        # 添加最后一个标题的内容（如果文档未以标题结束）
        if content:
            data[last_heading] = content.strip()
        return data

    document = Document(doc_path)
    data = iterate_paragraphs(document.paragraphs)

    return data
    # return json.dumps(data, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # 使用方法：指定你的docx文件路径
    doc_path = 'data/docx/hetong.docx'
    json_data = docx_to_json(doc_path)
    pprint(json_data)
