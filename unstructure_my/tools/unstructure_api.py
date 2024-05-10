#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/5/7 22:41
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/5/7 22:41
# @File         : unstructure_api.py
import os
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from dotenv import load_dotenv
load_dotenv()


client = UnstructuredClient(
    api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"),
    server_url=os.getenv("UNSTRUCTURED_API_URL"),
)

filename = "data/docx/hetong.docx"

with open(filename, "rb") as f:
    files = shared.Files(
        content=f.read(),
        file_name=filename,
    )

req = shared.PartitionParameters(files=files)

try:
    resp = client.general.partition(req)
    print(resp)
except SDKError as e:
    print(e)
