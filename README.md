# FanfanTenders_Robot
番番寻标宝招标数据爬虫(自用).

## 使用说明
```zsh
usage: fanfan_robot.py [-h] [-r] [-a] [-s]

番番寻标宝招标数据爬取

optional arguments:
  -h, --help          show this help message and exit
  -r, --run           爬取最新数据到all_data.json文件
  -a, --analys        从all_data.json解析数据到all_detail.json
  -s, --show-tenders  展示所有投标详细信息
```

### 爬取最新数据
`python3 fanfan_robot.py -r/--run`

默认爬取三个月内数据，默认保存在当前目录的all_data.json文件中。

### 解析详细招标数据
`python3 fanfan_robot.py -a/--analys`

默认保存在当前目录的all_detail.json文件中。

### 展示所有招标详细信息

`python3 fanfan_robot.py -s/--show-tenders`

展示所有的招标详细信息，默认不保存到文件。