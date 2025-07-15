import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

#Loading environment variables 
load_dotenv()
api_key= os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("AI Supplement Formulation Tool")
st.write("Describe your supplement idea below and get AI-generated formulations, costs, and production timelines.")

user_input= st.text_area("💬 Describe your product idea (e.g. hair growth gummies, sleep aid pills)...", height=200)

if st.button("✨ Generate Products"):
    if not user_input.strip():
        st.warning("Please describe your product idea.")
    else:
        with st.spinner("Generating customized product ideas for your brand"):

            #Prompt for CHATGPT 
            prompt1= f"""
            You are a healthcare supplement formulations development expert. Based on this product description: "{user_input}", generate 5-7 unique supplement products. The ingredients must be beneficial for the user & should have some studies done on it.
            For each product, output:
            - Product Name
            - Key Ingredients
            - Intended Benefit
            - Estimated Cost per Unit (USD)
            - Suggested Dosage
            """

            try:
                completion= client.chat.completions.create(
                    model="gpt-4",
                    messages= [{"role": "user", "content": prompt1}], 
                    temperature= 0.6
                )
                response_text= completion.choices[0].message.content
                st.subheader("Product Ideas & Formulations: ")
                st.markdown(response_text)

                #hardcoded turnaround and cost estimate (for prototype)
                st.subheader("Manufacturing Time & Cost Estimates")
                order_qtys= [1000, 5000, 10000, 20000, 25000, 30000]
                turnarounds = [14, 21, 25, 30, 35, 40]  # in days
                cost_per_bottle = [7.84, 7.13, 6.98, 6.30, 5.86, 5.12]  

                df = pd.DataFrame({
                    "Order Quantity": order_qtys,
                    "Estimated Turnaround Time (days)": turnarounds,
                    "Estimated Cost per Bottle (USD)": cost_per_bottle
                })

                st.dataframe(df)

                ## MARKET INSIGHTS PROMPT
                prompt2 = f"""
                Based on the product category "{user_input}", list the current Top 10 selling products in the US market. 
                Include product name, brand, and approximate market share or sales.
                """

                completion2 = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt2}],
                    temperature=0.7
                )

                st.subheader("📈 Top 10 Market Products")
                st.markdown(completion2.choices[0].message.content)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

