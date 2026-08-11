import streamlit as st
import json
from PIL import Image
import os

st.set_page_config(page_title="恶劣天气激光雷达点云处理", layout="wide")
st.title("① 恶劣天气下车载激光雷达点云一体化处理技术")
st.divider()

# 加载数据
with open("data/papers.json", "r", encoding="utf-8") as f:
    all_data = json.load(f)
data = all_data[0]

# 1.成果简介
st.header("一、成果简介")
st.markdown(data["intro"])
st.divider()

# 2.核心技术
st.header("二、三大核心技术")
for tech in data["core_tech"]:
    st.markdown(f"- {tech}")
st.divider()

# 3.配套原理图展示
st.header("三、算法架构与实验可视化")
img_paths = data["img_list"]
for img_p in img_paths:
    try:
        img = Image.open(img_p)
        st.image(img, use_column_width=True)
    except Exception as e:
        # 图片缺失：静默跳过，页面不再弹出黄色警告
        pass
st.divider()

# 4.应用前景
st.header("四、应用场景与市场前景")
st.markdown(f"适用领域：{data['application']}")
st.divider()

# 5.原始文档下载
st.header("五、原始推介文档下载")
if os.path.exists(data["doc_path"]):
    with open(data["doc_path"], "rb") as f:
        st.download_button("下载完整Word推介材料", data=f, file_name=data["doc_path"].split("/")[-1])
else:
    st.caption("📎配套推介文档暂未部署，待补充文件后启用下载")
st.divider()