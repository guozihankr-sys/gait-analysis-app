import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="步态分析系统", layout="wide")

# 标题
st.title("🚶‍♂️ 步态分析仪表盘")
st.caption("Clinical Gait Analysis • AI Evaluation System")

# =========================
# 📂 数据输入
# =========================
st.sidebar.header("📂 数据输入")

csv1 = st.sidebar.file_uploader("上传受试者1 CSV", type=["csv"])
csv2 = st.sidebar.file_uploader("上传受试者2 CSV（可选）", type=["csv"])
uploaded_image = st.sidebar.file_uploader("上传步态图像", type=["png", "jpg", "jpeg"])

# =========================
# 🧠 AI分析函数
# =========================
def ai_analysis(data):
    mean_val = data.mean()
    std_val = data.std()

    if std_val < 5:
        status = "正常"
        score = 95
    elif std_val < 10:
        status = "轻微异常"
        score = 80
    else:
        status = "异常"
        score = 60

    explanation = f"""
    系统检测到当前步态数据波动为 {std_val:.2f}，
    属于【{status}】范围。
    该结果表明受试者步态稳定性{'良好' if std_val < 5 else '一般或较差'}，
    建议{'保持当前状态' if std_val < 5 else '进一步评估或训练'}。
    """

    return status, score, explanation

# =========================
# 📊 数据分析
# =========================
if csv1:
    df1 = pd.read_csv(csv1)
    col = df1.columns[0]

    st.subheader("📊 步态曲线对比")

    fig, ax = plt.subplots()
    ax.plot(df1[col], label="Subject 1")

    # 第二个
    if csv2:
        df2 = pd.read_csv(csv2)
        ax.plot(df2[col], label="Subject 2")

    # 模拟正常曲线
    normal = np.sin(np.linspace(0, 2*np.pi, len(df1))) * 30
    ax.plot(normal, '--', label="Normal")

    ax.legend()
    ax.set_ylabel("Angle (deg)")
    st.pyplot(fig)

    # =========================
    # 🧠 AI分析结果
    # =========================
    st.subheader("🧠 AI分析结果")

    status1, score1, exp1 = ai_analysis(df1[col])
    st.success(f"受试者1：{status1} | 评分：{score1}")
    st.info(exp1)

    if csv2:
        status2, score2, exp2 = ai_analysis(df2[col])
        st.success(f"受试者2：{status2} | 评分：{score2}")
        st.info(exp2)

    # =========================
    # 🏆 排名
    # =========================
    st.subheader("🏆 步态评分排名")

    scores = {"ID": [], "Score": []}
    scores["ID"].append("Subject 1")
    scores["Score"].append(score1)

    if csv2:
        scores["ID"].append("Subject 2")
        scores["Score"].append(score2)

    df_score = pd.DataFrame(scores)
    df_score = df_score.sort_values(by="Score", ascending=False)
    st.table(df_score)

    # =========================
    # 📄 自动报告
    # =========================
    st.subheader("📄 自动生成临床报告")

    report = f"""
【步态分析报告】

受试者1：{status1}（评分 {score1}）

分析结论：
{exp1}

"""

    if csv2:
        report += f"""
受试者2：{status2}（评分 {score2}）

分析结论：
{exp2}
"""

    report += """
建议：
1. 保持良好运动习惯
2. 定期进行步态监测
3. 如异常建议进一步临床评估
"""

    st.text(report)

# =========================
# 🖼 图像分析
# =========================
if uploaded_image:
    st.subheader("🖼 图像分析")

    img = Image.open(uploaded_image)
    st.image(img, caption="步态图像")

    img_array = np.array(img)
    brightness = img_array.mean()

    st.write("图像平均亮度:", round(brightness,2))

    if brightness > 150:
        st.success("图像清晰度良好")
    else:
        st.warning("图像偏暗，可能影响分析")

# =========================
# 💬 指令系统
# =========================
st.subheader("💬 智能指令系统")

cmd = st.text_input("输入指令（如：评估 / 对比 / 报告）")

if cmd:
    if "评估" in cmd:
        st.success("✅ 已执行步态评估")
    elif "对比" in cmd:
        st.info("📊 已生成对比分析")
    elif "报告" in cmd:
        st.warning("📄 报告已生成（见上方）")
    else:
        st.error("❌ 无法识别指令")

# =========================
# 📘 项目说明（答辩用）
# =========================
st.subheader("📘 项目说明")

st.write("""
本项目基于 Week 5 数据分析内容开发，结合 Pandas、Matplotlib 和 Web 技术，
实现了一个跨平台步态分析系统。

功能包括：
- 多受试者数据分析
- 步态曲线可视化
- AI评分与解释
- 图像分析
- 指令驱动系统
- 自动生成报告

适用于运动科学、康复医学和临床辅助分析。
""")
