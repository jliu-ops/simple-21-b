import streamlit as st
import random

st.set_page_config(page_title="21 Sticks Game")

# --- 1. INITIALIZE STATE ---
if 'sticks' not in st.session_state:
    st.session_state.sticks = 21
    st.session_state.m = 3
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.message = "Your turn! How many sticks?"

# --- 2. THE CALLBACK (The Secret Sauce) ---
def handle_move():
    # Grab the value from the input widget using its 'key'
    take = st.session_state.user_move
    
    # Player Move
    st.session_state.sticks -= take
    st.session_state.history.append(f"You took {take} sticks.")
    
    if st.session_state.sticks <= 0:
        st.session_state.message = "🎉 YOU WIN!"
        st.session_state.game_over = True
        return

    # AI Move
    state = st.session_state.sticks % (st.session_state.m + 1)
    ai = state if state != 0 else random.randint(1, st.session_state.m)
    
    st.session_state.sticks -= ai
    st.session_state.history.append(f"Opponent took {ai} sticks.")
    
    if st.session_state.sticks <= 0:
        st.session_state.message = "💀 OPPONENT WINS!"
        st.session_state.game_over = True
    else:
        st.session_state.message = f"Opponent took {ai}. Your turn!"

def reset_game():
    st.session_state.sticks = 21
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.message = "Game reset. You go first!"

# --- 3. THE UI (Always reflects the LATEST state) ---
st.title("21 Sticks")

# Visual feedback that updates immediately
st.subheader(f"Sticks remaining: {max(0, st.session_state.sticks)}")
st.progress(max(0, st.session_state.sticks) / 21)

if not st.session_state.game_over:
    # Notice the 'key' and 'on_click' parameters
    st.number_input(f"How many to remove?", 1, st.session_state.m, key="user_move")
    st.button("Submit Move", on_click=handle_move)
else:
    st.button("Play Again", on_click=reset_game)

st.info(st.session_state.message)

# Display history
for move in reversed(st.session_state.history):
    st.write(move)
