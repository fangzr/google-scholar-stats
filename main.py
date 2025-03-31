import requests
from bs4 import BeautifulSoup
import json

def get_scholar_stats(user_id):
    url = f"https://scholar.google.com/citations?user={user_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取引用数
    try:
        citations = soup.select_one('#gsc_rsb_st tr:nth-child(1) td:nth-child(2)').text
        h_index = soup.select_one('#gsc_rsb_st tr:nth-child(2) td:nth-child(2)').text
        i10_index = soup.select_one('#gsc_rsb_st tr:nth-child(3) td:nth-child(2)').text
        
        return {
            'citations': citations,
            'h_index': h_index,
            'i10_index': i10_index
        }
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

def create_badge_file(label, message, color, filename):
    data = {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)

# 替换为你的Google Scholar ID
scholar_id = "yggQMJMAAAAJ"
stats = get_scholar_stats(scholar_id)

if stats:
    create_badge_file("citations", stats['citations'], "blue", "badge-citations.json")
    create_badge_file("h-index", stats['h_index'], "green", "badge-hindex.json")
    create_badge_file("i10-index", stats['i10_index'], "orange", "badge-i10index.json")
    print("Badge files created successfully.")
else:
    print("Could not retrieve Scholar stats. Creating placeholder badges.")
    create_badge_file("citations", "N/A", "gray", "badge-citations.json")
    create_badge_file("h-index", "N/A", "gray", "badge-hindex.json")
    create_badge_file("i10-index", "N/A", "gray", "badge-i10index.json")