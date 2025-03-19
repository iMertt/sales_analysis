# Sales Analysis Dashboard

A modern sales analytics dashboard built with Python and PyQt6 that helps analyze sales data, visualize trends, and forecast future sales.

## Features

- **Sales Statistics**
  - View top 5 products by revenue
  - Track sales quantities and revenue
  - Export detailed PDF reports

- **Data Visualization**
  - Monthly sales trend charts
  - Top products comparison graphs
  - Responsive and interactive visualizations

- **Sales Forecasting**
  - Generate revenue predictions for 1-12 months
  - View forecasted data in tabular format
  - Based on historical sales patterns

## Installation

1. Install required packages:
```bash
pip install PyQt6 pandas matplotlib seaborn scikit-learn reportlab
```
2. Generate sample data:
```bash
python generate_sample_data.py
 ```

3. Run the dashboard:
```bash
python sales_gui.py
 ```

## Usage
### Statistics Tab
- View top performing products
- See revenue and quantity metrics
- Generate PDF reports with detailed analysis
### Visualizations Tab
- Analyze monthly sales trends
- Compare product performance
- Interactive and responsive charts
### Forecasting Tab
1. Select forecast period (1-12 months)
2. Click "Generate Forecast"
3. View predicted revenue for future months
## Data Structure
The application uses a CSV file ( sales_data.csv ) with the following columns:

- product_id: Unique identifier for each product
- product_name: Name of the product
- quantity_sold: Number of units sold
- sale_date: Date of the sale
- price: Unit price of the product
## Technical Details
- Built with PyQt6 for modern UI
- Uses pandas for data analysis
- Matplotlib/Seaborn for visualizations
- Scikit-learn for sales forecasting
- ReportLab for PDF report generation
## File Structure
```plaintext
sales_analysis/
├── sales_gui.py         # Main GUI application
├── sales_analysis.py    # Core analysis functionality
├── sales_forecast.py    # Forecasting module
├── sales_report.py      # PDF report generator
├── generate_sample_data.py  # Sample data generator
└── README.md           # Documentation
 ```

## Requirements
- Python 3.8+
- PyQt6
- pandas
- matplotlib
- seaborn
- scikit-learn
- reportlab
## Output Files
- sales_data.csv : Raw sales data
- sales_report.pdf : Generated PDF reports
- monthly_sales.png : Sales trend visualization
- top_products.png : Product comparison chart
