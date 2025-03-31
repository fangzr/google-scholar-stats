import json
import jsonpickle

# 从最新生成的JSON文件中读取数据
# 假设文件名为"zhengrufang.json"，请替换为实际生成的文件名
try:
    with open('zhengrufang.json', 'r') as file:
        data_str = json.load(file)
        data = jsonpickle.decode(data_str)
        
    # 创建徽章所需的简单JSON格式
    badge_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(data['citedby']),
        "color": "blue"
    }
    
    # 创建h-index徽章数据
    hindex_data = {
        "schemaVersion": 1,
        "label": "h-index",
        "message": str(data['hindex']),
        "color": "green"
    }
    
    # 创建i10-index徽章数据
    i10index_data = {
        "schemaVersion": 1,
        "label": "i10-index",
        "message": str(data['i10index']),
        "color": "orange"
    }
    
    # 保存徽章数据
    with open('badge-citations.json', 'w') as outfile:
        json.dump(badge_data, outfile)
        
    with open('badge-hindex.json', 'w') as outfile:
        json.dump(hindex_data, outfile)
        
    with open('badge-i10index.json', 'w') as outfile:
        json.dump(i10index_data, outfile)
        
    print("Badge data files created successfully")
    
except Exception as e:
    print(f"Error creating badge data: {e}")