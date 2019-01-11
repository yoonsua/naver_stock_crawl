import requests
from bs4 import *
import matplotlib.pyplot as p

def make_pList(url, page):
    pList = []

    for i in range(1, page+1):
        wp = requests.get\
             (url+str(i))

        soup = BeautifulSoup(wp.text, 'html.parser')

        trList = soup.find_all('tr', {'onmouseover':"mouseOver(this)"})

        for tr in trList:
            td = tr.find_all('td')[1].get_text()
            td = td.replace(",", "")
            pList.append(int(td))
            
    pList.reverse()
    return pList

def input_company():

    days = int(input("종가 추출 기간을 입력하세요 : "))

    while not days > 0 :
        days = int(input("잘못 입력하셨습니다. 자연수를 입력하세요\n" + \
                         "종가 추출 기간을 입력하세요 : "))

    page = days // 20

    if days > page * 20:
        page = page + 1

    c_index = int(input("1:samsung, 2:lge, 3:hynix, 4:naver, 5:hyun_car\n" + \
                        "회사 번호를 입력하세요 : "))

    while not 0 < c_index < 6 :
        c_index = int(input("잘못 입력하셨습니다. 1 ~ 5 사이의 숫자를 입력하세요\n" +\
                            "1:samsung, 2:lge, 3:hynix, 4:naver, 5:hyun_car\n" + \
                            "회사 번호를 입력하세요 : "))
        

    company = ['005930', '066570', '000660', '035420', '005380']
    url = 'https://finance.naver.com/item/frgn.nhn?code={}&page='.\
          format(company[c_index-1])

    name_list = ['samsung', 'lge', 'hynix', 'naver', 'hyun_car']
    name = name_list[c_index-1]

    return page, url, name
    
    
def make_avg(numMA, pList):
    mList = list();
    Q = list();
    mSum = pList[0] * numMA
    
    for i in range(numMA):
        Q.append(pList[0])

    for price in pList:
        mSum = mSum - Q.pop(0)
        mSum = mSum + price
        mList.append(mSum / numMA)
        Q.append(price)

    return mList

def print_avg(name, pList):

    xAxis = list(range(1, len(pList)+1))

    p.plot(xAxis, pList, 'r', label = name)
    p.plot(xAxis, make_avg(5, pList), 'b', label = '5MA')
    p.plot(xAxis, make_avg(20, pList), 'g', label = '20MA')
    p.plot(xAxis, make_avg(60, pList), 'y', label = '60MA')
    p.xlabel('Day')
    p.ylabel('Last Price')
    p.grid(True)
    p.legend(loc = 'upper right')
    p.show()
