#Data Scraping

import requests
import time
import json
import csv
from tqdm import tqdm
import pandas as pd

# Replace 'your_token_here' with your GitHub token
GITHUB_TOKEN = 'your token F'
BASE_URL = 'https://api.github.com'
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

# Parameters
location = "Tokyo"
min_followers = 200

# File paths
json_file_path = "github_users_tokyo.json"
csv_file_path = "github_users_tokyo.csv"
detailed_json_path = "github_detailed_users_tokyo.json"
detailed_csv_path = "github_detailed_users_tokyo.csv"
final_csv_path = "github_detailed_users_tokyo_fixed.csv"
repos_json_path = "github_repos_data.json"
repos_csv_path = "github_repos_data.csv"

# Step 1: Collect User Data based on Location and Followers
user_data = []

def search_users(page=1):
    query = f"location:{location} followers:>{min_followers}"
    url = f"{BASE_URL}/search/users?q={query}&page={page}&per_page=30"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.json().get('message', '')}")
        return None

def collect_user_data():
    page = 1
    with tqdm(desc="Collecting User Data", unit="user") as progress_bar:
        while True:
            response_data = search_users(page)
            if response_data is None or not response_data.get("items"):
                break
            for user in response_data["items"]:
                user_data.append({"username": user["login"], "id": user["id"]})
                progress_bar.update(1)
            page += 1
            time.sleep(2)

# Step 2: Save Basic User Data to JSON and CSV
def save_basic_data():
    with open(json_file_path, "w") as json_file:
        json.dump(user_data, json_file, indent=4)
    with open(csv_file_path, mode="w", newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["username", "id"])
        writer.writeheader()
        writer.writerows(user_data)
    print(f"Basic data saved to {json_file_path} and {csv_file_path}")

# Step 3: Collect Detailed User Data
def clean_company(company):
    if company:
        company = company.strip()
        if company.startswith('@'):
            company = company[1:]
        company = company.upper()
    return company or ""

def get_user_details(username):
    url = f"{BASE_URL}/users/{username}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return {
                "username": username,
                "name": user_data.get("name", ""),
                "company": clean_company(user_data.get("company", "")),
                "location": user_data.get("location", ""),
                "email": user_data.get("email", ""),
                "hireable": user_data.get("hireable", False),
                "bio": user_data.get("bio", ""),
                "public_repos": user_data.get("public_repos", 0),
                "followers": user_data.get("followers", 0),
                "following": user_data.get("following", 0),
                "created_at": user_data.get("created_at", "")
            }
        else:
            print(f"Failed to fetch data for {username}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error for {username}: {e}")

detailed_user_data = []

def collect_detailed_data():
    with open(json_file_path, "r") as file:
        users = json.load(file)
    with tqdm(total=len(users), desc="Collecting Detailed User Data", unit="user") as progress_bar:
        for user in users:
            details = get_user_details(user["username"])
            if details:
                detailed_user_data.append(details)
            progress_bar.update(1)
            time.sleep(2)

# Step 4: Save Detailed Data to JSON and CSV
def save_detailed_data():
    with open(detailed_json_path, "w") as json_file:
        json.dump(detailed_user_data, json_file, indent=4)
    with open(detailed_csv_path, mode="w", newline='') as csv_file:
        fieldnames = ["username", "name", "company", "location", "email", "hireable", "bio", 
                      "public_repos", "followers", "following", "created_at"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for user in detailed_user_data:
            writer.writerow({field: user.get(field, "") for field in fieldnames})
    print(f"Detailed data saved to {detailed_json_path} and {detailed_csv_path}")

# Step 5: Fetch Repository Data for Each User
all_repos = []

def get_repo_data(username):
    try:
        response = requests.get(f"{BASE_URL}/users/{username}/repos", headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error for {username}: {e}")
        return []

def collect_repo_data():
    with open(json_file_path, "r") as file:
        users = json.load(file)
    for user in tqdm(users, desc="Fetching Repository Data"):
        repos = get_repo_data(user["username"])
        for repo in repos:
            all_repos.append({
                "login": repo.get("owner", {}).get("login", "N/A"),
                "full_name": repo.get("full_name", "N/A"),
                "created_at": repo.get("created_at", "N/A"),
                "stargazers_count": repo.get("stargazers_count", 0),
                "watchers_count": repo.get("watchers_count", 0),
                "language": repo.get("language", "N/A"),
                "has_projects": repo.get("has_projects", False),
                "has_wiki": repo.get("has_wiki", False),
                "license_name": repo.get("license", {}).get("key", "N/A") if repo.get("license") else "N/A"
            })
        time.sleep(1)

# Step 6: Save Repository Data to JSON and CSV
def save_repo_data():
    with open(repos_json_path, "w") as json_file:
        json.dump(all_repos, json_file, indent=4)
    pd.DataFrame(all_repos).to_csv(repos_csv_path, index=False)
    print(f"Repository data saved to {repos_json_path} and {repos_csv_path}")

# Run all functions in sequence
collect_user_data()
save_basic_data()
collect_detailed_data()
save_detailed_data()
collect_repo_data()
save_repo_data()
