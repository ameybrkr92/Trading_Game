import streamlit as st

# Initial setup
st.title("Trade Risk Game")
st.write("A multiplayer game where players take risks and trades are pre-decided!")

# Define game parameters
initial_balance = 1000
trade_results = [0.05, -0.03, 0.10, -0.07]  # Pre-decided trade results as percentages
num_trades = len(trade_results)
num_players = 4

# Initialize players' balances
if "balances" not in st.session_state:
    st.session_state.balances = [initial_balance] * num_players
    st.session_state.current_trade = 0

# Game loop
if st.session_state.current_trade < num_trades:
    st.subheader(f"Trade {st.session_state.current_trade + 1}/{num_trades}")
    st.write(f"Trade Result: **Hidden** (Known to the game only)")

    # Input risk for each player
    risks = []
    for i in range(num_players):
        risk = st.number_input(f"Player {i + 1} - Enter risk (%)", min_value=0.0, max_value=100.0, step=1.0, key=f"risk_{i}")
        risks.append(risk)

    # Submit button
    if st.button("Submit Risks"):
        trade_result = trade_results[st.session_state.current_trade]
        for i in range(num_players):
            risk_value = (risks[i] / 100) * st.session_state.balances[i]
            st.session_state.balances[i] += risk_value * trade_result

        st.session_state.current_trade += 1
        st.experimental_rerun()

else:
    # Display final results
    st.subheader("Game Over!")
    for i in range(num_players):
        st.write(f"Player {i + 1} - Final Balance: ${st.session_state.balances[i]:.2f}")
    winner = max(range(num_players), key=lambda x: st.session_state.balances[x])
    st.write(f"🏆 Winner: Player {winner + 1}!")
