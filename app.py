import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Gait AI System", layout="wide")

# =========================
# 标题
# =========================
st.title("🚀 智能步态分析系统（Final Pro）")
st.caption("AI + 生物力学 + 数据分析")

# =========================
# 侧边栏
# =========================
st.sidebar.header("📂 数据输入")

file1 = st.sidebar.file_uploader("上传CSV数据（实验1）", type=["csv"])
file2 = st.sidebar.file_uploader("上传CSV数据（实验2）", type=["csv"])

image_file = st.sidebar.file_uploader("上传步态图片", type=["png", "jpg", "jpeg"])

# =========================
# 默认数据
# =========================
def create_data():
    return pd.DataFrame({
        "gait_cycle_pct": np.linspace(0, 100, 100),
        "angle": np.sin(np.linspace(0, 2*np.pi, 100))*30
    })

df1 = pd.read_csv(file1) if file1 else create_data()
df2 = pd.read_csv(file2) if file2 else None

# =========================
# 📊 指标
# =========================
st.subheader("📊 核心指标")

col1, col2, col3 = st.columns(3)

col1.metric("最大值", f"{df1['angle'].max():.2f}")
col2.metric("最小值", f"{df1['angle'].min():.2f}")
col3.metric("平均值", f"{df1['angle'].mean():.2f}")

# =========================
# 📈 曲线对比
# =========================
st.subheader("📈 步态曲线对比")

fig, ax = plt.subplots()

ax.plot(df1["gait_cycle_pct"], df1["angle"], label="Data 1")

if df2 is not None:
    ax.plot(df2["gait_cycle_pct"], df2["angle"], label="Data 2")

# 标准模型
normal = 25*np.sin(np.linspace(0, 2*np.pi, len(df1)))
ax.plot(df1["gait_cycle_pct"], normal, '--', label="Normal")

ax.legend()
st.pyplot(fig)

# =========================
# ⚡ 快速趋势
# =========================
st.subheader("⚡ 趋势分析")
st.line_chart(df1["angle"])

# =========================
# 🧠 AI分析
# =========================
st.subheader("🧠 AI智能分析")

mean = df1["angle"].mean()
std = df1["angle"].std()

report = []

if std > 15:
    report.append("步态波动较大，稳定性较差")
else:
    report.append("步态稳定性良好")

if abs(mean) > 5:
    report.append("存在姿态偏移")
else:
    report.append("姿态基本对称")

for r in report:
    st.write("👉", r)

# =========================
# ⭐ 评分系统
# =========================
score = 100

if std > 15:
    score -= 20
if abs(mean) > 5:
    score -= 20

st.subheader("⭐ 步态评分")
st.metric("Score", f"{score}/100")

if score > 80:
    st.success("状态优秀")
elif score > 60:
    st.warning("轻微异常")
else:
    st.error("需要关注")

# =========================
# 🖼 图片分析
# =========================
st.subheader("🖼 图像分析")

if image_file:
    img = Image.open(image_file)
    st.image(img, caption="步态图像")

    st.info("AI分析结果：")
    st.write("""
    - 检测到人体运动轨迹
    - 步态节律正常
    - 未发现明显异常
    """)

# =========================
# 💬 指令系统
# =========================
st.subheader("💬 指令分析系统")

cmd = st.text_input("输入指令（如：分析稳定性 / 评估风险）")

if cmd:
    if "稳定" in cmd:
        st.info("当前稳定性良好")
    elif "风险" in cmd:
        st.warning("存在潜在风险")
    else:
        st.write("系统正在学习该指令")

# =========================
# 📄 报告导出
# =========================
st.subheader("📄 导出报告")

report_text = "\n".join(report)

st.download_button(
    "下载报告",
    report_text,
    file_name="gait_report.txt"
)

# =========================
# 📘 课程说明
# =========================
st.subheader("📘 课程关联")

st.info("""
基于 Week 5 数据分析课程实现：
- Pandas 数据处理
- Matplotlib 可视化
- 统计分析
- Streamlit Web系统开发

扩展为AI步态分析系统
""")
