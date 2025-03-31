import requests
from bs4 import BeautifulSoup
import json
import time
import random

def get_scholar_stats(user_id):
    """从Google Scholar获取引用统计数据"""
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    print(f"开始请求 URL: {url}")
    
    # 添加重试机制
    for attempt in range(3):
        try:
            # 添加随机延迟
            time.sleep(1 + random.random() * 2)
            
            response = requests.get(url, headers=headers, timeout=30)
            print(f"尝试 {attempt+1} 状态码: {response.status_code}")
            
            if response.status_code == 200:
                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 使用方法二：查找引用数字元素
                td_elements = soup.find_all('td', class_='gsc_rsb_std')
                if td_elements and len(td_elements) >= 3:
                    citations = td_elements[0].text
                    h_index = td_elements[1].text
                    i10_index = td_elements[2].text
                    print(f"获取成功: 引用: {citations}, h-index: {h_index}, i10-index: {i10_index}")
                    return {
                        'citations': citations,
                        'h_index': h_index,
                        'i10_index': i10_index
                    }
                else:
                    print(f"未找到足够的td元素，找到了 {len(td_elements) if td_elements else 0} 个")
            
            print(f"尝试 {attempt+1} 失败，将重试...")
            time.sleep(2)  # 等待一段时间后重试
        except Exception as e:
            print(f"尝试 {attempt+1} 出现异常: {e}")
            time.sleep(2)  # 等待一段时间后重试
    
    print("所有尝试均失败，无法获取数据")
    return None

def create_badge_file(label, message, color, style, filename):
    """创建普通徽章数据文件"""
    data = {
        "schemaVersion": 1,
        "label": label,
        "message": str(message),
        "color": color,
        "style": style
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"已创建徽章文件: {filename}")

def create_combined_badge(citations, filename):
    """创建带有Google Scholar logo的组合徽章"""
    data = {
        "schemaVersion": 1,
        "label": "Google Scholar",
        "message": f"Citations: {citations}",
        "color": "1f1f18",
        "style": "flat-square",
        "logoSvg": "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48cGF0aCBmaWxsPSIjNDI4NUY0IiBkPSJNMjU2IDQxMS4xMkwwIDIwMi42NjcgMjU2IDBoMjU2djIwMi42NjdsLTI1NiAyMDguNDUzeiIvPjxwYXRoIGZpbGw9IiNGRkZGRkYiIGQ9Ik0yNTYgNDExLjEyTDI1NiAzMTEuNjk0IDE3OC42NTcgMjU2IDE0Ni4wODcgMjU2bDEwOS45MTMgMTU1LjEyeiIvPjxjaXJjbGUgZmlsbD0iI0ZGRkZGRiIgY3g9IjIwMS4wNDMiIGN5PSIxODUuNzgyIiByPSI0MS4zOTEiLz48cGF0aCBmaWxsPSIjRkZGRkZGIiBkPSJNMzc3LjM5NiAxODIuODA5aC00Mi40MzV2NDIuNGgtMjEuMnYtNDIuNGgtNDIuMzk2di0yMS4yaDQyLjM5NnYtNDIuNGgyMS4ydjQyLjRoNDIuNDM1djIxLjJ6Ii8+PC9zdmc+"
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"已创建组合徽章文件: {filename}")

def main():
    # 替换为你的Google Scholar ID
    scholar_id = "yggQMJMAAAAJ"
    badge_style = "flat-square"
    badge_color = "1f1f18"
    
    print("开始获取Google Scholar数据...")
    stats = get_scholar_stats(scholar_id)
    
    if stats:
        print(f"成功获取数据: 引用: {stats['citations']}, h-index: {stats['h_index']}, i10-index: {stats['i10_index']}")
        
        # 创建组合徽章文件
        create_combined_badge(stats['citations'], "badge-scholar-citations.json")
        
        # 创建普通徽章文件
        create_badge_file("citations", stats['citations'], badge_color, badge_style, "badge-citations.json")
        create_badge_file("h-index", stats['h_index'], badge_color, badge_style, "badge-hindex.json")
        create_badge_file("i10-index", stats['i10_index'], badge_color, badge_style, "badge-i10index.json")
        
        print("所有徽章文件已成功创建")
        return True
    else:
        print("无法获取Scholar数据，创建占位徽章")
        create_combined_badge("N/A", "badge-scholar-citations.json")
        create_badge_file("citations", "N/A", "gray", badge_style, "badge-citations.json")
        create_badge_file("h-index", "N/A", "gray", badge_style, "badge-hindex.json")
        create_badge_file("i10-index", "N/A", "gray", badge_style, "badge-i10index.json")
        return False

if __name__ == "__main__":
    main()