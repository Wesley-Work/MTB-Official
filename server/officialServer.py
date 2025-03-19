import hashlib
import time
import aiofiles
import traceback
from typing import List, Optional
import pymysql
import json
import os
import fastapi
from fastapi.middleware.cors import CORSMiddleware
import requests
import httpx
import urllib
import uvicorn
from pymysql.converters import escape_string
import pymysql.cursors
from pydantic import BaseModel, Field
import xmltodict
from functools import lru_cache


# 官网业务API

# 上传文件路径，需要适配前端路径
UploadPath = "./public/static"
ReviewUploadPath = "./static"


def load_mysql_config():
    # 根据实际路径调整
    config_path = os.path.join(os.path.dirname(__file__), "./database.config.json")
    try:
        with open(config_path, "r") as f:
            cfg = json.load(f)
            cfg["cursorclass"] = pymysql.cursors.DictCursor
            return cfg
    except FileNotFoundError:
        print(f"配置文件 {config_path} 未找到！")
        quit()
    except json.JSONDecodeError as e:
        print(f"配置文件解析失败: {str(e)}")
        quit()


mysqlConfig = load_mysql_config()


def getValue(data, key: str):
    """
    获取字典或列表中的值，如果不存在则返回None。
    """
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


HeaderNode.model_rebuild()

FooterNode.model_rebuild()


async def save_upload_file_chunks(
    upload_file: fastapi.UploadFile, destination: str, chunk_size: int = 1024 * 1024
):
    """
    分块保存文件
    """
    try:
        async with aiofiles.open(destination, "wb") as out_file:
            while chunk := await upload_file.read(chunk_size):
                await out_file.write(chunk)
        return True
    except Exception as e:
        print(f"保存文件时发生错误: {str(e)}")
        return e


def CombineData(
    errcode: any = 0,
    errmsg: str = "",
    data: any = {},
    defaultData: str = "dict",
) -> dict:
    """
    CombineData
    :param errcode: 错误码
    :param errmsg: 错误信息
    :param data: 数据
    """
    if not data:
        if defaultData == "dict":
            data = {}
        else:
            data = []
    return {"errcode": errcode, "errmsg": errmsg, "data": data}


app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


URLPREFIX = "/api"


@app.get(f"{URLPREFIX}", description="API根")
def index():
    return {}


@app.get(f"{URLPREFIX}/getToppic", description="获取置顶通知内容列表")
def getToppic():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM toppic"
                cursor.execute(sql)
                result = cursor.fetchone()
                if not result:
                    result = []
                return CombineData(0, "ok", result)
    except:
        return CombineData("gte1", traceback.format_exc())


@app.get(f"{URLPREFIX}/getHeaderList", description="获取顶菜单内容配置")
def getHeaderList():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM header")
                result = cursor.fetchall()
                if not result:
                    result = []
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
                    del node["deep"]
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

                return CombineData(0, "ok", final_result, "list")
    except:
        return CombineData("ghe1", traceback.format_exc())


@app.get(f"{URLPREFIX}/getFooterList", description="获取底部页脚列表")
def getFooterList():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM footer")
                result = cursor.fetchall()
                if not result:
                    result = []
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

                final_result = {"list": [], "links": []}
                for root in root_nodes:
                    tree = build_tree(root)
                    if not tree["type"] in final_result:
                        final_result[tree["type"]] = []
                    if tree:
                        final_result[tree["type"]].append(tree)

                return CombineData(0, "ok", final_result, "list")
    except:
        return CombineData("gfe1", traceback.format_exc())


# 管理功能API
@app.post(f"{URLPREFIX}/setToppic/del", description="设置置顶通知内容-删除")
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


@app.post(f"{URLPREFIX}/setToppic/add", description="设置置顶通知内容-添加")
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


@app.post(f"{URLPREFIX}/setToppic/edit", description="设置置顶通知内容-修改")
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


@app.post(f"{URLPREFIX}/setHeader/del", description="设置顶菜单-删除")
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


@app.post(f"{URLPREFIX}/setHeader/add", description="设置顶菜单-新增")
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
                        if not "id" in node:
                            raise ValueError("传入的数据无效，id不存在于数据中")
                        # 检查ID是否冲突
                        if node["id"] in existing_ids:
                            raise ValueError(f"ID {node['id']} 已存在")
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
    except ValueError as e:

        return CombineData("ahe2", str(e))
    except:

        return CombineData("ahe1", f"添加失败: {traceback.format_exc()}")


@app.post(f"{URLPREFIX}/setHeader/edit", description="设置顶菜单-修改")
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

                    return CombineData("ehe3", "数据格式应为列表")
    except:

        return CombineData("ehe1", f"更新失败: {traceback.format_exc()}")


# ManageFooter
@app.post(f"{URLPREFIX}/setFooter/del", description="设置底部页脚-删除")
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


@app.post(f"{URLPREFIX}/setFooter/add", description="设置底部页脚-新增")
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
                            if not "id" in node:
                                raise ValueError("传入的数据无效，id不存在于数据中")
                            # 检查ID是否冲突
                            if node["id"] in existing_ids:
                                raise ValueError(f"ID {node['id']} 已存在")
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
    except ValueError as e:
        return CombineData("afe2", str(e))
    except:
        return CombineData("afe1", f"添加失败: {traceback.format_exc()}")


@app.post(f"{URLPREFIX}/setFooter/edit", description="设置底部页脚-修改")
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
                                raise ValueError(f"ID {node['id']} 已存在")
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
        return CombineData("efe1", f"更新失败: {traceback.format_exc()}")


# 滑动背景管理
@app.get(f"{URLPREFIX}/getBanner", description="获取滑动展示列表配置内容")
def getBanner():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM banner"
                cursor.execute(sql)
                result = cursor.fetchall()
                if not result:
                    result = []
                return CombineData(0, "ok", result, "list")
    except:
        return CombineData("gte1", traceback.format_exc())


@app.post(f"{URLPREFIX}/setBanner", description="设置滑动展示列表内容-数据库操作")
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


@app.post(f"{URLPREFIX}/setBanner/upload", description="设置滑动展示列表内容-上传文件")
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


####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################

# 共享网盘业务


def load_qnap_config():
    # 根据实际路径调整
    config_path = os.path.join(os.path.dirname(__file__), "./config/qnap.json")
    try:
        with open(config_path, "r") as f:
            cfg = json.load(f)
            return cfg
    except FileNotFoundError:
        print(f"配置文件 {config_path} 未找到！")
        quit()
    except json.JSONDecodeError as e:
        print(f"配置文件解析失败: {str(e)}")
        quit()


QNAP_Config = load_qnap_config()
SidCache = None


def XMLToDict(xml_data):
    try:
        dict_data = xmltodict.parse(xml_data)
        return dict_data
    except Exception as err:
        print(err)
        return None


@lru_cache(maxsize=2)
def getDBSid():
    global SidCache
    try:
        if QNAP_Config["useDatabaseCache"]:
            with pymysql.connect(**mysqlConfig) as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM sharenetdiskcache WHERE `key`='sid'"
                    cursor.execute(sql)
                    reault = cursor.fetchall()
                    if len(reault) > 1:
                        # 删除多余的记录
                        sql = "DELETE FROM sharenetdiskcache WHERE `key`='sid'"
                        cursor.execute(sql)
                        conn.commit()
                        return None
                    if reault:
                        return reault[0]["value"]
                    else:
                        return None
        return SidCache
    except Exception as err:
        print(err)
        return None


@lru_cache(maxsize=2)
def getDBQtoken():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM sharenetdiskcache WHERE `key`='qtoken'"
                cursor.execute(sql)
                reault = cursor.fetchall()
                if reault:
                    return reault[0]["value"]
                else:
                    return None
    except Exception as err:
        print(err)
        return None


# 清理sid缓存
def update_sid_cache():
    getDBSid.cache_clear()


# 清理qtoken缓存
def update_qtoken_cache():
    getDBQtoken.cache_clear()


def qtokenGetSid(qtoken: str):
    global SidCache
    try:
        api = f"http://{QNAP_Config['ip']}:{QNAP_Config['port']}/cgi-bin/authLogin.cgi?user={QNAP_Config['username']}&qtoken={qtoken}&remme=1&duration=-1"
        print(api)
        requestResult = requests.get(api)
        JsonData = XMLToDict(requestResult.content)
        # 若解析失败
        if not JsonData:
            print(f"Response{requestResult.content}")
            return None
        # 判断应有字段是否存在
        QDocRoot = getValue(JsonData, "QDocRoot")
        if not QDocRoot:
            return None
        AuthPassed = getValue(QDocRoot, "authPassed")
        if not AuthPassed == 1:
            return None
        AuthSid = getValue(QDocRoot, "authSid")
        if not AuthPassed or not AuthSid:
            return None
        # 插入数据库
        if QNAP_Config["useDatabaseCache"]:
            with pymysql.connect(**mysqlConfig) as conn:
                with conn.cursor() as cursor:
                    SidSQL = "INSERT INTO sharenetdiskcache (`key`,`value`) VALUES ('sid',%s)"
                    cursor.execute(SidSQL, (AuthSid))
                    conn.commit()
        SidCache = AuthSid
        return AuthSid
    except Exception as err:
        print(err)
        return CombineData("NAS-LoginFail:5", "NAS设备登录失败，无法通过qtoken获取sid")


def refreshQtoken():
    qtoken = getDBQtoken()
    if not qtoken:
        sid = QNAP_Login()
    else:
        sid = qtokenGetSid(qtoken)
    if not sid:
        sid = QNAP_Login()
    if isinstance(sid, dict):
        print(sid)
        return sid
    # 插入数据库
    with pymysql.connect(**mysqlConfig) as conn:
        with conn.cursor() as cursor:
            removeAll = "DELETE FROM sharenetdiskcache WHERE `key`='sid'"
            cursor.execute(removeAll)
            SidSQL = "INSERT INTO sharenetdiskcache (`key`,`value`) VALUES ('sid',%s)"
            cursor.execute(SidSQL, (sid))
            conn.commit()


def checkSid(sid: str):
    try:
        if not sid:
            return False
        api = f"http://{QNAP_Config['ip']}:{QNAP_Config['port']}/cgi-bin/filemanager/utilRequest.cgi?func=check_sid&sid={sid}"
        requestResult = requests.get(api)
        JsonData = requestResult.json()
        status = getValue(JsonData, "status")
        if status == 1:
            return True
        return False
    except:
        return False


def QNAP_Login():
    global SidCache
    try:
        api = f"http://{QNAP_Config['ip']}:{QNAP_Config['port']}/cgi-bin/authLogin.cgi?user={QNAP_Config['username']}&pwd={QNAP_Config['password']}&service=1&device=ShareNetdiskServer&duraion=-1&remme=1"
        requestResult = requests.get(api)
        JsonData = XMLToDict(requestResult.content)
        # 若解析失败
        if not JsonData:
            print(f"Response{requestResult.content}")
            return CombineData("NAS-LoginFail:1", "NAS设备登录失败，因为返回值解析失败")
        # 判断应有字段是否存在
        QDocRoot = getValue(JsonData, "QDocRoot")
        if not QDocRoot:
            return CombineData(
                "NAS-LoginFail:2", "NAS设备登录失败，因为返回值缺少QDocRoot字段"
            )
        AuthPassed = getValue(QDocRoot, "authPassed")
        if not AuthPassed == "1":
            return CombineData("NAS-LoginFail:3", "NAS设备登录失败，因为设备端校验失败")
        Qtoken = getValue(QDocRoot, "qtoken")
        AuthSid = getValue(QDocRoot, "authSid")
        if not AuthPassed or not Qtoken or not AuthSid:
            return CombineData(
                "NAS-LoginFail:4", "NAS设备登录失败，因为返回值缺少必要字段"
            )
        # 插入数据库
        if QNAP_Config["useDatabaseCache"]:
            with pymysql.connect(**mysqlConfig) as conn:
                with conn.cursor() as cursor:
                    sql = "SELECT * FROM sharenetdiskcache WHERE `key`='qtoken'"
                    cursor.execute(sql)
                    reault = cursor.fetchall()
                    if len(reault) > 1:
                        sql = "DELETE FROM sharenetdiskcache WHERE `key`='qtoken'"
                        cursor.execute(sql)
                    QtokenSQL = "INSERT INTO sharenetdiskcache (`key`,`value`) VALUES ('qtoken',%s)"
                    cursor.execute(QtokenSQL, (Qtoken))
                    SidSQL = "INSERT INTO sharenetdiskcache (`key`,`value`) VALUES ('sid',%s)"
                    cursor.execute(SidSQL, (AuthSid))
                    conn.commit()
        SidCache = AuthSid
        return AuthSid
    except Exception as err:
        print(err)
        return CombineData("NAS-LoginFail:5", "NAS设备登录失败，无法完成认证流程")


# 获取sid，应该一步到位，先获取db，判断是否有效，无效则，产生通过qtoken获取，还是不行就重新登录
async def getSid():
    global SidCache
    try:
        # 优先使用缓存
        sid = SidCache
        if QNAP_Config["useDatabaseCache"]:
            sid = getDBSid()
        if sid and checkSid(sid):
            return sid
        # 是否通过qtoken刷新sid
        if QNAP_Config["useDoubleSid"]:
            if (qtoken := getDBQtoken()) and (newSid := qtokenGetSid(qtoken)):
                if checkSid(newSid):
                    # 插入数据库
                    update_sid_cache()
                    return newSid
        # 直接登录
        loginSid = QNAP_Login()
        if isinstance(loginSid, str):
            update_sid_cache()
            return loginSid
        return CombineData("NAS-LoginFail:0", "NAS设备登录失败，无法获取sid")
    except:
        return CombineData("NAS-LoginFail:5", "NAS设备登录失败，无法获取会话id")


@app.get(f"{URLPREFIX}/netdisk/getFileList")
async def getFileList(
    path: str = None,
    sort: str = "filename",
    dirs: str = "DESC",
):
    global SidCache
    try:
        sid = await getSid()
        if isinstance(sid, dict):
            return CombineData(sid["errcode"], sid["errmsg"])
        # sort = "mt"  # (filename/filesize/filetype/mt/privilege/owner/group)
        # dirs = "DESC"  # ASC / DESC
        filePath = "/媒体部/@共享网盘"
        if path:
            filePath += path
        params = {
            "func": "get_list",
            "sid": sid,
            "sort": sort,
            "dir": dirs,
            "path": filePath,
            "start": 0,
            "limit": 9999,
            "list_mode": "all",
        }
        api = f"http://{QNAP_Config['ip']}:{QNAP_Config['port']}/cgi-bin/filemanager/utilRequest.cgi?{urllib.parse.urlencode(params)}"
        async with httpx.AsyncClient() as client:
            response = await client.get(api)
            JsonData = response.json()
            # 忽略文件夹
            ignore_folders = ["_upload"]
            filtered = [
                item
                for item in JsonData.get("datas", [])
                if isinstance(item, dict) and not item.get("filename") in ignore_folders
            ]
            filePath = filePath.replace("/媒体部/@共享网盘", "")
            if filePath == "":
                filePath = "/"
            returnStatus = getValue(JsonData, "status")
            if returnStatus == 5:
                return CombineData(
                    "GetFileListFail:5",
                    "文件夹不存在",
                    {
                        "datas": [],
                        "filePath": filePath,
                        "currentPath": path,
                    },
                )
            elif returnStatus == 3:
                return CombineData(
                    "GetFileListFail:3",
                    "登录凭证有误",
                    {
                        "datas": [],
                        "filePath": filePath,
                        "currentPath": path,
                    },
                )
            JsonData["datas"] = filtered
            JsonData.update(
                {
                    "filePath": filePath,
                    "currentPath": path,
                    "ignoreFolders": ignore_folders,
                }
            )
            return CombineData(
                0,
                "ok",
                JsonData,
            )
        return CombineData(
            "GetFileListFail:0",
            f"获取文件列表失败，因为返回状态为{JsonData['status']}",
            {},
        )
    except Exception as err:
        print(err)
        return CombineData(
            "NAS-GetListFail:1", f"无法获取文件列表，{traceback.format_exc()}"
        )


@app.get(f"{URLPREFIX}/netdisk/getDownloadUrl")
async def downloadFile():
    sid = await getSid()
    if isinstance(sid, dict):
        return CombineData(sid["errcode"], sid["errmsg"])
    # &source_total=4
    # source_file=
    path = f"/cgi-bin/filemanager/utilRequest.cgi?func=download&sid={sid}"
    return CombineData(
        0,
        "ok",
        {
            "protocol": "http",
            "out_ip": QNAP_Config["out_ip"],
            "out_port": QNAP_Config["out_port"],
            "internal_ip": QNAP_Config["ip"],
            "internal_port": QNAP_Config["port"],
            "path": path,
            "source_path": "/媒体部/@共享网盘",
            "source_total": None,
            "source_file": None,
        },
    )


@app.get(f"{URLPREFIX}/netdisk/pick-up")
def pickUp(
    code: str = None,
):
    if not code:
        return CombineData("GetPickUpCodeFail:2", "取件码为空")
    # 查找取件码
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM netdisk WHERE `key`='pickUpCode' AND `value`= %s"
                cursor.execute(sql, (code))
                reault = cursor.fetchone()
                return CombineData(0, "ok", reault)
    except:
        return CombineData(
            "GetPickUpCodeFail:1", f"获取取件码失败，因为{traceback.format_exc()}"
        )


@app.get(f"{URLPREFIX}/netdisk/pick-up/getList")
def getPickUpList():
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM netdisk WHERE `key`='pickUpCode'"
                cursor.execute(sql)
                reault = cursor.fetchall()
                return CombineData(0, "ok", reault)
    except:
        return CombineData(
            "GetPickUpCodeListFail:1",
            f"获取取件码列表失败，因为{traceback.format_exc()}",
        )


@app.post(f"{URLPREFIX}/netdisk/pick-up/add")
def addPickUp(
    code: str = fastapi.Form(default=None),
    extra: str = fastapi.Form(default=""),
    type: str = fastapi.Form(default="redirect"),
):
    try:
        if not code or not extra or not type:
            return CombineData("AddPickUpCodeFail:1", "参数错误")
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "INSERT INTO netdisk (`key`,`value`,`extra`,`type`) VALUES ('pickUpCode',%s,%s,%s)"
                cursor.execute(sql, (code, extra, type))
                conn.commit()
                id = cursor.lastrowid
                return CombineData(
                    0, "ok", {"id": id, "code": code, "extra": extra, "type": type}
                )
    except:
        return CombineData(
            "AddPickUpCodeFail:1", f"添加取件码失败，因为{traceback.format_exc()}"
        )


@app.post(f"{URLPREFIX}/netdisk/pick-up/delete")
def deletePickUp(
    id: int = fastapi.Form(default=None),
):
    try:
        with pymysql.connect(**mysqlConfig) as conn:
            with conn.cursor() as cursor:
                sql = "DELETE FROM netdisk WHERE `id`=%s"
                cursor.execute(sql, (id))
                conn.commit()
                return CombineData(0, "ok", {"id": id})
    except:
        return CombineData(
            "DeletePickUpCodeFail:1", f"删除取件码失败，因为{traceback.format()}"
        )


# TODO
# 上传默认路径是_upload，这是非
# @app.get("/getUploadUrl")
# def getUploadUrl():
#     http://ip:8080/cgi-bin/filemanager/utilRequest.cgi?func=upload&type=standard&sid=xxxx&dest_path=/Public&overwrite=1&progress=-Public-test.zip
#     api = f"http://{QNAP_Config['ip']}:{QNAP_Config['port']}/cgi-bin/filemanager/utilRequest.cgi?func=upload&type=standard&sid={sid}&dest_path=/媒体部/@共享网盘/_upload&overwrite=0&progress=$%7Bprogress%7D"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=16485)
