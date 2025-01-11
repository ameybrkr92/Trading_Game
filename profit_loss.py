import streamlit as st
import random
import pandas as pd
import time

# Initialize session state variables
if 'wallet' not in st.session_state:
    st.session_state.wallet = 100000  # Starting amount in rupees
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = 0  # Number of shares owned
if 'stock_price' not in st.session_state:
    st.session_state.stock_price = random.uniform(100, 500)  # Initial stock price
if 'history' not in st.session_state:
    st.session_state.history = [0]  # Tracks net profit/loss
if 'transactions' not in st.session_state:
    st.session_state.transactions = []  # Record of all transactions
if 'target_profit' not in st.session_state:
    st.session_state.target_profit = 10000  # Default profit target
if 'target_loss' not in st.session_state:
    st.session_state.target_loss = -10000  # Default loss target
if 'refresh_count' not in st.session_state:
    st.session_state.refresh_count = 0  # Count of price refreshes

def generate_stock_price():
    """Simulates stock price movement."""
    st.session_state.stock_price += random.uniform(-5, 5)
    st.session_state.stock_price = max(1, st.session_state.stock_price)  # Ensure price stays positive

def record_transaction(action, quantity, price, total):
    """Records a buy or sell transaction."""
    st.session_state.transactions.append({
        "Action": action,
        "Quantity": quantity,
        "Price": round(price, 2),
        "Total (₹)": round(total, 2)
    })

def update_history():
    """Updates the profit/loss history for the graph."""
    portfolio_value = st.session_state.wallet + (st.session_state.portfolio * st.session_state.stock_price)
    net_profit_loss = round(portfolio_value - 100000, 2)
    st.session_state.history.append(net_profit_loss)

# App layout
st.title("Virtual Trading Game")
st.sidebar.header("Your Trading Dashboard")

# Display current stock price
st.sidebar.metric("Current Stock Price (₹)", round(st.session_state.stock_price, 2))

# Wallet balance and portfolio value
portfolio_value = st.session_state.wallet + (st.session_state.portfolio * st.session_state.stock_price)
st.sidebar.metric("Balance (₹)", round(st.session_state.wallet, 2))
st.sidebar.metric("Net Profit/Loss (₹)", round(portfolio_value - 100000, 2))
st.sidebar.metric("Shares Owned", st.session_state.portfolio)

# Targets
profit_target = st.sidebar.number_input(
    "Set Profit Target (₹)", min_value=0, step=1000, value=st.session_state.target_profit
)
loss_target = st.sidebar.number_input(
    "Set Loss Target (₹)", min_value=-100000, step=1000, value=st.session_state.target_loss
)

if st.sidebar.button("Save Targets"):
    st.session_state.target_profit = profit_target
    st.session_state.target_loss = loss_target
    st.sidebar.success("Targets updated!")

# Refresh stock price
if st.sidebar.button("Refresh Price"):
    st.session_state.refresh_count += 1
    generate_stock_price()

st.sidebar.metric("Price Refreshes", st.session_state.refresh_count)

# Buy/Sell section
col1, col2 = st.columns(2)

with col1:
    buy_quantity = st.number_input("Quantity to Buy", min_value=1, step=1, value=1)
    if st.button("Buy"):
        cost = buy_quantity * st.session_state.stock_price
        if cost <= st.session_state.wallet:
            st.session_state.wallet -= cost
            st.session_state.portfolio += buy_quantity
            record_transaction("Buy", buy_quantity, st.session_state.stock_price, -cost)
            st.success(f"Bought {buy_quantity} shares at ₹{st.session_state.stock_price:.2f} each.")
            update_history()
        else:
            st.error("Not enough money to buy!")

with col2:
    sell_quantity = st.number_input("Quantity to Sell", min_value=1, step=1, value=1)
    if st.button("Sell"):
        if sell_quantity <= st.session_state.portfolio:
            revenue = sell_quantity * st.session_state.stock_price
            st.session_state.wallet += revenue
            st.session_state.portfolio -= sell_quantity
            record_transaction("Sell", sell_quantity, st.session_state.stock_price, revenue)
            st.success(f"Sold {sell_quantity} shares at ₹{st.session_state.stock_price:.2f} each.")
            update_history()
        else:
            st.error("Not enough shares to sell!")

# Display transaction history
st.subheader("Transaction History")
if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    st.table(df)
else:
    st.write("No transactions yet.")

# Profit/Loss graph
st.subheader("Net Profit/Loss Over Time")
st.line_chart(st.session_state.history)

# Target notifications
net_profit_loss = round(portfolio_value - 100000, 2)
if net_profit_loss >= st.session_state.target_profit:
    st.success(f"Congratulations! You've reached your profit target of ₹{st.session_state.target_profit}!")
if net_profit_loss <= st.session_state.target_loss:
    st.error(f"Warning: You've hit your loss target of ₹{st.session_state.target_loss}.")
