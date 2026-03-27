import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bird Species Observation Analysis",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>

/* ── FULL PAGE BACKGROUND ── */
.stApp {
    background: url("https://images.unsplash.com/photo-1501785888041-af3ef285b470") no-repeat center center fixed;
    background-size: cover;
}

/* Light overlay for readability */
[data-testid="stAppViewContainer"] {
    background: rgba(255, 255, 255, 0.85);
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e5631, #4c956c);
    color: white;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ── FIX INPUT BOX VISIBILITY (IMPORTANT) ── */
section[data-testid="stSidebar"] .stSelectbox div,
section[data-testid="stSidebar"] .stMultiSelect div,
section[data-testid="stSidebar"] .stTextInput div,
section[data-testid="stSidebar"] .stNumberInput div {
    background-color: white !important;
    color: black !important;
    border-radius: 8px;
}

/* Dropdown selected value */
section[data-testid="stSidebar"] .stSelectbox span,
section[data-testid="stSidebar"] .stMultiSelect span {
    color: black !important;
}

/* Dropdown menu options */
div[role="listbox"] {
    background-color: white !important;
    color: black !important;
}

/* Slider text fix */
section[data-testid="stSidebar"] .stSlider {
    color: white !important;
}

/* ── HEADER ── */
.main-header {
    background: linear-gradient(135deg, #1F4E79, #2E86AB);
    padding: 20px 30px;
    border-radius: 12px;
    color: white;
    margin-bottom: 25px;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 10px;
    border-left: 5px solid #2E86AB;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    text-align: center;
}

/* ── SECTION HEADERS ── */
.section-header {
    color: #1F4E79;
    border-bottom: 2px solid #2E86AB;
    padding-bottom: 6px;
    margin: 20px 0 15px 0;
}

/* ── FILTER LABELS ── */
.stSelectbox label, .stMultiSelect label {
    font-weight: 600;
    color: white !important;
}

/* ── OPTIONAL BOTTOM BIRDS ── */
body::before {
    content: "";
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 140px;
    background: url("https://i.imgur.com/6IUbEMk.png") no-repeat center bottom;
    background-size: cover;
    opacity: 0.9;
    z-index: 0;
    pointer-events: none;
}

</style>
""", unsafe_allow_html=True)
# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("bird_data.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month_Name"] = pd.Categorical(df["Month_Name"], categories=["May", "June", "July"], ordered=True)
    return df

df = load_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1997/1997007.png", width=60)
    st.markdown("## 🔽 Filters")
    st.markdown("---")

    habitat_options = ["All"] + sorted(df["Location_Type"].dropna().unique().tolist())
    selected_habitat = st.selectbox("🌿 Habitat Type", habitat_options)

    month_options = ["All"] + ["May", "June", "July"]
    selected_month = st.selectbox("🗓️ Month", month_options)

    all_species = sorted(df["Common_Name"].dropna().unique().tolist())
    selected_species = st.multiselect("🐦 Species (optional)", all_species, placeholder="Select species...")

    all_observers = sorted(df["Observer"].dropna().unique().tolist())
    selected_observer = st.selectbox("👁️ Observer", ["All"] + all_observers)

    sky_options = ["All"] + sorted(df["Sky"].dropna().unique().tolist())
    selected_sky = st.selectbox("☁️ Sky Condition", sky_options)

    st.markdown("---")
    temp_min = float(df["Temperature"].min())
    temp_max = float(df["Temperature"].max())
    temp_range = st.slider("🌡️ Temperature Range", temp_min, temp_max, (temp_min, temp_max), step=0.5)

    st.markdown("---")
    watchlist_only = st.checkbox("⚠️ PIF Watchlist Species Only")
    steward_only   = st.checkbox("🛡️ Regional Stewardship Only")
    flyover_only   = st.checkbox("🕊️ Flyover Observations Only")

# ── Apply Filters ─────────────────────────────────────────────────────────────
fdf = df.copy()
if selected_habitat != "All":
    fdf = fdf[fdf["Location_Type"] == selected_habitat]
if selected_month != "All":
    fdf = fdf[fdf["Month_Name"] == selected_month]
if selected_species:
    fdf = fdf[fdf["Common_Name"].isin(selected_species)]
if selected_observer != "All":
    fdf = fdf[fdf["Observer"] == selected_observer]
if selected_sky != "All":
    fdf = fdf[fdf["Sky"] == selected_sky]
fdf = fdf[(fdf["Temperature"] >= temp_range[0]) & (fdf["Temperature"] <= temp_range[1])]
if watchlist_only:
    fdf = fdf[fdf["PIF_Watchlist_Status"] == True]
if steward_only:
    fdf = fdf[fdf["Regional_Stewardship_Status"] == True]
if flyover_only:
    fdf = fdf[fdf["Flyover_Observed"] == True]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size:2rem;">🦅 Bird Species Observation Analysis</h1>
    <p style="margin:6px 0 0 0; opacity:0.85;">Forest & Grassland Biodiversity | ANTI Region | 2018</p>
</div>
""", unsafe_allow_html=True)

# ── Navigation Tabs ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🐦 Species Analysis",
    "🗓️ Temporal Trends",
    "🌡️ Environmental",
    "🛡️ Conservation"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<h2 class='section-header'>📊 Overview & Summary</h2>", unsafe_allow_html=True)

    # Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value'>{len(fdf):,}</div>
            <div class='metric-label'>Total Observations</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value'>{fdf['Common_Name'].nunique()}</div>
            <div class='metric-label'>Unique Species</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value'>{fdf['Location_Type'].nunique()}</div>
            <div class='metric-label'>Habitat Types</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value'>{fdf['Observer'].nunique()}</div>
            <div class='metric-label'>Observers</div></div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value'>{fdf['Plot_Name'].nunique()}</div>
            <div class='metric-label'>Plots</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        habitat_counts = fdf["Location_Type"].value_counts().reset_index()
        habitat_counts.columns = ["Habitat", "Observations"]
        fig = px.pie(habitat_counts, names="Habitat", values="Observations",
                     title="Observations by Habitat Type",
                     color="Habitat",
                     color_discrete_map={"Forest": "#2E86AB", "Grassland": "#A8C256"},
                     hole=0.4)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(showlegend=True, height=380)
        st.plotly_chart(fig, use_container_width=True, key="chart_1")

    with col2:
        id_counts = fdf["ID_Method"].value_counts().reset_index()
        id_counts.columns = ["Method", "Count"]
        fig = px.bar(id_counts, x="Method", y="Count",
                     title="Identification Method Distribution",
                     color="Method",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, height=380, xaxis_title="", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True, key="chart_2")

    col3, col4 = st.columns(2)

    with col3:
        dist_counts = fdf[fdf["Distance"] != "Unknown"]["Distance"].value_counts().reset_index()
        dist_counts.columns = ["Distance", "Count"]
        fig = px.bar(dist_counts, x="Distance", y="Count",
                     title="Observation Distance from Observer",
                     color="Distance",
                     color_discrete_sequence=["#1ABC9C", "#3498DB"],
                     text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, height=350, xaxis_title="", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True, key="chart_3")

    with col4:
        sex_counts = fdf["Sex"].value_counts().reset_index()
        sex_counts.columns = ["Sex", "Count"]
        color_map = {"Male": "#3498DB", "Female": "#E91E8C", "Undetermined": "#95A5A6", "Unknown": "#BDC3C7"}
        fig = px.pie(sex_counts, names="Sex", values="Count",
                     title="Sex Distribution",
                     color="Sex", color_discrete_map=color_map, hole=0.4)
        fig.update_traces(textposition="outside", textinfo="percent+label")
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True, key="chart_4")

    # Raw data preview
    with st.expander("📋 View Raw Data"):
        st.dataframe(fdf.reset_index(drop=True), use_container_width=True, height=300)
        csv = fdf.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Filtered Data", csv, "filtered_bird_data.csv", "text/csv")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — SPECIES ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<h2 class='section-header'>🐦 Species Analysis</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        n_species = st.slider("Number of top species to show", 5, 30, 15)

    top_species = fdf["Common_Name"].value_counts().head(n_species).reset_index()
    top_species.columns = ["Species", "Observations"]
    fig = px.bar(top_species, x="Observations", y="Species",
                 orientation="h",
                 title=f"Top {n_species} Most Observed Species",
                 color="Observations",
                 color_continuous_scale="RdYlGn",
                 text="Observations")
    fig.update_traces(textposition="outside")
    fig.update_layout(height=500, yaxis={"categoryorder": "total ascending"},
                      coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True, key="chart_5")

    col1, col2 = st.columns(2)
    with col1:
        for habitat in ["Forest", "Grassland"]:
            h_df = fdf[fdf["Location_Type"] == habitat]
            if len(h_df) == 0:
                continue
            top_h = h_df["Common_Name"].value_counts().head(10).reset_index()
            top_h.columns = ["Species", "Count"]
            color = "#2E86AB" if habitat == "Forest" else "#A8C256"
            fig = px.bar(top_h, x="Count", y="Species", orientation="h",
                         title=f"Top 10 — {habitat}",
                         text="Count", color_discrete_sequence=[color])
            fig.update_traces(textposition="outside")
            fig.update_layout(height=380, yaxis={"categoryorder": "total ascending"},
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key="chart_6")
            break

    with col2:
        for habitat in ["Grassland", "Forest"]:
            h_df = fdf[fdf["Location_Type"] == habitat]
            if len(h_df) == 0:
                continue
            top_h = h_df["Common_Name"].value_counts().head(10).reset_index()
            top_h.columns = ["Species", "Count"]
            color = "#2E86AB" if habitat == "Forest" else "#A8C256"
            fig = px.bar(top_h, x="Count", y="Species", orientation="h",
                         title=f"Top 10 — {habitat}",
                         text="Count", color_discrete_sequence=[color])
            fig.update_traces(textposition="outside")
            fig.update_layout(height=380, yaxis={"categoryorder": "total ascending"},
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key="chart_7")
            break

    # Species exclusivity
    st.markdown("<h3 class='section-header'>Species Habitat Exclusivity</h3>", unsafe_allow_html=True)
    forest_sp    = set(fdf[fdf["Location_Type"] == "Forest"]["Common_Name"])
    grassland_sp = set(fdf[fdf["Location_Type"] == "Grassland"]["Common_Name"])
    shared       = forest_sp & grassland_sp
    forest_only  = forest_sp - grassland_sp
    grass_only   = grassland_sp - forest_sp

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🌲 Forest Only", len(forest_only))
        if forest_only:
            st.write(", ".join(sorted(forest_only)))
    with c2:
        st.metric("🔀 Both Habitats", len(shared))
    with c3:
        st.metric("🌾 Grassland Only", len(grass_only))

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TEMPORAL TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<h2 class='section-header'>🗓️ Temporal Trends</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        month_counts = fdf.groupby("Month_Name", observed=True).size().reset_index(name="Observations")
        fig = px.line(month_counts, x="Month_Name", y="Observations",
                      title="Monthly Observation Trend",
                      markers=True, line_shape="spline",
                      color_discrete_sequence=["#E84855"])
        fig.update_traces(line_width=3, marker_size=12)
        fig.update_layout(height=380, xaxis_title="Month", yaxis_title="Observations")
        st.plotly_chart(fig, use_container_width=True, key="chart_8")

    with col2:
        month_habitat = fdf.groupby(["Month_Name", "Location_Type"], observed=True).size().reset_index(name="Observations")
        fig = px.bar(month_habitat, x="Month_Name", y="Observations",
                     color="Location_Type", barmode="group",
                     title="Monthly Observations by Habitat",
                     color_discrete_map={"Forest": "#2E86AB", "Grassland": "#A8C256"})
        fig.update_layout(height=380, xaxis_title="Month", yaxis_title="Observations", legend_title="Habitat")
        st.plotly_chart(fig, use_container_width=True, key="chart_9")

    col3, col4 = st.columns(2)

    with col3:
        month_species = fdf.groupby("Month_Name", observed=True)["Common_Name"].nunique().reset_index(name="Unique_Species")
        fig = px.bar(month_species, x="Month_Name", y="Unique_Species",
                     title="Unique Species per Month",
                     color="Unique_Species", color_continuous_scale="Blues",
                     text="Unique_Species")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=350, coloraxis_showscale=False, xaxis_title="Month")
        st.plotly_chart(fig, use_container_width=True, key="chart_10")

    with col4:
        interval_order = ["0-2.5 min", "2.5 - 5 min", "5 - 7.5 min", "7.5 - 10 min"]
        interval_counts = fdf["Interval_Length"].value_counts().reindex(interval_order).fillna(0).reset_index()
        interval_counts.columns = ["Interval", "Count"]
        fig = px.bar(interval_counts, x="Interval", y="Count",
                     title="Observations by Time Interval",
                     color="Count", color_continuous_scale="Oranges",
                     text="Count")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=350, coloraxis_showscale=False, xaxis_title="Interval")
        st.plotly_chart(fig, use_container_width=True, key="chart_11")

    # Visit analysis
    visit_data = fdf.groupby("Visit").agg(
        Observations=("Common_Name", "count"),
        Unique_Species=("Common_Name", "nunique")
    ).reset_index()
    fig = px.bar(visit_data, x="Visit", y="Observations",
                 title="Observations per Visit Number",
                 color="Unique_Species", color_continuous_scale="Viridis",
                 text="Observations",
                 labels={"Unique_Species": "Unique Species"})
    fig.update_traces(textposition="outside")
    fig.update_layout(height=350, xaxis_title="Visit Number")
    st.plotly_chart(fig, use_container_width=True, key="chart_12")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ENVIRONMENTAL CONDITIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<h2 class='section-header'>🌡️ Environmental Conditions</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(fdf, x="Temperature", color="Location_Type",
                           title="Temperature Distribution by Habitat",
                           barmode="overlay", nbins=25, opacity=0.7,
                           color_discrete_map={"Forest": "#2E86AB", "Grassland": "#A8C256"})
        fig.update_layout(height=370, xaxis_title="Temperature", yaxis_title="Count", legend_title="Habitat")
        st.plotly_chart(fig, use_container_width=True, key="chart_13")

    with col2:
        fig = px.histogram(fdf, x="Humidity", color="Location_Type",
                           title="Humidity Distribution by Habitat",
                           barmode="overlay", nbins=25, opacity=0.7,
                           color_discrete_map={"Forest": "#2E86AB", "Grassland": "#A8C256"})
        fig.update_layout(height=370, xaxis_title="Humidity (%)", yaxis_title="Count", legend_title="Habitat")
        st.plotly_chart(fig, use_container_width=True, key="chart_14")

    col3, col4 = st.columns(2)

    with col3:
        sky_counts = fdf["Sky"].value_counts().reset_index()
        sky_counts.columns = ["Sky", "Count"]
        fig = px.bar(sky_counts, x="Sky", y="Count",
                     title="Sky Conditions During Observations",
                     color="Sky", text="Count",
                     color_discrete_sequence=["#87CEEB", "#B0C4DE", "#708090", "#4682B4"])
        fig.update_traces(textposition="outside")
        fig.update_layout(height=370, showlegend=False, xaxis_title="")
        st.plotly_chart(fig, use_container_width=True, key="chart_15")

    with col4:
        dist_order = ["No effect on count", "Slight effect on count",
                      "Moderate effect on count", "Serious effect on count"]
        dist_counts = fdf["Disturbance"].value_counts().reindex(dist_order).fillna(0).reset_index()
        dist_counts.columns = ["Disturbance", "Count"]
        short_labels = ["None", "Slight", "Moderate", "Serious"]
        dist_counts["Label"] = short_labels
        fig = px.bar(dist_counts, x="Label", y="Count",
                     title="Disturbance Level Impact",
                     color="Label", text="Count",
                     color_discrete_sequence=["#2ECC71", "#F39C12", "#E67E22", "#E74C3C"])
        fig.update_traces(textposition="outside")
        fig.update_layout(height=370, showlegend=False, xaxis_title="Disturbance Level")
        st.plotly_chart(fig, use_container_width=True, key="chart_16")

    # Scatter: Temp vs Humidity coloured by habitat
    fig = px.scatter(fdf, x="Temperature", y="Humidity",
                     color="Location_Type", hover_data=["Common_Name", "Observer", "Month_Name"],
                     title="Temperature vs Humidity (coloured by Habitat)",
                     color_discrete_map={"Forest": "#2E86AB", "Grassland": "#A8C256"},
                     opacity=0.6)
    fig.update_layout(height=420, legend_title="Habitat")
    st.plotly_chart(fig, use_container_width=True, key="chart_17")

    # Wind
    wind_counts = fdf["Wind"].value_counts().reset_index()
    wind_counts.columns = ["Wind", "Count"]
    wind_counts["Wind_Short"] = wind_counts["Wind"].apply(lambda x: x.split("(")[0].strip()[:25])
    fig = px.bar(wind_counts, x="Count", y="Wind_Short", orientation="h",
                 title="Wind Conditions During Observations",
                 color="Count", color_continuous_scale="YlOrRd", text="Count")
    fig.update_traces(textposition="outside")
    fig.update_layout(height=350, coloraxis_showscale=False, yaxis_title="")
    st.plotly_chart(fig, use_container_width=True, key="chart_18")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CONSERVATION
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<h2 class='section-header'>🛡️ Conservation Insights</h2>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        wl_count = fdf[fdf["PIF_Watchlist_Status"] == True]["Common_Name"].nunique()
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value' style='color:#E74C3C;'>{wl_count}</div>
            <div class='metric-label'>⚠️ PIF Watchlist Species</div></div>""", unsafe_allow_html=True)
    with c2:
        st_count = fdf[fdf["Regional_Stewardship_Status"] == True]["Common_Name"].nunique()
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value' style='color:#E67E22;'>{st_count}</div>
            <div class='metric-label'>🛡️ Regional Stewardship Species</div></div>""", unsafe_allow_html=True)
    with c3:
        fly_count = int(fdf["Flyover_Observed"].sum())
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-value' style='color:#3498DB;'>{fly_count}</div>
            <div class='metric-label'>🕊️ Flyover Observations</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        watchlist_df = fdf[fdf["PIF_Watchlist_Status"] == True]
        if len(watchlist_df) > 0:
            wl_sp = watchlist_df.groupby(["Common_Name", "Location_Type"]).size().reset_index(name="Observations")
            fig = px.bar(wl_sp, x="Common_Name", y="Observations",
                         color="Location_Type", barmode="group",
                         title="PIF Watchlist Species by Habitat",
                         color_discrete_map={"Forest": "#2E86AB", "Grassland": "#A8C256"})
            fig.update_layout(height=400, xaxis_tickangle=-30, xaxis_title="", legend_title="Habitat")
            st.plotly_chart(fig, use_container_width=True, key="chart_19")
        else:
            st.info("No PIF Watchlist species in current filter selection.")

    with col2:
        steward_df = fdf[fdf["Regional_Stewardship_Status"] == True]
        if len(steward_df) > 0:
            st_sp = steward_df["Common_Name"].value_counts().head(15).reset_index()
            st_sp.columns = ["Species", "Observations"]
            fig = px.bar(st_sp, x="Observations", y="Species", orientation="h",
                         title="Top Regional Stewardship Species",
                         color="Observations", color_continuous_scale="Reds",
                         text="Observations")
            fig.update_traces(textposition="outside")
            fig.update_layout(height=400, coloraxis_showscale=False,
                              yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True, key="chart_20")
        else:
            st.info("No Regional Stewardship species in current filter selection.")

    # Flyover by month and habitat
    col3, col4 = st.columns(2)
    with col3:
        flyover_habitat = fdf.groupby(["Location_Type", "Flyover_Observed"]).size().reset_index(name="Count")
        flyover_habitat["Flyover"] = flyover_habitat["Flyover_Observed"].map({True: "Flyover", False: "No Flyover"})
        fig = px.bar(flyover_habitat, x="Location_Type", y="Count", color="Flyover",
                     title="Flyover Observations by Habitat",
                     barmode="group",
                     color_discrete_map={"Flyover": "#E74C3C", "No Flyover": "#3498DB"})
        fig.update_layout(height=370, xaxis_title="", legend_title="")
        st.plotly_chart(fig, use_container_width=True, key="chart_21")

    with col4:
        # Conservation summary table
        st.markdown("#### 📋 Watchlist Species Detail")
        if len(watchlist_df) > 0:
            wl_table = watchlist_df.groupby(["Common_Name", "Scientific_Name", "AOU_Code", "Location_Type"]).size().reset_index(name="Observations")
            wl_table = wl_table.sort_values("Observations", ascending=False)
            st.dataframe(wl_table.reset_index(drop=True), use_container_width=True, height=330)
        else:
            st.info("No watchlist species with current filters.")

    # Observer analysis
    st.markdown("<h3 class='section-header'>👁️ Observer Analysis</h3>", unsafe_allow_html=True)
    observer_stats = fdf.groupby("Observer").agg(
        Observations=("Common_Name", "count"),
        Unique_Species=("Common_Name", "nunique"),
        Plots_Visited=("Plot_Name", "nunique")
    ).reset_index().sort_values("Observations", ascending=False)

    col5, col6 = st.columns(2)
    with col5:
        fig = px.bar(observer_stats, x="Observer", y="Observations",
                     title="Total Observations per Observer",
                     color="Observations", color_continuous_scale="Blues",
                     text="Observations")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=370, coloraxis_showscale=False, xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True, key="chart_22")

    with col6:
        fig = px.bar(observer_stats, x="Observer", y="Unique_Species",
                     title="Unique Species per Observer",
                     color="Unique_Species", color_continuous_scale="Greens",
                     text="Unique_Species")
        fig.update_traces(textposition="outside")
        fig.update_layout(height=370, coloraxis_showscale=False, xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True, key="chart_23")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; font-size:0.85rem; padding:10px'>
    🦅 Bird Species Observation Analysis Dashboard &nbsp;|&nbsp;
    Domain: Environmental Studies & Biodiversity Conservation &nbsp;|&nbsp;
    Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
