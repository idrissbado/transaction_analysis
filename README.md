# Transaction Analysis Dashboard

This project analyzes transaction data stored in BigQuery and visualizes the results in an interactive dashboard built using Dash. It provides insights such as Monthly Active Users (MAU), churn rate, top merchants by age bracket, and transaction seasonality.

---

## **Features**

1. **Monthly Active Users (MAU):**
   - Calculates the number of unique active users per month.

2. **Churn Analysis:**
   - Identifies churned customers each month and calculates the churn rate.

3. **Top Merchants by Age Bracket:**
   - Groups clients by age brackets and lists the top 5 merchants by transaction volume for each bracket.

4. **Transaction Seasonality:**
   - Identifies the busiest days and hours for transactions.

5. **Interactive Dashboard:**
   - Visualizes all the above metrics dynamically.

---

## **Setup Instructions**

### Prerequisites

1. **Google Cloud Project** with BigQuery enabled.
2. **Python 3.7+** installed.
3. **Google Cloud SDK** installed ([instructions here](https://cloud.google.com/sdk/docs/install)).
4. **BigQuery Dataset**: The project uses the `data_test_senior_analyst` dataset.

### Authenticate with BigQuery

1. Run the following command to authenticate:
   ```bash
   gcloud auth application-default login
