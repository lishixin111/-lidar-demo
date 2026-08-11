import streamlit as st
import json

st.set_page_config(page_title="成果资料库", layout="wide")
st.title("🏛️ 成果资料库")
st.divider()

#加载json
with open("data/papers.json","r",encoding="utf-8") as f:
    paper_list = json.load(f)

#搜索框
keyword = st.text_input("输入关键词检索成果名称/方向：",value="")

#筛选逻辑
if keyword.strip()!="":
    filter_list = []
    for d in paper_list:
        text_all = (d["title"] + d["intro"] + d["application"]).lower()
        if keyword.lower() in text_all:
            filter_list.append(d)
else:
    filter_list = paper_list

#卡片循环渲染
for d in filter_list:
    with st.container(border=True):
        st.subheader(f"成果编号：{d['id']}｜{d['title']}")
        st.markdown(f"**应用场景**：{d['application']}")
        st.markdown(f"**成果简介**：{d['intro'][:320]}......")
        #下载按钮
        try:
            with open(d["doc_path"],"rb") as fdoc:
                st.download_button(
                    label="📥下载推介Word文档",
                    data=fdoc,
                    file_name=d["doc_path"].split("/")[-1],
                    key=f"dl_{d['id']}"
                )
        except Exception:
            st.warning("⚠️文档文件缺失，请检查docs目录")
    st.divider()

if len(filter_list)==0:
    st.info("🔍没有匹配到相关成果，请更换关键词")