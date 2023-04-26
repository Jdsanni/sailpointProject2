import requests
import datetime

# Define the repository information
owner = 'huggingface'
repo = 'transformers'

# Define the personal access token for authentication
token = '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'

# Define the API endpoint URLs
base_url = 'https://api.github.com/repos'
pulls_url = f'{base_url}/{owner}/{repo}/pulls'

# Define the date range for filtering pull requests
end_date = datetime.datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

# Define the headers for authentication and request formatting
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json' 
}

# Send the GET request to the pull requests endpoint
response = requests.get(pulls_url, headers=headers)

# Parse the JSON response to a list of dictionaries
pull_requests = response.json()

# Separate the pull requests by status
opened = []
closed = []
in_progress = []

for pull_request in pull_requests:
    created_date = datetime.datetime.strptime(pull_request['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
    if created_date < start_date or created_date > end_date:
        continue
    if pull_request['state'] == 'open':
        opened.append(pull_request)
    elif pull_request['merged_at'] is not None:
        closed.append(pull_request)
    else:
        in_progress.append(pull_request)

# Format and print the email summary report
from_email = 'josh@sailpoint.com'
to_email = 'manager_1@sailpoint.com'
subject = f'Report for {owner}/{repo} Pull Requests ({start_date} to {end_date})'
body = f'''
Hello Sailpoint Team Manager,

As Requested, Here is the summary report for {owner}/{repo} pull requests from {start_date} to {end_date}:

Opened Pull Requests ({len(opened)}):
'''

for pr in opened:
    body += f"\n- #{pr['number']}: {pr['title']} ({pr['html_url']})"

body += f'''

Closed Pull Requests ({len(closed)}):
'''

for pr in closed:
    body += f"\n- #{pr['number']}: {pr['title']} ({pr['html_url']})"

body += f'''

Pull Requests In Progress ({len(in_progress)}):
'''

for pr in in_progress:
    body += f"\n- #{pr['number']}: {pr['title']} ({pr['html_url']})"

print(f'From: {from_email}\nTo: {to_email}\nSubject: {subject}\n\n{body}')