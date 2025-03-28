from flask import Flask, url_for, render_template, request, redirect, flash, send_from_directory
import pandas as pd
import json
from hashlib import sha256
from jobspy import scrape_jobs

app = Flask(__name__, static_folder='static')
#app.secret_key = "9773e89f69e69285cf11c10cbc44a37945f6abbc5d78d5e20c2b1b0f12d75ab7"

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/submit',methods=['POST'])
def submit():
    job_title = request.form.get('job_title')
    job_location = request.form.get('job_location')
    include = [word.strip() for word in request.form.get('include', '').split(',') if word.strip()]
    exclude = [word.strip() for word in request.form.get('exclude', '').split(',') if word.strip()]
    
    if not job_title:
        flash('Please enter a job title.')
        return redirect(url_for('index'))
    
    jobs = generate_jobs(job_title, job_location, include, exclude)
    jobs_list = jobs.to_dict('records')
    
    # Ensure URLs are properly formatted
    for job in jobs_list:
        if 'job_url' not in job or not job['job_url']:
            job['job_url'] = '#'
        elif not str(job['job_url']).startswith(('http://', 'https://')):
            job['job_url'] = f"https://{job['job_url']}"
    
    return render_template('results.html', jobs=jobs_list)

# Add this route to help debug static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def generate_jobs(job_title,job_location,include,exclude):
    jobs = scrape_jobs(
        site_name=["indeed"],
        search_term=job_title,
        location=job_location,
        results_wanted=50,
        hours_old=168,
        country_indeed='Hong Kong',
    )
    
    # Only filter if include/exclude lists are not empty
    if include or exclude:
        filtered_jobs = jobs[
            jobs['description'].apply(lambda x: 
                (not include or all(word.lower() in str(x).lower() for word in include)) and 
                (not exclude or not any(word.lower() in str(x).lower() for word in exclude))
            )
        ]
    else:
        filtered_jobs = jobs
        
    filtered_jobs.to_csv('Jobs.csv')
    print(f"Filtered down to {len(filtered_jobs)} jobs")
    print(filtered_jobs.head())
    print(filtered_jobs.columns)
    return filtered_jobs