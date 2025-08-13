# ApexPlannerLight

A local Streamlit application for demand planning and forecast analysis. ApexPlannerLight helps demand planners manage sales data, analyze forecast performance, generate statistical forecasts, and detect outliers - all running locally with SQLite storage.

## ✨ Features

### 📊 Data Management
- **Sales Data Import**: Upload CSV files with actual sales data (Date, SKU, Actual Units, GeoLocation, Warehouse)
- **Product Masterdata**: Manage product information including ABC/XYZ classification, brand hierarchies, and product attributes
- **Forecast Data**: Import previous forecasts for performance analysis
- **Geography Data**: Handle geographical and warehouse information with aggregation levels
- **Data Validation**: Automatic validation of CSV schemas and column requirements
- **SQLite Storage**: Local database storage with data persistence

### 📈 Analysis Capabilities
- **Performance Analysis**: Compare forecasts vs actuals with configurable time offsets
- **Statistical Forecasting**: Generate ARIMA-based forecasts for any SKU
- **Outlier Detection**: Identify anomalies using Z-score analysis
- **KPI Calculation**: Monthly and year-to-date accuracy, bias, and error metrics
- **Interactive Visualizations**: Charts and graphs for trend analysis

### 🔧 Technical Features
- **Local-First**: No cloud dependencies, runs entirely on your machine
- **Streamlit UI**: Modern, responsive web interface
- **Data Privacy**: All data stays on your local system
- **Extensible**: Modular architecture for easy customization

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd apexplanner_light
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the application**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will automatically create the local database

## 📖 Usage Guide

### Data Management
1. Navigate to the **Data Management** tab
2. Upload CSV files for each data type:
   - **Sales**: Historical sales data with actual units
   - **Product Master**: Product information and classifications
   - **Forecasts**: Previous forecast data for performance analysis
   - **Geography**: Location and warehouse data
3. Validate your data - the system will check for required columns
4. Preview uploaded data tables

### Analysis Workflows

#### Forecast Performance Analysis
1. Go to **Main Analysis** → **Performance**
2. Set offset months to align forecast and actual periods
3. Optionally filter by specific SKU
4. View accuracy metrics and trends

#### Statistical Forecasting
1. Select **Statistical Forecast** analysis type
2. Enter the SKU you want to forecast
3. Set forecast horizon (1-24 months)
4. Generate ARIMA-based forecast with visualization

#### Outlier Detection
1. Choose **Outliers** analysis type
2. Specify SKU and Z-score threshold
3. Identify anomalous data points in sales history

## 📋 Data Schema Requirements

### Sales Data
```csv
Date,SKU,Actual Units,GeoLocation,Warehouse
2024-01-01,SKU001,150,US-East,WH001
```

### Product Master
```csv
SKU,ABC,XYZ,BrandHierarchy1,BrandHierarchy2,BrandHierarchy3,BrandHierarchy4,BrandHierarchy5,Production Site,Product Type,Sales Type,Product Status
SKU001,A,X,Brand1,SubBrand1,Product1,Variant1,SKU001,Site1,Electronics,Retail,Active
```

### Forecasts
```csv
Version Date,Date,SKU,Forecast Units,Statistical Units,GeoLocation,Warehouse
2024-01-01,2024-02-01,SKU001,160,155,US-East,WH001
```

### Geography
```csv
GeoLocation,Warehouse,Aggregation1,Aggregation2,Aggregation3,Aggregation4,Aggregation5
US-East,WH001,North America,United States,East Coast,New York,NYC
```

## 🏗️ Project Structure

```
apexplanner_light/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── apexplanner_light/     # Core package
│   ├── __init__.py
│   ├── version.py         # Version management
│   ├── database.py        # SQLite operations and schemas
│   └── analysis.py        # Statistical analysis functions
├── docs/
│   └── prd.md            # Product Requirements Document
└── data/                 # Local data storage (auto-created)
    └── apexplanner_light.db
```

## 🔧 Technical Details

- **Framework**: Streamlit 1.36.0
- **Database**: SQLite with SQLAlchemy
- **Analytics**: pandas, numpy, scikit-learn, statsmodels
- **Forecasting**: ARIMA statistical models
- **Data Validation**: Pydantic schemas
- **Version**: 0.1.0-alpha.1

## 💾 Data Storage

Local data is stored in `/workspace/data/apexplanner_light.db` (SQLite database). The database contains tables for:
- `sales` - Historical sales data
- `product_master` - Product information
- `forecasts` - Forecast data
- `geography` - Geographic and warehouse data

## 🤝 Contributing

This project follows best practices for demand planning and forecasting. Contributions are welcome! Please see the PRD document in `docs/prd.md` for detailed requirements and specifications.

## 📄 License

MIT License with Commons Clause - see [LICENSE](LICENSE) file for details.

This allows community contributions and internal commercial use, but restricts selling the software as a service.

---

**Version**: 0.1.0-alpha.1  
**Documentation**: See `docs/prd.md` for complete product requirements
