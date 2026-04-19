import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 页面标题
st.title("步态分析系统")
st.write("基于关节角度数据的步态可视化分析")

# 读取数据（⚠️ 文件必须和 app.py 在同一目录）
df = pd.read_csv("gait_joint_angles.csv")

# 侧边栏参数选择
st.sidebar.header("⚙️ 参数选择")
column = st.sidebar.selectbox("选择分析关节", df.columns[1:])

# ===== 核心指标 =====
max_val = df[column].max()
min_val = df[column].min()
mean_val = df[column].mean()

st.subheader("📊 核心指标")
col1, col2, col3 = st.columns(3)
col1.metric("最大值", f"{max_val:.2f}")
col2.metric("最小值", f"{min_val:.2f}")
col3.metric("平均值", f"{mean_val:.2f}")

# ===== 数据预览 =====
st.subheader("📋 数据预览")
st.dataframe(df.head())

# ===== 步态曲线 =====
st.subheader("📈 步态曲线")

fig, ax = plt.subplots()
ax.plot(df["gait_cycle_pct"], df[column])

ax.set_xlabel("Gait Cycle (%)")
ax.set_ylabel(column)
ax.set_title(f"{column} Curve")

st.pyplot(fig)

# （加分项）快速图
st.subheader("⚡ 快速图")
st.line_chart(df.set_index("gait_cycle_pct")[column])

# ===== 简单分析 =====
st.subheader("🧠 简单分析")

if max_val > 40:
    st.warning("关节活动范围较大，可能存在代偿运动")
elif min_val < -30:
    st.warning("关节活动角度偏低，可能存在活动受限")
else:
    st.success("步态参数在正常范围内")
