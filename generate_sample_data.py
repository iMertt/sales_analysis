import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(num_records=1000):
    # Sample product names
    products = [
        "Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch",
        "Camera", "Speaker", "Monitor", "Keyboard", "Mouse"
    ]
    
    # Generate random data
    data = {
        'product_id': range(1, num_records + 1),
        'product_name': np.random.choice(products, num_records),
        'quantity_sold': np.random.randint(1, 50, num_records),
        'sale_date': [
            datetime.now() - timedelta(days=np.random.randint(0, 365))
            for _ in range(num_records)
        ],
        'price': np.random.uniform(10, 1000, num_records)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some missing values
    df.loc[np.random.choice(df.index, 50), 'price'] = np.nan
    
    # Save to CSV
    df.to_csv('sales_data.csv', index=False)

if __name__ == "__main__":
    generate_sample_data()