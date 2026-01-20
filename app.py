import streamlit as st
import google.generativeai as genai

# --- Page Configuration ---
st.set_page_config(page_title="Code Translator")

# --- Title and Header ---
st.title("AI Code Translator")
st.subheader("Your code language Friend :)")

# --- API Key Handling ---
try:
    # Try to get key from secrets (for the live website)
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # If running locally, ask the user
    api_key = st.text_input("Enter Gemini API Key", type="password")

# --- Main Interface ---
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "From Language", 
        ["Python", "JavaScript", "Java", "C++", "HTML/CSS", "SQL", "Plain English"]
    )

with col2:
    target_lang = st.selectbox(
        "To Language", 
        ["Python", "JavaScript", "Java", "C++", "HTML/CSS", "SQL", "Plain English"]
    )

code_input = st.text_area("Paste your code here:", height=200)

# --- The Logic ---
if st.button("Translate Code"):
    if not api_key:
        st.error("⚠️ Please provide an API Key.")
    elif not code_input:
        st.warning("⚠️ Please paste some code to translate.")
    else:
        # Configure Gemini
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Create Prompt
            prompt = f"You are an expert programmer. Translate the following {source_lang} code into {target_lang}. Return ONLY the code. Do not add explanations or markdown backticks.\n\n{code_input}"
            
            # --- CUSTOM SPINNER ADDED HERE ---
            with st.spinner("Please hold tight..."):
                response = model.generate_content(prompt)
            
            # Display Result
            st.success("Translation Complete!")
            st.subheader("Result:")
            st.code(response.text, language=target_lang.lower())
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

