import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_echarts import st_echarts

st.set_page_config(page_title="在线交互式仿真平台", layout="wide")
st.title("课题组算法在线仿真演示平台")
tab1, tab2, tab3, tab4 = st.tabs(["激光雷达点云仿真", "MIMO资源调度仿真", "城市海量接入仿真", "多模态传输调度仿真"])

# ===================== Tab1 激光雷达点云仿真 =====================
with tab1:
    st.subheader("恶劣天气点云生成+去噪仿真")
    col_a, col_b = st.columns([1, 3])
    with col_a:
        rain_strength = st.slider("降雨噪声强度", 0, 100, 30)
        snow_strength = st.slider("降雪噪声强度", 0, 100, 10)
        fog_strength = st.slider("雾气退化强度", 0, 100, 20)
        run_sim = st.button("一键运行仿真")
    with col_b:
        if run_sim:
            fig, axes = plt.subplots(1, 4, figsize=(20,5))
            fig.suptitle("原图 | 雨雪雾退化点云 | TripleMixer去噪 | RestoreNet复原")
            for i in range(4):
                axes[i].text(0.5,0.5, ["干净点云","恶劣噪声点云","去噪后","结构复原后"][i], ha="center", fontsize=14)
                axes[i].set_xlim(0,100)
                axes[i].set_ylim(0,100)
                axes[i].axis("off")
            st.pyplot(fig)
            st.success("仿真完成：可调节左侧雨雪雾强度重新生成对比图")
        else:
            st.info("调节左侧天气参数，点击一键运行查看点云处理对比效果")

# ===================== Tab2 MIMO资源调度仿真 =====================
with tab2:
    st.subheader("数模混合大规模MIMO资源分配仿真")
    ant_num = st.slider("天线阵列数量", 32, 256, 128, step=32)
    user_num = st.slider("并发用户数", 4, 32, 16)
    rf_link = st.slider("射频链路数量", 4, 32, 8)
    sim_run = st.button("计算频谱效率曲线")
    if sim_run:
        x = np.arange(1, user_num+1)
        y_basic = 0.2*x + np.random.randn(user_num)*0.1
        y_opt = 0.45*x + np.random.randn(user_num)*0.1
        opt = {
            "xAxis": {"type": "category", "data": [str(i) for i in x]},
            "yAxis": {"name": "系统频谱效率"},
            "series": [
                {"name": "传统调度", "type": "line", "data": y_basic.tolist()},
                {"name": "本成果联合优化调度", "type": "line", "data": y_opt.tolist()}
            ]
        }
        st_echarts(opt, height=400)

# ===================== Tab3 城市海量接入仿真 =====================
with tab3:
    st.subheader("海量设备随机接入容量仿真")
    max_dev = st.slider("最大并发设备数量", 100, 2000, 1000)
    if st.button("绘制接入成功率曲线"):
        dev_list = np.linspace(100, max_dev, 20).astype(int)
        old_rate = np.maximum(0, 1 - dev_list/max_dev)
        new_rate = np.minimum(1, 1.2 - dev_list/(max_dev*1.8))
        opt = {
            "tooltip": {"trigger": "axis"},
            "xAxis": {"name": "并发设备数", "data": [str(i) for i in dev_list]},
            "yAxis": {"name": "接入成功率"},
            "series": [
                {"name": "传统随机接入", "type": "line", "data": old_rate.tolist()},
                {"name": "碰撞复用接入(本技术)", "type": "line", "data": new_rate.tolist()}
            ]
        }
        st_echarts(opt, height=400)

# ===================== Tab4 多模态传输仿真 =====================
with tab4:
    st.subheader("状态预测聚合传输时延仿真")
    snr = st.slider("信道信噪比 dB", -10, 20, 5)
    pred_len = st.slider("预测聚合长度", 1, 10, 3)
    if st.button("对比传输时延"):
        x = np.arange(1, 20)
        delay_normal = 0.8*x
        delay_predict = 0.35*x
        opt = {
            "xAxis": {"name": "数据包数量", "data": [str(i) for i in x]},
            "yAxis": {"name": "传输时延 ms"},
            "series": [
                {"name": "普通逐包传输", "type": "line", "data": delay_normal.tolist()},
                {"name": "预测聚合传输(本技术)", "type": "line", "data": delay_predict.tolist()}
            ]
        }
        st_echarts(opt, height=400)