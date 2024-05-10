#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/4/20 22:47
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/4/20 22:47
# @File         : utils.py
import os
from datetime import datetime

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import (
    PromptTemplate,
)
# from langchain_community.chat_models import MiniMaxChat
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import MiniMaxEmbeddings
from langchain_pinecone import PineconeVectorStore
from xata.client import XataClient

load_dotenv()

xata_api_key = os.getenv("XATA_API_KEY")
xata_db_url = os.getenv("XATA_ESG_DB_URL")
pinecone_serverless_api = os.getenv("PINECONE_SERVERLESS_API_KEY")
pinecone_serverless_index_name = os.getenv("PINECONE_SERVERLESS_INDEX_NAME")
minimax_group_id = os.getenv("MINIMAX_GROUP_ID")
minimax_api_key = os.getenv("MINIMAX_API_KEY")
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")

langchain_verbose = True


def search_pinecone(query: str, filters: dict = {}, top_k: int = 16):
    """
    Performs a similarity search on Pinecone's vector database based on a given query and optional date filter, and returns a list of relevant documents.

    :param query: The query to be used for similarity search in Pinecone's vector database.
    :type query: str
    :param created_at: The date filter to be applied in the search, specified in a format compatible with Pinecone's filtering options.
    :type created_at: str or None
    :param top_k: The number of top matching documents to return. Defaults to 16.
    :type top_k: int or None
    :returns: A list of dictionaries, each containing the content and source of the matched documents. The function returns an empty list if 'top_k' is set to 0.
    :rtype: list of dicts

    Function Behavior:
        - Initializes Pinecone with the specified API key and environment.
        - Conducts a similarity search based on the provided query and optional date filter.
        - Extracts and formats the relevant document information before returning.

    Exceptions:
        - This function relies on Pinecone and Python's os library. Exceptions could propagate if there are issues related to API keys, environment variables, or Pinecone initialization.
        - TypeError could be raised if the types of 'query', 'created_at', or 'top_k' do not match the expected types.

    Note:
        - Ensure the Pinecone API key and environment variables are set before running this function.
        - The function uses 'OpenAIEmbeddings' to initialize Pinecone's vector store, which should be compatible with the embeddings in the Pinecone index.
    """

    if top_k == 0:
        return []

    # embeddings = OpenAIEmbeddings(model=os.environ["PINECONE_EMBEDDING_MODEL"])
    embeddings = MiniMaxEmbeddings(
        model="embo-01",
        minimax_api_key=minimax_api_key,
        minimax_group_id=minimax_group_id,
    )

    # vectorstore = PineconeVectorStore(embedding=embeddings, namespace="sci")
    vectorstore = PineconeVectorStore(
        embedding=embeddings,
        index_name=pinecone_serverless_index_name,
        namespace="esg",
        pinecone_api_key=pinecone_serverless_api,
    )

    if filters:
        print(filters)
        docs = vectorstore.similarity_search(query, k=top_k, filter=filters)
    else:
        print("no filters")
        docs = vectorstore.similarity_search(query, k=top_k)

    doi_set = set()
    for doc in docs:
        doi_set.add(doc.metadata["rec_id"])

    print(doi_set)

    xata_docs = XataClient(api_key=xata_api_key, db_url=xata_db_url)

    xata_response = xata_docs.data().query(
        "ESG_Fulltext",
        {
            "columns": ["sortNumber", "text", "reportId"],
            "filter": {
                "reportId": {"$any": list(doi_set)},
            },
        },
    )
    records = xata_response.get("records", [])
    records_dict = {record["text"]: record for record in records}

    docs_list = []
    for doc in docs:
        docs_list.append(
            {"content": doc.page_content, "source": doc.metadata["rec_id"]}
        )
        # try:
        #     record = records_dict.get(doc.metadata["rec_id"], {})
        #     authors = ", ".join(record["authors"]) if record.get("authors") else ""
        #     date = datetime.fromtimestamp(doc.metadata["date"])
        #     formatted_date = date.strftime("%Y-%m")  # Format date as 'YYYY-MM'
        #     url = "https://doi.org/{}".format(doc.metadata["doi"])
        #     source_entry = "[{}. {}. {}. {}.]({})".format(
        #         record["title"],
        #         doc.metadata["journal"],
        #         authors,
        #         formatted_date,
        #         url,
        #     )
        #     docs_list.append({"content": doc.page_content, "source": source_entry})
        #
        #     # date = datetime.fromtimestamp(doc.metadata["created_at"])
        #     # formatted_date = date.strftime("%Y-%m")  # Format date as 'YYYY-MM'
        #     # source_entry = "[{}. {}. {}. {}.]({})".format(
        #     #     doc.metadata["source_id"],
        #     #     doc.metadata["source"],
        #     #     doc.metadata["author"],
        #     #     formatted_date,
        #     #     doc.metadata["url"],
        #     # )
        #     # docs_list.append({"content": doc.page_content, "source": source_entry})
        # except:
        #     docs_list.append(
        #         {"content": doc.page_content, "source": doc.metadata["source"]}
        #     )

    return docs_list


def main_chain():
    """
    Creates and returns a main Large Language Model (LLM) chain configured to produce responses only to science-related queries while avoiding sensitive topics.

    :return: A configured LLM chain object for producing responses that adhere to the defined conditions.
    :rtype: Object

    Function Behavior:
        - Initializes a ChatOpenAI instance for a specific language model with streaming enabled.
        - Configures a prompt template instructing the model to strictly respond to science-related questions while avoiding sensitive topics.
        - Constructs and returns an LLMChain instance, which uses the configured language model and prompt template.

    Exceptions:
        - Exceptions could propagate from underlying dependencies like the ChatOpenAI or LLMChain classes.
        - TypeError could be raised if internal configurations within the function do not match the expected types.
    """

    # llm_chat = ChatOpenAI(
    #     model=llm_model,
    #     temperature=0,
    #     streaming=True,
    #     verbose=langchain_verbose,
    # )

    # llm_chat = MiniMaxChat(
    #     MINIMAX_GROUP_ID=minimax_group_id,
    #     MINIMAX_API_KEY=minimax_api_key,
    #     model_name="abab5-chat",
    #     temperature=0.01,
    #     streaming=True,
    # )

    llm_chat = ChatTongyi(
        model_name="qwen-max",
        dashscope_api_key=dashscope_api_key,
        temperature=0.01,
        streaming=True,
    )

    template = """{input}"""

    prompt = PromptTemplate(
        input_variables=["input"],
        template=template,
    )

    chain = LLMChain(
        llm=llm_chat,
        prompt=prompt,
        verbose=langchain_verbose,
    )

    return chain


if __name__ == '__main__':
    main_chain().invoke(
        {"input": "番茄是什么植物？"},
        # {"callbacks": [st_callback]},
    )
