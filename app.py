import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv



load_dotenv()

def initialize_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=500,
        timeout=None,
        max_retries=2,
    )

# Streamlit App
def main():
    # Add custom HTML and CSS
    st.markdown(
        """
        <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .center-logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            background-color: #000000; /* Black background */
            padding: 10px 0;
            font-size: 14px;
            color: #ffffff; /* White text */
            border-top: 1px solid #e9ecef;
        }
        .footer a {
            text-decoration: none;
            color: #ffffff; /* White link color */
        }
        .footer a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Add the logo
    st.markdown(
        """
        <div class="center-logo">
            <img src="data:image/png;base64,{}" alt="GenCode Labs Logo" width="150">
        </div>
        """.format(get_base64_encoded_image("GenCode Labs.png")),
        unsafe_allow_html=True,
    )

    st.title("AI Content Humanizer")
    st.write("This app takes AI-generated content and rewrites it in a human-like, natural, and conversational style.")

    # Check for API Key in .env
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.warning("GROQ_API_KEY is not set. Please configure it in a .env file.")
        st.stop()

    # Set the API key for the application
    os.environ["GROQ_API_KEY"] = groq_api_key

    # Initialize the LLM
    llm = initialize_llm()

    # User Input
    st.header("Input")
    input_text = st.text_area("Paste the AI-generated content here:", height=200)

    if st.button("Humanize Content"):
        if not input_text.strip():
            st.error("Please provide some content to humanize.")
        else:
            with st.spinner("Humanizing your content..."):
                try:
                    # Custom prompt for the system
                    system_prompt = (
                    '''You are an advanced AI model specialized in transforming text into a natural, human-like conversation. Your goal is to rewrite any input in a way that feels fluid, relatable, and emotionally engaging—while preserving the original intent. The output should be clear, concise, and effortlessly readable, as if written by a real person.

                    When rewriting:

                    Simplify complex or technical terms into everyday language.
                    Infuse a natural, conversational tone with subtle emotional depth.
                    Structure sentences in a way that mimics human speech and storytelling.
                    Ensure clarity and coherence while maintaining the essence of the message.
                    If the input text is already conversational, refine it further to enhance relatability and warmth.
                    Your responses should feel less like an AI-generated rewrite and more like a polished, engaging human-written piece.'''
                    )

                    # Messages for the model
                    messages = [
                        ("system", system_prompt),
                        ("human", input_text),
                    ]
                    # Invoke the model
                    response = llm.invoke(messages)
                    
                    # Access the content attribute of the response
                    humanized_content = response.content
                    
                    st.header("Humanized Content")
                    st.write(humanized_content)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # # Footer
    # st.markdown(
    #     """
    #     <div class="footer">
    #         Created with ❤️ by <a href="https://gencodelabs.com" target="_blank">GenCode Labs</a>
    #     </div>
    #     """,
    #     unsafe_allow_html=True,
    # )

# Function to encode the image to base64
def get_base64_encoded_image(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

if __name__ == "__main__":
    main()
