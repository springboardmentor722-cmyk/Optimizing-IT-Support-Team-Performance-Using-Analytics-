## Milestone 1 - Data Acquisition, Cleaning and Feature Engineering

## Overview

This milestone establishes the analytical foundation of the Supportlytics project. The focus is on acquiring the IT support ticket dataset, performing a thorough data quality assessment, applying systematic data cleaning procedures, and engineering meaningful features to support downstream analysis.

---

## Dataset Summary

| Attribute | Details |
|-----------|---------|
| File Name | customer_support_tickets.xlsx |
| Total Records | 8,469 tickets |
| Total Columns | 17 columns |
| Source | Internal IT Support Ticket System |

---

## Methodology

### Step 1 - Data Acquisition and Exploration

The dataset was loaded using the Pandas library and subjected to an initial structural analysis. The following tasks were performed:

- Verified dataset dimensions: 8,469 rows and 17 columns
- Examined column names, data types, and null value distribution
- Identified key categorical and numerical features for analysis
- Computed initial ticket distribution across Ticket Type, Ticket Priority, and Ticket Channel

### Step 2 - Data Cleaning

A structured data cleaning process was applied to improve data quality and relevance. The following columns were removed:

| Column Removed | Reason |
|----------------|--------|
| Unnamed: 9 | Completely empty column with no data |
| Customer Email | Personally identifiable information, not required for analysis |
| Customer Satisfaction Rating | Excessive missing values (67% null) |
| Resolution | Excessive missing values (67% null) |

Dataset dimensions after cleaning: 8,469 rows and 13 columns

### Step 3 - Feature Engineering

Two new features were engineered to enhance the analytical capability of the dataset:

- Resolution Duration - Calculated as the difference between Time to Resolution and First Response Time. This metric quantifies the time taken to resolve each support ticket.
- Priority Score - A numerical encoding of the Ticket Priority field to support quantitative analysis and performance comparisons.

---

## Ticket Distribution Analysis

| Ticket Type | Volume | Share |
|-------------|--------|-------|
| Refund Request | 1,752 | 20.69% |
| Technical Issue | 1,747 | 20.63% |
| Cancellation Request | 1,695 | 20.01% |
| Product Inquiry | 1,641 | 19.38% |
| Billing Inquiry | 1,634 | 19.29% |

The distribution across ticket types is balanced, indicating a diverse range of support requests with no single category dominating the dataset.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core programming language |
| Pandas | Data loading, exploration, and cleaning |
| NumPy | Numerical computations and feature engineering |
| Jupyter Notebook | Interactive development and documentation |

---

## Deliverables

- Cleaned dataset saved as Supportlytics_Final_Data.csv
- Feature engineering summary documented in Python_notebook.ipynb
- Data dictionary covering all 13 retained columns

---

