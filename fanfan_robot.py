import argparse
import json
import os
import concurrent.futures

import requests

# 用于获取数据的完整请求头
headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "sec-ch-ua": 'Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123',
    "Cache-Control": "no-cache",
    "Auth-Type": "PAAS",
    "sec-ch-ua-mobile": "?1",
    "Env": "WEB",
    "Client-Version": "0",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "content-type": "application/json;charset=UTF-8",
    "X-Sourceid": "f790b1138142c666731aae015daa292b",
    "X-Timestamp": "1712652720",
    "X-Requested-With": "XMLHttpRequest",
    "Api-Version": "0",
    "User-Info": "uc_id=;uc_appid=585;acc_token=10737291d9cf19fe62d918b8925bf7145f68f84cb31ec7822ca806e851f13960;acc_id=336216333;login_id=336216333:0;device_type=bid-h5;paas_appid=16;version=12;login_type=passport",
    "sec-ch-ua-platform": '"Android"',
    "Cookie": 'BIDUPSID=AA644029E70509BE2C769E5FECA0CEF1; PSTM=1713449207; BAIDUID=AA644029E70509BE2C769E5FECA0CEF1:SL=0:NR=10:FG=1; H_WISE_SIDS=40445_40080_60189; H_PS_PSSID=40445_40080_60189; BDUSS=mRJWG9DYTRLQVp4OEs1MH5oWWhXc3ZyWGRhYUNpenNUN3VhNmg4U2FvMX5BRk5tSVFBQUFBJCQAAAAAAAAAAAEAAACcu62dtM3X09PoioVpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH9zK2Z~cytmY; BDUSS_BFESS=mRJWG9DYTRLQVp4OEs1MH5oWWhXc3ZyWGRhYUNpenNUN3VhNmg4U2FvMX5BRk5tSVFBQUFBJCQAAAAAAAAAAAEAAACcu62dtM3X09PoioVpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH9zK2Z~cytmY; H_WISE_SIDS_BFESS=40445_40080_60189; BA_HECTOR=ag8g25ak200ha12h240la5ak09ksms1j33r1t1s; delPer=0; PSINO=1; ZFY=Sdw6wLfiSANI1ZJfTjlpzvVNc5:AFkbDpEUDun89JdO0:C; BAIDUID_BFESS=AA644029E70509BE2C769E5FECA0CEF1:SL=0:NR=10:FG=1; sajssdk_2015_cross_new_user=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218f3350d0a319fb-08675022d5ee29-26001d51-2073600-18f3350d0a41e76%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmMzM1MGQwYTMxOWZiLTA4Njc1MDIyZDVlZTI5LTI2MDAxZDUxLTIwNzM2MDAtMThmMzM1MGQwYTQxZTc2In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218f3350d0a319fb-08675022d5ee29-26001d51-2073600-18f3350d0a41e76%22%7D; __bid_n=18f222d87638592e9e5bb8; Hm_lvt_8cfca2ee1c078aaed86e031c3eb09486=1712667822,1713923162,1714265361,1714559058; Hm_lpvt_8cfca2ee1c078aaed86e031c3eb09486=1714559058; ab_sr=1.0.1_NjYxNjFjMmNjNDZjMjUxZmQwOThlODIyMzAwNmE1OTFiYzQ4MTcwNjEyMmViMzFmNzc3ZmE5YjBhZmUxMTMzMDg2MDgzMjY4YTFjMzMzYmYzNGNkMTNjN2ZmYjlmYjRjZmE4NmY0YjJiNzgwZTAxMjFmNmEyZDJjNzQwZTc0ZmVlN2Y2NDZmMGE0OThlOWFlMzEzZDRlZjNjM2E4MmFmMQ==; RT="z=1&dm=baidu.com&si=adb05693-71d1-4267-95b0-efb344d3cf1a&ss=lvno1hri&sl=2&tt=5h5&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"'
}

# 用于获取四川招标总数量的请求包
count_data = '{"query":{"entName":"网络安全","enterpriseId":"","keyword":"网络安全","noticeTypes":[],"informationTypes":["招标"],"areaQuery":{"dicts":[{"code":"510000","children":[]}]},"startTime":"2024-01-09 00:00:00","endTime":"2024-04-09 23:59:59","matchType":"term","tenderPrincipalTypeCodes":[],"matchFields":["title"],"sortType":"desc","biddingAcquireTimeItem":"","tenderTimeItem":"","openBidingTimeItem":"","fromBudget":"","toBudget":"","contactFilterType":"","agencyPrincipalFilterType":"","attachmentFilterType":"","winnerFilterType":"","tenderItemIndustries":["1113:1","1113:2","1113:3","1113:4","1113:5","1113:6","1113:7","1113:8","1113:9","1113:10","1113:11","1113:12","1113:13","1113:14","1113:15","1113:16","1113:17","1113:18","1113:19","1113:20","1113:21","1113:22","1113:23","1113:0"],"tenderItemCategories":["1110:1","1110:2","1110:3","1110:4"],"pageNum":1,"pageSize":100,"platform":"h5"}}'

# 用于获取四川招标详细信息的请求包
content_data = {
    "query": {
        "entName": "网络安全",
        "enterpriseId": "",
        "keyword": "网络安全",
        "noticeTypes": [],
        "informationTypes": [
            "招标"
        ],
        "areaQuery": {
            "dicts": [
                {
                    "code": "510000",
                    "children": []
                }
            ]
        },
        "startTime": "2024-01-09 00:00:00",
        "endTime": "2024-04-09 23:59:59",
        "matchType": "term",
        "tenderPrincipalTypeCodes": [],
        "matchFields": [
            "title"
        ],
        "sortType": "desc",
        "biddingAcquireTimeItem": "",
        "tenderTimeItem": "",
        "openBidingTimeItem": "",
        "fromBudget": "",
        "toBudget": "",
        "contactFilterType": "",
        "agencyPrincipalFilterType": "",
        "attachmentFilterType": "",
        "winnerFilterType": "",
        "tenderItemIndustries": [
            "1113:1",
            "1113:2",
            "1113:3",
            "1113:4",
            "1113:5",
            "1113:6",
            "1113:7",
            "1113:8",
            "1113:9",
            "1113:10",
            "1113:11",
            "1113:12",
            "1113:13",
            "1113:14",
            "1113:15",
            "1113:16",
            "1113:17",
            "1113:18",
            "1113:19",
            "1113:20",
            "1113:21",
            "1113:22",
            "1113:23",
            "1113:0"
        ],
        "tenderItemCategories": [
            "1110:1",
            "1110:2",
            "1110:3",
            "1110:4"
        ],
        "pageNum": 1,
        "pageSize": 100,
        "platform": "h5"
    }
}


def run():
    """
    爬取最新数据
    :return:
    """
    count_response = requests.post("https://xunbiaobao.baidu.com/crm/web/bid/xbb/na/bidding/search/api/search/count",
                                  headers=headers, data=count_data.encode('utf-8'))
    count_dict = json.loads(count_response.text)
    count_value = count_dict['data']
    print("四川全地区网络安全相关今日招标总数：" + str(count_value))

    all_data = []
    # 按照目标需求的格式化处理json, 否则会报错
    formatted_content_data = str(content_data).replace("'", "\"").replace(", ", ",").replace(": ", ":")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(1, int(count_value) // 100 + 2):
            try:
                print("当前请求第{}页".format(i))
                future = executor.submit(requests.post, "https://xunbiaobao.baidu.com/crm/web/bid/xbb/bidding/search/api/search",
                                         headers=headers,
                                         data=formatted_content_data.replace('"pageNum":1',
                                                                             '"pageNum":{}'.format(i)).encode('utf-8'))
                futures.append(future)
            except:
                print("第{}页请求失败,请求重试,若再次失败则跳过".format(i))
                future = executor.submit(requests.post, "https://xunbiaobao.baidu.com/crm/web/bid/xbb/bidding/search/api/search",
                                         headers=headers,
                                         data=formatted_content_data.replace('"pageNum":1',
                                                                             '"pageNum":{}'.format(i)).encode('utf-8'))
                futures.append(future)
                continue

        for future in concurrent.futures.as_completed(futures):
            all_data.append(future.result().json())

    # 将数据输出到JSON文件
    with open('all_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)


def analys():
    """
    从爬取的数据文件中解析所有的详细招标数据
    :return:
    """
    all_detail = []

    with open('all_data.json', 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    page_num = 1
    for page in all_data:
        print(f"正在整理第{page_num}页")
        page_num += 1
        for data in page['data']['dataList']:
            all_detail.append(data)

    with open('all_detail.json', 'w', encoding='utf-8') as f:
        json.dump(all_detail, f, indent=4, ensure_ascii=False)


def show_tenders():
    with open("all_detail.json", "r", encoding='utf-8') as f:
        tenders_data = json.load(f)
    print_centered("====")
    for tenders in tenders_data:
        if tenders['projectNo'] is None:
            tenders['projectNo'] = "暂无信息"
        if tenders['budget'] is None:
            tenders['budget'] = "暂无预算信息"
        if tenders['winnerAmount'] is None:
            tenders['winnerAmount'] = "暂无中标信息"
        print("id: " + tenders['id'])
        print("title: " + tenders['title'].replace("<em>", "").replace("</em>", ""))
        print("项目编号: " + tenders['projectNo'])
        print("预算: " + str(tenders['budget']))
        print("中标: " + str(tenders['winnerAmount']))
        print_centered("====")


def print_centered(text):
    """
    打印分割线
    @param text: 居中文字
    @return:
    """
    terminal_width = os.get_terminal_size().columns
    text_width = len(text)
    left_padding = (terminal_width - text_width - 4) // 2  # 10是因为"----------"占用了10个字符
    print('=' * left_padding + text + '=' * left_padding)


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="番番寻标宝招标数据爬取", formatter_class=argparse.RawTextHelpFormatter)
    parse.add_argument("-r", "--run", action="store_true", help="爬取最新数据到all_data.json文件")
    parse.add_argument("-a", "--analys", action="store_true", help="从all_data.json解析数据到all_detail.json")
    parse.add_argument("-s", "--show-tenders", action="store_true", help="展示所有投标详细信息")

    args = parse.parse_args()

    if args.run is True:
        run()

    if args.analys is True:
        analys()

    if args.show_tenders is True:
        show_tenders()
