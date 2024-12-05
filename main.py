from google.cloud import bigquery
import pandas as pd
import dash
from dash import dcc, html
import os

# Set up BigQuery client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"  # Path to your service account
client = bigquery.Client()

# Queries for analysis
queries = {
    "mau": """
        WITH monthly_transactions AS (
            SELECT
                DATE_TRUNC(issueddate, MONTH) AS month,
                accountid
            FROM `your_project_id.data_test_senior_analyst.transactions`
            WHERE status = 'completed' AND isactive = TRUE
            GROUP BY 1, 2
        )
        SELECT
            month,
            COUNT(DISTINCT accountid) AS mau
        FROM monthly_transactions
        GROUP BY month
        ORDER BY month;
    """,
    "churn_rate": """
        WITH monthly_transactions AS (
            SELECT
                DATE_TRUNC(issueddate, MONTH) AS month,
                accountid
            FROM `your_project_id.data_test_senior_analyst.transactions`
            WHERE status = 'completed' AND isactive = TRUE
            GROUP BY 1, 2
        ),
        active_clients AS (
            SELECT
                month,
                accountid
            FROM monthly_transactions
        ),
        churned_clients AS (
            SELECT
                curr.month AS current_month,
                COUNT(prev.accountid) AS churners
            FROM active_clients curr
            LEFT JOIN active_clients prev
            ON curr.accountid = prev.accountid AND curr.month = prev.month + INTERVAL '1 month'
            WHERE prev.accountid IS NULL
            GROUP BY curr.month
        )
        SELECT
            current_month,
            churners,
            (churners::FLOAT / prev_mau.mau) * 100 AS churn_rate
        FROM churned_clients
        JOIN (
            SELECT
                month,
                COUNT(DISTINCT accountid) AS mau
            FROM monthly_transactions
            GROUP BY month
        ) AS prev_mau
        ON churned_clients.current_month = prev_mau.month + INTERVAL '1 month';
    """,
    "top_merchants": """
        WITH client_age AS (
            SELECT
                clients.id AS client_id,
                profiles.placeofbirth,
                DATE_PART('year', AGE(clients.createdat)) AS age
            FROM `your_project_id.data_test_senior_analyst.clients` AS clients
            JOIN `your_project_id.data_test_senior_analyst.profiles` AS profiles
            ON clients.profileid = profiles.id
        ),
        age_brackets AS (
            SELECT
                client_id,
                CASE
                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN age BETWEEN 36 AND 50 THEN '36-50'
                    ELSE '50+'
                END AS age_bracket
            FROM client_age
        ),
        merchant_volume AS (
            SELECT
                transactions.merchantname,
                age_brackets.age_bracket,
                SUM(transactions.chargedamount) AS total_volume
            FROM `your_project_id.data_test_senior_analyst.transactions` AS transactions
            JOIN `your_project_id.data_test_senior_analyst.accounts` AS accounts
            ON transactions.accountid = accounts.id
            JOIN age_brackets
            ON accounts.clientid = age_brackets.client_id
            GROUP BY transactions.merchantname, age_brackets.age_bracket
        )
        SELECT
            age_bracket,
            merchantname,
            total_volume
        FROM (
            SELECT
                age_bracket,
                merchantname,
                total_volume,
                ROW_NUMBER() OVER (PARTITION BY age_bracket ORDER BY total_volume DESC) AS rank
            FROM merchant_volume
        ) ranked_merchants
        WHERE rank <= 5;
    """
}

# Fetch and process data
results = {}
for key, query in queries.items():
    print(f"Fetching {key}...")
    results[key] = client.query(query).to_dataframe()

# Dashboard App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Transaction Analysis Dashboard"),
    
    html.Div([
        html.H3("Monthly Active Users (MAU)"),
        dcc.Graph(
            figure={
                "data": [
                    {"x": results["mau"]["month"], "y": results["mau"]["mau"], "type": "bar", "name": "MAU"}
                ],
                "layout": {"title": "Monthly Active Users"}
            }
        ),
    ]),

    html.Div([
        html.H3("Churn Rate"),
        dcc.Graph(
            figure={
                "data": [
                    {"x": results["churn_rate"]["current_month"], "y": results["churn_rate"]["churn_rate"], "type": "line", "name": "Churn Rate"}
                ],
                "layout": {"title": "Monthly Churn Rate"}
            }
        ),
    ]),

    html.Div([
        html.H3("Top Merchants by Age Bracket"),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": results["top_merchants"][results["top_merchants"]["age_bracket"] == age]["merchantname"],
                        "y": results["top_merchants"][results["top_merchants"]["age_bracket"] == age]["total_volume"],
                        "type": "bar",
                        "name": age
                    }
                    for age in results["top_merchants"]["age_bracket"].unique()
                ],
                "layout": {"title": "Top Merchants by Age Bracket"}
            }
        ),
    ]),
])

if __name__ == "__main__":
    app.run_server(debug=True)
