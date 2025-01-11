import streamlit as st

# Initial setup
st.title("Trade Risk Game")
st.write("A multiplayer game where players take risks and trades are pre-decided!")

# Define game parameters
initial_balance = 1000
trade_results = [0.2, -0.1, 0.15, -0.2, 0.05, -0.15, 0.25, -0.05, 0.1, -0.1]  # Amplified trade results as percentages
num_trades = len(trade_results)
num_players = 4

# Initialize players' balances and game state
if "balances" not in st.session_state:
    st.session_state.balances = [initial_balance] * num_players
    st.session_state.current_trade = 0
    st.session_state.risks = [0.0] * num_players  # Store risks temporarily

if st.session_state.current_trade < num_trades:
    st.subheader(f"Trade {st.session_state.current_trade + 1}/{num_trades}")
    st.write(f"Trade Result: **Hidden** (Known to the game only)")

    # Input risk for each player in monetary amounts
    for i in range(num_players):
        max_risk = float(st.session_state.balances[i])  # Ensure max_risk is a float
        st.session_state.risks[i] = st.number_input(
            f"Player {i + 1} - Enter risk amount ($, max ${max_risk:.2f})",
            min_value=0.0,
            max_value=max_risk,
            step=1.0,  # Use integer step to avoid fractional risks
            value=st.session_state.risks[i],  # Preserve previous input
            key=f"risk_{i}",
        )

    # Submit button
    if st.button("Submit Risks"):
        # Process the trade
        trade_result = trade_results[st.session_state.current_trade]
        for i in range(num_players):
            risk_value = st.session_state.risks[i]
            # Update balance based on trade result
            st.session_state.balances[i] += risk_value * trade_result
            # Subtract the risked amount regardless of trade result
            st.session_state.balances[i] -= risk_value

        # Move to the next trade
        st.session_state.current_trade += 1

else:
    # Display final results
    st.subheader("Game Over!")
    for i in range(num_players):
        st.write(f"Player {i + 1} - Final Balance: ${st.session_state.balances[i]:.2f}")
    winner = max(range(num_players), key=lambda x: st.session_state.balances[x])
    st.write(f"🏆 Winner: Player {winner + 1}!")
