import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="AI Code Swiss Army Knife",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CUSTOM CSS (Pacifico Font + Animated Background) ---
st.markdown("""
    <style>
        /* Import Google Fonts: Inter (Body) and Pacifico (Headers) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

        /* Global Font Application (Body uses Inter) */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* --- HEADER STYLING (The Pacifico Font) --- */
        h1, h2, h3 {
            font-family: 'Pacifico', cursive;
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            letter-spacing: 1px;
            font-weight: 400; /* Pacifico looks best at normal weight */
        }
        
        /* Make the main title extra big */
        h1 {
            font-size: 4rem !important;
            margin-bottom: 0px;
        }

        /* --- THE ANIMATED BACKGROUND --- */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #141E30);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* --- UI ELEMENTS --- */
        .stButton>button {
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            font-family: 'Inter', sans-serif;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.3);
        }

        .result-box {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. API KEY HANDLING ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
except:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# --- 4. HEADER SECTION ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
with col2:
    st.title("Swiss Army Knife")
    st.markdown("### for Code") # Using a subheader to keep the Pacifico style flowing

st.write("---")

# --- 5. MAIN INTERFACE ---
tab1, tab2, tab3 = st.tabs(["🔀 Translate", "🐞 Bug Fixer", "📖 Explainer"])

mode = None
submit_text = "Run"

with tab1:
    st.write("### Translate Code")
    col_a, col_b = st.columns(2)
    with col_a:
        source_lang = st.selectbox("From Language", ["Python", "JavaScript", "Java", "C++", "SQL", "Plain English"], key="s_lang")
    with col_b:
        target_lang = st.selectbox("To Language", ["Python", "JavaScript", "Java", "C++", "SQL", "Plain English"], key="t_lang")
    mode = "Translate"
    submit_text = "Translate Code 🚀"

with tab2:
    st.write("### Find & Fix Bugs")
    st.info("Paste your broken code below. AI will find errors and write the fixed version.")
    mode = "Bug Fixer"
    submit_text = "Fix My Code 🔧"

with tab3:
    st.write("### Code Explainer")
    st.info("Paste complex code below. AI will explain it line-by-line.")
    mode = "Explainer"
    submit_text = "Explain It 🧠"

# --- 6. INPUT AREA ---
code_input = st.text_area("Paste your code here:", height=300, key="main_input")

# --- 7. THE LOGIC ---
if st.button(submit_text, type="primary"):
    if not api_key:
        st.error("⚠️ Please provide an API Key in the sidebar.")
    elif not code_input:
        st.warning("⚠️ Please paste some code first.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Smart Prompts
            if mode == "Translate":
                prompt = f"Act as an expert developer. Translate this {source_lang} code into {target_lang}. Return ONLY the code, no markdown backticks.\n\n{code_input}"
            elif mode == "Bug Fixer":
                prompt = f"Act as an expert developer. 1. Find the bugs in this code. 2. Explain them briefly. 3. Provide the FIXED code.\n\n{code_input}"
            elif mode == "Explainer":
                prompt = f"Act as a computer science teacher. Explain this code in simple terms. Break it down step-by-step.\n\n{code_input}"

            with st.spinner("🤖 AI is working its magic..."):
                response = model.generate_content(prompt)

            # --- 8. THE RESULT ---
            st.markdown(f"<div class='result-box'><h3>✨ Result ({mode})</h3></div>", unsafe_allow_html=True)
            
            res_tab1, res_tab2 = st.tabs(["💻 Code View", "📄 Raw Text"])
            
            with res_tab1:
                lang_code = target_lang.lower() if mode == "Translate" else "python"
                st.code(response.text, language=lang_code)
                
            with res_tab2:
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- 9. FOOTER ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Gemini 1.5")
