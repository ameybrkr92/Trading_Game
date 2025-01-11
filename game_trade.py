import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go

# Initialize session state
def initialize_state():
    if "current_trade" not in st.session_state:
        st.session_state.current_trade = 1
    if "results" not in st.session_state:
        st.session_state.results = []
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "show_next_button" not in st.session_state:
        st.session_state.show_next_button = False

# Setup game page
def setup_game():
    st.title("Trading Game Setup")
    st.session_state.name = st.text_input("Enter your name:", "")
    st.session_state.num_bots = st.slider("Select number of bots:", 1, 4, 2)
    st.session_state.num_trades = st.slider("Select number of trades:", 5, 20, 10)
    st.session_state.initial_amount = st.number_input("Enter initial amount (₹):", min_value=1000, step=500, value=10000)

    if st.button("Start Game"):
        st.session_state.current_trade = 1
        st.session_state.results = []
        st.session_state.game_over = False
        st.session_state.show_next_button = False
        st.experimental_rerun()

# Trading page
def trade_page():
    st.title(f"Trading Round {st.session_state.current_trade}")

    trade_amount = st.slider(
        "Select trade amount (₹):", 
        min_value=0, 
        max_value=int(st.session_state.initial_amount / 2), 
        step=500, 
        value=0, 
        key=f"slider_{st.session_state.current_trade}"
    )

    if not st.session_state.show_next_button:
        if st.button("Trade"):
            result = calculate_trade_result(trade_amount)
            st.session_state.results.append(result)
            st.session_state.initial_amount += result["profit_loss"]

            if result["profit_loss"] > 0:
                st.success(f"You made a profit of ₹{result['profit_loss']:.2f}!")
            else:
                st.error(f"You incurred a loss of ₹{-result['profit_loss']:.2f}!")

            st.session_state.show_next_button = True
            st.experimental_rerun()

    if st.session_state.show_next_button:
        if st.button("Next Trade"):
            st.session_state.current_trade += 1
            st.session_state.show_next_button = False
            if st.session_state.current_trade > st.session_state.num_trades:
                st.session_state.game_over = True
            st.experimental_rerun()

# Calculate trade result
def calculate_trade_result(trade_amount):
    profit_loss_percent = random.uniform(-50, 50) / 100
    profit_loss = trade_amount * profit_loss_percent
    return {
        "trade": st.session_state.current_trade,
        "trade_amount": trade_amount,
        "profit_loss": profit_loss,
        "remaining_balance": st.session_state.initial_amount + profit_loss,
    }

# Results page
def results_page():
    st.title("Game Over - Results")

    df = pd.DataFrame(st.session_state.results)
    df["profit_loss"] = df["profit_loss"].round(2)
    df["remaining_balance"] = df["remaining_balance"].round(2)

    st.dataframe(df)

    # Plotting the results
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["trade"], y=df["profit_loss"], mode="lines+markers", name="Profit/Loss",
                             hovertemplate="Trade %{x}: ₹%{y:.2f}<extra></extra>"))
    fig.update_layout(title="Profit/Loss per Trade", xaxis_title="Trade Number", yaxis_title="Profit/Loss (₹)")
    st.plotly_chart(fig)

# Main
initialize_state()

if "name" not in st.session_state or not st.session_state.name:
    setup_game()
elif st.session_state.game_over:
    results_page()
else:
    trade_page()
