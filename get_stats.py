import requests
from bs4 import BeautifulSoup
import json
import time

def get_scholar_stats(user_id):
    """从Google Scholar获取引用统计数据"""
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 添加重试机制
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                break
            print(f"尝试 {attempt+1} 失败，HTTP状态码: {response.status_code}")
            time.sleep(2)  # 等待2秒后重试
        except Exception as e:
            print(f"尝试 {attempt+1} 出现异常: {e}")
            time.sleep(2)  # 等待2秒后重试
    
    if response.status_code != 200:
        print(f"无法获取数据，HTTP状态码: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        # 找到引用统计表格
        stats_table = soup.select_one('table#gsc_rsb_st')
        if not stats_table:
            print("未找到统计表格")
            return None
        
        # 提取各项指标数据
        rows = stats_table.select('tr.gsc_rsb_std')
        if not rows or len(rows) < 3:
            print("未找到足够的统计行")
            return None
        
        citations = rows[0].select_one('td.gsc_rsb_std').text
        h_index = rows[1].select_one('td.gsc_rsb_std').text
        i10_index = rows[2].select_one('td.gsc_rsb_std').text
        
        # 尝试获取作者姓名
        name_elem = soup.select_one('#gsc_prf_in')
        name = name_elem.text if name_elem else "Scholar"
        
        return {
            'name': name,
            'citations': citations,
            'h_index': h_index,
            'i10_index': i10_index
        }
    except Exception as e:
        print(f"解析数据时出错: {e}")
        return None

def create_badge_file(label, message, color, style, filename):
    """创建徽章数据文件"""
    data = {
        "schemaVersion": 1,
        "label": label,
        "message": message,
        "color": color,
        "style": style
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"已创建徽章文件: {filename}")

# 主函数
def main():
    # 替换为你的Google Scholar ID
    scholar_id = "yggQMJMAAAAJ"
    badge_style = "flat-square"
    badge_color = "1f1f18"
    
    print("开始获取Google Scholar数据...")
    stats = get_scholar_stats(scholar_id)
    
    if stats:
        print(f"成功获取数据: 引用: {stats['citations']}, h-index: {stats['h_index']}, i10-index: {stats['i10_index']}")
        
        # 创建徽章文件
        create_badge_file("citations", stats['citations'], badge_color, badge_style, "badge-citations.json")
        create_badge_file("h-index", stats['h_index'], badge_color, badge_style, "badge-hindex.json")
        create_badge_file("i10-index", stats['i10_index'], badge_color, badge_style, "badge-i10index.json")
        
        print("所有徽章文件已成功创建")
    else:
        print("无法获取Scholar数据，创建占位徽章")
        create_badge_file("citations", "N/A", "gray", badge_style, "badge-citations.json")
        create_badge_file("h-index", "N/A", "gray", badge_style, "badge-hindex.json")
        create_badge_file("i10-index", "N/A", "gray", badge_style, "badge-i10index.json")

if __name__ == "__main__":
    main()