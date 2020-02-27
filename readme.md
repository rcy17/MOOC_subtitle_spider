# 清华慕课字幕爬虫

如题。

## 使用方法

### 环境

- Python3.6及以上
- 执行`pip install -r requirements.txt` (如果不行就试试`pip`改成`pip3`)

### 运行

- 执行`python main.py -t "<url>" -c "<cookie>" -d "<dir>"`
- `url`指进入课程的“课件”页面的url（具体在哪个课件不重要）
- `cookie`指登录成功时访问网页所用的cookie，可以用chrome的network（网络）中的包看到
- `dir`指保存字母的路径，相对路径绝对路径皆可
