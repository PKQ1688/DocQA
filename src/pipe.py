#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/4/21 19:07
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/4/21 19:07
# @File         : pipe.py
from langchain.schema import HumanMessage
from loguru import logger

from src.utils import search_pinecone, main_chain


def rag_pipe(user_query, chat_history_recent="", prompt_template=None, filters={}):
    xata_history = []
    # user_query = "What is the capital of France?"
    # user_query = "In the context of Bayesian analysis and complex designs, would you like more guidance on selecting priors and configuring Markov chain Monte Carlo settings, identifying appropriate testing levels, and calculating effect sizes such as Cohen's d and Pearson's r? Our web collection on statistics for biologists covers these topics."

    human_message = HumanMessage(
        content=user_query,
        additional_kwargs={"id": 0},
    )

    xata_history.append(human_message)
    # print(human_message)
    # exit()

    search_knowledge_base_top_k = 4
    # filters = {"rec_id": "plan"}
    # filters = {}
    docs_response = []

    docs_response.extend(
        search_pinecone(
            query=user_query,
            filters=filters,
            top_k=search_knowledge_base_top_k,
        )
    )
    # chat_history_recent = ""
    # print(docs_response)

    if prompt_template is None:
        input = f"""必须遵守的规则:
    - 根据"{user_query}"提出的问题，利用"{docs_response}"（如果有的话）中的信息及你自身的知识，提供一个逻辑清晰、条理分明且经过批判性分析的回答，回答应使用与问题相同的语言。
    - 利用"{chat_history_recent}"（如果有）中的聊天上下文，调整你的回答详略程度，使之更贴合对话情境。
    - 适当使用项目符号列表以增加条理性和清晰度。
    - 如适用，在正文中采用作者-日期引用格式来标注来源。
    - 使用 LaTeX 记法，通过 '$' 或 '$$' 在Markdown中包裹数学公式以正确渲染。
    
    必须避免的行为:
    - 重复人类用户的查询内容。
    - 将引用的参考文献翻译成提问时使用的语言。
    - 在回答前使用任意标识符，如“AI:”"""
    else:
        input = f"""必须遵守的规则:
    - 根据"{user_query}"提出的问题，利用"{docs_response}"（如果有的话）中的信息及你自身的知识，直接给出有或者没有的，不要有多余的回答。
    
    必须避免的行为:
    - 重复人类用户的查询内容。
    - 出现有或者没有之外的回答。
    - 在回答前使用任意标识符，如“AI:”
    """

    response = main_chain().invoke(
        {"input": input},
        # {"callbacks": [st_callback]},
    )
    chat_history_recent += "Human: " + user_query + "\nAI: " + response["text"] + "\n"

    logger.info(response["text"])
    return response["text"], chat_history_recent


if __name__ == '__main__':
    user_query_ = "有无项目实施地点？"
    rag_pipe(user_query=user_query_, chat_history_recent="", prompt_template="new")  # noqa
