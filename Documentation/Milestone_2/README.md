# Supportlytics: Exploratory Data Analysis (Milestone 2)

## 1. Introduction to EDA
Exploratory Data Analysis (EDA) is employed to uncover underlying patterns, detect anomalies, and identify initial trends within the cleaned IT support dataset. This phase utilizes descriptive statistics and visual storytelling to establish a thorough understanding of ticket distributions and the day-to-day realities of the IT support desk.

## 2. Visualizations
To interpret the dataset holistically, the following foundational visualizations were developed:
- **Ticket Distribution by Priority**: An assessment of the volume of tickets segmented by urgency levels.
- **Ticket Distribution by Channel**: A comparison of ticket volumes originating from various communication platforms.
- **Ticket Type Distribution**: An analysis of the specific categories of support issues requested by users.
- **Ticket Status Distribution**: A snapshot of the operational pipeline, showing the ratio of active versus resolved cases.

## 3. Key Insights
The EDA phase surfaced several critical operational realities:
- **Most Frequent Issues**: Software and Access/Authentication requests consistently constitute the highest volume of incoming tickets.
- **Priority Distribution**: While 'Medium' and 'Low' priority tickets make up the bulk of the queue, 'Critical' tickets demand a disproportionate amount of immediate attention.
- **Channel Usage**: The 'Web Portal' and 'Email' are the preferred, highest-volume methods for issue submission, whereas the 'Phone' channel is typically reserved for urgent escalations.

## 4. Charts Explanation
A comprehensive suite of 8 visual charts was generated to interpret the data:
1. **Bar Chart (Priority Distribution)**: Highlights the demand placed on resources across varying levels of urgency, showing which priorities dominate the queue.
2. **Pie Chart (Channel Breakdown)**: Illustrates user preferences for communication, indicating where self-service or automated responses might be most effective.
3. **Horizontal Bar Chart (Ticket Types)**: Clearly ranks issue categories by volume, helping identify which technical domains require the largest dedicated workforce.
4. **Donut Chart (Ticket Status)**: Visualizes the current backlog versus completed work, representing the overall clearance rate of the support desk.
5. **Histogram (First Response Minutes)**: Maps the density of response times, revealing the average time users wait before acknowledging. 
6. **Box Plot (Resolution Times)**: Identifies statistical outliers, showcasing specific tickets that took anomalously long to resolve.
7. **Stacked Column Chart (Type by Priority)**: Uncovers correlations, demonstrating whether specific issue types (like Network failures) are inherently associated with higher priority flags.
8. **Treemap (Categorical Overview)**: Provides a hierarchical view of the overall ticket taxonomy, making it easy to see the largest segments of IT support work at a glance.
