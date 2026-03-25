# Supportlytics: Data Preparation (Milestone 1)

## 1. Project Overview
Supportlytics is an IT Support Analytics initiative aimed at analyzing IT support ticket data to uncover performance trends, optimize support operations, and reduce issue resolution times. By leveraging systematic data preparation and analytics, this project transforms raw support data into actionable insights, ultimately enhancing overall IT service delivery and user satisfaction.

## 2. Dataset Description
The foundation of this analysis is a comprehensive dataset of IT support tickets. The primary columns include:
- **Ticket ID**: A unique identifier assigned to each support ticket.
- **Ticket Priority**: The urgency level of the ticket (e.g., Low, Medium, High, Critical).
- **Ticket Channel**: The communication medium through which the ticket was raised (e.g., Email, Phone, Web Portal).
- **Ticket Type**: The categorization of the technical issue (e.g., Hardware, Software, Network, Access).
- **Ticket Status**: The current state of the ticket in the resolution pipeline (e.g., Open, In Progress, Resolved, Closed).
- **First Response Minutes**: The time elapsed (in minutes) from ticket creation to the first response by an agent.
- **Resolution_Time**: The total duration taken to fully resolve and close the ticket.
- **Country**: The geographic origin of the user submitting the request.

## 3. Data Understanding
An initial inspection of the dataset provides essential context for the project:
- **Number of Rows and Columns**: The dataset comprises thousands of records representing individual tickets and 8 structural features (columns). *(Note: Replace with exact row count).*
- **Data Types**: The dataset features a mix of quantitative continuous data (First Response Minutes, Resolution_Time) and categorical string data (Priority, Channel, Type, Status, Country).

## 4. Data Cleaning
To ensure accuracy in downstream analysis, rigorous preprocessing steps were implemented:
- **Handling Missing Values**: Null or missing entries in critical fields were addressed. Numerical blanks were imputed using median values to avoid outlier skewing, while missing text fields were categorized as 'Unknown'.
- **Removing Duplicates**: Duplicate records based on the 'Ticket ID' were identified and eliminated to prevent skewed analytics.
- **Standardizing Text Fields**: Categorical features like 'Ticket Channel' and 'Ticket Type' were converted to a uniform title case to consolidate variations (e.g., unifying 'email', 'EMAIL', and 'Email' into a single category).

## 5. Feature Engineering
New variables were derived to facilitate deeper performance evaluations:
- **Resolution_Time Calculation**: Derived by calculating the exact duration between the ticket's creation timestamp and its final closure timestamp.
- **Priority_Score Creation**: A numerical weight was assigned to 'Ticket Priority' (e.g., Low = 1, Medium = 2, High = 3, Critical = 4) to allow for quantitative correlation analysis and metric sorting.

## 6. Output
- **Cleaned Dataset**: A finalized, structured tabular dataset (CSV/Excel) ready for exploratory analysis.
- **Summary of Preprocessing Steps**: A documented log of all transformations, establishing a reliable and reproducible foundation for the next milestones.
