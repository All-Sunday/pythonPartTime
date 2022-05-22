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
        ['PLAYER', 'TEAM', 'AGE', 'GP', 'W', 'L', 'MIN', 'PTS', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA',
         'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PF', 'FP', 'DD2', 'TD3', '+/-'])

    return wk, ws


def query_details(ws):
    api_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2021-22&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
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
        res = [res[1], res[4]] + list(map(int, res[5:9])) + list(
            map(float, [res[10], res[30], res[11], res[12]])) + ['%.1f' % (res[13] * 100)] + list(
            map(float, res[14:16])) + ['%.1f' % (res[16] * 100)] + list(
            map(float, res[17:19])) + ['%.1f' % (res[19] * 100)] + list(
            map(float, res[20:27] + [res[28], res[32]])) + res[33:35] + [res[31]]

        ws.append(res)

    return True, ws


if __name__ == '__main__':
    wk, ws = init()
    query_details(ws)
    wk.save('res.xlsx')
