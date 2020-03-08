import time
import pymysql


def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


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


def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)

    return res


def get_date():
    sql = "select sum(confirm),"\
          "(select suspect from history order by ds desc limit 1),"\
          "sum(heal),"\
          "sum(dead) "\
          "from detail "\
          "where update_time=(select update_time from detail order by update_time desc limit 1)"
    res = query(sql)
    return res[0]


def get_china():
    sql = "select province,sum(confirm) from detail "\
          "where update_time=(select update_time from detail order by update_time desc limit 1) "\
          "group by province"

    res = query(sql)
    return res


def get_lj():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


def get_xz():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res
