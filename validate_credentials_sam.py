import streamlit as st
import openai
from openai import OpenAI
import os

#os.environ["AZURE_OPENAI_API_KEY"] = "2xxxxx1"
#s.environ["AZURE_OPENAI_ENDPOINT"] = "https://xxxx.openai.azure.com/"

# Set Azure OpenAI API configuration
openai.api_type = "azure"
#openai.api_base = "https://edhopenaitest.openai.azure.com/"
openai.azure_endpoint=  "https://edhopenaitest.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "e83a3572341642228cd2fbd04b0b2da7"
#openai.api_key = st.secrets["OPENAI_API_KEY"]

conn = st.connection("snowflake")
df = conn.query("select current_warehouse()")
st.write(df)

"""
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "What is theory of relativity?"}
  ]
)

st.write(completion.choices[0].message.content)
"""

def generate_code(description, language):
    try:
        response = openai.chat.completions.create(
            model="gpt-4-edh",
            messages=[{"role": "system", "content": f"Translate this into {language} code: {description}"}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    st.title("Plain English to Code Translator")

    # User inputs
    description = st.text_area("Enter your plain English description here:")
    language = st.selectbox("Select Programming Language", ["Python", "JavaScript", "C++", "Java", "Others"])
    translate_button = st.button("Translate to Code")

    if translate_button and description:
        generated_code = generate_code(description, language)
        st.text_area("Generated Code:", generated_code, height=300)

if __name__ == "__main__":
    main()


