import streamlit as st
import google.generativeai as genai

# --- Page Configuration ---
st.set_page_config(page_title="AI Code Companion", page_icon="🚀", layout="wide")

# --- Title and Header ---
st.title("🚀 AI Code Companion")
st.subheader("Translate, Debug, and Explain your code.")

# --- API Key Handling ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
except:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# --- Main Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    # Feature 1: The Mode Selector
    mode = st.radio(
        "What do you want to do?",
        ["Translate Code", "Find & Fix Bugs", "Explain Code"],
        horizontal=True
    )

    # Feature 2: Dynamic Dropdowns
    # We only need language selectors if we are Translating
    if mode == "Translate Code":
        source_lang = st.selectbox("From", ["Python", "JavaScript", "Java", "C++", "SQL", "Plain English"])
        target_lang = st.selectbox("To", ["Python", "JavaScript", "Java", "C++", "SQL", "Plain English"])
    
    code_input = st.text_area("Paste your code here:", height=300)

with col2:
    st.write("### Result")
    result_container = st.empty() # Placeholder for the result

# --- The Logic ---
if st.button("Run AI Magic ✨"):
    if not api_key:
        st.error("⚠️ Please provide an API Key.")
    elif not code_input:
        st.warning("⚠️ Please paste some code.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # --- DYNAMIC PROMPTS ---
            if mode == "Translate Code":
                prompt = f"Translate this {source_lang} code into {target_lang}. Return ONLY the code.\n\n{code_input}"
            
            elif mode == "Find & Fix Bugs":
                prompt = f"Analyze this code for errors. 1. List the bugs found. 2. Provide the corrected code block.\n\n{code_input}"
                
            elif mode == "Explain Code":
                prompt = f"Explain exactly what this code does in simple terms. Break it down line by line if complex.\n\n{code_input}"

            # --- RUN ---
            with st.spinner(f"Please hold tight... AI is {mode.split()[0].lower()}ing..."):
                response = model.generate_content(prompt)
            
            # --- DISPLAY ---
            with col2:
                st.success("Done!")
                st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
