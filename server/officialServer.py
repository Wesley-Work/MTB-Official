import hashlib
import time
import aiofiles
import traceback
from typing import List, Optional
import pymysql
import json
import os
import fastapi
import uvicorn
from pymysql.converters import escape_string
import pymysql.cursors
from pydantic import BaseModel, Field


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


# 上传文件路径，需要适配前端路径
UploadPath = "./public/static"
ReviewUploadPath = "./static"
mysqlConfig = load_config()

print(mysqlConfig)

app = fastapi.FastAPI()


def CombineData(errcode: any = 0, errmsg: str = "", data: any = {}):
    # if data:
    return {"errcode": errcode, "errmsg": errmsg, "data": data}


# else:
#     return {"errcode": errcode, "errmsg": errmsg}


@app.get("/", description="INDEX")
def index():
    return {}


# data: 消息内容
# type: 消息类型 static 或  dynamic
@app.get("/getToppic")
def getToppic():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM toppic"
                cursor.execute(sql)
                result = cursor.fetchone()
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

                    # 创建节点副本避免修改原数据
                    node = node.copy()

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
                            if not "children" in node:
                                node["children"] = []
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

                    # 创建节点副本避免修改原数据
                    node = node.copy()

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
                            if not "children" in node:
                                node["children"] = []
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

                final_result = {}
                for root in root_nodes:
                    tree = build_tree(root)
                    if not tree["type"] in final_result:
                        final_result[tree["type"]] = []
                    if tree:
                        final_result[tree["type"]].append(tree)

                return CombineData(0, "ok", final_result)
    except:
        return CombineData("gfe1", traceback.format_exc())


# ManageToppic
@app.post("/setToppic/del")
def delToppic(
    id: int = fastapi.Form(),
):
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM toppic WHERE id = %s"
                cursor.execute(sql, (id))
                conn.commit()
                if cursor.rowcount == 0:
                    return CombineData("dte2", f"删除失败: 找不到ID为{id}的数据")
                return CombineData(0, "删除成功")
    except:
        return CombineData("dte1", f"删除失败: {traceback.format_exc()}")


@app.post("/setToppic/add")
def addToppic(
    data: str = fastapi.Form(),
    type: str = fastapi.Form(),
):
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                select_sql = "SELECT * FROM toppic"
                cursor.execute(select_sql)
                selectResult = cursor.fetchall()
                if selectResult:
                    return CombineData(
                        "ate2",
                        f"添加失败: 数据表有其他数据，根据规则，只允许一条置顶消息通知。",
                    )
                # 可以添加
                sql = "INSERT INTO toppic (data, type) VALUES (%s, %s)"
                cursor.execute(sql, (data, type))
                conn.commit()
                return CombineData(0, "ok", {"id": cursor.lastrowid})
    except:
        return CombineData(
            "ate1",
            f"添加失败: {traceback.format_exc()}",
        )


@app.post("/setToppic/edit")
def editToppic(
    id: int = fastapi.Form(),
    data: str = fastapi.Form(),
    type: str = fastapi.Form(),
):
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "UPDATE toppic SET data = %s, type = %s WHERE id = %s"
                cursor.execute(sql, (data, type, id))
                conn.commit()
                if cursor.rowcount == 0:
                    return CombineData("ste2", f"更新失败: 找不到ID为{id}的数据")
                return CombineData(0, "ok", {"id": cursor.lastrowid})
    except:
        return CombineData(
            "ste1",
            f"添加失败: {traceback.format_exc()}",
        )


# ManageHeader
@app.post("/setHeader/del")
def delHeader(
    id: List[int] = fastapi.Form(),
):
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                ids = id if isinstance(id, list) else [id]
                if not ids:
                    return CombineData("dhe3", "无效的ID参数")
                placeholder = ", ".join(["%s"] * len(ids))
                sql = f"DELETE FROM header WHERE id IN ({placeholder})"
                cursor.execute(sql, tuple(ids))
                conn.commit()
                affected_rows = cursor.rowcount
                if affected_rows == 0:
                    return CombineData("dhe2", f"删除失败：未找到ID {ids} 的数据")
                return CombineData(
                    0, "ok", {"deltedCount": affected_rows, "deltedID": ids}
                )
    except:
        return CombineData("dhe1", f"删除失败: {traceback.format_exc()}")


# 获取值，不存在则返回None
def getValue(data, key: str):
    if isinstance(data, dict):
        return data.get(key)
    elif isinstance(data, list):
        for item in data:
            result = getValue(item, key)
            if result is not None:
                return result
    return None


class HeaderNode(BaseModel):
    id: int
    label: str
    type: str = Field(alias="type")  # 处理关键字
    title: Optional[str] = None
    target: Optional[str] = None
    href: Optional[str] = None
    isRouter: bool = False
    onlyPC: bool = False
    onlyMobile: bool = False
    extraClass: Optional[str] = None
    children: List["HeaderNode"] = []


HeaderNode.model_rebuild()


@app.post("/setHeader/add")
def addHeader(data: str = fastapi.Form()):
    # 解析数据
    try:
        data = json.loads(data)
    except:
        return CombineData("ahe3", "传入的数据无效")
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                conn.begin()

                # 检查是否存在重复ID
                existing_ids = set()
                cursor.execute("SELECT id FROM header")
                existing_ids.update(row["id"] for row in cursor.fetchall())

                def insert_nodes(
                    node: List[HeaderNode] | HeaderNode,
                    parent_id: int = 0,
                    deep: int = 0,
                ):
                    if type(node) is list:
                        for i in node:
                            insert_nodes(i, parent_id, deep)
                    else:
                        # 检查ID是否冲突
                        if node["id"] in existing_ids:
                            raise ValueError(f"ID {node["id"]} 已存在")
                        sql = """
                            INSERT INTO header
                            (`id`, `title`, `label`, `href`, `target`, `isRouter`, `onlyPC`, `onlyMobile`, `type`, `extraClass`, `bindParent`, `deep`)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        values = (
                            node["id"],
                            node.get("title"),
                            node.get("label"),
                            node.get("href"),
                            node.get("target"),
                            node.get("isRouter", False),
                            node.get("onlyPC", False),
                            node.get("onlyMobile", False),
                            node.get("type"),
                            node.get("extraClass"),
                            parent_id or 0,
                            deep or 0,
                        )
                        cursor.execute(sql, values)
                        existing_ids.add(node["id"])
                        # 递归
                        if "children" in node:
                            insert_nodes(node["children"], node["id"], deep + 1)

                insert_nodes(data)
                conn.commit()
                return CombineData(
                    0,
                    "ok",
                    {
                        "all": len(existing_ids),
                        "root": len(data),
                        "root-branch": len(existing_ids) - len(data),
                    },
                )
    except:
        conn.rollback()
        return CombineData("ahe1", f"添加失败: {traceback.format_exc()}")


@app.post("/setHeader/edit")
def editHeader(data: str = fastapi.Form()):
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return CombineData("ehe2", "JSON格式错误")

    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                conn.begin()

                cursor.execute("DELETE FROM header")

                existing_ids = set()

                def insert_nodes(nodes, parent_id=0, deep=0):
                    for node in nodes:
                        sql = """
                            INSERT INTO header
                            (id, title, label, href, target, isRouter,
                             onlyPC, onlyMobile, type, extraClass, bindParent, deep)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        values = (
                            node["id"],
                            node.get("title"),
                            node.get("label", ""),
                            node.get("href", ""),
                            node.get("target", "_self"),
                            node.get("isRouter", False),
                            node.get("onlyPC", False),
                            node.get("onlyMobile", False),
                            node.get("type", "parent"),
                            node.get("extraClass", ""),
                            parent_id,
                            deep,
                        )
                        # 执行插入
                        cursor.execute(sql, values)
                        existing_ids.add(node["id"])
                        # 递归
                        if "children" in node:
                            insert_nodes(node["children"], node["id"], deep + 1)

                # 执行插入
                if isinstance(data, list):
                    insert_nodes(data)
                    conn.commit()
                    return CombineData(
                        0,
                        "ok",
                        {
                            "all": len(existing_ids),
                            "root": len(data),
                            "root-branch": len(existing_ids) - len(data),
                        },
                    )
                else:
                    conn.rollback()
                    return CombineData("ehe3", "数据格式应为列表")
    except:
        conn.rollback()
        return CombineData("ehe1", f"更新失败: {traceback.format_exc()}")


# ManageFooter
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
@app.post("/setFooter/del")
def delFooter(
    id: List[int] = fastapi.Form(),
):
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                ids = id if isinstance(id, list) else [id]
                if not ids:
                    return CombineData("dfe3", "无效的ID参数")
                placeholder = ", ".join(["%s"] * len(ids))
                sql = f"DELETE FROM footer WHERE id IN ({placeholder})"
                cursor.execute(sql, tuple(ids))
                conn.commit()
                affected_rows = cursor.rowcount
                if affected_rows == 0:
                    return CombineData("dfe2", f"删除失败：未找到ID {ids} 的数据")
                return CombineData(
                    0, "ok", {"deltedCount": affected_rows, "deltedID": ids}
                )
    except:
        return CombineData("dfe1", f"删除失败: {traceback.format_exc()}")


class FooterNode(BaseModel):
    id: int
    type: str = Field(alias="type")  # 处理关键字
    title: Optional[str] = None
    label: str
    target: Optional[str] = None
    href: Optional[str] = None
    isRouter: bool = False
    onlyPC: bool = False
    onlyMobile: bool = False
    children: List["FooterNode"] = []


FooterNode.model_rebuild()


@app.post("/setFooter/add")
def addFooter(data: str = fastapi.Form()):
    # 解析数据
    try:
        data = json.loads(data)
    except:
        return CombineData("afe3", "传入的数据无效")
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                conn.begin()

                # 检查是否存在重复ID
                existing_ids = set()
                cursor.execute("SELECT id FROM footer")
                existing_ids.update(row["id"] for row in cursor.fetchall())

                def insert_nodes(
                    node: List[FooterNode] | FooterNode,
                    types: str = None,
                    parent_id: int = 0,
                    deep: int = 0,
                ):
                    if isinstance(node, list):
                        for i in node:
                            insert_nodes(i, types, parent_id, deep)
                    else:
                        keys = node.keys()
                        for i in keys:
                            # 根节点，拆分links和list
                            if i in data.keys():
                                insert_nodes(data[i], i, parent_id, deep)
                                continue
                        # 非根节点
                        if types:
                            # 检查ID是否冲突
                            if node["id"] in existing_ids:
                                raise ValueError(f"ID {node["id"]} 已存在")
                            sql = """
                                INSERT INTO footer
                                (`id`, `type`, `title`, `label`, `target`, `href`, `isRouter`, `onlyPC`, `onlyMobile`, `bindParent`, `deep`)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            values = (
                                node["id"],
                                types,
                                node.get("title"),
                                node.get("label"),
                                node.get("target"),
                                node.get("href"),
                                node.get("isRouter", False),
                                node.get("onlyPC", False),
                                node.get("onlyMobile", False),
                                parent_id or 0,
                                deep or 0,
                            )
                            cursor.execute(sql, values)
                            existing_ids.add(node["id"])
                            # 递归
                            if "children" in node:
                                insert_nodes(
                                    node["children"], types, node["id"], deep + 1
                                )

                insert_nodes(data)
                conn.commit()
                return CombineData(
                    0,
                    "ok",
                    {
                        "all": len(existing_ids),
                        "root": len(data),
                        "root-branch": len(existing_ids) - len(data),
                    },
                )
    except:
        conn.rollback()
        return CombineData("afe1", f"添加失败: {traceback.format_exc()}")


@app.post("/setFooter/edit")
def editFooter(data: str = fastapi.Form()):
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return CombineData("ehe2", "JSON格式错误")

    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                conn.begin()

                cursor.execute("DELETE FROM footer")

                existing_ids = set()

                # 添加部分同添加处代码，这里直接复制了
                def insert_nodes(
                    node: List[FooterNode] | FooterNode,
                    types: str = None,
                    parent_id: int = 0,
                    deep: int = 0,
                ):
                    if isinstance(node, list):
                        for i in node:
                            insert_nodes(i, types, parent_id, deep)
                    else:
                        keys = node.keys()
                        for i in keys:
                            if i in data.keys():
                                insert_nodes(data[i], i, parent_id, deep)
                                continue
                        if types:
                            if node["id"] in existing_ids:
                                raise ValueError(f"ID {node["id"]} 已存在")
                            sql = """
                                INSERT INTO footer
                                (`id`, `type`, `title`, `label`, `target`, `href`, `isRouter`, `onlyPC`, `onlyMobile`, `bindParent`, `deep`)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            values = (
                                node["id"],
                                types,
                                node.get("title"),
                                node.get("label"),
                                node.get("target"),
                                node.get("href"),
                                node.get("isRouter", False),
                                node.get("onlyPC", False),
                                node.get("onlyMobile", False),
                                parent_id or 0,
                                deep or 0,
                            )
                            cursor.execute(sql, values)
                            existing_ids.add(node["id"])
                            # 递归
                            if "children" in node:
                                insert_nodes(
                                    node["children"], types, node["id"], deep + 1
                                )

                insert_nodes(data)
                conn.commit()
                return CombineData(
                    0,
                    "ok",
                    {
                        "all": len(existing_ids),
                        "root": len(data),
                        "root-branch": len(existing_ids) - len(data),
                    },
                )
    except:
        conn.rollback()
        return CombineData("efe1", f"更新失败: {traceback.format_exc()}")


# 滑动背景管理
@app.get("/getBanner")
def getBanner():
    return {"data": "getBanner"}


# 设置背景，包含删除、添加、修改
@app.post("/setBanner")
def setBanner(
    id: int = fastapi.Form(),
    mode: str = fastapi.Form(),  # add or delete or edit
    url: str = fastapi.Form(),
    title: str = fastapi.Form(),
    desc: str = fastapi.Form(),  # subTitle
    type: str = fastapi.Form(),  # video or picture
):
    if mode == "add":
        try:
            with pymysql.connect(**mysqlConfig) as conn:
                with conn.cursor() as cursor:
                    sql = "INSERT INTO banner (title, `desc`, url, type) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (title, desc, url, type))
                    conn.commit()
                    return CombineData(0, "ok", {"id": cursor.lastrowid})
        except:
            return CombineData(
                "abe1",
                f"添加失败: {traceback.format_exc()}",
            )
    elif mode == "delete":
        try:
            with pymysql.connect(**mysqlConfig) as conn:
                with conn.cursor() as cursor:
                    sql = "DELETE FROM banner WHERE id = %s"
                    cursor.execute(sql, (id))
                    conn.commit()
                    return CombineData(0, "ok", {"id": id})
        except:
            return CombineData(
                "dee1",
                f"删除失败: {traceback.format_exc()}",
            )
    elif mode == "edit":
        try:
            with pymysql.connect(**mysqlConfig) as conn:
                with conn.cursor() as cursor:
                    sql = "UPDATE banner SET title = %s, `desc` = %s, url = %s, type = %s WHERE id = %s"
                    cursor.execute(sql, (title, desc, url, type, id))
                    conn.commit()
                    return CombineData(0, "ok", {"id": id})
        except:
            return CombineData(
                "ede1",
                f"更新失败: {traceback.format_exc()}",
            )
    return {"data": "uploadBanner"}


async def save_upload_file_chunks(
    upload_file: fastapi.UploadFile, destination: str, chunk_size: int = 1024 * 1024
):
    try:
        async with aiofiles.open(destination, "wb") as out_file:
            while chunk := await upload_file.read(chunk_size):
                await out_file.write(chunk)
        return True
    except Exception as e:
        print(f"保存文件时发生错误: {str(e)}")
        return e


@app.post("/setBanner/upload")
async def uploadBanner(
    file: fastapi.UploadFile = fastapi.File(...),
    title: str = fastapi.Form(),
    desc: str = fastapi.Form(),  # subTitle
):
    try:
        # 分块保存大小
        chunk_size: Optional[int] = 1024 * 1024
        # 黑名单扩展名
        BLACKLIST_EXTENSIONS = [
            ".exe",
            ".bat",
            ".cmd",
            ".scr",
            ".com",
            ".pif",
            ".php",
            ".py",
            ".rb",
            ".pl",
            ".sh",
            ".asp",
            ".aspx",
            ".jsp",
            ".jspx",
            ".html",
            ".htm",
            ".xhtml",
            ".js",
            ".mht",
            ".mhtml",
            ".zip",
            ".rar",
            ".7z",
            ".tar.gz",
            ".tgz",
            ".bz2",
            ".doc",
            ".docm",
            ".xls",
            ".xlsm",
            ".ppt",
            ".pptm",
            ".dotm",
            ".xltx",
            ".xltm",
            ".potm",
            ".ppam",
            ".ppsm",
        ]
        # 黑名单 Content-Type
        BLACKLIST_CONTENT_TYPES = [
            "application/x-msdownload",
            "application/x-dosexec",
            "application/x-httpd-php",
            "application/x-python-code",
            "application/x-ruby",
            "text/plain",
            "text/html",
            "application/javascript",
            "text/javascript",
            "application/zip",
            "application/x-rar-compressed",
            "application/x-7z-compressed",
            "application/msword",
            "application/vnd.ms-excel",
            "application/vnd.ms-powerpoint",
        ]
        # 文件类型
        fileContent_type = file.content_type.split("/")[0]
        if fileContent_type == "image":
            fileType = "picture"
        else:
            fileType = fileContent_type
        # file.size 是 字节 为单位的
        # 判断黑名单
        if file.filename in BLACKLIST_EXTENSIONS or fileType in BLACKLIST_CONTENT_TYPES:
            return CombineData("efe1", "文件类型在黑名单中，请确认文件类型是否正确！")
        # 唯一文件名
        fileNames = file.filename.split(".")
        # 在第一个点前面加时间戳
        fileName = f"{fileNames[0]}_{int(time.time()*1000)}"
        fileNames.pop(0)
        fileName = f"{fileName}.{'.'.join(fileNames)}"
        fileContent = await file.read()
        # 判断上传文件路径是否存在，不存在就创建
        if not os.path.exists(UploadPath):
            os.makedirs(UploadPath, exist_ok=True)
        filePath = f"{UploadPath}/{fileName}"
        # 储存文件
        saveSuccess = await save_upload_file_chunks(file, filePath, chunk_size)
        if not saveSuccess is True:
            return CombineData("sbe_u2", saveSuccess)
        fileUrl = f"{ReviewUploadPath}/{fileName}"
        try:
            append = setBanner(None, "add", fileUrl, title, desc, fileType)
            if append["errcode"] != 0:
                return CombineData("sbe_u4", append["errmsg"])
        except:
            return CombineData("sbe_u3", traceback.format_exc())
        return {
            "url": fileUrl,
            "filename": file.filename,
            "combineFilename": fileName,
            "content_type": file.content_type,
            "size": len(fileContent),
            "md5": hashlib.md5(fileContent).hexdigest(),
        }
    except:
        return CombineData("sbe_u1", traceback.format_exc())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=16485)
