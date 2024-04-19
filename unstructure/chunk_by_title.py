#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/4/19 16:22
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/4/19 16:22
# @File         : chunk_by_title.py
import os
import pickle

from dotenv import load_dotenv
from xata.client import XataClient

from tools.unstructure_pdf import unstructure_pdf

load_dotenv()

xata = XataClient(
    api_key=os.getenv("XATA_API_KEY"), db_url=os.getenv("XATA_ESG_DB_URL")
)

table_name = "ESG_Reports"
columns = ["id"]
filter = {"$notExists": "embeddingTime"}


def fetch_all_records(xata, table_name, columns, filter, page_size=1000):
    all_records = []
    cursor = None
    more = True

    while more:
        page = {"size": page_size}
        if not cursor:
            results = xata.data().query(
                table_name,
                {
                    "page": page,
                    "columns": columns,
                    "filter": filter,
                },
            )
        else:
            page["after"] = cursor
            results = xata.data().query(
                table_name,
                {
                    "page": page,
                    "columns": columns,
                },
            )

        all_records.extend(results["records"])
        cursor = results["meta"]["page"]["cursor"]
        more = results["meta"]["page"]["more"]

    return all_records


# records = fetch_all_records(xata, table_name, columns, filter)


def process_pdf(record):
    record_id = record["id"]

    text_list = unstructure_pdf("data/pdf/" + record_id + ".pdf")

    with open("data/pickle/" + record_id + ".pkl", "wb") as f:
        pickle.dump(text_list, f)

    text_str = "\n----------\n".join(text_list)

    with open("data/txt/" + record_id + ".txt", "w") as f:
        f.write(text_str)


records = [{"id": item.replace(".pdf", "")} for item in os.listdir("data/pdf")]

for record in records:
    process_pdf(record=record)

# record = {"id": "rec_clu17n8bslsq4fnfc8s0"}

# record = {"id": "rec_cltid4e9hf9adk7qf2rg"}

# process_pdf(record)

# for record in records:
#     process_pdf(record)

# with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
#     executor.map(process_pdf, records)
