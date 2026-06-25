import streamlit as st
import requests

# 1. Page Configuration & Styling
st.set_page_config(page_title="Enterprise AI Workflow Agent", page_icon="🤖", layout="centered")

st.title("🤖 Autonomous Workflow Agent")
st.caption("Integrated via n8n with Google Sheets, Tasks, Calendar, Gmail, and Docs")

# 2. Connection Settings (Stored in Streamlit Sidebar)
st.sidebar.header("⚙️ Integration Settings")
n8n_url = st.sidebar.text_input(
    "n8n Webhook URL", 
    value="http://localhost:5678/webhook/b894e9ee-4435-4249-92f3-5ee39146ecfe",
    help="Paste your live n8n cloud or local ngrok tunnel URL here."
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📋 Sample Prompts to Try:
- *Add an expense of ₹450 on Dominos dinner yesterday under Food*
- *Create a task named 'Review n8n pipeline' in my N8N Practice list*
- *Create a new note titled 'Project Launch Strategy 2026'*
- *Send an email to boss@company.com with the subject 'Status Update' saying everything is live*
""")

# 3. Maintain Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages in the UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle Natural Multi-line User Input (Enter/Shift+Enter natively supported)
if user_prompt := st.chat_input("Ask your agent to handle a task..."):
    
    # Render user message instantly
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Prepare data payload (Python requests serializes natural line breaks automatically into JSON)
    payload = {"message": user_prompt}

    # Render assistant processing state
    with st.chat_message("assistant"):
        with st.spinner("Executing autonomous workflow steps..."):
            try:
                # Trigger the n8n backend pipeline
                response = requests.post(n8n_url, json=payload, timeout=15)
                
                if response.status_code == 200:
                    # Parse output safely assuming it matches your verified n8n schema format
                    res_data = response.json()
                    
                    # Handle array formats or text block extraction directly
                    if isinstance(res_data, list) and len(res_data) > 0:
                        output_text = res_data[0].get("output", "Workflow executed successfully, but no text output was generated.")
                    elif isinstance(res_data, dict):
                        output_text = res_data.get("output", "Workflow executed successfully.")
                    else:
                        output_text = str(res_data)
                        
                    st.markdown(output_text)
                    st.session_state.messages.append({"role": "assistant", "content": output_text})
                else:
                    error_msg = f"⚠️ Connection made, but n8n returned Status Code {response.status_code}.\n\n*Ensure your local n8n workflow is set to 'Listen for test event' or active.*"
                    st.markdown(error_msg)
                    
            except requests.exceptions.RequestException:
                # Portfolio Fallback: If your laptop is closed, show recruiters a realistic preview of the system architecture output!
                fallback_text = (
                    "⚙️ **[Portfolio Sandbox Mode Active]**\n\n"
                    "Your request was captured cleanly! Because the local backend instance is currently offline, "
                    "here is a structural preview of how the n8n agent maps this input parameters dynamically:\n\n"
                    "```json\n"
                    "{\n"
                    f"  \"extracted_input\": \"{user_prompt.strip()}\",\n"
                    f"  \"mapped_timezone\": \"Asia/Kolkata (IST)\",\n"
                    "  \"parameter_extraction_rule\": \"\$fromAI() rigid mapping schema enforced\"\n"
                    "}\n"
                    "```\n"
                    "Check out the full workflow JSON mapping blueprint on my GitHub repository link above!"
                )
                st.markdown(fallback_text)
                st.session_state.messages.append({"role": "assistant", "content": fallback_text})
