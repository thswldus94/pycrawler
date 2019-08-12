import requests
import os
import time
from bs4 import BeautifulSoup
import dbModule
from datetime import datetime


def request_content(url):
	response = requests.get(url)
	if response.status_code == 200:
		html_content = response.text

		index_path = '/home/python/crawler/files/index.html'
		if len(html_content) > 0:
			f = open(index_path, 'a')
			f.write(html_content)
			f.close()
		else:
			print('Fail to create index file')
			return false

		# file exists
		if os.path.isfile(index_path):
			index_f = open(index_path, "r")
			soup = BeautifulSoup(index_f.read(), "html.parser")

			news_rows = parse_content(soup)
			#print(news_rows)
			db_class = dbModule.Mysql()
			sql = """INSERT INTO social_news (title, content, link, date, rdate) VALUES (%s, %s, %s, %s, now())"""

			db_class.cursor.executemany(sql, news_rows)
			db_class.commit()

			return len(news_rows)
		else:
			return false

		os.remove(index_path)


def parse_content(soup):
	news_ul = soup.find(class_="list_allnews")
	news_li = news_ul.find_all("li")

	news = []
	for n in range(len(news_li)):
		news_title = news_li[n].find("div").find(class_="tit_thumb")

		title = news_title.find("a").string
		#print("title  = " + title)
		date = news_title.find(class_="info_time").string
		#print("date = " + date)
		link = news_title.a.attrs['href']
		#print("link = " + link)
		content = news_li[n].find("div").find(class_="desc_thumb").find("span").string.strip()
		#print("content = " + content)

		tmp = [title, content, link, date]
		#print(tmp)
		news.append(tmp)

	return news


def get_page():
	now = datetime.now()
	current_time = '%04d%02d%02d' % ( now.year, now.month, now.day )
	current_page = '1'

	target_url = 'https://media.daum.net/cp/8?cateId=1001&regDate={date}&page={page}'.format(date=current_time, page=current_page)

	response = requests.get(target_url)
	if response.status_code == 200:
		html_content = response.text

		index_path = '/home/python/crawler/files/index.html'
		if len(html_content) > 0:
			f = open(index_path, 'a')
			f.write(html_content)
			f.close()
		else:
			print('Fail to create index file')
			return false

		# file exists
		if os.path.isfile(index_path):
			index_f = open(index_path, "r")
			soup = BeautifulSoup(index_f.read(), "html.parser")

			# get page count
			paging = soup.find(class_="paging_news")
			paging_element = paging.find_all("a")
			final_page = int(paging_element[len(paging_element) - 1].string)
			print(final_page)

			# crawling pages
			total_count = 0
			for r in range(0, final_page):
				p_url = 'https://media.daum.net/cp/8?cateId=1001&regDate={date}&page={page}'.format(date=current_time, page=r+1)
				print(p_url)
				cur_count = request_content(p_url)
				if cur_count == False: 
					cur_count = 0
				total_count = total_count + cur_count

			insertStatNews(total_count)



def insertStatNews(count):
	db_class = dbModule.Mysql()
	sql = """INSERT INTO stat_news (rdate, count) VALUES (now(), %s)"""

	db_class.cursor.execute(sql, (count))
	db_class.commit()



get_page()
