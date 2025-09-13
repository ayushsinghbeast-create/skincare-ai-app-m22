import streamlit as st
import pandas as pd
from PIL import Image
import altair as alt
from datetime import datetime
from io import BytesIO

# ---------- Page Config ----------
st.set_page_config(page_title="Skincare Pro Analyzer", layout="wide")

# ---------- Session States ----------
if "users" not in st.session_state:
    st.session_state["users"] = {}
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "points" not in st.session_state:
    st.session_state["points"] = 0

# ---------- Sidebar Navigation ----------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", [
    "Login / Register",
    "Skincare Pro Analyzer",
    "Daily Skincare Tips",
    "AI Skincare Chatbot",
    "AR Try-On",
    "Voice Assistant",
    "Skin Prediction AI",
    "Skincare Gamification",
    "Hyper-Personalized Advice",
    "25 Skincare Tips",
    "Daily Routine AI Checker"
])

# ---------- LOGIN SYSTEM ----------
if menu == "Login / Register":
    st.sidebar.subheader("Login / Register")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username in st.session_state["users"] and st.session_state["users"][username]["password"] == password:
            st.session_state["current_user"] = username
            st.sidebar.success("Login Successful!")
        else:
            st.sidebar.error("Invalid username or password!")

    if st.sidebar.button("Register"):
        if username and password:
            st.session_state["users"][username] = {"password": password, "data": []}
            st.sidebar.success("Registration Successful!")
        else:
            st.sidebar.error("Please enter valid details!")

    if st.session_state["current_user"]:
        st.success(f"Welcome {st.session_state['current_user']}! Use sidebar to explore features.")

# ---------- CHECK LOGIN ----------
if not st.session_state["current_user"] and menu != "Login / Register":
    st.warning("Please login to access the features!")
    st.stop()

# ---------------- Feature 1: Skincare Pro Analyzer ----------------
if menu == "Skincare Pro Analyzer":
    st.title("🌸 Skincare Pro Analyzer")
    uploaded_photo = st.file_uploader("Upload a clear photo", type=["jpg", "png", "jpeg"])
    if uploaded_photo:
        image = Image.open(uploaded_photo)
        st.image(image, caption="Uploaded Photo", use_column_width=True)

    st.subheader("Enter Your Health & Lifestyle Details")
    sleep_hours = st.slider("Sleep Hours", 0, 12, 7)
    water_intake = st.number_input("Water Intake (Litres/day)", min_value=0.0, step=0.1)
    stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
    diet_quality = st.slider("Diet Quality (1-10)", 1, 10, 5)
    exercise_freq = st.slider("Exercise Frequency (days/week)", 0, 7, 3)
    screen_time = st.slider("Screen Time (hours/day)", 0, 24, 5)
    pollution = st.slider("Pollution Exposure (1-10)", 1, 10, 5)
    skin_type = st.selectbox("Skin Type", ["Normal", "Dry", "Oily", "Combination", "Sensitive"])

    if st.button("Analyze"):
        score = (sleep_hours + water_intake + diet_quality + (10 - stress_level)) * 2
        future_score = score + 10 if exercise_freq > 3 else score

        data = {"Date": datetime.now().strftime("%Y-%m-%d"), "Score": score, "Future_Score": future_score}
        st.session_state["users"][st.session_state["current_user"]]["data"].append(data)
        st.session_state["points"] += 10

        st.subheader("Skin Health Score")
        st.metric("Current Score", score)
        st.metric("Future Score", future_score)

        st.subheader("Recommendations")
        st.write("- Drink 2-3 liters water daily")
        st.write("- Maintain 7-8 hours of sleep")
        st.write("- Reduce stress via meditation")
        st.write("- Use sunscreen to reduce pollution effects")

        st.subheader("Product Suggestions (Affiliate Links)")
        st.markdown("[Moisturizer - Amazon](https://amazon.in)")
        st.markdown("[Sunscreen - Amazon](https://amazon.in)")

        st.subheader("Skin Progress Over Time")
        df = pd.DataFrame(st.session_state["users"][st.session_state["current_user"]]["data"])
        chart = alt.Chart(df).mark_line(point=True).encode(x='Date', y='Score', tooltip=['Date', 'Score']).properties(width=600, height=400)
        st.altair_chart(chart)

        # PDF Download
        report = f"Skin Report\nDate: {data['Date']}\nCurrent Score: {score}\nFuture Score: {future_score}"
        buffer = BytesIO()
        buffer.write(report.encode())
        st.download_button("Download PDF", data=buffer.getvalue(), file_name="skin_report.pdf", mime="application/pdf")

# ---------------- Feature 2: Daily Skincare Tips ----------------
if menu == "Daily Skincare Tips":
    st.title("💡 Daily Skincare Tips")
    tips = [
        "Cleanse daily: Wash your face twice a day.",
        "Moisturize regularly.",
        "Use sunscreen daily.",
        "Exfoliate once a week.",
        "Use eye cream for delicate skin.",
        "Stay hydrated, drink 3-4L water.",
        "Eat a balanced diet.",
        "Get enough sleep.",
        "Manage stress daily.",
        "Exercise regularly.",
        "Avoid harsh scrubbing.",
        "Use non-comedogenic moisturizers.",
        "Wash pillowcases regularly.",
        "Clean makeup tools weekly.",
        "Check skin regularly.",
        "Consult dermatologist if needed.",
        "Increase indoor humidity in winters.",
        "Don't smoke.",
        "Extend care to neck area.",
        "Layer serums for best results."
    ]
    for tip in tips:
        st.write("✅", tip)

# ---------------- Feature 3: AI Chatbot ----------------
if menu == "AI Skincare Chatbot":
    st.title("🤖 AI Skincare Chatbot")
    questions = {
        "Best routine for oily skin?": "Use gentle cleanser, oil-free moisturizer, sunscreen.",
        "How to reduce acne?": "Cleanse twice, avoid oily food, use salicylic acid products.",
        "Best anti-aging cream?": "Look for retinol or peptides-based creams.",
        "How much water should I drink?": "3-4 liters daily.",
        "Is sunscreen important?": "Yes, use SPF 30+ daily.",
        "How to get glowing skin?": "Hydration + Vitamin C serum + Sleep.",
        "Reduce dark circles?": "Sleep well + use eye cream + reduce screen time.",
        "Best diet for skin?": "Fruits, vegetables, omega-3, nuts.",
        "Why moisturize oily skin?": "Even oily skin needs hydration to balance sebum.",
        "Is exfoliation needed?": "Yes, 1-2 times a week only."
    }
    q = st.selectbox("Ask a question", list(questions.keys()))
    if st.button("Get Answer"):
        st.write("💬", questions[q])

# ---------------- Placeholder Features ----------------
if menu == "AR Try-On":
    st.title("🕶️ AR Try-On (Coming Soon)")

if menu == "Voice Assistant":
    st.title("🎤 Voice Assistant (Coming Soon)")

if menu == "Skin Prediction AI":
    st.title("📈 Skin Prediction AI (Coming Soon)")

# ---------------- Gamification ----------------
if menu == "Skincare Gamification":
    st.title("🏆 Gamification Points")
    st.write("Your Points:", st.session_state["points"])

# ---------------- Hyper-Personalized Advice ----------------
if menu == "Hyper-Personalized Advice":
    st.title("🧠 Hyper-Personalized Advice")
    st.write("""
    The future of skincare likely involves hyper-personalized plans analyzing diet, sleep, and stress using advanced technology to identify root causes and tailor treatments for optimal skin health.
    ...
    [The future of skincare likely involves hyper-personalized advice integrating diet, sleep, and stress data through advanced technology, moving beyond basic recommendations to offer truly tailored solutions. This approach will leverage AI and consumer data to identify connections between lifestyle factors and skin conditions, enabling the suggestion of specific products and routines that address individual skin needs and external influences. 
How it works:
1. Data Collection:
You would provide data through surveys, wearables, and potentially genetic information about your diet, sleep patterns, and stress levels. 
2. AI Analysis:
Advanced artificial intelligence (AI) and machine learning algorithms would analyze this vast amount of data. 
3. Pattern Identification:
The AI would identify correlations and patterns between your diet, sleep quality, stress, and your skin's current state, such as acne, dryness, or sensitivity. 
4. Personalized Skincare Recommendations:
Based on these insights, you would receive a hyper-personalized skincare plan, including product recommendations and advice on lifestyle adjustments. 
Benefits:
Proactive Approach:
It shifts skincare from reactive to proactive, addressing potential issues before they become significant problems. 
Holistic View:
It acknowledges that skin health is intertwined with overall well-being, not just topical treatments. 
Increased Efficacy:
Tailoring advice to your unique biological and lifestyle factors is expected to result in more effective skincare outcomes. 
Examples of what it could look like:
Diet:
If your data reveals a correlation between high sugar intake and increased breakouts, your plan might recommend reducing sugar or incorporating certain antioxidants. 
Sleep:
Poor sleep might be linked to increased inflammation, leading to specific product suggestions or advice on improving sleep hygiene. 
Stress:
High stress levels could trigger eczema or other skin conditions, prompting recommendations for calming ingredients in your skincare or stress-reduction techniques. )

# ---------------- 25 Skincare Tips ----------------
if menu == "25 Skincare Tips":
    st.title("📜 25 Skincare Tips")
    tips25 = [
        "Cleanse Properly", "Exfoliate Regularly", "Moisturize Daily", "Use Sunscreen",
        "Remove Makeup Before Sleeping", "Eat a Healthy Diet", "Stay Hydrated",
        "Prioritize Sleep", "Reduce Stress", "Avoid Smoking", "Know Your Skin Type",
        "Use Gentle Products", "Use Vitamin C Serum", "Incorporate Retinol",
        "Protect from Pollution", "Be Gentle When Washing", "Pat Dry Gently",
        "Don't Pop Pimples", "Care for Body Skin", "Use Alcohol-free Toner",
        "Try 7-Skin Method", "Double Cleanse at Night", "Use Topical Treatments",
        "Health Screenings", "Professional Advice if Needed"
    ]
    for tip in tips25:
        st.write("✨", tip)

# ---------------- Daily Routine AI Checker ----------------
if menu == "Daily Routine AI Checker":
    st.title("📅 Daily Routine AI Checker")
    st.write("Follow the routines and diet daily. Each Yes = +5 points, No = -5 points.")

    steps = {
        "Morning": ["Cleansing", "Toning", "Serum", "Moisturizer", "Sunscreen"],
        "Night": ["Makeup Removed", "Cleanse & Tone", "Night Serum", "Eye Cream", "Night Cream/Mask"],
        "Diet": ["Fruits/Vegetables", "Healthy Fats", "Whole Grains/Legumes", "Water", "Green Tea"]
    }

    score = 0
    for section, items in steps.items():
        st.subheader(section + " Routine")
        for item in items:
            ans = st.radio(f"{item} done?", ["Yes", "No"], key=section + item)
            if ans == "Yes":
                score += 5
            else:
                score -= 5

    if st.button("Calculate Score"):
        st.success(f"Your Daily Routine Score: {score}")
        if score >= 50:
            st.write("🌟 Great job! You're following a healthy routine.")
        else:
            st.write("⚠️ Try to follow more steps for better skin health.")
