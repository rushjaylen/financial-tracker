import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample data for demonstration purposes
data = {
    "Date": ["2025-01-01", "2025-01-15", "2025-01-20", "2025-02-01", "2025-02-10"],
    "Category": ["Rent", "Groceries", "Entertainment", "Savings", "Utilities"],
    "Amount": [-1200, -300, -150, 500, -100]
}

# Convert to DataFrame
df = pd.DataFrame(data)
df["Date"] = pd.to_datetime(df["Date"])

# Aggregate expenses and income
expense_data = df[df["Amount"] < 0]
income_data = df[df["Amount"] > 0]

# Summarize expenses by category
expense_summary = expense_data.groupby("Category")["Amount"].sum().reset_index()

# Create Plotly figures
expense_fig = px.bar(
    expense_summary, 
    x="Category", 
    y="Amount", 
    title="Expenses by Category",
    labels={"Amount": "Amount ($)"},
    text="Amount",
    color="Category"
)
expense_fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

# Dashboard layout
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Personal Finance Dashboard", style={"textAlign": "center"}),
    
    dcc.Graph(figure=expense_fig),

    html.Div([
        html.H3("Key Insights:"),
        html.P(f"Total Expenses: ${-expense_data['Amount'].sum():,.2f}"),
        html.P(f"Total Income: ${income_data['Amount'].sum():,.2f}"),
        html.P(f"Net Balance: ${df['Amount'].sum():,.2f}")
    ], style={"marginTop": "20px", "padding": "10px", "border": "1px solid #ddd", "borderRadius": "10px"})
])

if __name__ == "__main__":
    app.run_server(debug=True)
