#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time         : 2024/5/6 15:46
# @Author       : adolf
# @Email        : adolf1321794021@gmail.com
# @LastEditTime : 2024/5/6 15:46
# @File         : 审核.py
import os

import streamlit as st
from pypinyin import lazy_pinyin

from src.pipe import rag_pipe
from unstructure_my.embedding import embed_from_ori_file

_page_config = {
    "label": "审核",
    "icon": "🌟"
}


def save_uploaded_file(uploadedfile):
    with open(os.path.join("uploads", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())


st.set_page_config(page_title="审核", page_icon="🌟", layout="wide")

st.title('合同智能审核系统')
# st.write('This is page 1.')
# 合同类型选项
contract_types = ["采购合同", "合作合同", "借款合同", "租房合同"]

selected_contract_type = st.selectbox("请选择合同类型:", contract_types)

uploaded_file = st.file_uploader("请选择一个docx合同文件进行上传", type=["docx"])

cg_content_check = [
    "有无负责人的名称或者姓名和联系方式",
    "有无项目实施地点",
    "有无商品的数量和质量要求",
    "有无价格及付款方式",
    "有无履行期限、地点和方式",
    "有无服务响应时间和地点"
]

cg_integrity_check = [
    "有无合同标的",
    "有无双方权利与义务说明",
    "有无合同生效及其他",
    "有无违约责任说明",
    "有无解决争议的方法",
    "有无验收或评价及结果应用",
]

hz_integrity_check = [
    "有无合作方式和利润分配方式",
    "有无甲方的权利与义务",
    "有无乙方的权利与义务",
    "有无说明违约责任",
    "有无规定保密义务",
    "有无不可抗力事件的解决方法",
    "有无解决争议方式"
]

hz_content_check = [
    "有无甲方和乙方的详细信息",
    "有无规定具体的合作期限",
    "有无具体的付款方式",
    "有无说明双方利润分配方式",
]

jk_content_check = [
    "有无规定违约责任",
    "有无规定争议条款",
    "有无规定借款利率",
]

jk_integrity_check = [
    "有无具体的借款人，出借人和担保人信息",
    "有无规定具体借款金额",
    "有无具体付款方式",
    "有无具体的借款期限",
    "有无说明借款用途",
    "有无规定具体的还款方式",
]

zf_content_check = [
    "有无房屋所有权及使用权情况",
    "有无房屋产权登记情况",
    "有无房屋概况说明",
    "租赁期限有无具体时间",
    "有无具体租金",
    "有无具体交纳期限和交纳方式"
]

zf_integrity_check = [
    "出租方信息与产权登记信息是否对应",
    "有无免责说明",
    "有无租赁期限",
    "有无租金、交纳期限和交纳方式",
    "有无违约责任",
    "有无争议解决的方式",
]
if contract_types == "采购合同":
    content_check = cg_content_check
    integrity_check = cg_integrity_check
elif contract_types == "合作合同":
    content_check = hz_content_check
    integrity_check = hz_integrity_check
elif contract_types == "借款合同":
    content_check = jk_content_check
    integrity_check = jk_integrity_check
else:
    content_check = zf_content_check
    integrity_check = zf_integrity_check

if uploaded_file is not None:
    # 调用函数保存文件到本地"uploads"文件夹
    if not os.path.exists("uploads"):
        os.makedirs("uploads")  # 如果uploads文件夹不存在，则创建它

    save_uploaded_file(uploaded_file)
    st.success("文件上传成功！")

    # for i in os.listdir("uploads"):
    #     print(f"uploads/{i}")
    print(f"uploads/{uploaded_file.name}")
    embed_from_ori_file(ori_file_path=f"uploads/{uploaded_file.name}")

    st.success("文件处理完成！")

    s1 = st.button("开始内容审核")
    s2 = st.button("开始完整性审核")

    file_id = uploaded_file.name.split(".")[0]
    file_id = lazy_pinyin(file_id)
    file_id = "".join(file_id)

    filters = {
        "rec_id": {
            "$eq": file_id  # 指定 my_field 必须等于 111
        }
    }

    if s1:
        for i in content_check:
            # st.write(i)
            response, history = rag_pipe(i, prompt_template="new", filters=filters)
            if response[0] == "有":
                st.success("该合同" + i.replace("有无", "") + "存在")
            else:
                st.error("该合同" + i.replace("有无", "") + "不存在")
        # st.success("该合同合规")
        # st.error("该合同不合规")

    if s2:
        for i in integrity_check:
            response, history = rag_pipe(i, prompt_template="new", filters=filters)
            if response[0] == "有":
                st.success("该合同" + i.replace("有无", "") + "存在")
            else:
                st.error("该合同" + i.replace("有无", "") + "不存在")
#
