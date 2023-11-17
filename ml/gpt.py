import openai
import os
import pandas as pd
import time

openai.api_key = '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'

def get_completion(prompt, messages, model="gpt-4", temperature=0):
    messages.append({"role": "user", "content": prompt})

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        messages.append({"role": "assistant", "content": response.choices[0].message["content"]})
        
        return response.choices[0].message["content"]
    
    except Exception as e:
        return f"An error occurred: {e}"

conversation_history = []

prompt1 = "Hi, my name is Taekwan. Nice to meet you!"

response = get_completion(prompt=prompt1, messages=conversation_history)

print(response)

prompt2 = "Do you know my name?"

response = get_completion(prompt=prompt2, messages=conversation_history)

print(response)