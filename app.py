import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="AI Code Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM CSS (Mesh Gradient + Glassmorphism) ---
st.markdown("""
    <style>
        /* Import Font: Inter (The Standard for Premium UI) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        /* --- GLOBAL STYLES --- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }

        /* --- THE ANIMATED MESH BACKGROUND (No Image Needed!) --- */
        [data-testid="stAppViewContainer"] {
            background-color: #000000;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
            background-size: 200% 200%;
            animation: mesh_animation 10s ease-in-out infinite;
        }

        @keyframes mesh_animation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* --- GLASS CARDS (Frosted Effect) --- */
        .stTextInput, .stSelectbox, .stTextArea {
            background-color: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: white !important;
        }
        
        /* Focus Glow */
        .stTextInput:focus-within, .stTextArea:focus-within {
            border: 1px solid #a855f7; /* Purple glow */
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
        }

        /* --- TYPOGRAPHY --- */
        h1 {
            font-weight: 800;
            background: -webkit-linear-gradient(eee, #999);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem !important;
            letter-spacing: -1px;
        }

        /* --- BUTTONS --- */
        .stButton>button {
            background: linear-gradient(to right, #6366f1, #a855f7); /* Indigo to Purple */
            color: white;
            border: none;
            border-radius: 30px; /* Pill shape */
            padding: 12px 30px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(168, 85, 247, 0.3);
        }

        /* --- RESULT CONTAINER --- */
        .result-box {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-top: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
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

# --- 4. HEADER ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/12308/12308696.png", width=70) # Abstract logo
with col2:
    st.title("Lumina Code")
    st.caption("Advanced AI Development Environment")

st.markdown("---")

# --- 5. MAIN NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["✨ Translate", "🐞 Debug", "🧬 Explain"])

mode = None
submit_text = "Run"

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        source_lang = st.selectbox("Source Language", ["Python", "JavaScript", "Java", "C++", "SQL", "English"])
    with col_b:
        target_lang = st.selectbox("Target Language", ["Python", "JavaScript", "Java", "C++", "SQL", "English"])
    mode = "Translate"
    submit_text = "Translate Code"

with tab2:
    st.info("Paste your code. Lumina will detect bugs and offer fixes.")
    mode = "Bug Fixer"
    submit_text = "Debug Code"

with tab3:
    st.info("Paste complex code to get a line-by-line breakdown.")
    mode = "Explainer"
    submit_text = "Explain Code"

# --- 6. INPUT AREA ---
code_input = st.text_area("", height=300, placeholder="// Paste your code here...", key="main_input")

# --- 7. LOGIC ---
if st.button(submit_text, type="primary"):
    if not api_key:
        st.error("Please provide an API Key.")
    elif not code_input:
        st.warning("Please enter some code.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            if mode == "Translate":
                prompt = f"Act as a Principal Engineer. Translate this {source_lang} code to {target_lang}. Return ONLY the code.\n\n{code_input}"
            elif mode == "Bug Fixer":
                prompt = f"Act as a QA Lead. Find bugs in this code, explain them, and provide the fixed version.\n\n{code_input}"
            elif mode == "Explainer":
                prompt = f"Act as a Distinguished Engineer. Explain this code simply and clearly.\n\n{code_input}"

            with st.spinner("Processing..."):
                response = model.generate_content(prompt)

            # --- RESULT DISPLAY ---
            st.markdown(f"<div class='result-box'>", unsafe_allow_html=True)
            st.subheader(f"Output: {mode}")
            
            res_tab1, res_tab2 = st.tabs(["Code", "Explanation"])
            
            with res_tab1:
                lang_code = target_lang.lower() if mode == "Translate" else "python"
                st.code(response.text, language=lang_code)
            with res_tab2:
                st.markdown(response.text)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- FOOTER ---
st.markdown("<br><center style='opacity: 0.5; font-size: 0.8rem;'>Designed with Lumina AI • 2026</center>", unsafe_allow_html=True)
