from jobspy import scrape_jobs
from ollama import chat
from ollama import ChatResponse
import pandas as pd
import requests
import time

def check_ollama_service():
    try:
        response = requests.get('http://localhost:11434/api/tags')
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def job_search(name,country,city):
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term=name,
        location=city,
        results_wanted=20,
        hours_old=168,
        country_indeed=country,
        
        # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
        # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    )
    descriptions = jobs['description']
    combined_descriptions = "\n".join([f"{i+1}. {desc}" for i, desc in enumerate(descriptions)])
    print(combined_descriptions)
    return combined_descriptions

def aiSummary(description):
    # Check if Ollama is running
    if not check_ollama_service():
        print("Error: Ollama service is not running. Please start Ollama first.")
        print("Run 'ollama serve' in your terminal")
        return None
    
    try:
        response: ChatResponse = chat(model='llama3.2', messages=[  # Changed to llama2 as it's more commonly available
            {
                'role': 'user',
                'content': f'Below I will give you a text which is a bunch of companies job listing descriptions. They are all combined together and numbered. I want you to take all these descriptions and only look at the requirements and ignore everything else. Take all the job requirements and create a summary highlighting the top 10 most common requirements. below is the job description {description}',
            },
        ])
        print(response['message']['content'])
        return response['message']['content']
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        print("Please ensure Ollama is running with 'ollama serve'")
        return None

job_description = job_search('Data analyst','Hong Kong','Hong Kong')
aiSummary(job_description)