#
import json
import traceback
import flask
from flask import request, render_template
from fake_useragent import UserAgent
import requests
from flask_cors import CORS

ua = UserAgent()
# 请求头
# headers={"User-Agent":ua.random,"Host":"10.3.146.102:5000"}
headers = {
    "User-Agent": ua.random,
    "Host": "10.3.146.10:5000",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
}

# 初始化
app = flask.Flask(__name__)
CORS(app, supports_credentials=True)
# 主地址
main_UrlT = "http://10.3.146.10:5000"

# 共享目录ssid
ssid = "a5458f75cd1346799519c7f3346af397"

# 获取文件列表地址【GET、POST】

# 可选参数
# sort {非必填} 排序根据: natural：名称；mt：修改日期；filesize：文件大小
# dir {非必填} 排序方式：ASC：正序；DESC：倒序
# start {非必填} 获取的起始位置，配合limit使用：以0开始
# limit {非必填} 单页数量：默认50
# path {非必填} 子路径(/xxx、/xxx/xxx)
# fid {必填} 文件夹fid（即ssid）

# 返回示例
# total 数据总数 {number}
# option  {number}
# link_name  {string}
# foldername  {string}
# multiple  {number}
# datas 文件列表 {Array|list}
# daras[Props]↓ 文件信息
# epochmt {number}
# filename 文件名称 {string}
# filesize 文件大小 {number}
# isfolder 是否是文件夹 {number}，0（否） or 1（是）
# mp3 {number}
# mp4_240 {number}
# mp4_360 {number}
# mp4_480 {number}
# mp4_720 {number}
# mp4_1080 {number}
# mp4_org {number}
# mt 修改时间 {number}
main_Url = f"{main_UrlT}/share.cgi?func=get_list&ssid={ssid}&fid={ssid}"

# 下载单文件地址【前端GET】
# filename {必填} 文件名
# path {非必填} 路径(/xxx、/xxx/xxx)，根目录下非必填
download_file_Url = (
    f"{main_UrlT}/share.cgi?ssid={ssid}&openfolder=forcedownload&fid={ssid}&filename="
)

# 下载全部文件（打包zip）地址【前端GET】
download_all_file_Url = (
    f"{main_UrlT}/share.cgi?ssid={ssid}&openfolder=forcedownload&fid={ssid}"
)

# 屏蔽文件列表
# 支持文件全名、文件后缀、一级目录
# /filefolder
# *.suffix
shieldFileList = []

# 不显示后缀的文件列表
notShowSuffixFileList = [".txt", ".md"]

# 外部配置文件
# with open(sys.path[0]+'/config.yaml', 'r', encoding='utf-8') as f:
#     s = yaml.safe_load(f)
# print(yaml.dump(s,default_flow_style=False)) # 输出yaml文件内容

# 屏蔽文件列表
# shieldFileList = s['shieldFileList']
# 不显示后缀的文件列表
# notShowSuffixFileList = s['notShowSuffixFileList']


# 获取共享文件夹ssid
@app.route("/getssid", methods=["GET", "POST"])
def getssid():
    res = {}
    try:
        res["errcode"] = 0
        res["errmsg"] = "ok"
        res["ssid"] = ssid
    except:
        res = {"errcode": -1, "errmsg": traceback.format_exc()}
    return flask.jsonify(res)


# 获取文件列表
@app.route("/getFileList", methods=["GET", "POST"])
def getFileList(sort="natural", dirs="ASC", start=0, limit=50, path=None):

    res = {}
    resdata = {}
    total = 0
    filelist = []
    comment = ""
    try:
        try:
            needparam = "path"
            if request.method == "GET":
                comment = request.args.get(needparam)
            if request.method == "POST":
                if request.content_type.startswith("application/json"):
                    comment = request.json.get(needparam)
                elif request.content_type.startswith("multipart/form-data"):
                    comment = request.form.get(needparam)
                else:
                    comment = request.values.get(needparam)
            if comment is None or comment == "":
                comment = "/"
        except:
            res = {"errcode": 1, "errmsg": "参数错误"}
            return flask.jsonify(res)
        print(comment)
        data = {
            "sort": sort,
            "dir": dirs,
            "start": start,
            "limit": limit,
            "path": comment,
        }
        reqresult = requests.post(url=main_Url, data=data, headers=headers, stream=True)
        # print(reqresult.text)
        if reqresult.status_code != 200:
            if reqresult.status_code == 500:
                res = {"errcode": -404, "errmsg": "文件路径不存在"}
                return flask.jsonify(res)
            res = {"errcode": 2, "errmsg": "请求失败", "code": reqresult.status_code}
            return flask.jsonify(res)
        result = reqresult.json()
        # 忽略文件
        for i in reqresult.json()["datas"]:
            if shieldFileList == []:
                pass
            # 因为or运算符特性，所以不用not in
            i1 = i["filename"] in shieldFileList  # 全文件名
            i2_1 = i["filename"].split(".")  # 后缀名
            i3_1 = i["isfolder"] == 1  # 目录
            if i3_1:
                i3 = f"/{i['filename']}" in shieldFileList
            else:
                i3 = False
            # 判断后缀名
            if len(i2_1) >= 2:
                # 拆分到了，判断后缀在不在列表中
                i2 = f"*.{i2_1[1]}" in shieldFileList
            else:
                # 因为拆分不到，所以不是
                i2 = False
            # 目录只支持一级目录
            if i1 or i2 or i3:
                pass
            else:
                filelist.append(i)
                total += 1
        # 处理数据
        for l in filelist:
            # 获取下载链接
            l["download_url"] = getFileDownloadURL(l["filename"], comment)
            # 不显示后缀
            try:
                wfilehassuffix = l["filename"].split(".", 1)
            except:
                print("分割失败")
            if len(wfilehassuffix) >= 2:
                filesuffix = f".{wfilehassuffix[1]}"
                l["suffix"] = wfilehassuffix[1]
            else:
                filesuffix = None
                l["suffix"] = ""
            if filesuffix in notShowSuffixFileList:
                l["filename"] = l["filename"].split(".", 1)[0]
        # 处理后数据返回
        resdata["filelist"] = filelist
        resdata["total"] = total
        # 原厂数据返回
        resdata["foldername"] = result["foldername"]
        resdata["link_name"] = result["link_name"]
        resdata["multiple"] = result["multiple"]
        resdata["option"] = result["option"]
        # 输出
        res["errcode"] = 0
        res["errmsg"] = "ok"
        res["data"] = resdata
    except:
        res = {"errcode": -1, "errmsg": traceback.format_exc()}
    return flask.jsonify(res)


# 获取文件下载地址
@app.route("/getFileDownloadURL", methods=["GET", "POST"])
def APPgetFileDownloadURL():
    res = {}
    try:
        p_data = request.form
        g_data = request.args
        try:
            filename = (
                str(g_data.get("filename"))
                if str(p_data.get("filename")) == "None"
                else str(p_data.get("filename"))
            )
            path = (
                str(g_data.get("path"))
                if str(p_data.get("path")) == "None"
                else str(p_data.get("path"))
            )
        except:
            res = {"errcode": 1, "errmsg": "参数错误"}
        if filename == "None":
            res = {"errcode": 1, "errmsg": "参数错误"}
            return flask.jsonify(res)
        url = getFileDownloadURL(filename, path)
        res["errcode"] = 0
        res["errmsg"] = "ok"
        res["url"] = url
    except:
        res = {"errcode": -1, "errmsg": traceback.format_exc()}
    return flask.jsonify(res)


def getFileDownloadURL(filename, path):
    if path != None or path != "None":
        url = f"{download_file_Url}{filename}&path={path}"
    else:
        url = f"{download_file_Url}{filename}"
    return url


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=9091, debug=False)
    app.run(host="0.0.0.0", port=9090, debug=False)
