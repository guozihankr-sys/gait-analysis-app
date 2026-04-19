import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="步态分析系统", layout="wide")

# ===== 标题 =====
st.title("🚶 步态分析仪表盘（最终答辩版）")
st.caption("Clinical Gait Analysis · AI Evaluation System")

# ===== 左侧输入 =====
st.sidebar.header("📂 数据输入")

file1 = st.sidebar.file_uploader("上传受试者1 CSV", type=["csv"])
file2 = st.sidebar.file_uploader("上传受试者2 CSV（可选）", type=["csv"])
image_file = st.sidebar.file_uploader("上传步态图片", type=["png", "jpg", "jpeg"])

st.sidebar.header("🧠 指令系统")
command = st.sidebar.text_input("输入指令（如：分析 / 对比 / 报告）")

# ===== 工具函数 =====
def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except:
        return None

def analyze(df):
    if "hip_flexion_deg" in df.columns:
        data = df["hip_flexion_deg"]
        mean = data.mean()
        deviation = abs(mean)

        score = max(60, 100 - deviation * 2)

        if deviation < 5:
            status = "正常"
        elif deviation < 15:
            status = "轻微异常"
        else:
            status = "异常"

        return status, deviation, score
    return "未知", 0, 0

# ===== 主界面 =====

# 如果没有数据 → 显示说明
if file1 is None:
    st.info("👈 请在左侧上传CSV数据开始分析")

    st.subheader("📘 项目说明")
    st.write("""
    本系统基于 Week5 数据分析课程开发，结合 Pandas 与可视化技术，实现：
    
    - 多受试者步态分析
    - 曲线可视化
    - AI智能评估
    - 图像辅助分析
    - 指令驱动系统
    
    支持电脑 / 手机 / 平板访问
    """)

else:
    df1 = load_data(file1)
    df2 = load_data(file2) if file2 else None

    st.subheader("📊 步态曲线分析")

    fig, ax = plt.subplots()

    if df1 is not None and "hip_flexion_deg" in df1.columns:
        ax.plot(df1["hip_flexion_deg"], label="Subject 1")

    if df2 is not None and "hip_flexion_deg" in df2.columns:
        ax.plot(df2["hip_flexion_deg"], label="Subject 2")

    # 正常参考曲线（模拟）
    normal = 30 * np.sin(np.linspace(0, 2*np.pi, 100))
    ax.plot(normal, linestyle="--", label="Normal")

    ax.set_title("Gait Curve Comparison")
    ax.legend()

    st.pyplot(fig)

    # ===== AI分析 =====
    st.subheader("🧠 AI分析结果")

    status1, dev1, score1 = analyze(df1)

    st.write(f"👉 受试者1：状态={status1} | 偏差={dev1:.2f} | 评分={score1:.1f}")

    if df2 is not None:
        status2, dev2, score2 = analyze(df2)
        st.write(f"👉 受试者2：状态={status2} | 偏差={dev2:.2f} | 评分={score2:.1f}")

    # ===== 排名 =====
    st.subheader("🏆 步态评分排名")

    results = [
        {"ID": "1", "Score": score1}
    ]

    if df2 is not None:
        results.append({"ID": "2", "Score": score2})

    result_df = pd.DataFrame(results).sort_values(by="Score", ascending=False)
    st.dataframe(result_df)

    # ===== 图像分析 =====
    if image_file:
        st.subheader("🖼 图像分析")
        img = Image.open(image_file)
        st.image(img, caption="上传的步态图像", use_container_width=True)
        st.success("图像已加载，可用于辅助分析（演示功能）")

    # ===== 指令系统 =====
    if command:
        st.subheader("💬 指令响应")

        if "报告" in command:
            report = f"""
【步态分析报告】

受试者1：{status1}（评分 {score1:.1f}）

结论：建议进一步临床评估或保持当前状态。
"""
            st.text(report)

        elif "对比" in command and df2 is not None:
            st.success("已完成两受试者对比分析")

        else:
            st.warning("指令已接收（支持：分析 / 对比 / 报告）")
