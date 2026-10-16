
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Fraud Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #f1f5f9;
}
[data-testid="stMetric"] {
    background: #111d31;
    border: 1px solid #263954;
    padding: 18px;
    border-radius: 12px;
}
[data-testid="stMetricLabel"] {
    color: #b8c7dc;
}
[data-testid="stMetricValue"] {
    color: #60a5fa;
}
h1, h2, h3 {
    color: #e5edff;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Financial Transactions & Fraud Trends")
st.caption("PaySim synthetic dataset | MySQL + Python + Plotly")

with st.sidebar:
    st.header("⚙️ Database Connection")
    mysql_user = st.text_input("MySQL username", value="root")
    mysql_password = st.text_input("MySQL password", type="password")
    connect_button = st.button("Connect & Load Dashboard", type="primary")

if not connect_button:
    st.info("Enter your MySQL credentials in the sidebar and click Connect & Load Dashboard.")
    st.stop()

try:
    connection = mysql.connector.connect(
        host="localhost",
        user=mysql_user,
        password=mysql_password,
        database="fraud_analysis",
        connection_timeout=10
    )

    @st.cache_data(ttl=300)
    def load_data():
        queries = {
            "summary": """
                SELECT
                    isFraud,
                    COUNT(*) AS total_transactions,
                    ROUND(AVG(amount), 2) AS average_amount
                FROM fraud_transactions
                GROUP BY isFraud
            """,
            "types": """
                SELECT
                    type,
                    COUNT(*) AS total_transactions,
                    SUM(isFraud) AS fraud_transactions,
                    ROUND(
                        SUM(isFraud) * 100.0 / COUNT(*), 4
                    ) AS fraud_rate_percentage
                FROM fraud_transactions
                GROUP BY type
                ORDER BY fraud_rate_percentage DESC
            """,
            "high_value": """
                SELECT
                    CASE WHEN amount >= 1000000
                         THEN 'High Value'
                         ELSE 'Other Transactions'
                    END AS category,
                    COUNT(*) AS total_transactions,
                    SUM(isFraud) AS fraud_transactions,
                    ROUND(
                        SUM(isFraud) * 100.0 / COUNT(*), 4
                    ) AS fraud_rate_percentage,
                    ROUND(AVG(amount), 2) AS average_amount
                FROM fraud_transactions
                GROUP BY category
            """,
            "distribution": """
                SELECT
                    isFraud,
                    COUNT(*) AS total_transactions
                FROM fraud_transactions
                GROUP BY isFraud
            """
        }

        result = {}
        for name, query in queries.items():
            result[name] = pd.read_sql(query, connection)
        return result

    data = load_data()
    connection.close()

except Exception as error:
    st.error("Database connection or query failed.")
    st.code(str(error))
    st.stop()

summary = data["summary"]
types_df = data["types"]
high_df = data["high_value"]
distribution = data["distribution"]

normal_row = summary[summary["isFraud"] == 0]
fraud_row = summary[summary["isFraud"] == 1]

normal_count = int(normal_row["total_transactions"].iloc[0])
fraud_count = int(fraud_row["total_transactions"].iloc[0])
total_count = normal_count + fraud_count

normal_avg = float(normal_row["average_amount"].iloc[0])
fraud_avg = float(fraud_row["average_amount"].iloc[0])

fraud_pct = fraud_count * 100 / total_count
normal_pct = normal_count * 100 / total_count

st.subheader("Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Transactions", f"{total_count:,}")
c2.metric("Fraud-labelled", f"{fraud_count:,}", f"{fraud_pct:.4f}% of total")
c3.metric("Normal-labelled", f"{normal_count:,}", f"{normal_pct:.4f}% of total")
c4.metric("Average Amount", f"{(normal_avg * normal_count + fraud_avg * fraud_count) / total_count:,.2f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Transaction Distribution")
    distribution["Category"] = distribution["isFraud"].map({
        0: "Normal-labelled",
        1: "Fraud-labelled"
    })

    fig = px.pie(
        distribution,
        names="Category",
        values="total_transactions",
        hole=0.65,
        color="Category",
        color_discrete_map={
            "Normal-labelled": "#3b82f6",
            "Fraud-labelled": "#f43f5e"
        }
    )
    fig.update_traces(
        textinfo="none",
        hovertemplate="%{label}<br>Transactions: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, b=20, l=10, r=10),
        annotations=[dict(
            text=f"{total_count:,}<br>Total",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="white")
        )]
    )
    st.plotly_chart(fig, width="stretch")
    st.caption(
        f"Fraud-labelled: {fraud_pct:.4f}% ({fraud_count:,}) · "
        f"Normal-labelled: {normal_pct:.4f}% ({normal_count:,})"
    )

with right:
    st.subheader("Average Transaction Amount")
    amount_df = pd.DataFrame({
        "Category": ["Normal-labelled", "Fraud-labelled"],
        "Average Amount": [normal_avg, fraud_avg]
    })
    fig = px.bar(
        amount_df,
        x="Category",
        y="Average Amount",
        color="Category",
        text_auto=",.2f",
        color_discrete_map={
            "Normal-labelled": "#3b82f6",
            "Fraud-labelled": "#f43f5e"
        }
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        yaxis_title="Average Amount",
        xaxis_title=""
    )
    st.plotly_chart(fig, width="stretch")

st.divider()

st.subheader("Fraud Rate by Transaction Type")
fig = px.bar(
    types_df,
    x="type",
    y="fraud_rate_percentage",
    color="fraud_rate_percentage",
    text="fraud_rate_percentage",
    color_continuous_scale=["#3b82f6", "#a78bfa", "#f43f5e"],
    hover_data=["total_transactions", "fraud_transactions"]
)
fig.update_traces(
    texttemplate="%{text:.4f}%",
    textposition="outside",
    cliponaxis=False
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    coloraxis_showscale=False,
    xaxis_title="Transaction Type",
    yaxis_title="Fraud-labelled Rate (%)"
)
st.plotly_chart(fig, width="stretch")

st.divider()

st.subheader("High-Value vs Other Transactions")
st.caption("High-value threshold: amount ≥ 1,000,000 dataset currency units.")

left, right = st.columns(2)

with left:
    fig = px.bar(
        high_df,
        x="category",
        y="fraud_rate_percentage",
        color="category",
        text="fraud_rate_percentage",
        color_discrete_map={
            "High Value": "#f43f5e",
            "Other Transactions": "#3b82f6"
        }
    )
    fig.update_traces(texttemplate="%{text:.4f}%", textposition="outside")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis_title="",
        yaxis_title="Fraud-labelled Rate (%)"
    )
    st.plotly_chart(fig, width="stretch")

with right:
    st.dataframe(
        high_df.rename(columns={
            "category": "Category",
            "total_transactions": "Total Transactions",
            "fraud_transactions": "Fraud-labelled",
            "fraud_rate_percentage": "Fraud Rate (%)",
            "average_amount": "Average Amount"
        }),
        hide_index=True,
        width="stretch"
    )

st.divider()

st.subheader("Key Insights")

high_rate = high_df.loc[
    high_df["category"] == "High Value", "fraud_rate_percentage"
].iloc[0]
other_rate = high_df.loc[
    high_df["category"] == "Other Transactions", "fraud_rate_percentage"
].iloc[0]

st.markdown(
    f"""
- Fraud-labelled transactions account for **{fraud_pct:.4f}%** of all records.
- The average amount for fraud-labelled transactions is **{fraud_avg:,.2f}**, compared with **{normal_avg:,.2f}** for normal-labelled transactions.
- The high-value transaction fraud-labelled rate is **{high_rate:.4f}%**, compared with **{other_rate:.4f}%** for other transactions.
- These are patterns in a **synthetic dataset**; they do not establish that a transaction is fraudulent in real life.
"""
)

st.caption("Data source: PaySim synthetic financial transaction dataset.")
st.caption("Dashboard results are calculated from the local MySQL fraud_analysis database.")
st.caption("Refresh data by reconnecting after the five-minute cache expires.")
