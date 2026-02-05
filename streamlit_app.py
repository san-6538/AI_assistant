import streamlit as st
import httpx
import pandas as pd

st.set_page_config(page_title="AI Operations Assistant", page_icon="🤖")

st.title("🤖 AI Operations Assistant")
st.markdown("### Multi-Agent System (Planner → Executor → Verifier)")

# Sidebar for status
with st.sidebar:
    st.header("System Status")
    try:
        httpx.get("http://127.0.0.1:8000/docs", timeout=1)
        st.success("Backend API is Online")
    except:
        st.error("Backend API is Offline (Run `python main.py`)")
    
    st.info("""
    **Architecture:**
    1. **Planner**: Deconstructs task into JSON plan
    2. **Executor**: Calls APIs (Open-Meteo, Wikipedia, etc.)
    3. **Verifier**: Validates and formats output
    """)

# Main input
task = st.text_input("Enter your request:", placeholder="e.g. What is the weather in London and Paris?")

if st.button("Run Task", type="primary"):
    if not task:
        st.warning("Please enter a task.")
    else:
        with st.status("Processing...", expanded=True) as status:
            st.write("📤 Sending task to Orchestrator...")
            
            try:
                # Call Backend
                response = httpx.post(
                    "http://127.0.0.1:8000/run-task", 
                    json={"task": task},
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    status.update(label="Task Completed!", state="complete", expanded=False)
                    
                    # Display Results
                    st.divider()
                    st.subheader("📝 Summary")
                    st.write(result.get("summary", "No summary provided."))
                    
                    st.subheader("📊 Data")
                    st.markdown(result.get("data", "No data returned."))
                    
                    st.subheader("🔍 Sources")
                    sources = result.get("sources", [])
                    if sources:
                        st.json(sources)
                    else:
                        st.write("No sources cited.")
                        
                else:
                    status.update(label="Error!", state="error")
                    st.error(f"API Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                status.update(label="Connection Failed", state="error")
                st.error(f"Failed to connect to backend: {e}")
