import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Exercise Dashboard", page_icon="🏃", layout="wide")

# ===== Theme =====
st.markdown(
    """
    <style>
        :root {
            --bg: #07111f;
            --panel: #101d2d;
            --panel-raised: #142338;
            --line: rgba(157, 184, 216, 0.16);
            --text: #f1f6fd;
            --muted: #a9bbd0;
            --blue: #80cdf4;
            --blue-strong: #43a6df;
            --cyan: #58d5df;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: var(--bg);
            color: var(--text);
            font-family: "Segoe UI", "Noto Sans Thai", "Tahoma", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(ellipse at 80% 0%, rgba(35, 92, 137, 0.16), transparent 36%),
                linear-gradient(180deg, #091625 0%, #07111f 45%, #060f1b 100%);
        }

        .main .block-container {
            padding: 2rem clamp(1.25rem, 4vw, 3.5rem) 3rem;
            max-width: 1500px;
        }

        .stSidebar {
            background: #0c1725;
            border-right: 1px solid var(--line);
        }

        .stSidebar .block-container {
            padding: 1.5rem 1rem;
        }

        .sidebar-title {
            color: var(--text);
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        [data-testid="stSidebar"] label {
            color: #d5e2f1 !important;
            font-weight: 600;
        }

        [data-testid="stSidebar"] [data-baseweb="tag"],
        [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] {
            background: #245279 !important;
            border: 1px solid rgba(128, 205, 244, 0.3) !important;
            border-radius: 7px !important;
            color: #eff8ff !important;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #111f30;
            border-color: var(--line);
            border-radius: 10px;
        }

        .main-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin: 0 0 0.75rem;
            padding: 1.5rem 1.65rem;
            border: 1px solid rgba(128, 205, 244, 0.2);
            border-radius: 20px;
            background:
                linear-gradient(115deg, rgba(31, 77, 111, 0.58), rgba(16, 29, 45, 0.78) 58%),
                var(--panel);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
        }

        .icon-badge {
            width: 52px;
            height: 52px;
            flex: 0 0 52px;
            border-radius: 15px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(145deg, #66c9f3, #367fca);
            box-shadow: inset 0 1px rgba(255, 255, 255, 0.35), 0 8px 22px rgba(45, 137, 200, 0.25);
            font-size: 1.55rem;
        }

        h1 {
            font-size: clamp(1.8rem, 3.5vw, 2.65rem) !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em;
            color: var(--text) !important;
            margin: 0 !important;
            font-family: "Segoe UI", "Noto Sans Thai", "Tahoma", sans-serif;
        }

        .subtitle {
            font-size: 0.98rem;
            color: var(--muted);
            margin: 0.65rem 0 1.1rem;
            font-family: "Segoe UI", "Noto Sans Thai", "Tahoma", sans-serif;
        }

        .section-title {
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            color: var(--text) !important;
            margin: 1.8rem 0 0.8rem !important;
        }

        .stMetric {
            background: linear-gradient(145deg, rgba(20, 35, 56, 0.96), rgba(14, 27, 43, 0.96));
            border: 1px solid var(--line);
            border-radius: 15px;
            padding: 1rem 1.1rem;
            min-height: 112px;
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.14);
        }

        .stMetric [data-testid="stMetricValue"] {
            color: var(--text) !important;
            font-size: clamp(1.15rem, 2vw, 1.65rem) !important;
            font-weight: 700 !important;
            overflow-wrap: anywhere;
        }

        .stMetric [data-testid="stMetricLabel"] {
            color: var(--muted) !important;
            font-size: 0.86rem !important;
            font-weight: 600 !important;
        }

        .stDataFrame {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid var(--line);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 14px;
            overflow: hidden;
        }

        .stDownloadButton > button {
            background: linear-gradient(110deg, #338dc2, #3477ba) !important;
            border: 1px solid rgba(128, 205, 244, 0.35) !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            padding: 0.7rem 1.1rem !important;
            transition: filter 150ms ease, transform 150ms ease;
        }

        .stDownloadButton > button:hover {
            filter: brightness(1.12);
            transform: translateY(-1px);
        }

        [data-testid="stAlert"] {
            border-radius: 12px;
        }

        @media (max-width: 700px) {
            .main .block-container {
                padding: 1.1rem 1rem 2rem;
            }

            .main-header {
                padding: 1.1rem;
                border-radius: 16px;
            }

            .icon-badge {
                width: 44px;
                height: 44px;
                flex-basis: 44px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
    return df.dropna(subset=["year", "region", "exercise_type", "value"]).reset_index(drop=True)


df = load_data("datasport.csv.xlsx")

regions = sorted(df["region"].dropna().unique().tolist())
source_years = set(df["year"].dropna().astype(int).unique().tolist())
years = list(range(2547, 2555))
exercise_types = sorted(df["exercise_type"].dropna().unique().tolist())

with st.sidebar:
    st.markdown('<div class="sidebar-title">Filter ข้อมูล</div>', unsafe_allow_html=True)
    selected_years = st.multiselect("ปี", years, default=years)
    selected_regions = st.multiselect("ภาค", regions, default=regions)
    selected_exercise = st.multiselect("ประเภทการออกกำลังกาย", exercise_types, default=exercise_types)

filtered_df = df[
    df["year"].astype(int).isin(selected_years)
    & df["region"].isin(selected_regions)
    & df["exercise_type"].isin(selected_exercise)
].copy()

if filtered_df.empty:
    st.warning("ไม่มีข้อมูลในช่วงที่เลือก กรุณาเปลี่ยนตัวกรอง")
    st.stop()

filtered_df = filtered_df.sort_values(["year", "region", "exercise_type"]).reset_index(drop=True)

# ===== Header =====
st.markdown(
    """
    <div class="main-header">
        <span class="icon-badge">🏃</span>
        <h1>Exercise Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="subtitle">Dashboard การออกกำลังกาย</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">ใช้สำหรับวิเคราะห์ปริมาณคนที่ออกกำลังกาย ตามแต่ละปี/ภาค และ ประเภทการออกกำลังกาย</div>',
    unsafe_allow_html=True,
)

# ===== Metrics =====
summary_total = filtered_df["value"].sum()
summary_mean = filtered_df["value"].mean()
summary_max_region = filtered_df.groupby("region")["value"].sum().idxmax()
summary_max_year = filtered_df.groupby("year")["value"].sum().idxmax()
summary_top_type = filtered_df.groupby("exercise_type")["value"].sum().idxmax()

def fmt_num(value: float) -> str:
    return f"{value:,.1f}"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("คนที่เข้าร่วม", f"{fmt_num(summary_total)}")
with col2:
    st.metric("เฉลี่ยต่อปี", f"{fmt_num(summary_mean)}")
with col3:
    st.metric("ภาคที่สูงสุด", summary_max_region)

col4, col5 = st.columns(2)
with col4:
    st.metric("ปีสูงสุด", str(summary_max_year))
with col5:
    st.metric("ประเภทยอดนิยม", summary_top_type)

st.markdown("<hr style='border:1px solid rgba(255,255,255,.12); margin: 1.5rem 0 1rem 0'>", unsafe_allow_html=True)

# ===== Charts =====
def style_chart(chart):
    return (
        chart.configure(background="#101d2d")
        .configure_view(strokeOpacity=0)
        .configure_axis(
            gridColor="#26384d",
            domainColor="#40546c",
            tickColor="#40546c",
            labelColor="#c6d5e5",
            titleColor="#dce8f5",
            labelFont="Segoe UI",
            titleFont="Segoe UI",
        )
        .configure_legend(
            labelColor="#d4e1ef",
            titleColor="#e9f2fb",
            labelFont="Segoe UI",
            titleFont="Segoe UI",
        )
    )

st.markdown('<div class="section-title">ปริมาณการออกกำลังกายตามปี</div>', unsafe_allow_html=True)
yearly = (
    filtered_df.groupby("year")["value"]
    .sum()
    .rename("ปริมาณ")
    .rename_axis("year")
    .reset_index()
)
y_ticks = [0, 10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000, 50_000_000, 100_000_000]
yearly["ตำแหน่งแกน"] = np.interp(
    yearly["ปริมาณ"],
    y_ticks,
    range(len(y_ticks)),
)
tick_labels = [f"{tick:,}" for tick in y_ticks]

yearly_chart = style_chart(alt.Chart(yearly).mark_line(
    point=True,
    strokeWidth=3,
    color="#7ccaf3",
).encode(
    x=alt.X(
        "year:O",
        scale=alt.Scale(domain=selected_years),
        axis=alt.Axis(title="ปีพ.ศ.", labelAngle=0, values=selected_years, labelOverlap=False),
    ),
    y=alt.Y(
        "ตำแหน่งแกน:Q",
        scale=alt.Scale(domain=[0, len(y_ticks) - 1], nice=False),
        axis=alt.Axis(
            title="จำนวน (คน)",
            values=list(range(len(y_ticks))),
            labelExpr=f"{tick_labels}[round(datum.value)]",
            labelOverlap=False,
            labelLimit=140,
        ),
    ),
    tooltip=["year", "ปริมาณ"],
).properties(height=320))
st.altair_chart(yearly_chart, width="stretch")
missing_years = [year for year in selected_years if year not in source_years]
if missing_years:
    st.caption(
        "ปีที่ไม่มีข้อมูลในไฟล์ Excel: "
        + ", ".join(str(year) for year in missing_years)
        + " (กรุณาเลือกปีอื่นเพื่อดูข้อมูล)"
    )

st.markdown('<div class="section-title">สัดส่วนตามประเภทการออกกำลังกาย</div>', unsafe_allow_html=True)
donut_df = filtered_df.groupby("exercise_type", as_index=False)["value"].sum()
donut = style_chart(alt.Chart(donut_df).mark_arc(
    innerRadius=72,
    outerRadius=150,
    stroke="#091827",
    strokeWidth=2,
).encode(
    theta=alt.Theta(field="value", type="quantitative"),
    color=alt.Color(
        field="exercise_type",
        type="nominal",
        title="ประเภท",
        scale=alt.Scale(
            domain=sorted(donut_df["exercise_type"].unique().tolist()),
            range=[
                "#54b8df",
                "#55c5aa",
                "#e8b85e",
                "#9b91e8",
                "#ed8d8d",
                "#7fb4d8",
                "#d18fc1",
                "#9cac72",
                "#ed9b68",
                "#91a5bd",
                "#6ccec6",
                "#c3a377",
            ],
        ),
        legend=alt.Legend(orient="right"),
    ),
    tooltip=[
        alt.Tooltip("exercise_type:N", title="ประเภท"),
        alt.Tooltip("value:Q", title="จำนวน (คน)", format=",.1f"),
    ],
).properties(height=380))
st.altair_chart(donut, width="stretch")

# ===== Comparison charts =====
st.markdown('<div class="section-title">ปริมาณตามภาค</div>', unsafe_allow_html=True)
region_df = filtered_df.groupby("region", as_index=False)["value"].sum().sort_values("value", ascending=False)
region_colors = [
    "#59b8e5",
    "#58c6a8",
    "#efb75e",
    "#a494ee",
    "#ed8994",
    "#78a9df",
    "#d18fc1",
    "#9cac72",
    "#ed9b68",
    "#6ccec6",
]
region_chart = style_chart(alt.Chart(region_df).mark_bar(cornerRadiusEnd=5).encode(
    x=alt.X("value:Q", title="จำนวน (คน)"),
    y=alt.Y("region:N", sort="-x", title="ภาค"),
    color=alt.Color(
        "region:N",
        scale=alt.Scale(
            domain=sorted(region_df["region"].unique().tolist()),
            range=region_colors,
        ),
        legend=None,
    ),
    tooltip=[
        alt.Tooltip("region:N", title="ภาค"),
        alt.Tooltip("value:Q", title="จำนวน (คน)", format=",.1f"),
    ],
).properties(height=320))
st.altair_chart(region_chart, width="stretch")

st.markdown('<div class="section-title">ประเภทการออกกำลังกายที่ได้รับความนิยม</div>', unsafe_allow_html=True)
top_groups = filtered_df.groupby("exercise_type")["value"].sum().sort_values(ascending=False).head(10).reset_index()
top_groups.columns = ["ประเภท", "ปริมาณ"]
top_chart = style_chart(alt.Chart(top_groups).mark_bar(cornerRadiusEnd=5).encode(
    x=alt.X("ปริมาณ:Q", title="จำนวน (คน)"),
    y=alt.Y("ประเภท:N", sort="-x", title="ประเภท"),
    color=alt.Color(
        "ประเภท:N",
        scale=alt.Scale(
            domain=sorted(top_groups["ประเภท"].unique().tolist()),
            range=region_colors,
        ),
        legend=None,
    ),
    tooltip=[
        alt.Tooltip("ประเภท:N", title="ประเภท"),
        alt.Tooltip("ปริมาณ:Q", title="จำนวน (คน)", format=",.1f"),
    ],
).properties(height=360))
st.altair_chart(top_chart, width="stretch")

# ===== Data table =====
st.markdown('<div class="section-title">รายละเอียดข้อมูล</div>', unsafe_allow_html=True)

filtered_display = filtered_df[["year", "region", "exercise_type", "value", "unit", "source"]].copy()
filtered_display = filtered_display.rename(columns={
    "year": "ปี",
    "region": "ภาค",
    "exercise_type": "ประเภทการออกกำลังกาย",
    "value": "ปริมาณ (กก.)",
    "unit": "หน่วย",
    "source": "แหล่งข้อมูล",
})

st.dataframe(filtered_display, width="stretch", hide_index=True)

csv_data = filtered_display.to_csv(index=False).encode("utf-8")
st.download_button(
    label="ดาวน์โหลดข้อมูลทั้งหมด (CSV)",
    data=csv_data,
    file_name="dashboard_data.csv",
    mime="text/csv",
    type="primary",
)
