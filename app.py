import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Lumina Code Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. VERCEL-STYLE DARK THEME (Clean, Matte, Professional) ---
st.markdown("""
    <style>
        /* Import Font: Inter */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* --- GLOBAL RESET & DARK THEME --- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #e5e7eb; /* Gray-200 */
        }
        
        .stApp {
            background-color: #000000; /* Deep Black */
        }

        /* --- INPUTS & TEXT AREAS --- */
        .stTextInput, .stSelectbox, .stTextArea, .stFileUploader {
            background-color: #0a0a0a; /* Very dark gray */
            border: 1px solid #333333;
            border-radius: 8px;
            color: #ffffff;
        }
        
        /* Focus states for inputs */
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #ffffff !important;
            box-shadow: none !important;
        }

        /* --- BUTTONS --- */
        .stButton>button {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #ffffff;
            border-radius: 6px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.2s ease;
            width: 100%;
        }

        .stButton>button:hover {
            background-color: #e5e5e5;
            border-color: #e5e5e5;
            transform: translateY(-1px);
        }

        /* --- HEADERS --- */
        h1, h2, h3 {
            font-weight: 700;
            letter-spacing: -0.02em;
            color: #ffffff;
        }

        /* --- CUSTOM CONTAINERS --- */
        .editor-container {
            border: 1px solid #333;
            border-radius: 10px;
            padding: 15px;
            background-color: #050505;
        }
        
        /* Remove default streamlit padding at top */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Custom Success/Info Boxes */
        .stAlert {
            background-color: #111;
            border: 1px solid #333;
            color: #aaa;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. API KEY HANDLING ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

# --- 4. HEADER (Icon Removed) ---
st.markdown("### **AI Code Translator** <span style='color:#666; font-weight:400; font-size: 0.9em;'>by Arannayava</span>", unsafe_allow_html=True)
st.write("") # Spacer

# --- 5. MAIN LOGIC ---
tab1, tab2, tab3 = st.tabs(["Translate", "Debug", "Explain"])

# ==========================================
# TAB 1: TRANSLATOR (SIDE-BY-SIDE LAYOUT)
# ==========================================
with tab1:
    # --- Toolbar Row ---
    col_tools1, col_tools2, col_tools3 = st.columns([2, 2, 4])
    
    with col_tools1:
        source_lang = st.selectbox("From", ["Python", "JavaScript", "Java", "C++", "SQL", "CSV", "JSON", "English"], index=0, label_visibility="collapsed")
    
    with col_tools2:
        target_lang = st.selectbox("To", ["Python", "JavaScript", "Java", "C++", "SQL", "CSV", "JSON", "English"], index=1, label_visibility="collapsed")
        
    with col_tools3:
        # --- FILE INSERT OPTION ---
        uploaded_file = st.file_uploader("Upload file", type=['py', 'js', 'java', 'cpp', 'sql', 'txt', 'csv', 'json'], label_visibility="collapsed")

    # --- Content Logic ---
    initial_code = ""
    if uploaded_file is not None:
        try:
            initial_code = uploaded_file.read().decode("utf-8")
            st.toast(f"File '{uploaded_file.name}' loaded successfully!", icon="✅")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    # --- Editor Row (Split Screen) ---
    col_input, col_output = st.columns(2)

    with col_input:
        st.markdown(f"**Input ({source_lang})**")
        code_input = st.text_area(
            "Input Code", 
            value=initial_code, 
            height=400, 
            label_visibility="collapsed",
            placeholder=f"Paste your {source_lang} code here or drop a file..."
        )
        
        if st.button("Translate Code", type="primary", use_container_width=True):
            if not api_key:
                st.error("API Key missing.")
            elif not code_input:
                st.warning("No code to translate.")
            else:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash') 
                    prompt = f"Act as a Principal Engineer. Translate this {source_lang} to {target_lang}. Return ONLY the code/data, no markdown backticks, no explanations.\n\n{code_input}"
                    
                    with st.spinner("Translating..."):
                        response = model.generate_content(prompt)
                        st.session_state['translation_result'] = response.text
                except Exception as e:
                    st.error(f"Error: {e}")

    with col_output:
        st.markdown(f"**Output ({target_lang})**")
        
        # Display Result if it exists in session state
        if 'translation_result' in st.session_state:
            # Determine syntax highlighting
            lang_map = {"SQL": "sql", "JSON": "json", "CSV": "plaintext", "English": "markdown"}
            syntax = lang_map.get(target_lang, target_lang.lower())
            
            st.code(st.session_state['translation_result'], language=syntax, line_numbers=True)
        else:
            # Placeholder for empty state
            st.markdown(
                """
                <div style='height: 400px; border: 1px dashed #333; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #555;'>
                    Waiting for translation...
                </div>
                """, 
                unsafe_allow_html=True
            )

# ==========================================
# TAB 2: BUG FIXER
# ==========================================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_bug = st.columns([1, 6, 1])[1] # Centered column
    
    with col_bug:
        st.markdown("### 🐞 Intelligent Debugger")
        bug_input = st.text_area("Paste code to debug", height=200)
        
        if st.button("Analyze & Fix Bugs", use_container_width=True):
            if bug_input and api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.0-flash')
                prompt = f"Act as a QA Lead. Find bugs, explain them, and provide the fixed code.\n\n{bug_input}"
                with st.spinner("Debugging..."):
                    res = model.generate_content(prompt)
                    st.markdown(res.text)

# ==========================================
# TAB 3: EXPLAINER
# ==========================================
with tab3:
    st.markdown("### 🧬 Code Explainer")
    exp_input = st.text_area("Paste code to explain", height=200)
    if st.button("Explain Logic", use_container_width=True):
        if exp_input and api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"Explain this code simply.\n\n{exp_input}"
            with st.spinner("Analyzing..."):
                res = model.generate_content(prompt)
                st.markdown(res.text)

# --- FOOTER ---
st.markdown("<br><hr style='border-color: #333;'><center style='color: #444; font-size: 0.8rem;'>By Arannayava Debnath</center>", unsafe_allow_html=True)
