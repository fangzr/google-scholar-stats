import requests
from bs4 import BeautifulSoup
import time
import random

def get_scholar_stats(user_id):
    """从Google Scholar获取引用统计数据"""
    url = f"https://scholar.google.com/citations?user={user_id}&hl=en"
    
    # 使用较常见的User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    print(f"开始请求 URL: {url}")
    
    try:
        # 添加短暂延迟，模拟人类行为
        time.sleep(1 + random.random())
        
        # 发送请求
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"请求状态码: {response.status_code}")
        
        if response.status_code != 200:
            print("请求失败")
            return None
        
        # 保存HTML用于检查（可选）
        with open("scholar_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("已保存HTML响应到 scholar_response.html")
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 方法一：通过标准选择器
        print("\n尝试方法一：标准CSS选择器")
        try:
            stats_table = soup.select_one('table#gsc_rsb_st')
            if stats_table:
                print("找到统计表格")
                rows = stats_table.select('tr.gsc_rsb_std')
                if rows and len(rows) >= 3:
                    citations = rows[0].select_one('td.gsc_rsb_std').text
                    h_index = rows[1].select_one('td.gsc_rsb_std').text
                    i10_index = rows[2].select_one('td.gsc_rsb_std').text
                    print(f"方法一成功: 引用: {citations}, h-index: {h_index}, i10-index: {i10_index}")
                    return {
                        'citations': citations,
                        'h_index': h_index,
                        'i10_index': i10_index
                    }
                else:
                    print("找到表格但未找到足够的行数据")
            else:
                print("未找到统计表格")
        except Exception as e:
            print(f"方法一出错: {e}")
        
        # 方法二：查找引用数字元素
        print("\n尝试方法二：查找特定元素")
        try:
            td_elements = soup.find_all('td', class_='gsc_rsb_std')
            if td_elements and len(td_elements) >= 3:
                citations = td_elements[0].text
                h_index = td_elements[1].text
                i10_index = td_elements[2].text
                print(f"方法二成功: 引用: {citations}, h-index: {h_index}, i10-index: {i10_index}")
                return {
                    'citations': citations,
                    'h_index': h_index,
                    'i10_index': i10_index
                }
            else:
                print(f"未找到足够的td元素，找到了 {len(td_elements) if td_elements else 0} 个")
        except Exception as e:
            print(f"方法二出错: {e}")
        
        # 方法三：基于文本搜索
        print("\n尝试方法三：基于文本模式")
        try:
            # 打印页面的基本内容以便检查
            page_text = soup.get_text()
            print(f"页面文本前200字符: {page_text[:200]}...")
            
            # 查找是否包含关键词
            if "Citations" in page_text and "h-index" in page_text:
                print("页面包含关键词 'Citations' 和 'h-index'")
            else:
                print("页面不包含预期关键词")
                
            # 查找所有数字文本
            import re
            numbers = re.findall(r'\d+', page_text)
            print(f"页面中找到的数字: {numbers[:10]}...")
        except Exception as e:
            print(f"方法三出错: {e}")
            
        print("\n所有方法均无法获取数据")
        return None
            
    except Exception as e:
        print(f"请求过程中发生错误: {e}")
        return None

# 测试函数
def test():
    # 替换为你的Google Scholar ID
    scholar_id = "yggQMJMAAAAJ"  # 这里替换为你要测试的ID
    
    print(f"开始测试Google Scholar ID: {scholar_id}")
    stats = get_scholar_stats(scholar_id)
    
    if stats:
        print("\n成功获取数据:")
        print(f"引用数: {stats['citations']}")
        print(f"h-index: {stats['h_index']}")
        print(f"i10-index: {stats['i10_index']}")
    else:
        print("\n无法获取数据")

if __name__ == "__main__":
    test()