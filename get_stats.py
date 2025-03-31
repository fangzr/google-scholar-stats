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

def create_styled_badge(citations, filename):
    """创建类似示例样式的徽章JSON"""
    data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(citations),
        "color": "9cf",
        "labelColor": "f6f6f6",
        "style": "flat",
        "logo": "Google Scholar"
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"已创建徽章文件: {filename}")

def main():
    # 替换为你的Google Scholar ID
    scholar_id = "yggQMJMAAAAJ"
    
    print("开始获取Google Scholar数据...")
    stats = get_scholar_stats(scholar_id)
    
    if stats:
        print(f"成功获取数据: 引用: {stats['citations']}, h-index: {stats['h_index']}, i10-index: {stats['i10_index']}")
        
        # 创建样式化的徽章
        create_styled_badge(stats['citations'], "gs_data_shieldsio.json")
        
        print("徽章文件已成功创建")
        return True
    else:
        print("无法获取Scholar数据，创建占位徽章")
        create_styled_badge("N/A", "gs_data_shieldsio.json")
        return False

if __name__ == "__main__":
    main()