
## 📊 IT Support Ticket Analysis Dashboard

## 🚀 Project Overview

This project analyzes IT support ticket data to uncover operational inefficiencies, SLA risks, and performance bottlenecks. The goal is not just visualization, but enabling data-driven decision-making for IT support teams.


**🎯 Business Problem**

IT support teams often struggle with:

High volume of unresolved tickets

Poor SLA compliance

Lack of visibility into critical issues

Inefficient resource allocation

## 📁 Dataset Details

## Sources:

customer_support_tickets.xlsx

Processed_data.csv

**Data Includes:

Ticket ID
Priority (Low / Medium / High / Critical)

Status (Open / Closed / In Progress)

First Response Time

Resolution Time

Created & Closed Dates

## 🛠️ Tools & Technologies

**Python** → Data cleaning & preprocessing
**SQL** → Data querying & transformation
**Power BI** → Dashboard & visualization
**Excel** → Initial data handling

## Data Processing Steps

Removed null and inconsistent values

Standardized categorical fields (priority, status)

Created calculated fields:

    1.SLA Breach Indicator
    
    2.Resolution Delay

    3.Ticket Aging


## 📊 Dashboard Features

## 🔹 KPI Metrics
        a)Total Tickets
        b)% High & Critical Tickets
        c)SLA Breach Rate
        d)Average Resolution Time
 ## 🔹 Functional Highlights
        a)Conditional formatting to highlight SLA breaches
        b)Interactive filters (priority, status, date)
        c)Drill-down capability for root cause analysis

## 📌 Key Insights

1.49.76% of tickets are High & Critical, exceeding the acceptable threshold of 20% → indicates poor ticket prioritization and potential operational risk
2.SLA breach rate is significantly high, highlighting inefficiencies in response and resolution workflows
3.Ticket volume spikes observed on specific days, suggesting mismatch between workload and resource allocation
4.Long resolution times concentrated in high-priority tickets, indicating escalation or handling inefficiencies   

## 💡 Business Impact

1.Identified SLA compliance gaps, enabling targeted process improvements
2.Provided insights for resource reallocation during peak periods
3.Highlighted high-risk tickets early, improving response prioritization
4.Enabled management to take data-driven operational decisions

## 👤 Author

Dhanunjaya Rao Sivvala

Aspiring Data Analyst | Python | SQL | Power BI
