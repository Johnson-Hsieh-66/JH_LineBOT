import requests
from bs4 import BeautifulSoup


class StockInfo:
    def __init__(self):
        self.name = ''
        self.date = ''
        self.price = ''
        self.change = ''
        self.changePercent = ''
        self.share = ''
        self.infoString = ''

    def getStockInfo(self, strStock):
        rs = requests.session()
        url = 'https://goodinfo.tw/tw/StockDetail.asp?STOCK_ID=' + strStock
        headers = headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = rs.get(url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        stock = soup.find(class_='b1 p4_2 r10 box_shadow')
        if stock is not None:
            self.name = stock.find_all('nobr')[0].a.contents[0]
            self.date = stock.find_all('nobr')[4].contents[0]
            self.price = stock.find_all('tr')[3].td.contents[0]
            self.change = stock.find_all('tr')[3].find_all('td')[2].contents[0]
            self.changePercent = stock.find_all('tr')[3].find_all('td')[3].contents[0]
            self.share = stock.find_all('nobr')[21].contents[0]


        return self

    def getInfoString(self):
        return self.name+'_'+self.date+' 成交價:'+self.price+' 漲跌:'+self.change+' '+self.changePercent+' 成交金額:'+self.share

