import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

st.set_page_config(
    page_title="DH Gemini Trading Analyzer",
    page_icon="📈",
    layout="centered"
)

# Custom Cyberpunk / Dark UI Styling
st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #00d26a;
        color: black;
        font-weight: bold;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00b359;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 DH Gemini AI Vision Chart Analyzer")
st.caption("1-Minute Binary Options Candlestick Deep Analyzer")

# Streamlit Secrets থেকে স্বয়ংক্রিয়ভাবে API Key সংগ্রহ
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.sidebar.warning("Secrets-এ API Key পাওয়া যায়নি!")
    api_key = st.sidebar.text_input("Enter Gemini API Key manually", type="password")

uploaded_file = st.file_uploader("Upload 1-Minute Chart Screenshot (Quotex)", type=["jpg", "jpeg", "png"])

MASTER_PROMPT = """
Act as an elite Quantitative Price Action & Binary Trading Technical Analyst. This analysis is specifically for a **1-MINUTE** candlestick chart. Use deep institutional market structure reasoning to predict the immediate NEXT 1-MINUTE CANDLE direction. Perform a granular, candle-by-candle breakdown focusing on immediate price movements, using the following framework:

1. MARKET CONTEXT & 1-MINUTE MOMENTUM:
   - Identify the micro-trend on this chart (Uptrend, Downtrend, or Range/Consolidation).
   - Analyze the current 1-minute momentum: Are buyers or sellers more aggressive? Look at the most recent candles for clues.
   - Note any evidence of buyer-to-seller or seller-to-buyer exhaustion.

2. KEY LEVELS & PRICE ACTION:
   - Identify the immediate Support & Resistance (S/R) zones, Round Numbers, or Supply/Demand zones near the current price.
   - Analyze any wick rejections, false breakouts, liquidity grabs, or gap levels relevant to the immediate next candle.

3. 1-MINUTE CANDLE PSYCHOLOGY:
   - Precisely name and interpret the exact formation of the last 2-3 candles (e.g., Hammer, Engulfing, Pinbar, Doji, Marubozu).
   - Explain the battle between buyers and sellers within the most recent candle and what it implies for the very next candle.

4. FINAL VERDICT & 1-MINUTE PREDICTION:
   - Direction: **CALL (UP / Green)** OR **PUT (DOWN / Red)**
   - Estimated Probability/Confidence: (Realistic percentage based on technical confluence)
   - Core Reason: A very concise summary of why this outcome has the highest edge for the next 1 minute.
   - Risk/Caution: What specific immediate price movement or rejection would invalidate this setup?

**Deliver the entire final analysis in clear, professional Bengali with structured bullet points.** Ensure the analysis is quick, actionable, and focuses entirely on the next 1 minute.
"""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_container_width=True)
    
    if st.button("🚀 Analyze Next Candle"):
        if not api_key:
            st.error("API Key পাওয়া যায়নি! দয়া করে Streamlit Secrets চেক করুন।")
        else:
            with st.spinner("মার্কেট কাঠামো ও ক্যান্ডেলস্টিক সাইকোলজি বিশ্লেষণ করা হচ্ছে..."):
                try:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[image, MASTER_PROMPT]
                    )
                    st.success("বিশ্লেষণ সম্পন্ন হয়েছে!")
                    st.markdown("### 📊 অ্যানালাইসিস রেজাল্ট:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"একটি সমস্যা হয়েছে: {str(e)}")
