import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="步态分析系统", layout="wide")

st.title("🧠 步态分析系统")

# 读取数据
df = pd.read_csv("gait_joint_angles.csv")

# ===== 指标卡 =====
st.subheader("📊 核心指标")

col1, col2, col3 = st.columns(3)

col1.metric("最大膝关节角度", f"{df.iloc[:,2].max():.2f}")
col2.metric("最小膝关节角度", f"{df.iloc[:,2].min():.2f}")
col3.metric("平均膝关节角度", f"{df.iloc[:,2].mean():.2f}")

# ===== 数据展示 =====
st.subheader("📄 数据预览")
st.dataframe(df.head())

# ===== 曲线图 =====
st.subheader("📈 步态曲线")

fig, ax = plt.subplots()
ax.plot(df.iloc[:, 0], df.iloc[:, 2])
ax.set_xlabel("步态周期 (%)")
ax.set_ylabel("膝关节角度")
ax.set_title("膝关节运动曲线")

st.pyplot(fig)
