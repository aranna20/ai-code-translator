import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="AI Code Swiss Army Knife",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CUSTOM CSS (The "Better UI & Font" Magic) ---
st.markdown("""
    <style>
        /* Import Google Font: Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

        /* Apply Font to Whole App */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Styling the Title */
        h1 {
            color: #ffffff;
            font-weight: 600;
        }

        /* Styling Buttons */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.02);
        }

        /* Custom Box for Results */
        .result-box {
            background-color: #262730;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #4CAF50;
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
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
with col2:
    st.title("Swiss Army Knife for Code")
    st.markdown("**Translate, Debug, and Explain** your code with AI.")

st.write("---")

# --- 5. MAIN INTERFACE (Using Tabs for "Better UI") ---
tab1, tab2, tab3 = st.tabs(["🔀 Translate", "🐞 Bug Fixer", "📖 Explainer"])

# We use a variable to store the user's choice based on the tab
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

# --- 6. INPUT AREA (Shared across all tabs) ---
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

            # --- 8. THE RESULT (Better UI: Chat Bubble Style) ---
            st.markdown(f"<div class='result-box'><h3>✨ Result ({mode})</h3></div>", unsafe_allow_html=True)
            
            # Using tabs for the result view (Raw text vs Code)
            res_tab1, res_tab2 = st.tabs(["💻 Code View", "📄 Raw Text"])
            
            with res_tab1:
                # If it's a translation, we guess the language for syntax highlighting
                lang_code = target_lang.lower() if mode == "Translate" else "python"
                st.code(response.text, language=lang_code)
                
            with res_tab2:
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- 9. FOOTER ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Gemini 2.5")
