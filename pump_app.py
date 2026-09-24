import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from pathlib import Path

# ==========================================
# CONFIG
# ==========================================

FILE_NAME = "pump_inspections.xlsx"

st.set_page_config(
    page_title="Pump Maintenance",
    page_icon="⚙️",
    layout="wide"
)

# ==========================================
# STYLE
# ==========================================

st.markdown("""
<style>
.stApp{
    background-color:#0F172A;
}

[data-testid="stMetric"]{
    background:#1E293B;
    border:1px solid #00E5FF;
    border-radius:12px;
    padding:10px;
}

h1,h2,h3{
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

if Path(FILE_NAME).exists():
    df_history = pd.read_excel(FILE_NAME)
else:
    df_history = pd.DataFrame()

# ==========================================
# HEADER
# ==========================================

st.title("⚙️ Pump Maintenance Management")

st.caption("Multi-user Inspection Application")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Equipment")

pump = st.sidebar.selectbox(
    "Pump",
    [
        "PUM001",
        "PUM002",
        "PUM003",
        "PUM004"
    ]
)

inspector = st.sidebar.text_input(
    "Inspector Name"
)

# ==========================================
# INPUTS
# ==========================================

c1,c2,c3 = st.columns(3)

with c1:
    vibration = st.number_input(
        "Vibration (mm/s)",
        min_value=0.0,
        value=4.0
    )

with c2:
    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        value=45.0
    )

with c3:
    oil = st.selectbox(
        "Oil Level",
        [
            "Good",
            "Low",
            "Critical"
        ]
    )

# ==========================================
# HEALTH
# ==========================================

if vibration < 4.5:
    status = "Healthy"

elif vibration < 7.1:
    status = "Warning"

else:
    status = "Critical"

# ==========================================
# KPIs
# ==========================================

k1,k2,k3,k4 = st.columns(4)

k1.metric("Pump",pump)
k2.metric("Vibration",f"{vibration:.2f}")
k3.metric("Temperature",f"{temperature:.1f}")
k4.metric("Status",status)

# ==========================================
# SAVE
# ==========================================

if st.button("💾 Save Inspection"):

    rec = pd.DataFrame([{
        "Date":datetime.now(),
        "Inspector":inspector,
        "Pump":pump,
        "Vibration":vibration,
        "Temperature":temperature,
        "Oil Level":oil,
        "Status":status
    }])

    if Path(FILE_NAME).exists():

        old = pd.read_excel(FILE_NAME)

        old = pd.concat(
            [old,rec],
            ignore_index=True
        )

        old.to_excel(
            FILE_NAME,
            index=False
        )

    else:

        rec.to_excel(
            FILE_NAME,
            index=False
        )

    st.success("Inspection Saved")

    st.rerun()

# ==========================================
# HISTORY
# ==========================================

if len(df_history) > 0:

    st.subheader("Inspection History")

    st.dataframe(
        df_history,
        use_container_width=True
    )

    # =====================================
    # CHARTS
    # =====================================

    col1,col2 = st.columns(2)

    with col1:

        fig = px.line(
            df_history,
            x="Date",
            y="Vibration",
            color="Pump",
            markers=True,
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig2 = px.line(
            df_history,
            x="Date",
            y="Temperature",
            color="Pump",
            markers=True,
            template="plotly_dark"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # =====================================
    # STATUS BREAKDOWN
    # =====================================

    st.subheader("Status Breakdown")

    fig3 = px.pie(
        df_history,
        names="Status",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # =====================================
    # DOWNLOAD
    # =====================================

    with open(FILE_NAME,"rb") as f:

        st.download_button(
            "📥 Download Excel",
            f,
            file_name=FILE_NAME
        )

else:
    st.info("No inspection data saved yet.")