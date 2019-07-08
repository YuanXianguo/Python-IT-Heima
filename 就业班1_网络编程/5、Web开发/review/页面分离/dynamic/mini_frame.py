import re
import urllib.parse
import logging
from my_sql import PyMySQL


URL_DICT = dict()
mysql = PyMySQL("localhost", 3306, "root", "2017916", "stock_db")


def route(url):
    def decorator(func):
        URL_DICT[url] = func  # URL_DICT["/index.py"] = index
        
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner
    return decorator


@route(r"/add/(\d+)\.html")
def add_focus(ret):
    # 获取股票代码
    stock_code = ret.group(1)
    # 判断下是否有这个股票
    sql = "select * from info where code=%s;"
    stock = mysql.get_one(sql, (stock_code,))
    if not stock:
        return "没有这支股票"
    # 判断下是否已经关注过
    # sql = "select * from focus where info_id=%s;"
    sql = "select * from info inner join focus on info.code=focus.info_id" \
          " where info.code=%s;"
    if mysql.get_one(sql, stock_code):
        return "已经关注过了"
    # sql = "insert into focus (info_id) values (%s);"
    sql = "insert into focus (info_id) select id from info where code=%s;"
    mysql.insert(sql, stock_code)
    return "关注成功"


@route(r"/del/(\d+)\.html")
def del_focus(ret):
    # 获取股票代码
    stock_code = ret.group(1)
    # 判断下是否有这个股票
    sql = "select * from info where code=%s;"
    stock = mysql.get_one(sql, (stock_code,))
    if not stock:
        return "没有这支股票"
    # 判断下是否已经关注过
    # sql = "select * from focus where info_id=%s;"
    sql = "select * from info inner join focus on info.code=focus.info_id" \
          " where info.code=%s;"
    if not mysql.get_one(sql, (stock_code,)):
        return "未关注该股票"
    # sql = "insert into focus (info_id) values (%s);"
    sql = "delete from focus where info_id=(select id from info where code=%s);"
    mysql.delete(sql, stock_code)
    return "取消关注成功"


@route(r"/update/(\d+)\.html")
def update(ret):
    with open("./templates/update.html", "r", encoding="utf-8") as f:
        content = f.read()
    stock_code = ret.group(1)
    sql = "select note_info from focus as f inner join info as i on f.info_id=i.id where i.code=%s;"
    note_info = mysql.get_one(sql, (stock_code,))[0]
    content = re.sub(r"\{%content%\}", note_info, content)
    content = re.sub(r"\{%stock_code%\}", stock_code, content)
    return content


@route(r"/update/(\d+)/(w*)\.html")
def save_update(ret):
    stock_code = ret.group(1)
    new_info = ret.group(2)
    # url解码
    new_info = urllib.parse.unquote(new_info)
    sql = "insert into focus set note_info=%s where info_id=(select id from info_id where code=%s);"
    mysql.insert(sql, (new_info, stock_code))
    return "修改成功"


@route(r"/index.html")
def index(ret):
    with open("./templates/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    sql = "select * from info"
    stock_info = mysql.get_all(sql, [])
    new_html = ""
    for stock in stock_info:
        tr = "<tr>"
        for td in stock[1:]:
            tr += "<td>%s</td>" % td
        tr += "<td><input type='button' value='添加' id='toAdd' name='toAdd' " \
              "systemidvalue='%s'></td>" % stock[1]
        tr += "</tr>"
        new_html += tr
    content = re.sub(r"\{%content%\}", new_html, content)
    return content


@route(r"/center.html")
def center(ret):
    with open("./templates/center.html", "r", encoding="utf-8") as f:
        content = f.read()
    sql = "select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info " \
          "from info as i inner join focus as f on i.id=f.info_id; "
    stock_info = mysql.get_all(sql, [])
    new_html = ""
    for stock in stock_info:
        tr = "<tr>"

        for td in stock:
            tr += "<td>%s</td>" % td
        tr += "<td><a type='button' href='/update/%s.html'>修改</a></td>" % stock[0]
        tr += "<td><input type='button' value='删除' id='toDel' name='toDel' systemidvalue='%s'></td>" % stock[0]

        tr += "</tr>"
        new_html += tr
    content = re.sub(r"\{%content%\}", new_html, content)
    return content


def application(env, get_response):
    get_response("200 OK", [("Content-Type", "text/html;charset=utf-8")])
    file = env["file"]

    logging.basicConfig(level=logging.INFO,
                        filename=".log.txt",
                        filemode="w",
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    logging.info("访问的文件是%s" % file)
    try:
        for url, func in URL_DICT.items():
            ret = re.match(url, file)
            if ret:
                return func(ret)
        else:
            logging.warning("没有对应的函数")
            return "请求的url(%s)没有对应的函数..." % file
    except Exception as ret:
        return "产生了异常：" + str(ret)
