import requests
import streamlit as st


API_KEY = "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"  
MODEL = "deepseek/deepseek-r1" 

st.set_page_config(page_title="Smart Reply Generator", page_icon="💬", layout="centered")

#styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
    .stApp {
        background: linear-gradient(to bottom right, #96C2DB, #E5EDF1);
        font-family: 'Press Start 2P', monospace;
        color: #222;
        padding: 2rem;
    }
     .overlay {
        background-color: rgba(0, 0, 0, 0.4); 
        padding: 2rem;
        border-radius: 20px;
        backdrop-filter: blur(6px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .title {
        font-size: 2.5em;
        color: #00334e;  /* dark steel blue */
        font-weight: 800;
        text-align: center;
        text-shadow: 0 1px 3px rgba(0,0,0,0.1);
        animation: fadeIn 1s ease forwards;
        opacity: 0;
    }

    label, .stSelectbox label {
        color: #00334e;
        font-weight: bold;
    }

    .stSelectbox > div {
        background-color: #ffffff !important;
        color: #00334e !important;
        border-radius: 8px;
    }

    textarea {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        color: #00334e !important;
        font-size: 1rem !important;
    }

    button[kind="primary"] {
        animation: pop 0.5s ease;
        border-radius: 10px;
        transition: all 0.2s ease-in-out;
        font-weight: bold;
        background-color: #3E7CB1;
        color: white;
    }

    button[kind="primary"]:hover {
        transform: scale(1.05);
        background-color: #265D85;
    }

    .footer {
        text-align: center;
        color: #555555;
        font-size: 0.8em;
        margin-top: 2rem;
    }

    @keyframes pop {
        0% { transform: scale(0.95); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    @keyframes fadeIn {
        to { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)



st.markdown("<div class='title'>🧠 Smart Reply Generator</div>", unsafe_allow_html=True)
st.markdown("### 💌 Paste the message you received:")
ip = st.text_area("", placeholder="e.g. hey wyd 👀")

tone = st.selectbox("🎭 Choose the tone of your reply:", ["Funny", "Flirty", "Professional", "Normal", "Emotional"])

st.markdown("---")

# prompt
def build_prompt(tone, message):
    if tone == "Funny":
        return f"Reply in a funny and witty way to: {message}"
    elif tone == "Flirty":
        return f"Reply flirtatiously to: {message}"
    elif tone == "Professional":
        return f"Reply in a formal, professional tone to: {message}"
    elif tone == "Emotional":
        return f"Reply with deep emotion, empathy, or care to: {message}"
    else:  # Normal
        return f"Reply in a casual, normal way to: {message}"

# api
def generate_reply(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",  # or your domain
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an assistant that writes replies based on tone."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {response.status_code}: {response.text}"


if st.button("✨ Generate Smart Reply") and ip.strip():
    with st.spinner("Generating a brilliant reply..."):
        prompt = build_prompt(tone, ip)
        reply = generate_reply(prompt)
        st.success("Here’s your AI-generated reply:")
        st.markdown(f"```{reply}```")


st.markdown("<div class='footer'>Made with 💖 using OpenRouter & Streamlit</div>", unsafe_allow_html=True)

