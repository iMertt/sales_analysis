from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                           QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                           QSpinBox, QScrollArea, QMessageBox, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys
from sales_analysis import SalesDataAnalyzer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ModernSalesGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Analysis Dashboard")
        self.setMinimumSize(1200, 800)
        self.analyzer = SalesDataAnalyzer('sales_data.csv')
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: none;
                background: #ffffff;
            }
            QTabBar::tab {
                padding: 12px 25px;
                margin: 0 2px;
                background: #e8eaf6;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #3f51b5;
                font-weight: bold;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #3f51b5;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: #c5cae9;
            }
        """)
        
        # Add tabs
        tabs.addTab(self.create_stats_tab(), "Statistics")
        tabs.addTab(self.create_viz_tab(), "Visualizations")
        tabs.addTab(self.create_forecast_tab(), "Forecasting")
        
        layout.addWidget(tabs)
        
        self.setStyleSheet("""
            QMainWindow {
                background: #ffffff;
            }
            QPushButton {
                padding: 12px 24px;
                background: #3f51b5;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #303f9f;
            }
            QLabel {
                color: #263238;
                font-size: 14px;
                padding: 8px;
            }
            QSpinBox {
                padding: 10px;
                border: 2px solid #3f51b5;
                border-radius: 6px;
                background: white;
                color: #263238;
                font-size: 14px;
                min-width: 100px;
            }
            QScrollArea {
                border: none;
                background: white;
                border-radius: 8px;
            }
            QWidget#stats_content {
                background: white;
                padding: 25px;
            }
            QTextEdit {
                background: white;
                border: 2px solid #e8eaf6;
                border-radius: 8px;
                padding: 15px;
                color: #263238;
                font-size: 14px;
                line-height: 1.6;
            }
        """)

    def create_stats_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Add scrollable area for statistics
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setObjectName("stats_content")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        # Add top products
        top_products = self.analyzer.get_top_products(5)
        stats_label = QLabel("Top 5 Products by Revenue:")
        stats_label.setStyleSheet("""
            font-weight: bold;
            font-size: 18px;
            color: #212529;
            padding: 10px 0;
        """)
        scroll_layout.addWidget(stats_label)
        
        for product, row in top_products.iterrows():
            product_info = f"{product}: ${row['revenue']:,.2f} ({row['quantity_sold']} units)"
            label = QLabel(product_info)
            label.setStyleSheet("""
                background: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
                color: #495057;
                font-size: 14px;
            """)
            scroll_layout.addWidget(label)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Export button
        export_btn = QPushButton("Export PDF Report")
        export_btn.clicked.connect(self.export_pdf)
        layout.addWidget(export_btn)
        
        return tab
    
    def create_viz_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create scroll area for responsive behavior
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        viz_layout = QVBoxLayout(scroll_content)
        
        # Create matplotlib figures
        self.analyzer.visualize_monthly_sales()
        self.analyzer.visualize_top_products()
        
        # Load images with responsive behavior
        monthly_sales = QLabel()
        monthly_sales.setScaledContents(True)
        monthly_sales.setMaximumHeight(400)
        monthly_sales.setMinimumHeight(300)
        pixmap = QPixmap('monthly_sales.png')
        monthly_sales.setPixmap(pixmap)
        
        top_products = QLabel()
        top_products.setScaledContents(True)
        top_products.setMaximumHeight(400)
        top_products.setMinimumHeight(300)
        pixmap = QPixmap('top_products.png')
        top_products.setPixmap(pixmap)
        
        viz_layout.addWidget(monthly_sales)
        viz_layout.addWidget(top_products)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        return tab
    
    def create_forecast_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Sales Forecast Analysis")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Control panel
        control_panel = QWidget()
        control_panel.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        control_layout = QHBoxLayout(control_panel)
        
        # Period selection
        period_widget = QWidget()
        period_layout = QVBoxLayout(period_widget)
        period_label = QLabel("Forecast Period")
        period_label.setStyleSheet("font-weight: bold; color: #34495e;")
        
        self.months_input = QSpinBox()
        self.months_input.setMinimum(1)
        self.months_input.setMaximum(12)
        self.months_input.setValue(3)
        self.months_input.setStyleSheet("""
            QSpinBox {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.months_input)
        control_layout.addWidget(period_widget)
        
        # Generate button
        forecast_btn = QPushButton("Generate Forecast")
        forecast_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 30px;
                background: #3498db;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        forecast_btn.clicked.connect(self.show_forecast)
        control_layout.addWidget(forecast_btn)
        control_layout.addStretch()
        
        layout.addWidget(control_panel)
        
        # Results area
        self.forecast_result = QTextEdit()
        self.forecast_result.setReadOnly(True)
        self.forecast_result.setStyleSheet("""
            QTextEdit {
                background: white;
                border-radius: 10px;
                padding: 20px;
                font-size: 14px;
                line-height: 1.6;
                margin-top: 20px;
            }
        """)
        layout.addWidget(self.forecast_result)
        
        return tab

    def show_forecast(self):
        from sales_forecast import generate_forecast
        months = self.months_input.value()
        forecast = generate_forecast(self.analyzer, months)
        
        
        result_text = "<h2 style='color: #3f51b5; margin-bottom: 20px;'>Forecasted Revenue</h2>"
        result_text += "<table style='width:100%; border-collapse: collapse;'>"
        result_text += "<tr><th style='padding:12px; background:#e8eaf6; color:#3f51b5;'>Month</th>"
        result_text += "<th style='padding:12px; background:#e8eaf6; color:#3f51b5;'>Revenue</th></tr>"
        
        for date, value in forecast.items():
            result_text += f"<tr><td style='padding:12px; border-bottom:1px solid #e8eaf6;'>{date.strftime('%B %Y')}</td>"
            result_text += f"<td style='padding:12px; border-bottom:1px solid #e8eaf6;'>${value:,.2f}</td></tr>"
        
        result_text += "</table>"
        self.forecast_result.setHtml(result_text)

    def export_pdf(self):
        try:
            from sales_report import generate_pdf_report
            generate_pdf_report(self.analyzer)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("PDF Report Generated Successfully!")
            msg.setWindowTitle("Success")
            msg.exec()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText(f"Error generating PDF: {str(e)}")
            msg.setWindowTitle("Error")
            msg.exec()

def main():
    app = QApplication(sys.argv)
    window = ModernSalesGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()