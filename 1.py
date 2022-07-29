import requests
import xlwt
import os.path
import threading
import re
import bs4
from bs4 import BeautifulSoup
import time

def get_content(url):#发请求，返回网页源码
    headers={'User Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'}
    try:
        response=requests.get(url,headers)
        if response.status_code==200:
                return response.text
    except requests.RequestException as e:
        print(e)
        return None

car_data = xlwt.Workbook(encoding='utf-8',style_compression=0)
sheet = car_data.add_sheet('Publication',cell_overwrite_ok=True)
sheet.write(0,0,'主题')
sheet.write(0,1,'作者')
sheet.write(0,2,'期刊')
sheet.write(0,3,'年份')
sheet.write(0,4,'页码')
sheet.write(0,5, 'DOI')
sheet.write(0,6, '链接')
n = 1
def get_data(response):
    soup=BeautifulSoup(response,'lxml')
    print(soup)
    all_data=soup.select('td',class_="column-2")
    print(all_data)
    if isinstance(all_data, bs4.element.ResultSet):
        for i in all_data:
            year = i.select('strong')
            print(year)
            journal = i.find('span')
            title = i.find('a')
            DOI = i.find('a').find('span')
            link = i.a['href']
            author = i.find('span').text
            page = i.find('span').text
        print(title,author,journal,year,page,DOI,link)
        save_csv(title,author,journal,year,page,DOI,link)
def save_csv(title,author,journal,year,page,DOI,link):
    global n
    sheet.write(n,0,str(title))
    sheet.write(n,1,str(author))
    sheet.write(n,2,str(journal))
    sheet.write(n,3,str(year))
    sheet.write(n,4,str(page))
    sheet.write(n,5,str(DOI))
    sheet.write(n,6,str(link))
    n=n+1
    print('开始爬取保存csv===>>')
    car_data.save(u'Publication.xlsx')
def main():
    baseurl="https://bren.xmu.edu.cn/Publications1/Publications/a2022.htm"
    for i in range(0,20):
        if i<19:
            year=2022-i
            url=baseurl.replace("2022",str(year))
        else:
            url="https://bren.xmu.edu.cn/Publications1/Publications/a2003_.htm"
        response=get_content(url)
        get_data(response)
if __name__ == '__main__':
    thred = threading.Thread(target=main)
    thred.start()