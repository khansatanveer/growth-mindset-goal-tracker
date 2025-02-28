import streamlit as st
import datetime
import pandas as pd
import os
import json

st.set_page_config(page_title="🚀 Growth Mindset Goal Tracker", layout="wide")

GOALS_FILE = "goals.csv"

def load_goals():
    if os.path.exists(GOALS_FILE):
        try:
            df = pd.read_csv(GOALS_FILE)
            df["steps"] = df["steps"].apply(lambda x: json.loads(x) if isinstance(x, str) else [])
            return df.to_dict('records')
        except Exception as e:
            st.error(f"Error loading goals: {e}")
            return []
    return []

def save_goals(goals):
    df = pd.DataFrame(goals)
    if "steps" in df:
        df["steps"] = df["steps"].apply(json.dumps)  # Store steps as JSON string
    df.to_csv(GOALS_FILE, index=False)

def remove_goal(index):
    if 0 <= index < len(st.session_state.goals):
        del st.session_state.goals[index]
        save_goals(st.session_state.goals)
        st.rerun()

def main():
    st.markdown("<h1 style='text-align: center; color: #007BFF;'>🎯 Growth Mindset Goal Tracker</h1>", unsafe_allow_html=True)

    if "goals" not in st.session_state:
        st.session_state.goals = load_goals()
    
    st.markdown("### ✏️ Set Your Goal")
    col1, col2 = st.columns(2)

    with col1:
        goal = st.text_input("🌟 Your Main Goal:")
        deadline = st.date_input("📅 Set a Deadline:", datetime.date.today())

    with col2:
        priority = st.selectbox("🚀 Priority Level:", ["Low", "Medium", "High"])
        steps = st.text_area("📝 Action Steps (Separate by new line)").split("\n")
    
    steps = [step.strip() for step in steps if step.strip()]
    progress = st.slider("📊 Track Your Progress:", 0, 100, 0)
    st.progress(progress / 100)

    if st.button("💾 Save Goal"):
        if goal and steps:
            st.session_state.goals.append({
                "goal": goal,
                "steps": steps,
                "deadline": str(deadline),
                "priority": priority,
                "progress": progress
            })
            save_goals(st.session_state.goals)
            st.balloons()
            st.success(f"✅ Your goal has been saved! Keep going: **{goal}**")
        else:
            st.warning("⚠️ Please enter a goal and action steps before saving.")

    if st.session_state.goals:
        st.markdown("### 📌 Saved Goals")
        df = pd.DataFrame(st.session_state.goals)
        if "steps" in df:
            df["steps"] = df["steps"].apply(lambda x: " | ".join(x) if isinstance(x, list) else x)
        st.dataframe(df, height=min(500, 50 * (len(df) + 1)), width=1000)

        if st.session_state.goals:
            st.markdown("### 📌 Saved Goals")
            for idx, goal in enumerate(st.session_state.goals):
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                    <h4>🎯 {goal['goal']}</h4>
                    <p>📅 Deadline: <b>{goal['deadline']}</b> | 🚀 Priority: <b>{goal['priority']}</b></p>
                    <progress value="{goal['progress']}" max="100" style="width:100%; height: 20px;"></progress>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🗑️ Remove {idx+1}", key=f"remove_{idx}"):
                    remove_goal(idx)

if __name__ == "__main__":
    main()
