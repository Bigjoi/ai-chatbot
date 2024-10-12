import streamlit as st 
import google.generativeai as genai 
 
st.title("🐧 My chatbot app") 
st.subheader("Conversation") 
 
# Capture Gemini API Key 
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password") 
 
# Initialize the Gemini Model 
if gemini_api_key: 
    try: 
        # Configure Gemini with the provided API Key 
        genai.configure(api_key=gemini_api_key) 
        model = genai.GenerativeModel("gemini-pro") 
        st.success("Gemini API Key successfully configured.") 
    except Exception as e: 
        st.error(f"An error occurred while setting up the Gemini model: {e}") 
 
 

# Initialize session state for storing chat history 
if "chat_history" not in st.session_state: 
    st.session_state.chat_history = []  # Initialize with an empty list 
 
# Display previous chat history using st.chat_message (if available) 
for role, message in st.session_state.chat_history: 
    st.chat_message(role).markdown(message) 
 
# Capture user input and generate bot response 
if user_input := st.chat_input("Type your message here..."): 
    # Store and display user message 
    st.session_state.chat_history.append(("user", user_input)) 
    st.chat_message("user").markdown(user_input) 
 
    # Use Gemini AI to generate a bot response 
    if model: 
        try: 
            response = model.generate_content(user_input) 
            bot_response = response.text 


 
            # Store and display the bot response 
            st.session_state.chat_history.append(("assistant", bot_response)) 
            st.chat_message("assistant").markdown(bot_response) 
        except Exception as e: 
            st.error(f"An error occurred while generating the response: {e}") 

# Add a ﬁle uploader for CSV data 
st.subheader("Upload CSV for Analysis") 
uploaded_ﬁle = st.ﬁle_uploader("Choose a CSV ﬁle", type=["csv"]) 

 


if uploaded_ﬁle is not None: 
    try: 
        # Load the uploaded CSV ﬁle 
        st.session_state.uploaded_data = pd.read_csv(uploaded_ﬁle) 
        st.success("File successfully uploaded and read.") 
         
        # Display the content of the CSV 
        st.write("### Uploaded Data Preview") 
        st.dataframe(st.session_state.uploaded_data.head()) 
    except Exception as e: 
        st.error(f"An error occurred while reading the ﬁle: {e}") 

# Checkbox for indicating data analysis need 
analyze_data_checkbox = st.checkbox("Analyze CSV Data with AI") 