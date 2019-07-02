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
			print(len(malware_rows))

			for i in len(malware_rows):
				print(malware_rows[i])
				db_class = dbModule.Mysql()
				#960: {'URL': 'pool.ug/tesptc/ck/updatewin2.exe', 'Country': 'RU', 'ASN': '48347', 'MD5': '996ba35165bb62473d2a6743a5200d45', 'IPAddress': '194.87.239.100', 'title': 'pool.ug'},
				sql = """INSERT INTO MALWARE_INFO VALUES(URL, Country, MD5, IPAddress, title) values (%s, %s, %s, %s, %s)"""
				db_class.execute(sql, (row.URL, row.Country, row.MD5, row.IPAddress, row.title))
				db_class.commit()
				break
		else:
			return false


def parse_content(soup):
	all_item = soup.find_all("item")

	malware_list = {}
	for n in range(len(all_item)):
		title = all_item[n].find("title")
		desc = all_item[n].find("description").string

		if len(desc) > 0:
			desc_parse = desc.replace(" ", "").split(",")

			malware_list[n] = {
				'title': title.string
			}

			detail_list = list(map(parse_description, desc_parse))
			for detail in detail_list:
				malware_list[n][detail[0]] = detail[1]
		else:
			return false

	return malware_list




def parse_description(desc):
	return desc.split(":")


request_content(target_url)
