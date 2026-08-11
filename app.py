import streamlit as st
import json
from streamlit_echarts import st_echarts

# ========== 页面基础配置 ==========
st.set_page_config(
    page_title="朱旭教授课题组科研成果平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 全局CSS｜字节/抖音现代简约风格 ==========
st.markdown("""
<style>
* {
    box-sizing: border-box;
}
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    color: #161823;
    background-color: #ffffff;
}
h1 {
    font-size: 36px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    margin: 12px 0 6px 0 !important;
    color: #0F172A !important;
}
h2 {
    font-size: 28px !important;
    font-weight: 600 !important;
    color: #0F172A !important;
    margin: 8px 0 !important;
}
h3 {
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #1E293B !important;
}
.subtitle-desc {
    font-size: 18px;
    color: #64748B;
    border-left: 4px solid #2563EB;
    padding-left: 16px;
    margin: 16px 0 32px 0;
    line-height: 1.6;
}
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.06);
    border: 1px solid #F1F5F9;
    transition: all 0.28s ease-in-out;
    margin-bottom: 24px;
}
.card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08), 0 12px 24px rgba(0,0,0,0.07);
    transform: translateY(-3px);
}
.metric-card {
    background: linear-gradient(145deg, #F8FAFC, #FFFFFF);
    border-radius: 16px;
    padding: 30px 16px;
    text-align: center;
    border: 1px solid #E2E8F0;
    height: 100%;
    transition: 0.28s ease;
}
.metric-card:hover {
    border-color: #2563EB;
}
.metric-label {
    font-size: 16px;
    color: #64748B;
    margin-bottom: 10px;
}
.metric-value {
    font-size: 42px;
    font-weight: 700;
    color: #2563EB;
}
.divider-line{
    width:100%;
    height:1px;
    background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
    margin:40px 0;
}
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: none !important;
}
.footer {
    margin-top: 60px;
    padding-top: 24px;
    border-top: 1px solid #E2E8F0;
    text-align: center;
    font-size: 14px;
    color: #94A3B8;
}
.block-container {
    padding-top: 24px !important;
    padding-left: 4rem !important;
    padding-right: 4rem !important;
}
</style>
""", unsafe_allow_html=True)

# ========== 加载成果JSON数据 ==========
with open("data/papers.json", "r", encoding="utf-8") as f:
    paper_data = json.load(f)

# ========== 头部区域 ==========
st.title("朱旭教授课题组 | 科研成果一体化展示与仿真平台")
st.markdown(
    '<div class="subtitle-desc">研究方向：车载激光雷达环境感知 · 6G大规模MIMO通信 · 数字孪生城市智能互联</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

# ========== 负责人简介卡片（修复空白框BUG） ==========
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 2.5])
with col1:
    st.subheader("课题组负责人")
    st.markdown('<div style="font-size:24px;font-weight:700;color:#0F172A;">朱旭 教授</div>', unsafe_allow_html=True)
with col2:
    st.markdown("""
    - 国家青年高层次人才、深圳市鹏城学者特聘教授
    - 哈尔滨工业大学（深圳）信息科学与工程学院副院长
    - IEEE杰出讲师、无线智联网通信重点实验室主任
    - 曾任英国利物浦大学电气与电子工程终身教职（Reader）
    - 发表高水平论文340+篇，授权专利18项；主持国家重点研发计划、国家自然科学基金等纵向项目40余项
    """)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

# ========== 成果统计看板 ==========
st.header("核心技术成果总览")
cnt_lidar = sum(1 for item in paper_data if item.get("direction","").startswith("车载感知"))
cnt_mimo = sum(1 for item in paper_data if item.get("direction","").startswith("6G大规模MIMO"))
cnt_total = len(paper_data)

stat_cols = st.columns(3)
with stat_cols[0]:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">车载激光雷达感知成果</div>
        <div class="metric-value">{cnt_lidar}</div>
    </div>
    ''', unsafe_allow_html=True)
with stat_cols[1]:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">6G大规模MIMO通信成果</div>
        <div class="metric-value">{cnt_mimo}</div>
    </div>
    ''', unsafe_allow_html=True)
with stat_cols[2]:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-label">全部核心技术成果总数</div>
        <div class="metric-value">{cnt_total}</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

# ========== 应用领域饼图【图例移动到底部横向排布】 ==========
st.subheader("成果应用领域分布")
echart_option = {
    "tooltip": {"trigger": "item"},
    "legend": {
        "orient": "horizontal",
        "bottom": "0%",
        "textStyle": {"fontSize":14}
    },
    "series": [
        {
            "type": "pie",
            "radius": ["45%", "75%"],
            "center": ["50%", "38%"],
            "data": [
                {"name": "自动驾驶/车路协同", "value": 3},
                {"name": "5G/6G移动通信基站", "value": 2},
                {"name": "数字孪生/智慧城市", "value": 2},
                {"name": "低空经济/空地协同通信", "value": 2},
                {"name": "工业互联网智能制造", "value": 2},
            ],
            "color": ["#2563EB", "#3B82F6", "#60A5FA", "#93C5FD", "#BFDBFE"]
        }
    ],
}
st_echarts(options=echart_option, height="460px")

st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

# ========== 导航指引卡片 ==========
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("成果浏览与仿真入口")
st.info("""
使用页面左侧侧边栏导航菜单快速访问：
✅ 五大核心技术成果详情展示
✅ 成果推介文档资料库
✅ 交互式算法仿真演示平台
""")
st.markdown('</div>', unsafe_allow_html=True)

# ========== 底部版权信息 ==========
st.markdown('''
<div class="footer">
© 2026 哈尔滨工业大学（深圳）朱旭教授课题组 · 科研成果一体化展示平台
</div>
''', unsafe_allow_html=True)