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

#################################
# USER INPUT EXAMPLE
name = "John Smith"
date = "1999-10-13"
relationship_to_victim = "Grandfather"
case_summary = "His grandchild was found dead in the house. His grandchild was stabbed 13 times."
case_evidence = "His neighbor saw that he was at the house at the time of the crime."
criminal_record = "He previously stole a bicycle when he was a teenager."

#################################
# FIRST INPUT TO GPT
prompt = f"Hello, I am a detective trying to interrogate a suspect. I will provide the background information related to the crime, and I want you to provide me exactly three questions for me to ask the suspect so that I can interrogate him. The name of the criminal is {name}, and the crime happened in {date}. He is the {relationship_to_victim} of the victim, and the case summary is as follows: {case_summary}. The evidence is as follows: {case_evidence}. The criminal record of the suspect is as follows: {criminal_record}. Do not return anything else other than the three questions in json format, with 1, 2, 3 as the keys. The suspect must be able to answer the questions in one sentence or with 'yes' or 'no'."

response = get_completion(prompt=prompt, messages=conversation_history)

print(response)
################################ REPEAT
# USER INPUT EXAMPLE 
question_chosen = "Can you confirm your whereabouts on the date of October 13, 1999?"
answer = "I was at the gym."
################################
# SECOND INPUT TO GPT
prompt = f"The question chosen was this: {question_chosen}. The answer was this: {answer}. Just like what you did before, do no return anything else other than the next three questions based on the answer in the same json format, with 1, 2, 3 as the keys."
response = get_completion(prompt=prompt, messages=conversation_history)

print(response)
################################
# AFTER THIS, REPEAT FROM 'REPEAT'