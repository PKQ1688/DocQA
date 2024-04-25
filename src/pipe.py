#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/4/21 19:07
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/4/21 19:07
# @File         : pipe.py
from langchain.schema import HumanMessage

from src.utils import search_pinecone, main_chain


def rag_pipe(user_query):
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

    search_knowledge_base_top_k = 8
    filters = {}
    docs_response = []

    docs_response.extend(
        search_pinecone(
            query=user_query,
            filters=filters,
            top_k=search_knowledge_base_top_k,
        )
    )
    chat_history_recent = ""
    # print(docs_response)

    input = f"""Must Follow:
    - Respond to "{user_query}" by using information from "{docs_response}" (if available) and your own knowledge to provide a logical, clear, and critically analyzed reply in the same language.
    - Use the chat context from "{chat_history_recent}" (if available) to adjust the level of detail in your response.
    - Employ bullet points selectively, where they add clarity or organization.
    - Cite sources in main text using the Author-Date citation style where applicable.
    - Provide a list of references in markdown format of [title.journal.authors.date.](hyperlinks) at the end (or just the source file name), only for the references mentioned in the generated text.
    - Use LaTeX quoted by '$' or '$$' within markdown to render mathematical formulas.
    
    Must Avoid:
    - Repeat the human's query.
    - Translate cited references into the query's language.
    - Preface responses with any designation such as "AI:"."""

    response = main_chain().invoke(
        {"input": input},
        # {"callbacks": [st_callback]},
    )

    print(response)
    return response["text"]


if __name__ == '__main__':
    user_query_ = "In the context of Bayesian analysis and complex designs, would you like more guidance on selecting priors and configuring Markov chain Monte Carlo settings, identifying appropriate testing levels, and calculating effect sizes such as Cohen's d and Pearson's r? Our web collection on statistics for biologists covers these topics."
    rag_pipe(user_query=user_query_)
