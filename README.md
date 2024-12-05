# Transaction Analysis Dashboard

This project analyzes transaction data stored in BigQuery and visualizes the results in an interactive dashboard built using Dash. It provides insights such as Monthly Active Users (MAU), churn rate, top merchants by age bracket, and transaction seasonality.

---

## **Features**

1. **Monthly Active Users (MAU):**
   - Calculates the number of unique active users per month based on transactions.

2. **Churn Analysis:**
   - Identifies churned customers each month and calculates the churn rate.

3. **Top Merchants by Age Bracket:**
   - Groups clients by age brackets and lists the top 5 merchants by transaction volume for each bracket.

4. **Transaction Seasonality:**
   - Identifies the busiest days and hours for transactions.

5. **Interactive Dashboard:**
   - Visualizes all the above metrics dynamically.

---

## **Dataset Schema**

The project uses the BigQuery dataset `data_test_senior_analyst`, which contains the following tables:

### **Transactions Table**
| Column             | Description                                             |
|--------------------|---------------------------------------------------------|
| `id`               | Unique identifier for the transaction.                  |
| `createdat`        | Timestamp when the transaction was created.             |
| `updatedat`        | Timestamp when the transaction was last updated.        |
| `deletedat`        | Timestamp when the transaction was deleted (if any).    |
| `isactive`         | Indicates if the transaction is active (`TRUE`/`FALSE`).|
| `label`            | Label or description of the transaction.                |
| `issueddate`       | Effective date of the transaction.                      |
| `chargedamount`    | Transaction amount charged.                             |
| `accountid`        | Identifier of the associated account.                   |
| `status`           | Status of the transaction (e.g., `completed`).          |
| `type`             | Type of transaction (e.g., `deposit`, `transfer`).      |
| `merchantname`     | Name of the merchant involved in the transaction.       |
| `transactionservice` | Service associated with the transaction.              |
| `subscriptionplan` | Subscription plan tied to the transaction (if any).     |

### **Accounts Table**
| Column                  | Description                                               |
|-------------------------|-----------------------------------------------------------|
| `clientid`              | Identifier for the associated client.                     |
| `createdat`             | Timestamp when the account was created.                   |
| `updatedat`             | Timestamp when the account was last updated.              |
| `isactive`              | Indicates if the account is active (`TRUE`/`FALSE`).      |
| `status`                | Status of the account.                                    |
| `category`              | Category of the account.                                  |
| `id`                    | Unique identifier for the account.                        |
| `deletedat`             | Timestamp when the account was deleted (if any).          |
| `account_type`          | Type of the account.                                      |
| `first_account_createdat` | Timestamp of the first account creation for the client. |

### **Clients Table**
| Column          | Description                                         |
|-----------------|-----------------------------------------------------|
| `createdat`     | Timestamp when the client signed up.                |
| `updatedat`     | Timestamp when the client information was updated.  |
| `deletedat`     | Timestamp when the client was deleted (if any).     |
| `isactive`      | Indicates if the client is active (`TRUE`/`FALSE`). |
| `profileid`     | Identifier for the associated profile.              |
| `blockedreason` | Reason why the client is blocked (if applicable).   |

### **Profiles Table**
| Column                | Description                                            |
|-----------------------|--------------------------------------------------------|
| `maritalStatus`       | Marital status of the client.                          |
| `fundOrigin`          | Source of the client's funds.                          |
| `taxObligations`      | Tax obligations of the client.                         |
| `americanCitizen`     | Indicates if the client is a U.S. citizen (`TRUE`/`FALSE`). |
| `placeOfBirth`        | Place of birth of the client.                          |
| `professionalSituation` | Professional situation of the client.                |
| `maritalRegime`       | Marital regime of the client.                          |
| `avatar`              | Avatar of the client.                                  |
| `avatarUpdatedAt`     | Timestamp when the avatar was last updated.            |
| `emailIsVerified`     | Indicates if the client's email is verified (`TRUE`/`FALSE`). |

---

## **Setup Instructions**

### Prerequisites

1. **Google Cloud Project** with BigQuery enabled.
2. **Python 3.7+** installed.
3. **Google Cloud SDK** installed ([instructions here](https://cloud.google.com/sdk/docs/install)).
4. A service account key file (`service-account.json`).

### Authenticate with BigQuery

1. Run the following command to authenticate:
   ```bash
   gcloud auth application-default login
## Place the service-account.json file in the project directory.
Set the GOOGLE_APPLICATION_CREDENTIALS environment variable:

export GOOGLE_APPLICATION_CREDENTIALS="service-account.json"
## Install Dependencies
## Install Python dependencies from the requirements.txt file:


pip install -r requirements.txt
# Run the Application
## Execute the main script to launch the dashboard:


python main.py
 ##  Open your browser and navigate to the local server (default: http://127.0.0.1:8050/).
## Key Features and Visualizations
Monthly Active Users (MAU):

Bar chart displaying monthly active users.
Churn Rate:

Line chart showing the percentage of churned customers each month.
Top Merchants by Age Bracket:

Grouped bar chart showcasing top merchants for each age bracket.
Transaction Seasonality:

Heatmap highlighting the busiest days and hours for transactions.
