import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from scipy import stats

class SalesDataAnalyzer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.clean_data()
    
    def detect_outliers(self, column):
        # Using IQR method to detect outliers
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)
    
    def clean_data(self):
        # Convert sale_date to datetime
        self.df['sale_date'] = pd.to_datetime(self.df['sale_date'])
        
   
        self.df['price'] = self.df['price'].fillna(self.df['price'].median())
        
        # Remove negative quantities and prices
        self.df = self.df[self.df['quantity_sold'] > 0]
        self.df = self.df[self.df['price'] > 0]
        
        # Remove outliers from price and quantity
        price_mask = self.detect_outliers('price')
        quantity_mask = self.detect_outliers('quantity_sold')
        self.df = self.df[price_mask & quantity_mask]
        
        # Calculate total revenue per sale
        self.df['revenue'] = self.df['quantity_sold'] * self.df['price']
    
    def analyze_trends(self):
        # Simple moving average for trend analysis
        monthly_sales = self.get_monthly_sales()
        rolling_mean = monthly_sales.rolling(window=3).mean()
        
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_sales.index, monthly_sales.values, label='Monthly Sales')
        plt.plot(rolling_mean.index, rolling_mean.values, label='3-Month Moving Average')
        plt.title('Sales Trend Analysis')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('sales_trend.png')
        plt.close()
    
    def get_product_statistics(self):
        stats = self.df.groupby('product_name').agg({
            'quantity_sold': ['sum', 'mean', 'std'],
            'revenue': ['sum', 'mean', 'std'],
            'price': ['mean', 'min', 'max']
        }).round(2)
        
        return stats
    
    def filter_by_date_range(self, days=30):
        end_date = self.df['sale_date'].max()
        start_date = end_date - timedelta(days=days)
        return self.df[self.df['sale_date'].between(start_date, end_date)]
    
    def get_top_products(self, n=10):
        return self.df.groupby('product_name')[['quantity_sold', 'revenue']].sum()\
               .sort_values('revenue', ascending=False).head(n)
    
    def get_monthly_sales(self):
        
        return self.df.set_index('sale_date').resample('ME')['revenue'].sum()
    
    def visualize_monthly_sales(self):
        monthly_sales = self.get_monthly_sales()
        
        plt.figure(figsize=(12, 6))
        plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
        plt.title('Monthly Sales Revenue')
        plt.xlabel('Month')
        plt.ylabel('Revenue')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('monthly_sales.png')
        plt.close()
    
    def visualize_top_products(self, n=10):
        top_products = self.get_top_products(n)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=top_products['revenue'], y=top_products.index)
        plt.title(f'Top {n} Products by Revenue')
        plt.xlabel('Revenue')
        plt.tight_layout()
        plt.savefig('top_products.png')
        plt.close()
    
    def export_analysis(self, output_file):
        # Prepare summary data
        summary = self.df.groupby('product_name').agg({
            'quantity_sold': 'sum',
            'revenue': 'sum',
            'price': 'mean'
        }).round(2)
        
        summary.to_csv(output_file)

def main():
    analyzer = SalesDataAnalyzer('sales_data.csv')
    
    # Generate visualizations
    analyzer.visualize_monthly_sales()
    analyzer.visualize_top_products()
    analyzer.analyze_trends()
    
    # Export detailed analysis
    analyzer.export_analysis('sales_analysis_results.csv')
    
    # Print enhanced statistics
    print("\nProduct Statistics:")
    print(analyzer.get_product_statistics())
    
    print("\nTop 5 Products by Revenue:")
    print(analyzer.get_top_products(5))
    
    print("\nLast 30 Days Analysis:")
    recent_data = analyzer.filter_by_date_range(30)
    print(f"Total Revenue: ${recent_data['revenue'].sum():,.2f}")
    print(f"Total Sales: {recent_data['quantity_sold'].sum():,}")

if __name__ == "__main__":
    main()