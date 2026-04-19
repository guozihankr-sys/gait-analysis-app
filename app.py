import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="步态分析系统（高级版）", layout="wide")

st.title("🚀 步态分析系统（增强版）")
st.markdown("基于关节角度数据的智能步态分析")

@st.cache_data
def load_data():
    return pd.read_csv("gait_joint_angles.csv")

df = load_data()

# ======================
# 侧边栏
# ======================
st.sidebar.header("⚙️ 参数选择")
columns = [col for col in df.columns if col != "gait_cycle_pct"]
selected_col = st.sidebar.selectbox("选择分析关节", columns)

data = df[selected_col]

# ======================
# 核心指标
# ======================
st.subheader("📊 核心指标")

col1, col2, col3 = st.columns(3)

max_val = data.max()
min_val = data.min()
mean_val = data.mean()
range_val = max_val - min_val

col1.metric("最大值", f"{max_val:.2f}")
col2.metric("最小值", f"{min_val:.2f}")
col3.metric("平均值", f"{mean_val:.2f}")

# ======================
# 数据预览
# ======================
with st.expander("📋 查看原始数据"):
    st.dataframe(df)

# ======================
# 曲线
# ======================
st.subheader("📈 步态曲线")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["gait_cycle_pct"], data)
ax.set_xlabel("Gait Cycle (%)")
ax.set_ylabel(selected_col)
ax.set_title(f"{selected_col} Curve")
ax.grid(True)

st.pyplot(fig)

# ======================
# 高级分析
# ======================
st.subheader("🧠 智能分析报告")

# 正常范围（可根据文献改）
NORMAL_RANGE = {
    "hip_flexion_deg": (30, 60),
    "knee_flexion_deg": (0, 70),
    "ankle_dorsiflexion_deg": (-10, 20)
}

score = 100
analysis = []

# 1. 活动范围分析
if range_val < 30:
    score -= 20
    analysis.append("关节活动范围偏小，可能存在僵硬或受限")
elif range_val > 90:
    score -= 10
    analysis.append("关节活动范围较大，可能存在不稳定")
else:
    analysis.append("关节活动范围正常")

# 2. 对称性分析
if abs(mean_val) > 5:
    score -= 15
    analysis.append("运动存在明显偏移，可能对称性不足")
else:
    analysis.append("运动基本对称")

# 3. 峰值分析
if max_val < 20:
    score -= 10
    analysis.append("峰值较低，动力输出可能不足")
elif max_val > 80:
    score -= 10
    analysis.append("峰值过高，可能存在异常负荷")
else:
    analysis.append("峰值在合理范围")

# ======================
# 打分展示
# ======================
st.metric("综合评分", f"{score}/100")

if score > 85:
    st.success("步态表现优秀")
elif score > 70:
    st.info("步态基本正常")
else:
    st.warning("步态可能存在异常")

# ======================
# 分析文本
# ======================
st.markdown("### 📋 分析结论")

for item in analysis:
    st.write(f"- {item}")

# ======================
# AI风格总结（重点🔥）
# ======================
st.markdown("### 🤖 综合评价")

summary = f"""
该受试者在 {selected_col} 指标上表现为：

- 最大值 {max_val:.2f}°
- 最小值 {min_val:.2f}°
- 平均值 {mean_val:.2f}°

综合评分为 {score}/100。

整体来看，{'步态稳定性良好' if score > 80 else '存在一定异常特征'}，
建议结合临床或更多数据进一步评估。
"""

st.info(summary)
