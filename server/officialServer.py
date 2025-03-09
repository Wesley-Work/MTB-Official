import traceback
import pymysql
import json
import os
import fastapi
import uvicorn
from pymysql.converters import escape_string
import pymysql.cursors

# /getToppic
# /getHeaderList
# /getFooterList
# /getBanner


def load_config():
    # 根据实际路径调整
    config_path = os.path.join(os.path.dirname(__file__), "./database.config.json")
    try:
        with open(config_path, "r") as f:
            cfg = json.load(f)
            cfg["cursorclass"] = pymysql.cursors.DictCursor
            return cfg
    except FileNotFoundError:
        print(f"配置文件 {config_path} 未找到！")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"配置文件解析失败: {str(e)}")
        exit(1)


mysqlConfig = load_config()

print(mysqlConfig)

app = fastapi.FastAPI()


def CombineData(errcode: any = 0, errmsg: str = "", data: any = {}):
    if data:
        return {"errcode": errcode, "errmsg": errmsg, "data": data}
    else:
        return {"errcode": errcode, "errmsg": errmsg}


@app.get("/", description="INDEX")
def index():
    return {}


@app.get("/getToppic")
def getToppic():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM toppic"
                cursor.execute(sql)
                result = cursor.fetchall()
                return CombineData(0, "ok", result)
    except:
        return CombineData("gte1", traceback.format_exc())


# id: 时间戳
# title: 项标题 only type=label
# label: 文字内容
# href: 跳转地址，本地路由时为本地地址
# target: 跳转方式
# isRouter: 是否本地路由
# onlyPC: 是否仅PC端
# onlyMobile: 是否仅移动端
# type: 类型 only parent
# extraClass: 额外class类 only parent
# bindParent: 绑定父级id，为0则为根节点
# deep: 层级
@app.get("/getHeaderList")
def getHeaderList():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM header")
                result = cursor.fetchall()
                all_nodes = [dict(row) for row in result]

                # 构建快速查询字典（处理无效节点）
                node_dict = {}
                valid_ids = set()
                for node in all_nodes:
                    node_id = node["id"]
                    if node_id in node_dict:
                        print(f"数据重复ID: {node_id}")
                        continue
                    node_dict[node_id] = node
                    valid_ids.add(node_id)

                # 递归构建树形结构（带循环检测）
                def build_tree(node, parent_ids=None):
                    if parent_ids is None:
                        parent_ids = set()

                    current_id = node["id"]
                    if current_id in parent_ids:
                        print(f"检测到循环引用: {current_id}")
                        return None

                    parent_ids.add(current_id)

                    # 初始化children字段
                    node = node.copy()  # 创建节点副本避免修改原数据
                    node["children"] = []

                    # 查找所有直接子节点
                    children = [
                        node_dict[child_id]
                        for child_id in valid_ids
                        if node_dict[child_id]["bindParent"] == current_id
                    ]

                    # 递归处理子节点
                    for child in children:
                        processed_child = build_tree(child, parent_ids.copy())
                        if processed_child:
                            node["children"].append(processed_child)

                    # 清理技术字段（处理完成后统一删除）
                    del node["deep"], node["bindParent"]
                    return node

                # 构建完整树形结构
                root_nodes = [
                    node
                    for node in node_dict.values()
                    if node["bindParent"] == 0 or node["bindParent"] not in valid_ids
                ]

                final_result = []
                for root in root_nodes:
                    tree = build_tree(root)
                    if tree:
                        final_result.append(tree)

                return CombineData(0, "ok", final_result)
    except:
        return CombineData("ghe1", traceback.format_exc())


# Footer
# id: id
# type: 内容类型，list 或 links，links是普通的带有标题和子项的，list是简单的链接列，单独出现的
# title 标题，type为links时有效
# label: 文字内容
# target: 跳转方式
# href: 跳转地址，本地路由时为本地地址
# isRouter: 是否本地路由
# onlyPC: 是否仅PC端
# onlyMobile: 是否仅移动端
# bindParent: 绑定父级id，仅type为links时有效，为0则为根节点
# deep: 层级
@app.get("/getFooterList")
def getFooterList():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM footer")
                result = cursor.fetchall()
                all_nodes = [dict(row) for row in result]

                # 构建快速查询字典（处理无效节点）
                node_dict = {}
                valid_ids = set()
                for node in all_nodes:
                    node_id = node["id"]
                    if node_id in node_dict:
                        print(f"footer数据重复ID: {node_id}")
                        continue
                    node_dict[node_id] = node
                    valid_ids.add(node_id)

                def build_footer_tree(node, parent_ids=None):
                    if parent_ids is None:
                        parent_ids = set()

                    current_id = node["id"]
                    if current_id in parent_ids:
                        print(f"footer检测到循环引用: {current_id}")
                        return None

                    parent_ids.add(current_id)

                    # 创建节点副本并初始化children
                    node = node.copy()
                    node["children"] = []

                    # 仅处理 type='links' 的父节点
                    if node["type"] == "links":
                        # 查找所有直接子节点（按 bindParent 关联）
                        children = [
                            node_dict[child_id]
                            for child_id in valid_ids
                            if node_dict[child_id]["bindParent"] == current_id
                            and node_dict[child_id].get("type")
                            != "links"  # 子项不应是links类型
                        ]

                        # 递归处理子节点
                        for child in children:
                            processed_child = build_footer_tree(
                                child, parent_ids.copy()
                            )
                            if processed_child:
                                node["children"].append(processed_child)

                    # 清理技术字段
                    fields_to_remove = [
                        "deep",
                        "bindParent",
                        "onlyPC",
                        "onlyMobile",
                        "extraClass",
                    ]
                    for field in fields_to_remove:
                        if field in node:
                            del node[field]

                    # 类型兼容处理
                    if node["type"] == "list":
                        node.pop("children", None)  # list类型不需要children
                    return node

                root_nodes = [
                    node
                    for node in node_dict.values()
                    if (node["bindParent"] == 0 or node["bindParent"] not in valid_ids)
                    and node["type"] in ["links", "list"]
                ]

                links_data = []
                list_data = []
                for root in root_nodes:
                    tree = build_footer_tree(root)
                    if tree:
                        if tree["type"] == "links":
                            links_data.append(tree)
                        elif tree["type"] == "list":
                            list_data.append(tree)

                return CombineData(0, "ok", {"links": links_data, "list": list_data})
    except:
        return CombineData("gfe1", "traceback.format_exc()")


@app.get("/getBanner")
def getBanner():
    return {"data": "getBanner"}


# ManageToppic
@app.post("/setToppic/del")
def delToppic():
    return {"data": "delToppic"}


@app.post("/setToppic/add")
def addToppic():
    return {"data": "addToppic"}


@app.post("/setToppic/edit")
def editToppic():
    return {"data": "editToppic"}


# ManageHeader
@app.post("/setHeader/del")
def delHeader():
    return {"data": "delHeader"}


@app.post("/setHeader/add")
def addHeader():
    return {"data": "addHeader"}


@app.post("/setHeader/edit")
def editHeader():
    return {"data": "editHeader"}


# ManageFooter
@app.post("/setFooter/del")
def delFooter():
    return {"data": "delFooter"}


@app.post("/setFooter/add")
def addFooter():
    return {"data": "addFooter"}


@app.post("/setFooter/edit")
def editFooter():
    return {"data": "editFooter"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=16485)
