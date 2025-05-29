import streamlit as st
import openai

# Set Streamlit page configuration
st.set_page_config(page_title="Prompt Enhancer", layout="centered")

# Title
st.title("🔧 Prompt Enhancer App")

# Input form
with st.form("prompt_form"):
    role = st.text_input("Role", placeholder="e.g. You are an experienced data scientist")
    context = st.text_area("Context", placeholder="e.g. The user is analyzing sales data from an e-commerce store")
    task = st.text_area("Task", placeholder="e.g. Generate insights and visualize trends in product categories")
    api_key = st.text_input("OpenAI API Key", type="password")
    submit = st.form_submit_button("Enhance Prompt")

# Handle form submission
if submit:
    if not all([role, context, task, api_key]):
        st.error("Please fill in all fields.")
    else:
        openai.api_key = api_key

        # Construct the enhancement instruction
        instruction = f"""
        You are an assistant that improves prompts for ChatGPT.
        Given the following inputs, create a well-structured prompt that includes:
        - A clear role for GPT to assume.
        - Relevant context.
        - A defined task.
        - An instruction to clarify assumptions before answering.
        - A suggestion on how the answer should be formatted (e.g., bullet points, code blocks, tables).

        Role: {role}
        Context: {context}
        Task: {task}

        Provide only the enhanced prompt.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": instruction}
                ],
                temperature=0.7,
                max_tokens=500
            )
            enhanced_prompt = response["choices"][0]["message"]["content"].strip()
            st.subheader("✨ Enhanced Prompt")
            st.code(enhanced_prompt)
        except Exception as e:
            st.error(f"Error: {str(e)}")
