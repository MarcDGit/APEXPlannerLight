# Product Requirements Document (PRD) for ApexPlannerLight

## Version
Alpha 1.0.0

## Executive Summary

ApexPlannerLight is a Python application built with Streamlit. It runs on local machines with a local database. The tool helps demand planners and managers handle sales data, product details, forecasts, and geographical info. Key objectives include data import, forecast analysis, statistical generation, and outlier insights to improve planning.

This project is source-available, licensed under the MIT License with the Commons Clause, which permits community contributions and individual use, including commercial usage internally, but restricts selling the software.

## Problem Statement

Demand planners face challenges in managing sales data, forecasts, and product info. They need a tool to import data, analyze forecast performance, generate new forecasts, and spot outliers. Target audience: demand planners and demand planning managers in supply chain roles.

## Product Vision

The solution is a local Streamlit app for data management and planning. Key features: import tabs for sales, product masterdata, forecasts, and geographical data; main tab for analysis and forecasting. It calculates KPIs monthly or year-to-date. Follows best practices for forecasts and evaluations.

## User Stories

### Personas
- **Demand Planner**: Daily user who imports data and runs analyses.
- **Demand Planning Manager**: Oversees teams, reviews KPIs and insights.

### Journey Maps
1. User opens app on local machine.
2. Navigates to data management tab.
3. Uploads CSV files for sales, product masterdata, forecasts, geographical data.
4. Switches to main tab.
5. Selects analysis type: past performance, statistical forecast, or outlier analysis.
6. Views results with KPIs for month or year-to-date.
7. Exports insights or updated forecasts.

Example Use Case: Planner uploads sales data, selects offset for performance analysis, views accuracy KPIs.

## Functional Requirements

### Core Functionalities
- **Data Import**:
  - Upload actual sales: CSV with columns Date, SKU, Actual Units, GeoLocation, Warehouse.
  - Upload product masterdata: CSV with SKU, ABC, XYZ, BrandHierarchy1-5, Production Site, Product Type, Sales Type, Product Status.
  - Import previous forecasts: CSV with Version Date, Date, SKU, Forecast Units, Statistical Units, GeoLocation, Warehouse.
  - Import geographical masterdata: CSV with GeoLocation, Warehouse, Aggregation1-5.
- **Data Management Tab**:
  - View uploaded data tables.
  - Validate data formats.
  - Store data in local database (e.g., SQLite).
- **Main Tab**:
  - Analyze past forecast performance with offset (e.g., compare forecast to actuals shifted by months).
  - Generate statistical forecast using best practices (e.g., time series models).
  - Analyze outliers and provide insights (e.g., detect anomalies in sales vs. forecast).
- **Calculations**:
  - KPIs: Accuracy, bias, error rates, calculated monthly or year-to-date.
  - Aggregations based on hierarchies and geographies.

### Feature Specifications
- Filters: By SKU, date range, hierarchy levels.
- Visualizations: Charts for trends, errors.
- Export: CSV for results.

All requirements measurable: e.g., import succeeds if data matches schema; analysis runs in under 10 seconds.

## Non-Functional Requirements

- **Performance**: Load data in under 5 seconds; analyses complete in under 30 seconds for 10,000 rows.
- **Security**: Local data only; no external access.
- **Scalability**: Handle up to 100,000 rows per dataset on standard hardware.
- **Usability**: Intuitive Streamlit interface.
- **Reliability**: Data persistence across sessions via local DB.

All testable: e.g., performance via timing tests.

## Technical Specifications

### System Architecture
- Frontend: Streamlit for UI.
- Backend: Python scripts for logic.
- Database: Local SQLite for storage.
- Libraries: Pandas for data handling, Statsmodels or similar for forecasting.

### Data Flow Diagram
```
User -> Upload CSV -> Streamlit App -> Validate & Store in SQLite
User -> Select Analysis -> Query SQLite -> Process Data -> Display Results
```

(No assumptions on implementation details like specific algorithms.)

## User Interface Design

### Wireframes/Mockups
- **Data Management Tab**:
  - Upload buttons for each data type.
  - Data preview tables.
- **Main Tab**:
  - Dropdown for analysis type.
  - Input for offset or parameters.
  - Output: KPI table, charts.

Mockup Example (Text Description):
- Sidebar: Navigation between tabs.
- Main Area: File uploaders, then analysis selectors.

Use Streamlit components: st.file_uploader, st.dataframe, st.line_chart.

## Data Requirements

### Data Models
- **Sales Table**: Date (datetime), SKU (string), Actual Units (int), GeoLocation (string), Warehouse (string).
- **Product Masterdata Table**: SKU (string primary key), ABC (string), XYZ (string), BrandHierarchy1-5 (string), Production Site (string), Product Type (string), Sales Type (string), Product Status (string).
- **Forecasts Table**: Version Date (datetime), Date (datetime), SKU (string), Forecast Units (int), Statistical Units (int), GeoLocation (string), Warehouse (string).
- **Geographical Table**: GeoLocation (string), Warehouse (string), Aggregation1-5 (string).

### Storage Plans
- Local SQLite database file.
- Tables created on first run.
- Data appended or overwritten based on user choice.

## Milestones and Timeline

### Development Phases
1. **Phase 1: Setup (Week 1-2)** - Streamlit base, DB integration.
2. **Phase 2: Data Import (Week 3-4)** - Upload and validation features.
3. **Phase 3: Analysis Features (Week 5-7)** - Performance analysis, forecasting, outliers.
4. **Phase 4: UI Polish and Testing (Week 8)** - Visuals, exports.

Key Deliverables: Prototype after Phase 2; Beta after Phase 3.

## Testing and Quality Assurance

### Test Cases
- Unit: Data validation functions.
- Integration: Import to analysis flow.
- System: Full user journeys.

### Acceptance Criteria
- Imports: Data stored correctly, no errors on valid CSV.
- Analyses: KPIs match manual calculations (e.g., forecast accuracy = 1 - |forecast - actual| / actual).
- Edge Cases: Empty data, invalid formats.

## Deployment and Maintenance

- Deployment: Run via `streamlit run app.py` on local machine.
- Maintenance: Version control with Git; updates via code pulls.
- Support: Local logs for errors.

## Risks and Mitigation Strategies

- Risk: Data format mismatches. Mitigation: Strict validation with error messages.
- Risk: Performance on large data. Mitigation: Optimize queries, inform users of limits.
- Risk: Library dependencies. Mitigation: Use standard libraries, provide requirements.txt.

## Success Metrics

- KPIs: User adoption (sessions per week), analysis completion rate (>95%), forecast accuracy improvement (tracked via tool).
- Measurable: Log usage; compare before/after metrics.

## License

This project is licensed under the MIT License with the Commons Clause. This combination provides a source-available license that allows users to view, modify, and use the software, including for internal commercial purposes, but prohibits selling the software or providing it as a paid service where the value derives substantially from the software's functionality. A copy of the license should be included in the repository as a LICENSE file.

## Appendices

- Reference: Streamlit docs (https://docs.streamlit.io).
- Example CSV Templates: Linked in app or external (e.g., GitHub repo).
- Best Practices: Refer to supply chain forecasting standards (e.g., from APICS).
- License Reference: Commons Clause (https://commonsclause.com/).

## Contribution Guidelines

ApexPlannerLight is a source-available community project. Contributions are welcome via pull requests on the GitHub repository. Follow these steps:
- Fork the repository.
- Create a feature branch.
- Commit changes.
- Open a pull request.
- Adhere to code style and include tests.

For issues, use the GitHub issue tracker.

## Technical Instructions for Building the Product

To build ApexPlannerLight, follow these steps for an AI coder:

### File Structure
- `app.py`: Main Streamlit script.
- `requirements.txt`: List dependencies (streamlit, pandas, sqlite3, statsmodels).
- `database.py`: DB handling functions.
- `analysis.py`: Forecasting and KPI functions.
- `data/` folder: For sample CSVs or exports.
- `README.md`: Setup instructions.
- `LICENSE`: MIT License text with Commons Clause added.
- `.gitignore`: To ignore virtual env, DB files, etc.

### Step-by-Step Build Guide
1. **Setup Repository**:
   - Initialize Git: `git init`.
   - Create GitHub repo and push: Host on GitHub for community access.

2. **Add License**:
   - In LICENSE file: Include the MIT License text followed by the Commons Clause condition, with appropriate software name, licensor, etc.

3. **Setup Environment**:
   - Create virtual env: `python -m venv env`.
   - Install deps: `pip install -r requirements.txt`.

4. **Database Integration** (database.py):
   - Use sqlite3 to create tables matching data models.
   - Functions: create_tables(), insert_data(table_name, df).

5. **Data Import** (in app.py):
   - Use st.file_uploader for each data type.
   - Read CSV with pandas: pd.read_csv(uploaded_file).
   - Validate columns match expected.
   - Insert to DB.

6. **Analysis Functions** (analysis.py):
   - Performance: Join forecasts and actuals, calculate errors with offset.
   - Statistical Forecast: Use ARIMA or similar from statsmodels.
   - Outliers: Use z-score or isolation forest.
   - KPIs: Functions for accuracy, bias; aggregate by month/YTD.

7. **UI in app.py**:
   - st.sidebar for tab selection.
   - Data tab: Uploaders and previews.
   - Main tab: st.selectbox for analysis, inputs, display results with st.table, st.chart.

8. **Run and Test**:
   - `streamlit run app.py`.
   - Test with sample data.

Link to external: Statsmodels docs (https://www.statsmodels.org/stable/index.html) for forecasting models.
