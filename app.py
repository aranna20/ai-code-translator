import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="AI Code Swiss Army Knife",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. NEON CYBERPUNK CSS ---
st.markdown("""
    <style>
        /* Import Google Fonts: Orbitron (Headers) and JetBrains Mono (Code/Body) */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap');

        /* --- GLOBAL TEXT STYLES --- */
        html, body, [class*="css"] {
            font-family: 'JetBrains Mono', monospace; /* Developer vibe */
            color: #e0e0e0;
        }

        /* --- GLOWING HEADERS --- */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif;
            color: #00d2ff; /* Cyan Neon */
            text-shadow: 0 0 10px rgba(0, 210, 255, 0.7), 0 0 20px rgba(0, 210, 255, 0.5);
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        h1 { font-size: 3.5rem !important; margin-bottom: 0px; }
        h3 { font-size: 1.5rem !important; color: #ff0099; /* Pink Neon for subheaders */ text-shadow: 0 0 10px rgba(255, 0, 153, 0.6); }

        /* --- ANIMATED DEEP SPACE BACKGROUND --- */
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            background-size: 200% 200%;
            animation: gradientBG 20s ease infinite;
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* --- GLASSMORPHISM CARDS (The Containers) --- */
        .stTextArea, .stSelectbox, .stTextInput {
            background-color: rgba(0, 0, 0, 0.3) !important;
            border-radius: 10px;
            border: 1px solid rgba(0, 210, 255, 0.3); /* Subtle Cyan Border */
            transition: all 0.3s ease;
        }
        
        /* Focus Glow Effect on Inputs */
        .stTextArea:focus-within, .stTextInput:focus-within {
            border: 1px solid #00d2ff !important;
            box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
        }

        /* --- NEON BUTTON --- */
        .stButton>button {
            background: linear-gradient(90deg, #ff0099, #493240);
            color: white;
            border: 1px solid #ff0099;
            border-radius: 5px;
            padding: 10px 24px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(255, 0, 153, 0.4);
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255, 0, 153, 0.8);
            border-color: #fff;
        }

        /* --- RESULT BOX STYLING --- */
        .result-box {
            background: rgba(15, 52, 96, 0.6);
            border-left: 5px solid #00d2ff;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.5);
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
col1, col2 = st.columns([1, 6])
with col1:
    # A techy icon instead of the flower
    st.image("https://cdn-icons-png.flaticon.com/512/9088/9088266.png", width=80) 
with col2:
    st.title("CODE // NEXUS")
    st.markdown("### > AI-POWERED DEVELOPMENT SUITE")

st.markdown("---")

# --- 5. MAIN INTERFACE ---
# Tabs with Emoji Icons
tab1, tab2, tab3 = st.tabs(["⚡ TRANSLATE", "🐞 DEBUGGER", "🧠 EXPLAINER"])

mode = None
submit_text = "Run"

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        source_lang = st.selectbox("SOURCE LANGUAGE", ["Python", "JavaScript", "Java", "C++", "SQL", "Plain English"], key="s_lang")
    with col_b:
        target_lang = st.selectbox("TARGET LANGUAGE", ["Python", "JavaScript", "Java", "C++", "SQL", "Plain English"], key="t_lang")
    mode = "Translate"
    submit_text = "INITIATE TRANSLATION 🚀"

with tab2:
    st.info("SYSTEM READY: Paste broken code segments below for analysis.")
    mode = "Bug Fixer"
    submit_text = "EXECUTE DEBUGGING 🔧"

with tab3:
    st.info("SYSTEM READY: awaiting complex logic for deconstruction.")
    mode = "Explainer"
    submit_text = "ANALYZE LOGIC 🧠"

# --- 6. INPUT AREA ---
code_input = st.text_area("Input Code Block:", height=300, key="main_input")

# --- 7. THE LOGIC ---
if st.button(submit_text, type="primary"):
    if not api_key:
        st.error("⚠️ ACCESS DENIED: API KEY MISSING")
    elif not code_input:
        st.warning("⚠️ INPUT REQUIRED: BUFFER EMPTY")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Tech-themed Prompts
            if mode == "Translate":
                prompt = f"Role: Senior Developer. Task: Convert this {source_lang} code to {target_lang}. Constraint: Return strictly the code only.\n\n{code_input}"
            elif mode == "Bug Fixer":
                prompt = f"Role: QA Engineer. Task: 1. Identify syntax/logic errors. 2. Explain the root cause. 3. Provide the corrected code block.\n\n{code_input}"
            elif mode == "Explainer":
                prompt = f"Role: Tech Lead. Task: Deconstruct this code logic into simple terms for a junior developer.\n\n{code_input}"

            with st.spinner("🔄 PROCESSING DATA STREAM..."):
                response = model.generate_content(prompt)

            # --- 8. THE RESULT ---
            st.markdown(f"<div class='result-box'><h3>>> OPERATION SUCCESSFUL: {mode.upper()}</h3></div>", unsafe_allow_html=True)
            
            res_tab1, res_tab2 = st.tabs(["💻 TERMINAL OUTPUT", "📄 RAW LOG"])
            
            with res_tab1:
                lang_code = target_lang.lower() if mode == "Translate" else "python"
                st.code(response.text, language=lang_code)
                
            with res_tab2:
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"SYSTEM FAILURE: {e}")

# --- 9. FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #555;'>SYSTEM STATUS: ONLINE | VERSION 2.5 | POWERED BY GEMINI</div>", unsafe_allow_html=True)
