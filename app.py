import streamlit as st
import datetime
import pandas as pd
import random

def main():
    st.set_page_config(page_title="Growth Mindset Goal Tracker", layout="wide")
    
    # Page Styling
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(to right, rgb(40, 11, 95), rgb(54, 66, 62)); color: white; }
    .stTextInput, .stTextArea, .stDateInput, .stSelectbox, .stSlider { 
        background-color: white !important; 
        color: black !important; 
    }
    .stButton > button { 
        background-color: #4CAF50 !important; 
        color: white !important; 
        border-radius: 5px; 
        padding: 10px; 
        border: none; 
    }
    .stButton > button:hover { background-color: #45a049 !important; }
    .motivational-quote { color: #FFD700; font-weight: bold; } /* Change the color here */
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 Growth Mindset Goal Tracker")
    st.subheader("Set, track, and achieve your goals with a growth mindset!")
    
    # Motivational Quotes
    quotes = [
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Believe you can, and you're halfway there.",
        "Growth and comfort do not coexist.",
        "Difficulties strengthen the mind, as labor does the body.",
        "Do not be embarrassed by your failures, learn from them and start again."
    ]
    # Display the motivational quote in the main area
    st.markdown(f'<p class="motivational-quote">💡 **Motivation:** {random.choice(quotes)}</p>', unsafe_allow_html=True)
    
    # Goal Input Section
    st.markdown("### ✏️ Set Your Goal")
    goal = st.text_input("🌟 Your Main Goal:")
    steps = st.text_area("📝 Action Steps (Break it into small tasks):")
    deadline = st.date_input("📅 Set a Deadline:", datetime.date.today())
    priority = st.selectbox("🚀 Priority Level:", ["Low", "Medium", "High"])
    
    # Progress Tracking
    progress = st.slider("📊 Track Your Progress:", 0, 100, 0)
    st.progress(progress / 100)
    
    if "goals" not in st.session_state:
        st.session_state.goals = []
    
    if st.button("Save Goal"):
        if goal and steps:
            st.session_state.goals.append({"goal": goal, "steps": steps, "deadline": deadline, "priority": priority, "progress": progress})
            st.success(f"Your goal has been saved! Keep going: **{goal}**")
        else:
            st.warning("Please enter a goal and action steps before saving.")
    
    # Display Saved Goals
    if st.session_state.goals:
        st.markdown("### 📌 Saved Goals")
        df = pd.DataFrame(st.session_state.goals)
        st.table(df)
    
    # Progress Updates Section
    st.markdown("### 📢 Share Your Progress")
    progress_update = st.text_area("How are you progressing?")
    obstacles = st.text_area("⚠️ Any Challenges?")
    next_steps = st.text_area("🔄 Next Steps:")
    
    if st.button("Submit Progress"):
        if progress_update or obstacles or next_steps:
            st.success("Great job! Keep pushing forward! 🚀")
            if progress_update:
                st.write(f"✅ Progress: {progress_update}")
            if obstacles:
                st.write(f"⚠️ Challenges: {obstacles}")
            if next_steps:
                st.write(f"🔄 Next Steps: {next_steps}")
        else:
            st.warning("Please enter some updates before submitting.")
    
    # Celebrate Achievements
    st.markdown("### 🎉 Celebrate Your Wins!")
    achievement = st.text_area("What did you accomplish this week?")
    if st.button("Celebrate!"):
        if achievement:
            st.balloons()
            st.success(f"🎊 Amazing! You accomplished: {achievement} 🎉")
        else:
            st.warning("Please enter at least one achievement.")
    
if __name__ == "__main__":
    main()
