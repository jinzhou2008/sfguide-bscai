import streamlit as st
from openai import OpenAI

## Validate Snowflake connection ##
conn = st.connection("snowflake")
df = conn.query("select CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME(), CURRENT_ACCOUNT(), CURRENT_ROLE(), CURRENT_WAREHOUSE()")
st.write(df)

## Validate OpenAI connection ##
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#client = OpenAI(api_key="e83a3572341642228cd2fbd04b0b2da7")
client = OpenAI(api_key="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")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "What is theory of relativity?"}
  ]
)

st.write(completion.choices[0].message.content)
