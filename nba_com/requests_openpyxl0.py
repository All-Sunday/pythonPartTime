# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/22 21:13
# @File : requests_pandas.py
import json

import openpyxl
import requests


def init():
    wk = openpyxl.Workbook()
    ws = wk.active
    ws.append(
        ['Player', 'TEAM', 'AGE', 'HEIGHT', 'WEIGHT', 'COLLEGE', 'COUNTRY', 'DRAFT YEAR', 'DRAFT ROUND', 'DRAFT NUMBER',
         'GP', 'PTS', 'REB', 'AST', 'NETRTG', 'OREB%', 'DREB%', 'USG%', 'TS%', 'AST%'])

    return wk, ws


def query_details(ws):
    api_url = 'https://stats.nba.com/stats/leaguedashplayerbiostats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
    headers = {
        'Host': 'stats.nba.com',
        'Connection': 'keep-alive',
        'x-nba-stats-token': 'true',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
        'x-nba-stats-origin': 'stats',
        'Origin': 'https://www.nba.com',
        'Referer': 'https://www.nba.com/'
    }

    try:
        res_json = json.loads(requests.get(api_url, headers=headers).text)
    except:
        return False, '超时'

    res_list = res_json['resultSets'][0]['rowSet']
    for res in res_list:
        res = [res[1], res[3], int(res[4]), res[5], int(res[7])] + res[8:13] + [int(res[14])] + list(
            map(float, res[14:18])) + list(map(lambda x: '%.1f' % (x * 100) + '%', res[18:]))

        ws.append(res)

    return True, ws


if __name__ == '__main__':
    wk, ws = init()
    query_details(ws)
    wk.save('res.xlsx')
