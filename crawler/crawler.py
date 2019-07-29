import requests
import os
import time
from bs4 import BeautifulSoup
import dbModule

target_url = 'http://malc0de.com/rss/'



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

			malware_rows = parse_content(soup)

			db_class = dbModule.Mysql()
			sql = """INSERT INTO MALWARE_INFO (title, URL, IPAddress, Country, ASN, MD5, rdate, udate) VALUES (%s, %s, %s, %s, %s, %s, now(), now())
						ON DUPLICATE KEY UPDATE title = VALUES(title), URL = VALUES(URL), IPAddress = VALUES(IPAddress), Country = VALUES(Country), ASN = VALUES(ASN), udate = now()"""

			db_class.cursor.executemany(sql, malware_rows)
			db_class.commit()
		else:
			return false


def parse_content(soup):
	all_item = soup.find_all("item")

	malware_list = []
	for n in range(len(all_item)):
		title = all_item[n].find("title")
		desc = all_item[n].find("description").string

		if len(desc) > 0:
			desc_parse = desc.replace(" ", "").split(",")

			tmp = [title.string]

			detail_list = list(map(parse_description, desc_parse))
			for detail in detail_list:
				tmp.append(detail[1])

			malware_list.append(tmp)
		else:
			return false

	return malware_list


def parse_description(desc):
	return desc.split(":")


request_content(target_url)
