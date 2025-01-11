import random
import streamlit as st
import pandas as pd
import plotly.express as px

# Initial setup
st.title("💹 Indian Trading Simulation Game")
st.write("Welcome to the thrilling world of trading! Are you a master of risk or a victim of greed? Let's find out!")

# Constants
initial_balance = 100000
num_trades = 10
trade_range = (-50, 50)
num_players = 5
special_event_chance = 0.2  # 20% chance of special market events

# Initialize session state
if "balances" not in st.session_state:
    st.session_state.balances = [initial_balance] * num_players
    st.session_state.current_trade = 0
    st.session_state.risks = [0] * num_players
    st.session_state.trade_history = []
    st.session_state.bot_behaviors = ["random", "greedy", "conservative", "dynamic"]
    st.session_state.leaderboard = []

# Helper functions
def update_trade_history(trade_num, results):
    trade_data = {"Trade": trade_num}
    for i in range(num_players):
        role = "You" if i == 0 else f"Bot {i}"
        trade_data[f"{role} Risk"] = st.session_state.risks[i]
        trade_data[f"{role} Balance"] = st.session_state.balances[i]
        trade_data[f"{role} P/L"] = results[i]
    st.session_state.trade_history.append(trade_data)

def add_commentary(results):
    commentary = []
    for i, result in enumerate(results):
        role = "You" if i == 0 else f"Bot {i}"
        if result > 0:
            commentary.append(f"{role} made a profit of ₹{result:.2f}! 🎉")
        elif result < 0:
            commentary.append(f"{role} lost ₹{-result:.2f}. 😢")
        else:
            commentary.append(f"{role} broke even. 🤷")
    return commentary

# Display current trade
if st.session_state.current_trade < num_trades:
    trade_number = st.session_state.current_trade + 1
    st.subheader(f"📈 Trade {trade_number}/{num_trades}")
    st.write("Enter your risk amount in INR for this trade:")

    # Human player input
    max_risk_human = st.session_state.balances[0]
    st.session_state.risks[0] = st.slider(
        f"Your Risk Amount (Max: ₹{max_risk_human:.2f})",
        min_value=0,
        max_value=int(max_risk_human),
        step=100,
        key="human_risk",
    )

    # Bot decisions
    for i in range(1, num_players):
        bot_behavior = st.session_state.bot_behaviors[i - 1]
        bot_balance = st.session_state.balances[i]

        if bot_behavior == "random":
            st.session_state.risks[i] = random.randint(0, int(bot_balance * 0.5))
        elif bot_behavior == "greedy":
            st.session_state.risks[i] = int(bot_balance * 0.5)
        elif bot_behavior == "conservative":
            st.session_state.risks[i] = int(bot_balance * 0.1)
        elif bot_behavior == "dynamic":
            if random.random() > 0.5:
                st.session_state.risks[i] = int(bot_balance * 0.3)
            else:
                st.session_state.risks[i] = int(bot_balance * 0.2)

    # Special market event
    market_event_multiplier = 1
    if random.random() < special_event_chance:
        market_event_multiplier = random.choice([2, 0.5])
        st.markdown(f"### ⚠️ Special Market Event: Results amplified by {market_event_multiplier}x!")

    # Execute trade
    if st.button("Execute Trade"):
        trade_result = random.uniform(*trade_range) / 100 * market_event_multiplier
        trade_results = []
        for i in range(num_players):
            risk = st.session_state.risks[i]
            profit_loss = risk * trade_result
            st.session_state.balances[i] += profit_loss - risk
            trade_results.append(profit_loss)

        update_trade_history(trade_number, trade_results)
        commentary = add_commentary(trade_results)
        for comment in commentary:
            st.write(comment)

        # Leaderboard
        leaderboard = sorted(
            enumerate(st.session_state.balances),
            key=lambda x: x[1],
            reverse=True,
        )
        st.session_state.leaderboard = leaderboard
        st.session_state.current_trade += 1

else:
    # Game over, display results
    st.subheader("🏁 Game Over!")
    st.write("Final Results:")
    for i, (player, balance) in enumerate(st.session_state.leaderboard):
        role = "You" if player == 0 else f"Bot {player}"
        st.write(f"#{i + 1} - {role}: ₹{balance:.2f}")

# Trade history table and graph
if st.session_state.trade_history:
    st.subheader("📊 Trade History")
    df = pd.DataFrame(st.session_state.trade_history)
    st.dataframe(df)

    # Graph for Profit/Loss
    st.subheader("📈 Profit/Loss After Each Trade")
    pl_columns = [col for col in df.columns if "P/L" in col]
    plot_df = df.melt(id_vars=["Trade"], value_vars=pl_columns, var_name="Player", value_name="P/L")
    fig = px.line(plot_df, x="Trade", y="P/L", color="Player", title="Player Profit/Loss After Each Trade")
    st.plotly_chart(fig)
