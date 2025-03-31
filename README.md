# Google Scholar Statistics

[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-%2320beff?color=1f1f18&logo=google-scholar&style=flat-square)](https://scholar.google.com/citations?hl=en&user=yggQMJMAAAAJ)
[![Citations](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/fangzr/google-scholar-stats/main/badge-citations.json&style=flat-square)](https://scholar.google.com/citations?hl=en&user=yggQMJMAAAAJ)
[![H-index](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/fangzr/google-scholar-stats/main/badge-i10index.json&style=flat-square)](https://scholar.google.com/citations?hl=en&user=yggQMJMAAAAJ)

这个仓库使用GitHub Actions自动从Google Scholar获取引用统计数据，每天更新一次。

## 使用方法

1. Fork这个仓库
2. 修改`get_stats.py`中的Google Scholar ID
3. 确保GitHub Actions有写权限（在仓库设置中）
4. 更新README.md中的徽章URL，将`fangzr`替换为你的GitHub用户名

## 技术细节

- 使用Python的requests和BeautifulSoup库直接从Google Scholar页面获取数据
- 通过GitHub Actions每天自动更新统计数据
- 使用shields.io显示实时统计徽章

## 自定义

如果你想自定义徽章样式，可以修改`get_stats.py`中的以下参数：
- `badge_style`：徽章样式（如`flat`、`flat-square`、`for-the-badge`等）
- `badge_color`：徽章颜色（十六进制颜色代码）
