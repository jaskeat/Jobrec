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
        results_wanted=1,
        hours_old=168,
        country_indeed=country,
    )
    jobs = jobs.dropna(subset=['description'])
    descriptions = jobs['description']
    
    # Clean and format descriptions
    cleaned_descriptions = []
    for i, desc in enumerate(descriptions):
        # Remove extra whitespace and normalize line endings
        cleaned_text = ' '.join(desc.strip().split())
        if cleaned_text:  # Only add non-empty descriptions
            cleaned_descriptions.append(f"Job No.{i+1}. {cleaned_text}")
    
    # Join with single newline
    combined_descriptions = '\n'.join(cleaned_descriptions)
    
    print(f"Processed {len(cleaned_descriptions)} job descriptions")
    with open('/Users/jaskeatsingh/COding/JobRec/app/combined_descriptions.txt', 'w') as file:
        file.write(combined_descriptions)
    
    return combined_descriptions



def aiSummary(description):
    # Check if Ollama is running
    if not check_ollama_service():
        print("Error: Ollama service is not running. Please start Ollama first.")
        print("Run 'ollama serve' in your terminal")
        return None
    
    try:
        print('MODEL RUNNING')
        response: ChatResponse = chat(model='llama3.2', messages=[  # Changed to llama2 as it's more commonly available
            {
            'role': 'user',
            'content': f'''
            You are an AI Tool that has to follow my exact instructions and do nothing else.
            Below is a text containing combined job listing descriptions from various companies, each labeled as "Job No.1," "Job No.2," and so on till Job No.20. Your task is to extract only the requirements from these descriptions.
            Identify and summarize the top 5 most common job requirements, focus more on technical skills like programming and certifications needed for that position. BE MORE SPECIFIC 
            DO NOT SUMMARIZE THE JOB DESCRIPTION FOR EACH POSITION, instead take all the jobs and summarize the requirements AS A WHOLE
            Present your findings in a simple, numbered list without any additional titles or explanations.
            Ensure that the list accurately reflects the most frequently mentioned requirements across all descriptions. You are not allowed to give me any other response or text except the list
            Here is the description {description}
            ''',
            'options':{
            'num_ctx':30000    
            }
            },
        ])
        print(response['message']['content'])
        return response['message']['content']
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        print("Please ensure Ollama is running with 'ollama serve'")
        return None
    
def aiTester(description):
    if not check_ollama_service():
        print("Error: Ollama service is not running. Please start Ollama first.")
        print("Run 'ollama serve' in your terminal")
        return None
    
    try:
        print('MODEL RUNNING')
        response: ChatResponse = chat(model='llama3.2', messages=[  # Changed to llama2 as it's more commonly available
            {
            'role': 'user',
            'content': f'''
            You are an AI Tool that has to follow my exact instructions and do nothing else.
            Below is a text containing combined job listing descriptions from various companies, each labeled as "Job No.1," "Job No.2," and so on till Job No.20. Your task is to extract only the requirements from these descriptions.
            DO NOT TKAE IN ANY OTHER INFORMATION, simply remove everything EXCEPT THE REQUIREMENTS
            Here is the description {description}
            ''',
            'options':{
            'num_ctx':30000    
            }
            },
        ])
        print(response['message']['content'])
        return response['message']['content']
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        print("Please ensure Ollama is running with 'ollama serve'")
        return None
job_description = job_search('Software engineer','Hong Kong','Hong Kong')
aiSummary(job_description)