# Google Scholar Statistics

[![Citations](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/fangzr/google-scholar-stats/main/badge-citations.json)](https://scholar.google.com/citations?hl=en&user=yggQMJMAAAAJ)
[![h-index](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/fangzr/google-scholar-stats/main/badge-hindex.json)](https://scholar.google.com/citations?hl=en&user=yggQMJMAAAAJ)
[![i10-index](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/fangzr/google-scholar-stats/main/badge-i10index.json)](https://scholar.google.com/citations?hl=en&user=yggQMJMAAAAJ)

这个仓库使用GitHub Actions自动从Google Scholar获取引用统计数据，每天更新一次。

## 使用方法

1. Fork这个仓库
2. 修改`main.py`中的Google Scholar ID
3. 在`badge-data.py`和README.md中更新文件名和GitHub用户名
4. 启用GitHub Actions

## 技术细节

- 使用`scholarly` Python库抓取Google Scholar数据
- 通过GitHub Actions每天自动更新数据
- 使用shields.io显示实时统计徽章

## 也可以使用JavaScript动态更新网页

```javascript
$.getJSON('https://raw.githubusercontent.com/fangzr/google-scholar-stats/main/zhnegrufang.json', function(data) {
    data = JSON.parse(data)
    var text = `Citations: <strong>${data.citedby}</strong> | h-index: <strong>${data.hindex}</strong> | i10-index: <strong>${data.i10index}</strong>`

    document.getElementById('total_cit').innerHTML = text; 
});
```

记得将链接中的`fangzr`替换为你的GitHub用户名，`Author_Name.json`替换为实际生成的JSON文件名。