from flask import Flask, request, abort, render_template
import hashlib
import xmltodict
import time
import urllib.request
import json

# token
WECHAT_TOKEN = "daguopython"
WECHAT_APPID = "wx8c109bb8e404f4b6"
WECHAT_APPSECRET = "b776cd3465993c26dbabfc7d318366f9"

app = Flask(__name__)


@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    """对接微信公众号服务器"""
    # 接收微信服务器发送的参数
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")

    # 校验参数
    if not all([signature, timestamp, nonce]):
        abort(400)

    # 按照微信的流程进行计算签名
    # 处理字符串
    lst = [WECHAT_TOKEN, timestamp, nonce]
    lst.sort()
    tmp_str = "".join(lst)
    # 进行sha1加密，得到签名值
    sign = hashlib.sha1(tmp_str.encode("utf-8")).hexdigest()

    # 对比签名
    if signature != sign:
        abort(403)
    else:  # 表示是微信发送的请求
        if request.method == "GET":  # 表示是第一次接入微信服务器的验证
            echostr = request.args.get("echostr")
            if not echostr:
                abort(400)
            return echostr
        elif request.method == "POST":
            # 表示微信服务器转发消息过来
            xml_str = request.data
            if not xml_str:
                abort(400)
            # 解析
            xml_dict = xmltodict.parse(xml_str)
            xml_dict = xml_dict.get("xml")
            # 提取消息类型
            msg_type = xml_dict.get("MsgType")

            if msg_type == "text":  # 表示发送的是文本消息
                # 构造回复消息
                res_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": xml_dict.get("Content")
                    }
                }
            else:
                res_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": "success"
                    }
                }
            # 反解析
            res_xml_str = xmltodict.unparse(res_dict)
            return res_xml_str


@app.route("/wechat/index")
def index():
    """让用户通过微信访问的网页页面视图"""
    # 1.用户同意授权，获取code
    code = request.args.get("code")
    if not code:
        return "缺失code参数"

    def get_dict(url):
        # urlopen(url,data)，url：网站地址，str类型，也可以是一个request对象
        # data：data参数是可选的，内容为字节流编码格式的即bytes类型，如果传递data参数，urlopen将使用Post方式请求
        response = urllib.request.urlopen(url)
        # 获取响应体数据
        json_str = response.read()
        res_dict = json.loads(json_str)
        return res_dict

    # 2.通过code换取网页授权access_token
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}" \
          "&code={}&grant_type=authorization_code".format(WECHAT_APPID, WECHAT_APPSECRET, code)
    res_dict = get_dict(url)
    if "errcode" in res_dict:
        return "获取access_token失败"
    # 提取access_token
    access_token = res_dict.get("access_token")
    open_id = res_dict.get("openid")  # 用户编号

    # 3.向微信服务器发送http请求，获取用户信息
    url = "https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}" \
          "&lang=zh_CN".format(access_token, open_id)
    user_res_dict = get_dict(url)
    if "errcode" in user_res_dict:
        return "获取access_token失败"
    return render_template("index.html", user=user_res_dict)


if __name__ == '__main__':
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx8c109bb8e404f4b6&redirect_uri=http%3A//5504ac56.ngrok.io/wechat/index&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect"
    app.run(
        port=80,
        debug=True
    )
