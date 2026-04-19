import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="步态分析系统", layout="wide")

# ===== 标题 =====
st.title("🧠 步态分析系统")
st.markdown("基于关节角度数据的步态可视化分析")

# ===== 读取数据 =====
df = pd.read_csv("gait_joint_angles.csv")

# ===== 选择关节 =====
st.sidebar.title("⚙️ 参数选择")
joint = st.sidebar.selectbox(
    "选择分析关节",
    ["hip_flexion_deg", "knee_flexion_deg", "ankle_dorsiflexion_deg"]
)

# ===== 指标 =====
st.subheader("📊 核心指标")

col1, col2, col3 = st.columns(3)

col1.metric("最大值", f"{df[joint].max():.2f}")
col2.metric("最小值", f"{df[joint].min():.2f}")
col3.metric("平均值", f"{df[joint].mean():.2f}")

# ===== 数据 =====
with st.expander("📄 查看原始数据"):
    st.dataframe(df)

# ===== 曲线图 =====
st.subheader("📈 步态曲线")

fig, ax = plt.subplots()

ax.plot(df["gait_cycle_pct"], df[joint], linewidth=2)

ax.set_xlabel("步态周期 (%)")
ax.set_ylabel("角度 (deg)")
ax.set_title(f"{joint} 曲线")

ax.grid(True)

st.pyplot(fig)

# ===== 简单判断 =====
st.subheader("🧠 简单分析")

if df[joint].mean() > 30:
    st.success("步态偏大（可能活动幅度较大）")
elif df[joint].mean() < 10:
    st.warning("步态偏小（可能活动受限）")
else:
    st.info("步态在正常范围内")
