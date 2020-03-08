import pymysql
import time
import json
import traceback # 追踪异常
import requests

def get_detail_data():
	url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
	}
	res = requests.get(url, headers=headers)
	data_all = json.loads((json.loads(res.text))["data"])

	details = [] # 当日详细数据
	update_time = data_all["lastUpdateTime"]
	data_country = data_all["areaTree"] # 25个国家
	data_province = data_country[0]["children"] # 中国各省
	for pro_infos in data_province:
		province = pro_infos["name"]
		for city_infos in pro_infos["children"]:
			city = city_infos["name"]
			confirm = city_infos["total"]["confirm"]
			confirm_add = city_infos["today"]["confirm"]
			heal = city_infos["total"]["heal"]
			dead = city_infos["total"]["dead"]
			details.append([update_time, province, city, confirm, confirm_add, heal, dead])
	return details


def get_history_data():
	url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
	}
	res = requests.get(url, headers=headers)
	data_all = json.loads((json.loads(res.text))["data"])


	history = {} # 历史数据
	for i in data_all["chinaDayList"]:
		ds = "2020." + i["date"]
		tup = time.strptime(ds, "%Y.%m.%d")
		ds = time.strftime("%Y-%m-%d", tup) # 改变时间格式，不然插入数据库会报错，数据库是datetime格式
		confirm = i["confirm"]
		suspect = i["suspect"]
		heal = i["heal"]
		dead = i["dead"]
		history[ds] = {"confirm":confirm, "suspect":suspect, "heal":heal, "dead":dead}

	for i in data_all["chinaDayAddList"]:
		ds = "2020." + i["date"]
		tup = time.strptime(ds, "%Y.%m.%d")
		ds = time.strftime("%Y-%m-%d", tup)
		confirm = i["confirm"]
		suspect = i["suspect"]
		heal = i["heal"]
		dead = i["dead"]
		history[ds].update({"confirm_add":confirm, "suspect_add":suspect, "heal_add":heal, "dead_add":dead})

	return history

def get_conn():
	conn = pymysql.connect(host="127.0.0.1",
						   user="root",
						   password="123456",
						   db="cov",
						   charset="utf8")
	cursor = conn.cursor()
	return conn, cursor

def close_conn(conn, cursor):
	if cursor:
		cursor.close()
	if conn:
		conn.close()

def update_detail():
	"""
	更新details表
	"""

	cursor  =None
	conn = None

	try:
		li = get_detail_data()
		conn, cursor = get_conn()
		sql = "insert into detail(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
		sql_query = "select %s=(select update_time from detail order by id desc limit 1)"
		cursor.execute(sql_query, li[0][0])

		if not cursor.fetchone()[0]:
			print(f"{time.asctime()}开始更新最新数据")
			for item in li:
				cursor.execute(sql, item)
			conn.commit()
			print(f"{time.asctime()}更新最新数据完毕")
		else:
			print(f"{time.asctime()}已是最新数据")
	except:
		traceback.print_exc()
	finally:
		close_conn(conn, cursor)

def insert_history():
	"""
	插入历史数据
	"""
	cursor  =None
	conn = None

	try:
		dic = get_history_data()
		print(f"{time.asctime()}开始插入历史数据")
		conn, cursor = get_conn()
		
		sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		for k, v in dic.items():
			cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
						   v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
						   v.get("dead"), v.get("dead_add")])

		conn.commit()
		print(f"{time.asctime()}插入历史数据完毕")
	except:
		traceback.print_exc()
	finally:
		close_conn(conn, cursor)

def updata_history():
	"""
	更新历史数据
	"""
	cursor  =None
	conn = None

	try:
		dic = get_history_data()
		print(f"{time.asctime()}开始更新历史数据")
		conn, cursor = get_conn()
		
		sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		sql_query = "select confirm from history where ds=%s"
		for k, v in dic.items():
			if not cursor.execute(sql_query, k):
				cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
							   v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
							   v.get("dead"), v.get("dead_add")])

		conn.commit()
		print(f"{time.asctime()}历史数据更新完毕")
	except:
		traceback.print_exc()
	finally:
		close_conn(conn, cursor)


insert_history()
# update_detail()