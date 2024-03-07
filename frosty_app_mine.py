import openai
from openai import OpenAI
import re
import streamlit as st
from promptsmine import get_system_prompt

#os.environ["AZURE_OPENAI_API_KEY"] = "2xxxxx1"
#s.environ["AZURE_OPENAI_ENDPOINT"] = "https://xxxx.openai.azure.com/"

## Validate Snowflake connection ##
conn = st.connection("snowflake")
# df = conn.query("select current_warehouse(), current_database(), current_schema()")
# st.write(df)

# Set Azure OpenAI API configuration
openai.api_type = "azure"
#openai.api_base = "https://edhopenaitest.openai.azure.com/"
openai.azure_endpoint=  "https://edhopenaitest.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "e83a3572341642228cd2fbd04b0b2da7"
#openai.api_key = st.secrets["OPENAI_API_KEY"]

## Validate OpenAI connection ##
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#client = OpenAI(api_key="e83a3572341642228cd2fbd04b0b2da7")
# completion = openai.chat.completions.create(
#   model="gpt-4-edh",
#   messages=[
#     {"role": "user", "content": "What is 1+2?"}
#   ]
# )
# st.write(completion.choices[0].message.content)


st.title("☃️ Snowy")

# Initialize the chat messages history
#client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
if "messages" not in st.session_state:
    # system prompt includes table information, rules, and prompts the LLM to produce
    # a welcome message to the user.
    st.session_state.messages = [{"role": "system", "content": get_system_prompt()}]

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# display the existing chat messages
for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "results" in message:
            st.dataframe(message["results"])

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = ""
        resp_container = st.empty()
        for delta in openai.chat.completions.create(
            model="gpt-4-edh",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):  
            if delta.choices :
                response += (delta.choices[0].delta.content or "")
            resp_container.markdown(response)

        message = {"role": "assistant", "content": response}
        # Parse the response for a SQL query and execute if available
        sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
        if sql_match:
            sql = sql_match.group(1)
            conn = st.connection("snowflake")
            message["results"] = conn.query(sql)
            st.dataframe(message["results"])
        st.session_state.messages.append(message) 
        
