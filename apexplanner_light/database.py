from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd

DB_PATH = Path("/workspace/data/apexplanner_light.db")


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def create_tables() -> None:
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                date TEXT NOT NULL,
                sku TEXT NOT NULL,
                actual_units INTEGER NOT NULL,
                geolocation TEXT,
                warehouse TEXT
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS product_master (
                sku TEXT PRIMARY KEY,
                abc TEXT,
                xyz TEXT,
                brand_h1 TEXT,
                brand_h2 TEXT,
                brand_h3 TEXT,
                brand_h4 TEXT,
                brand_h5 TEXT,
                production_site TEXT,
                product_type TEXT,
                sales_type TEXT,
                product_status TEXT
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS forecasts (
                version_date TEXT NOT NULL,
                date TEXT NOT NULL,
                sku TEXT NOT NULL,
                forecast_units INTEGER,
                statistical_units INTEGER,
                geolocation TEXT,
                warehouse TEXT
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS geography (
                geolocation TEXT,
                warehouse TEXT,
                agg1 TEXT,
                agg2 TEXT,
                agg3 TEXT,
                agg4 TEXT,
                agg5 TEXT
            );
            """
        )
        conn.commit()


EXPECTED_SCHEMAS: dict[str, list[str]] = {
    "sales": ["Date", "SKU", "Actual Units", "GeoLocation", "Warehouse"],
    "product_master": [
        "SKU",
        "ABC",
        "XYZ",
        "BrandHierarchy1",
        "BrandHierarchy2",
        "BrandHierarchy3",
        "BrandHierarchy4",
        "BrandHierarchy5",
        "Production Site",
        "Product Type",
        "Sales Type",
        "Product Status",
    ],
    "forecasts": [
        "Version Date",
        "Date",
        "SKU",
        "Forecast Units",
        "Statistical Units",
        "GeoLocation",
        "Warehouse",
    ],
    "geography": [
        "GeoLocation",
        "Warehouse",
        "Aggregation1",
        "Aggregation2",
        "Aggregation3",
        "Aggregation4",
        "Aggregation5",
    ],
}


COLUMN_RENAMES: dict[str, dict[str, str]] = {
    "sales": {
        "Date": "date",
        "SKU": "sku",
        "Actual Units": "actual_units",
        "GeoLocation": "geolocation",
        "Warehouse": "warehouse",
    },
    "product_master": {
        "SKU": "sku",
        "ABC": "abc",
        "XYZ": "xyz",
        "BrandHierarchy1": "brand_h1",
        "BrandHierarchy2": "brand_h2",
        "BrandHierarchy3": "brand_h3",
        "BrandHierarchy4": "brand_h4",
        "BrandHierarchy5": "brand_h5",
        "Production Site": "production_site",
        "Product Type": "product_type",
        "Sales Type": "sales_type",
        "Product Status": "product_status",
    },
    "forecasts": {
        "Version Date": "version_date",
        "Date": "date",
        "SKU": "sku",
        "Forecast Units": "forecast_units",
        "Statistical Units": "statistical_units",
        "GeoLocation": "geolocation",
        "Warehouse": "warehouse",
    },
    "geography": {
        "GeoLocation": "geolocation",
        "Warehouse": "warehouse",
        "Aggregation1": "agg1",
        "Aggregation2": "agg2",
        "Aggregation3": "agg3",
        "Aggregation4": "agg4",
        "Aggregation5": "agg5",
    },
}


def validate_columns(table_key: str, dataframe: pd.DataFrame) -> tuple[bool, list[str]]:
    expected = EXPECTED_SCHEMAS[table_key]
    missing = [col for col in expected if col not in dataframe.columns]
    return (len(missing) == 0, missing)


def to_internal_dataframe(table_key: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    renamed = dataframe.rename(columns=COLUMN_RENAMES[table_key]).copy()
    date_columns: list[str] = [c for c in ["date", "version_date"] if c in renamed.columns]
    for column_name in date_columns:
        renamed[column_name] = pd.to_datetime(renamed[column_name], errors="coerce").dt.strftime("%Y-%m-%d")
    return renamed


def insert_dataframe(table_key: str, dataframe: pd.DataFrame, if_exists: str = "append") -> None:
    internal = to_internal_dataframe(table_key, dataframe)
    table_name_map = {
        "sales": "sales",
        "product_master": "product_master",
        "forecasts": "forecasts",
        "geography": "geography",
    }
    with connect() as conn:
        internal.to_sql(table_name_map[table_key], conn, if_exists=if_exists, index=False)


def preview_table(table_key: str, limit: int = 50) -> pd.DataFrame:
    table_name_map = {
        "sales": "sales",
        "product_master": "product_master",
        "forecasts": "forecasts",
        "geography": "geography",
    }
    with connect() as conn:
        query = f"SELECT * FROM {table_name_map[table_key]} LIMIT ?"
        return pd.read_sql_query(query, conn, params=(limit,))