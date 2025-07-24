from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

# Page Configuration
st.set_page_config(page_title="HealthBot Advisor 💬", page_icon="🩺", layout="centered")

# ---------------- Sidebar: BMI Calculator ----------------
st.sidebar.title("🧮 BMI Calculator")
st.sidebar.markdown("Enter your details:")

height = st.sidebar.number_input("📏 Height (cm):", min_value=50.0, max_value=250.0, step=0.1)
weight = st.sidebar.number_input("⚖️ Weight (kg):", min_value=10.0, max_value=250.0, step=0.1)

# Show BMI result in sidebar
if height and weight:
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    st.sidebar.markdown(f"### ✅ Your BMI: **{bmi:.2f}**")

    if bmi < 18.5:
        st.sidebar.warning("Underweight 🥺\nConsult a nutritionist.")
    elif 18.5 <= bmi < 24.9:
        st.sidebar.success("Healthy weight 🥳\nKeep it up!")
    elif 25 <= bmi < 29.9:
        st.sidebar.info("Overweight 🤔\nConsider lifestyle changes.")
    else:
        st.sidebar.error("Obese 🚨\nPlease consult a doctor.")

# ---------------- Gemini-Powered HealthBot ----------------

# Function using system prompt
def guide_me_on(query):
    if not query.strip():
        return "⚠️ Please enter a health-related question."

    system_prompt = (
        "You are a certified Dietician, Health Coach, and Fitness Expert. "
        "Respond to health, disease, and fitness-related questions with empathy and clarity. "
        "If a query is outside the health domain, reply: "
        "'❌ I am a Healthcare Expert and can only answer questions related to Health, Fitness, and Diet.' "
        "If someone asks about medicines, say: "
        "'❌ I am an AI model and cannot recommend medication or provide diagnosis. Please consult a doctor.'\n\n"
    )

    full_prompt = system_prompt + query
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating response: {e}"

# ---------------- Main Area ----------------

st.markdown("<h1 style='text-align: center;'>🩺 HealthBot Advisor</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Your personal AI-powered health assistant 🤖</h4>", unsafe_allow_html=True)
st.markdown("---")

st.subheader("💬 Ask HealthBot")
user_prompt = st.text_area("Type your health-related question here (e.g., 'What should I eat to lower blood pressure?')", height=100)

if st.button("💡 Get Advice"):
    if user_prompt.strip() == "":
        st.warning("⚠️ Please enter a question to get advice.")
    else:
        answer = guide_me_on(user_prompt)
        st.subheader("🤖 HealthBot says:")
        st.markdown(answer)

st.markdown("---")
st.markdown("<center>👨‍⚕️ Made with ❤️ using Streamlit + Gemini API</center>", unsafe_allow_html=True)
