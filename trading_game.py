import streamlit as st
import random
import plotly.graph_objects as go

# Function to set up the game configuration
def setup_game():
    st.title("Trading Game Setup")

    # Player Name
    player_name = st.text_input("Enter your name:", "")

    # Select Number of Bots (1 to 4)
    num_bots = st.selectbox("Select the number of bots:", [1, 2, 3, 4])

    # Select Number of Trades
    num_trades = st.slider("Select number of trades:", 5, 20, 10)

    # Initial Amount to Trade
    initial_amount = st.number_input("Enter your initial amount:", min_value=1000, value=100000)

    # Start Game Button
    if st.button("Start Game"):
        # Store the values in session state
        st.session_state.player_name = player_name
        st.session_state.num_bots = num_bots
        st.session_state.num_trades = num_trades
        st.session_state.player_balance = initial_amount
        st.session_state.current_trade = 1
        st.session_state.trade_results = {"Player": [], "Cautious Bot": [], "Aggressive Bot": [], "Balanced Bot": [], "Random Bot": []}
        st.session_state.bot_balances = {"Cautious Bot": initial_amount, "Aggressive Bot": initial_amount, "Balanced Bot": initial_amount, "Random Bot": initial_amount}
        st.session_state.page = "trading"

# Function to handle trading

def trade_page():
    # Ensure game setup is complete
    if 'page' not in st.session_state or st.session_state.page != "trading":
        st.error("Please complete the setup first!")
        return

    st.title(f"Welcome {st.session_state.player_name} to the Trading Game!")
    st.subheader(f"Trade {st.session_state.current_trade} of {st.session_state.num_trades}")
    st.write(f"Your current balance: ₹{st.session_state.player_balance:,.2f}")

    # Select trade amount
    trade_amount = st.slider(
        "Select amount to trade (₹):", 
        min_value=1000, 
        max_value=int(st.session_state.player_balance), 
        step=1000,
        value=int(st.session_state.player_balance // 10)
    )

    # Trade button
    if st.button("Trade"):
        # Simulate player's trade result
        outcome = random.randint(-50, 50) / 100
        trade_result = trade_amount * outcome
        st.session_state.player_balance += trade_result
        st.session_state.trade_results["Player"].append(trade_result)

        # Simulate bots' trades
        for bot, balance in st.session_state.bot_balances.items():
            if bot == "Cautious Bot":
                bot_trade = min(5000, balance * 0.05)
            elif bot == "Aggressive Bot":
                bot_trade = balance * 0.5
            elif bot == "Balanced Bot":
                bot_trade = balance * 0.2
            else:
                bot_trade = random.randint(1000, int(balance * 0.5))

            bot_outcome = random.randint(-50, 50) / 100
            bot_result = bot_trade * bot_outcome
            st.session_state.bot_balances[bot] += bot_result
            st.session_state.trade_results[bot].append(bot_result)

        # Display result
        st.write(f"Trade Result: ₹{trade_result:,.2f}")
        st.write(f"New Balance: ₹{st.session_state.player_balance:,.2f}")

        # Move to next trade
        st.session_state.current_trade += 1

    # Next Trade or End Game
    if st.session_state.current_trade > st.session_state.num_trades:
        end_game()
    else:
        st.button("Next Trade")

# Function to display results when the game ends
def end_game():
    st.subheader("Game Results")

    # Plot gain/loss for each trade
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(1, len(st.session_state.trade_results["Player"]) + 1)),
        y=st.session_state.trade_results["Player"],
        mode='lines+markers',
        name='Player',
        hovertemplate="Trade %{x}: ₹%{y:.2f}<extra></extra>"
    ))

    for bot in st.session_state.bot_balances.keys():
        fig.add_trace(go.Scatter(
            x=list(range(1, len(st.session_state.trade_results[bot]) + 1)),
            y=st.session_state.trade_results[bot],
            mode='lines+markers',
            name=bot,
            hovertemplate="Trade %{x}: ₹%{y:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title="Gain/Loss per Trade",
        xaxis_title="Trade Number",
        yaxis_title="Gain/Loss (₹)",
        hovermode="x unified"
    )

    st.plotly_chart(fig)

    # Final Balances
    st.write("### Final Balances")
    st.write(f"Your Balance: ₹{st.session_state.player_balance:,.2f}")
    for bot, balance in st.session_state.bot_balances.items():
        st.write(f"{bot}: ₹{balance:,.2f}")

# Main flow
if 'page' not in st.session_state:
    st.session_state.page = "setup"

if st.session_state.page == "setup":
    setup_game()
elif st.session_state.page == "trading":
    trade_page()
