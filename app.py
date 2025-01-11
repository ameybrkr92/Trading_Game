import streamlit as st
import pandas as pd
import numpy as np

# Initialize session state
if 'wallet' not in st.session_state:
    st.session_state.wallet = 100000  # ₹1,00,000 starting cash
    st.session_state.portfolio = 0  # Shares owned
    st.session_state.history = []  # Track net profit/loss over time
    st.session_state.transactions = []  # Transaction history
    st.session_state.target_profit = None  # Profit target
    st.session_state.target_loss = None  # Loss target
    st.session_state.achievements = set()  # Track achievements

# Generate dynamic stock price
def generate_stock_price():
    if 'stock_price' not in st.session_state:
        st.session_state.stock_price = 100  # Start price
    st.session_state.stock_price += np.random.uniform(-20, 20)  # Larger random movement
    return round(st.session_state.stock_price, 2)

# Record a transaction
def record_transaction(action, quantity, price, total):
    st.session_state.transactions.append({
        "Action": action,
        "Quantity": quantity,
        "Price": price,
        "Total (₹)": total
    })

# Check targets
def check_targets(net_profit_loss):
    if st.session_state.target_profit and net_profit_loss >= st.session_state.target_profit:
        st.success(f"🎉 You reached your profit target of ₹{st.session_state.target_profit}!")
        st.session_state.target_profit = None

    if st.session_state.target_loss and net_profit_loss <= st.session_state.target_loss:
        st.warning(f"⚠️ You hit your loss limit of ₹{st.session_state.target_loss}!")
        st.session_state.target_loss = None

# Update achievements
def update_achievements(net_profit_loss):
    if "First Trade" not in st.session_state.achievements and len(st.session_state.transactions) > 0:
        st.session_state.achievements.add("First Trade")
        st.balloons()
        st.success("🏆 Achievement Unlocked: First Trade!")

    if "Hit ₹10,000 Profit" not in st.session_state.achievements and net_profit_loss >= 10000:
        st.session_state.achievements.add("Hit ₹10,000 Profit")
        st.balloons()
        st.success("🏆 Achievement Unlocked: Hit ₹10,000 Profit!")

    if "Survived a ₹10,000 Loss" not in st.session_state.achievements and net_profit_loss <= -10000:
        st.session_state.achievements.add("Survived a ₹10,000 Loss")
        st.warning("🏆 Achievement Unlocked: Survived a ₹10,000 Loss!")

# Main App
st.title("🎮 Fun Trading Game")

# Sidebar: Wallet, stock price, and targets
st.sidebar.header("Your Wallet")
st.sidebar.metric("Balance (₹)", round(st.session_state.wallet, 2))
if st.sidebar.button("Refresh Price"):
    generate_stock_price()
current_price = st.session_state.stock_price
st.sidebar.metric("Current Stock Price (₹)", current_price)

st.sidebar.header("Set Targets")
profit_target = st.sidebar.number_input("Set Profit Target (₹)", min_value=0, step=1000, value=st.session_state.target_profit or 10000)
loss_target = st.sidebar.number_input("Set Loss Target (₹)", min_value=-100000, step=1000, value=st.session_state.target_loss or -10000)

if st.sidebar.button("Save Targets"):
    st.session_state.target_profit = profit_target
    st.session_state.target_loss = loss_target
    st.sidebar.success("Targets updated!")

# Trading actions
st.header("💰 Trade Stocks")
col1, col2 = st.columns(2)

with col1:
    buy_quantity = st.number_input("Buy Quantity", min_value=1, step=1, value=1)
    if st.button("Buy"):
        cost = buy_quantity * current_price
        if cost <= st.session_state.wallet:
            st.session_state.wallet -= cost
            st.session_state.portfolio += buy_quantity
            record_transaction("Buy", buy_quantity, current_price, -cost)
            st.success(f"Bought {buy_quantity} shares at ₹{current_price:.2f} each.")
        else:
            st.error("Not enough money to buy!")

with col2:
    sell_quantity = st.number_input("Sell Quantity", min_value=1, step=1, value=1)
    if st.button("Sell"):
        if sell_quantity <= st.session_state.portfolio:
            revenue = sell_quantity * current_price
            st.session_state.wallet += revenue
            st.session_state.portfolio -= sell_quantity
            record_transaction("Sell", sell_quantity, current_price, revenue)
            st.success(f"Sold {sell_quantity} shares at ₹{current_price:.2f} each.")
        else:
            st.error("Not enough shares to sell!")

# Update net profit/loss
portfolio_value = st.session_state.wallet + (st.session_state.portfolio * current_price)
net_profit_loss = portfolio_value - 100000  # Profit/Loss relative to the initial amount
st.session_state.history.append(net_profit_loss)

# Check targets and achievements
check_targets(net_profit_loss)
update_achievements(net_profit_loss)

# Show profit/loss graph
st.header("📈 Profit/Loss Over Time")
if len(st.session_state.history) > 1:
    df = pd.DataFrame(st.session_state.history, columns=["Net Profit/Loss"])
    st.line_chart(df)
else:
    st.write("Start trading to see your profit/loss performance!")

# Show transaction history
st.header("📜 Transaction History")
if st.session_state.transactions:
    transactions_df = pd.DataFrame(st.session_state.transactions)
    st.table(transactions_df)
else:
    st.write("No transactions yet. Start trading!")

# Show achievements
st.header("🏆 Achievements")
if st.session_state.achievements:
    st.write(", ".join(st.session_state.achievements))
else:
    st.write("No achievements yet. Start trading!")

# Footer
st.write("Note: This is a simple simulation for fun. Prices and trades are not real.")
