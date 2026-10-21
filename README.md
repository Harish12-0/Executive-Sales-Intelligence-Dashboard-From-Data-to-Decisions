# Sales Data Analysis Dashboard

An interactive sales analytics dashboard built with **Python, Streamlit, Pandas, and Plotly**. It provides an at-a-glance view of sales, profit, cost of goods sold (COGS), profitability, and regional/segment performance.

> **Important data note:** The repository includes a synthetic demonstration dataset (`data/sales_demo.csv`) so the project runs immediately. It is not the original source data behind the reference dashboard and should not be used for real business decisions. Replace it with data you are authorized to use.

## Dashboard Preview

![Sales Data Analysis dashboard reference](assets/dashboard-preview.jpg)

The image above is the reference design supplied for this project. The running Streamlit app recreates the main dashboard concepts with interactive charts and filters; it is not a pixel-perfect clone of the screenshot.

## Features

- **KPI cards:** Net Sales, Profit Margin, Profit, COGS, and Gross Sales.
- **Segment analysis:** Compare net sales across Consumer, Corporate, and Home Office segments.
- **Monthly trend:** Explore monthly net sales and profit over time.
- **Regional mix:** View each region's share of net sales in a donut chart.
- **State ranking:** Compare the highest-performing states by net sales.
- **Detail table:** Review region, state, shipping mode, gross sales, profit margin, COGS, net sales, and profit.
- **Interactive filters:** Filter by year range, region, and segment.
- **CSV upload:** Use a different sales dataset through the sidebar.
- **Export:** Download the currently filtered data as CSV.
- **Responsive layout:** Designed to work in a browser on desktop and laptop screens.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Dashboard UI and interactive controls |
| Pandas | Data cleaning, grouping, and KPI calculations |
| Plotly Express / Graph Objects | Interactive charts |
| CSV | Demo data and export format |

## Repository Structure

```text
sales-data-analysis/
├── app.py                  # Streamlit dashboard application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── data/
│   └── sales_demo.csv       # Synthetic sample dataset
└── assets/
    └── dashboard-preview.jpg
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/sales-data-analysis.git
cd sales-data-analysis
```

Replace `YOUR-USERNAME` with your GitHub username and use the repository URL you create.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Start the dashboard

```bash
streamlit run app.py
```

Streamlit will print a local URL, typically `http://localhost:8501`. Open it in your browser.

## Dataset Format

The app expects a CSV with these columns (column names are case-sensitive in the current implementation):

| Column | Meaning | Example |
|---|---|---|
| `Order Date` | Date of the order | `2017-06-15` |
| `Region` | Sales region | `West` |
| `State` | State or territory | `California` |
| `Segment` | Customer segment | `Consumer` |
| `Ship Mode` | Shipping service | `Standard Class` |
| `Gross Sales` | Gross sales amount | `342.19` |
| `Profit Margin` | Margin percentage for a row | `16.22` |
| `COGS` | Cost of goods sold | `298.76` |
| `Net` | Net sales amount | `401.56` |
| `Profit` | Profit amount | `62.80` |

The app derives `Year` and `Month Start` from `Order Date`. Additional columns are allowed and are preserved in the downloadable filtered dataset.

### Use your own dataset

1. Prepare a CSV using the required columns above.
2. Start the app.
3. In the sidebar, choose **Upload your sales CSV**.
4. Select your file and apply filters.

**Metric definition:** The app calculates the headline profit margin as `sum(Profit) / sum(Gross Sales) * 100`. Confirm this definition matches your organization's reporting rules before presenting results. The row-level `Profit Margin` column is displayed in the detail table but is not averaged for the headline KPI.

## KPI Definitions

- **Net Sales:** Sum of the `Net` column for the selected filters.
- **Profit Margin:** Total profit divided by total gross sales, multiplied by 100.
- **Profit:** Sum of the `Profit` column.
- **COGS:** Sum of the `COGS` column.
- **Gross Sales:** Sum of the `Gross Sales` column.

All figures respond to the active year, region, and segment filters.

## Suggested Business Questions

Use the dashboard to explore questions such as:

1. Which customer segment contributes the most net sales?
2. How do net sales and profit change month by month?
3. Which region contributes the largest share of net sales?
4. Which states have the highest net sales?
5. How does performance vary when filtering by year, region, or segment?
6. Are high sales accompanied by healthy profit?

## Publish on GitHub

1. Create a new repository on GitHub named `sales-data-analysis`.
2. Keep it public if you want recruiters to view it.
3. From this project folder, run:

```bash
git init
git add .
git commit -m "Build interactive sales data analysis dashboard"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/sales-data-analysis.git
git push -u origin main
```

If Git asks you to authenticate, use GitHub's supported sign-in or token workflow. Do not put passwords, access tokens, or private data in the repository.

### Recommended GitHub repository description

> Interactive sales analytics dashboard built with Python, Streamlit, Pandas and Plotly. Includes KPI cards, monthly trends, segment and regional analysis, state rankings, filters, and CSV export.

### Suggested GitHub topics

`python` · `streamlit` · `pandas` · `plotly` · `data-analytics` · `sales-dashboard` · `data-visualization`

## Deployment (Optional)

You can deploy this app using Streamlit Community Cloud:

1. Push the repository to GitHub.
2. Sign in to Streamlit Community Cloud.
3. Create an app and select this repository, branch `main`, and file `app.py`.
4. Deploy and test the public URL.

Check Streamlit's current deployment documentation for up-to-date account and deployment requirements. Avoid uploading confidential or personally identifiable business data to a public repository or public app.

## Future Improvements

- Add product/category-level analysis.
- Add target-versus-actual sales and profit.
- Add year-over-year growth and rolling averages.
- Add data-quality checks and automated tests.
- Add a database connector for regularly refreshed data.
- Add a Power BI version if the project is intended to demonstrate Power BI skills.

## Limitations

- Demo values are generated synthetic data, not verified company results.
- The dashboard does not infer business causation; it visualizes selected metrics.
- Profit margin depends on the business's chosen definition and data quality.
- Uploaded data must match the required schema.

## Author

**Your Name**  
Data Analyst / Power BI Analyst

- LinkedIn: `https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE/`
- GitHub: `https://github.com/YOUR-USERNAME`

Update the author section with your real profile links before publishing.

## License

This project is provided under the MIT License. Add a `LICENSE` file if you want others to reuse and modify the code under those terms.
