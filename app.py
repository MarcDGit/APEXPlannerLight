from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import streamlit as st

from apexplanner_light.version import get_version
from apexplanner_light.database import (
    create_tables,
    validate_columns,
    insert_dataframe,
    preview_table,
    EXPECTED_SCHEMAS,
)
from apexplanner_light import database
from apexplanner_light import analysis as al

APP_NAME = "ApexPlannerLight"
DATA_DIR = Path("/workspace/data")


@st.cache_data(show_spinner=False)
def read_csv(file: io.BytesIO) -> pd.DataFrame:
    return pd.read_csv(file)


def main() -> None:
    st.set_page_config(page_title=f"{APP_NAME}", layout="wide")
    st.sidebar.title(APP_NAME)
    st.sidebar.caption(f"Version {get_version()}")

    create_tables()

    page = st.sidebar.radio("Navigate", ["Data Management", "Main Analysis", "About"], index=0)

    if page == "Data Management":
        st.header("Data Management")
        st.write("Upload CSVs for each dataset. Files are validated and stored locally in SQLite.")

        # Uploaders
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Sales")
            sales_file = st.file_uploader("Upload sales CSV", type=["csv"], key="sales")
            if sales_file:
                df = read_csv(sales_file)
                ok, missing = validate_columns("sales", df)
                if not ok:
                    st.error(f"Missing columns in Sales: {missing}")
                else:
                    insert_dataframe("sales", df)
                    st.success("Sales data stored")
                    st.dataframe(df.head(50), use_container_width=True)

            st.subheader("Product Masterdata")
            pm_file = st.file_uploader("Upload product master CSV", type=["csv"], key="product_master")
            if pm_file:
                df = read_csv(pm_file)
                ok, missing = validate_columns("product_master", df)
                if not ok:
                    st.error(f"Missing columns in Product Master: {missing}")
                else:
                    insert_dataframe("product_master", df, if_exists="replace")
                    st.success("Product master data stored (replaced)")
                    st.dataframe(df.head(50), use_container_width=True)

        with col2:
            st.subheader("Forecasts")
            f_file = st.file_uploader("Upload forecasts CSV", type=["csv"], key="forecasts")
            if f_file:
                df = read_csv(f_file)
                ok, missing = validate_columns("forecasts", df)
                if not ok:
                    st.error(f"Missing columns in Forecasts: {missing}")
                else:
                    insert_dataframe("forecasts", df)
                    st.success("Forecasts stored")
                    st.dataframe(df.head(50), use_container_width=True)

            st.subheader("Geography")
            g_file = st.file_uploader("Upload geography CSV", type=["csv"], key="geography")
            if g_file:
                df = read_csv(g_file)
                ok, missing = validate_columns("geography", df)
                if not ok:
                    st.error(f"Missing columns in Geography: {missing}")
                else:
                    insert_dataframe("geography", df, if_exists="replace")
                    st.success("Geography stored (replaced)")
                    st.dataframe(df.head(50), use_container_width=True)

        st.divider()
        st.subheader("Preview Tables")
        preview_choice = st.selectbox("Select table to preview", list(EXPECTED_SCHEMAS.keys()))
        if st.button("Preview", type="primary"):
            st.dataframe(preview_table(preview_choice, 100), use_container_width=True)

    elif page == "Main Analysis":
        st.header("Main Analysis")
        analysis_type = st.selectbox("Analysis Type", ["Performance", "Statistical Forecast", "Outliers"], index=0)

        if analysis_type == "Performance":
            offset = st.number_input("Offset months (forecast vs actual)", value=0, step=1)
            sku = st.text_input("SKU filter (optional)")
            if st.button("Run Performance"):
                with st.spinner("Running performance analysis..."):
                    sales = database.preview_table("sales", limit=1000000)
                    forecasts = database.preview_table("forecasts", limit=1000000)
                    if sku:
                        sales = sales[sales["sku"] == sku]
                        forecasts = forecasts[forecasts["sku"] == sku]
                    if sales.empty or forecasts.empty:
                        st.warning("No data available. Please upload Sales and Forecasts.")
                    else:
                        kpis = al.performance_with_offset(forecasts, sales, int(offset))
                        st.dataframe(kpis, use_container_width=True)
                        st.line_chart(kpis.set_index("period")["accuracy"])

        elif analysis_type == "Statistical Forecast":
            sku = st.text_input("SKU", key="sf_sku")
            horizon = st.slider("Horizon (months)", min_value=1, max_value=24, value=12)
            if st.button("Generate Forecast"):
                sales = database.preview_table("sales", limit=1000000)
                if sku:
                    sales = sales[sales["sku"] == sku]
                if sales.empty:
                    st.warning("No sales data available.")
                else:
                    s = sales.copy()
                    s["date"] = pd.to_datetime(s["date"])  # internal format
                    series = s.set_index("date")["actual_units"].asfreq("MS").fillna(0)
                    fc = al.statistical_forecast(series, horizon=int(horizon))
                    df_fc = pd.DataFrame({"date": fc.index, "forecast": fc.values})
                    st.dataframe(df_fc, use_container_width=True)
                    st.line_chart(df_fc.set_index("date"))

        else:  # Outliers
            sku = st.text_input("SKU", key="ol_sku")
            threshold = st.slider("Z-score threshold", min_value=1.0, max_value=5.0, value=3.0, step=0.5)
            if st.button("Detect Outliers"):
                sales = database.preview_table("sales", limit=1000000)
                if sku:
                    sales = sales[sales["sku"] == sku]
                if sales.empty:
                    st.warning("No sales data available.")
                else:
                    s = sales.copy()
                    s["date"] = pd.to_datetime(s["date"])  # internal format
                    series = s.set_index("date")["actual_units"].asfreq("MS").fillna(0)
                    out = al.detect_outliers_zscore(series, threshold=float(threshold))
                    st.dataframe(out, use_container_width=True)
                    st.bar_chart(out[["z"]])

    else:
        st.header("About")
        st.write("ApexPlannerLight helps demand planners manage data and analyze forecasts locally.")
        st.markdown("- Local SQLite storage\n- Performance KPIs\n- Basic ARIMA forecasting\n- Outlier detection")
        st.caption("See docs/prd.md for details.")


if __name__ == "__main__":
    main()