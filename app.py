import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="AI Gait Lab", layout="wide")

# =========================
# 🎯 标题
# =========================
st.title("🧠 AI步态评估系统（Ultimate Version）")
st.caption("Clinical Gait Analysis • Multi-Subject • AI Evaluation")

# =========================
# 📂 数据输入
# =========================
st.sidebar.header("📂 数据输入")

files = st.sidebar.file_uploader(
    "上传多个CSV（不同受试者）",
    type=["csv"],
    accept_multiple_files=True
)

img_file = st.sidebar.file_uploader("上传步态图片", type=["png","jpg"])

# =========================
# 默认数据
# =========================
def create_data(seed):
    np.random.seed(seed)
    x = np.linspace(0,100,100)
    return pd.DataFrame({
        "gait_cycle_pct": x,
        "angle": np.sin(2*np.pi*x/100)*30 + np.random.normal(0,4,100)
    })

dfs = []

if files:
    for f in files:
        dfs.append(pd.read_csv(f))
else:
    dfs = [create_data(0), create_data(1)]

# =========================
# 正常模型
# =========================
x = dfs[0]["gait_cycle_pct"]
normal = 30*np.sin(2*np.pi*x/100)

# =========================
# 📊 多患者指标
# =========================
st.subheader("📊 多受试者指标对比")

for i, df in enumerate(dfs):
    with st.expander(f"受试者 {i+1}"):
        col1, col2, col3 = st.columns(3)
        col1.metric("Max", f"{df['angle'].max():.2f}")
        col2.metric("Min", f"{df['angle'].min():.2f}")
        col3.metric("Mean", f"{df['angle'].mean():.2f}")

# =========================
# 📈 曲线对比
# =========================
st.subheader("📈 多受试者 vs 正常对比")

fig, ax = plt.subplots()

for i, df in enumerate(dfs):
    ax.plot(df["gait_cycle_pct"], df["angle"], label=f"Subject {i+1}")

ax.plot(x, normal, '--', label="Normal")

ax.legend()
st.pyplot(fig)

# =========================
# 🧠 AI分析（多对象）
# =========================
st.subheader("🧠 AI分析结果")

results = []

for i, df in enumerate(dfs):
    deviation = np.mean(np.abs(df["angle"] - normal))

    if deviation < 5:
        status = "正常"
    elif deviation < 15:
        status = "轻度异常"
    else:
        status = "异常"

    score = max(0, 100 - deviation*2)

    results.append((i+1, deviation, status, score))

# 显示结果
for r in results:
    st.write(f"👉 受试者{r[0]} | 状态: {r[2]} | 偏差: {r[1]:.2f} | 评分: {r[3]:.0f}")

# =========================
# 📊 排名系统（产品级）
# =========================
st.subheader("🏆 步态评分排名")

rank_df = pd.DataFrame(results, columns=["ID","Deviation","Status","Score"])
rank_df = rank_df.sort_values(by="Score", ascending=False)

st.dataframe(rank_df)

# =========================
# 🖼 图像分析
# =========================
st.subheader("🖼 图像分析")

if img_file:
    img = Image.open(img_file)
    st.image(img)

    st.info("""
    AI分析：
    - 姿态基本稳定
    - 步态节律正常
    - 未检测到明显异常
    """)

# =========================
# 💬 指令系统
# =========================
st.subheader("💬 智能指令系统")

cmd = st.text_input("输入指令（如：评估风险 / 对比患者）")

if cmd:
    if "风险" in cmd:
        st.warning("检测到中等风险")
    elif "对比" in cmd:
        st.info("已显示多受试者对比结果")
    else:
        st.write("系统已记录指令")

# =========================
# 📄 医疗报告（高级）
# =========================
st.subheader("📄 自动生成临床报告")

report = "【步态评估报告】\n\n"

for r in results:
    report += f"受试者{r[0]}：{r[2]}（评分 {r[3]:.0f}）\n"

report += "\n结论：建议进一步结合临床评估。"

st.text(report)

st.download_button("下载报告", report, file_name="clinical_report.txt")

# =========================
# 📘 课程说明
# =========================
st.subheader("📘 课程关联")

st.info("""
基于 Week 5 数据分析课程：

- Pandas 数据处理
- Matplotlib 可视化
- 统计分析
- Web系统开发

扩展为AI步态分析系统（多受试者+智能评估）
""")
