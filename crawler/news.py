import requests
import os
import time
from bs4 import BeautifulSoup
import dbModule
from datetime import datetime

now = datetime.now()
current_time = '%04d%02d%02d' % ( now.year, now.month, now.day )
target_url = 'https://media.daum.net/cp/8?cateId=1001&regDate=' + current_time
print(target_url)


def request_content(url):
	response = requests.get(url)
	if response.status_code == 200:
		html_content = response.text

		index_path = os.getcwd() + '/files/index.html'
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
			print(news_rows)
			db_class = dbModule.Mysql()
			sql = """INSERT INTO social_news (title, content, date, rdate) VALUES (%s, %s, %s, now())"""

			db_class.cursor.executemany(sql, news_rows)
			db_class.commit()
		else:
			return false


def parse_content(soup):
	parsed_news = soup.find_all(class_="list_allnews")
	#print(parsed_news)

	news_list = []
	for n in range(len(parsed_news)):
		news = parsed_news[n].find("li").find("div").find(class_="tit_thumb")
		#print(news)
		title = news.find("a").string
		date = news.find(class_="info_time").string
		#print(title)
		#print(date)
		# desc = all_item[n].find("description").string

		content = parsed_news[n].find("li").find(class_="desc_thumb").find("span").string
		print(content)
		tmp = [title, content, date]
		
		news_list.append(tmp)


	return news_list




request_content(target_url)
