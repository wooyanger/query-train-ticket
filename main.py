import time
import requests
from prettytable import PrettyTable
from utils import send_email
from utils.exceptions import NoStationName, NoStationCode


class QueryTrainTicket(object):
    """Query train ticket"""
    def __init__(self, s, e, d):
        self.s = s
        self.e = e
        self.d = d
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    def get_station_code(self, sn):
        """Get station code"""
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9090'
        res = requests.get(url=url, headers=self.headers)
        result = res.text[21:-2].split('@')
        for si in result:
            data = si.split('|')
            if sn == data[1]:
                return data[2]
        raise NoStationName('No station name.')

    def get_station_name(self, sc):
        """Get station name"""
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9090'
        res = requests.get(url=url, headers=self.headers)
        result = res.text[21:-2].split('@')
        for si in result:
            data = si.split('|')
            if sc == data[2]:
                return data[1]
        raise NoStationCode('No station code.')

    def query(self, s, e, d):
        """Query train ticket"""
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(d, s, e)
        res = requests.get(url=url, headers=self.headers)
        result = res.json().get('data').get('result')
        train_details = []
        for info in result:
            train_data = info.split('|')
            train_details.append([
                train_data[3],
                self.get_station_name(train_data[6]),
                self.get_station_name(train_data[7]),
                train_data[8],
                train_data[9],
                train_data[10],
                train_data[32],
                train_data[31],
                train_data[30],
                train_data[29],
                train_data[28],
                train_data[23],
                train_data[26]
            ])
        return train_details

    def worker(self):
        try:
            ss = self.get_station_code(self.s)
        except NoStationName:
            exit('未查询到出发车站，请检查出发车站是否正确。')
        try:
            es = self.get_station_code(self.e)
        except NoStationName:
            exit('未查询到到达车站，请检查到达车站是否正确。')
        x = PrettyTable(['车次', '出发车站', '到达车站', '出发时间', '到达时间', '花费时间', '商务座', '一等座', '二等座', '硬座', '硬卧', '软卧', '无座'])
        for i in self.query(ss, es, self.d):
            if i[8] != '无' and i[8] != '':
                send_email('****', '****', '12306余票', '****', '****')
            x.add_row(i)
        print(x)


if __name__ == '__main__':
    q = QueryTrainTicket('北京', '绵阳', '2019-02-03')
    q.worker()
