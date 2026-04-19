import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 页面配置
st.set_page_config(page_title="步态分析系统", layout="wide")

# 标题
st.title("🚶 步态分析仪表盘")
st.markdown("**基于关节角度数据的步态可视化分析**")

# =========================
# 读取数据（防报错版本）
# =========================
DATA_PATH = "gait_joint_angles.csv"

if not os.path.exists(DATA_PATH):
    st.error("❌ 数据文件缺失，请检查 GitHub 仓库是否包含 gait_joint_angles.csv")
    st.stop()

df = pd.read_csv(DATA_PATH)

# =========================
# 侧边栏参数选择
# =========================
st.sidebar.header("⚙️ 参数选择")

columns = df.columns.tolist()

# 默认去掉 gait_cycle_pct
feature_cols = [col for col in columns if col != "gait_cycle_pct"]

selected_col = st.sidebar.selectbox(
    "选择分析关节",
    feature_cols
)

# =========================
# 核心指标
# =========================
st.subheader("📊 核心指标")

col1, col2, col3 = st.columns(3)

max_val = df[selected_col].max()
min_val = df[selected_col].min()
mean_val = df[selected_col].mean()

col1.metric("最大值", f"{max_val:.2f}")
col2.metric("最小值", f"{min_val:.2f}")
col3.metric("平均值", f"{mean_val:.2f}")

# =========================
# 数据预览（可展开）
# =========================
with st.expander("📄 查看原始数据"):
    st.dataframe(df)

# =========================
# 步态曲线
# =========================
st.subheader("📈 步态曲线")

fig, ax = plt.subplots()

ax.plot(df["gait_cycle_pct"], df[selected_col])
ax.set_xlabel("Gait Cycle (%)")
ax.set_ylabel(selected_col)
ax.set_title(f"{selected_col} Curve")

st.pyplot(fig)

# =========================
# 快速图（更好看一点）
# =========================
st.subheader("⚡ 快速趋势图")

st.line_chart(df.set_index("gait_cycle_pct")[selected_col])

# =========================
# 简单分析（自动）
# =========================
st.subheader("🧠 简单分析")

if max_val < 40:
    st.warning("关节活动范围偏小，可能存在活动受限")
elif max_val > 80:
    st.warning("关节活动范围较大，需注意稳定性")
else:
    st.success("关节活动范围正常")

if abs(mean_val) < 1:
    st.info("整体运动趋势较为平衡")
