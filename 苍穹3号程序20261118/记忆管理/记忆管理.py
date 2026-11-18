#记忆管理（记忆包的扫描、导入、导出；本模块不弹任何命令行输入，交互全部交给界面）
import os

import 公共状态


数据根目录 = "意识数据"

#9 类意识数据的规格
#  键：内部标识
#  名称：界面显示名
#  目录：意识数据下的子目录
#  前缀/后缀：文件名 = 前缀 + 包名 + 后缀
#  变量：对应 公共状态 里的变量（ART 单独处理）
类型规格 = [
    {"键": "喜",       "名称": "喜习惯列表",     "目录": os.path.join("情绪习惯列表", "喜习惯列表"), "前缀": "喜习惯列表",     "后缀": ".txt", "变量": "haphablist"},
    {"键": "哀",       "名称": "哀习惯列表",     "目录": os.path.join("情绪习惯列表", "哀习惯列表"), "前缀": "哀习惯列表",     "后缀": ".txt", "变量": "sadhablist"},
    {"键": "行为空间", "名称": "行为空间",       "目录": "行为空间",         "前缀": "行为空间",       "后缀": ".txt", "变量": "allact"},
    {"键": "行为习惯", "名称": "行为习惯列表",   "目录": "行为习惯列表",     "前缀": "行为习惯列表",   "后缀": ".txt", "变量": "acthablist"},
    {"键": "自传体",   "名称": "自传体记忆",     "目录": "自传体记忆",       "前缀": "自传体记忆",     "后缀": ".txt", "变量": "memorylist"},
    {"键": "状态转移", "名称": "状态转移概率矩阵","目录": "状态转移概率矩阵", "前缀": "状态转移概率矩阵","后缀": ".txt", "变量": "transmatrix"},
    {"键": "词典",     "名称": "词典",           "目录": "词典",             "前缀": "词典",           "后缀": ".txt", "变量": "dictionary"},
    {"键": "词转移",   "名称": "词转移概率矩阵", "目录": "词转移概率矩阵",   "前缀": "词转移概率矩阵", "后缀": ".txt", "变量": "word_trans_matrix"},
    {"键": "ART",      "名称": "ART原型",        "目录": "ART",              "前缀": "ART",            "后缀": ".csv", "变量": None},
]

# ---------------- 包名 ----------------

def 规范化包名(版本号):
    """版本号（纯数字）→ 包名；不合法时返回 (None, 原因)。
    包名就是版本号本身，与旧版命令行只输版本号的习惯保持一致。"""
    版本号 = (版本号 or "").strip()
    if not 版本号:
        return None, "请填写版本号"
    if not (版本号.isascii() and 版本号.isdigit()):
        return None, "版本号必须是数字"
    return 版本号, ""


def 建议版本号():
    """纯数字包名里已有的最大版本号 + 1（用于导出界面预填，避免误覆盖）"""
    最大 = 0
    for 包名 in 列出记忆包():
        if 包名.isascii() and 包名.isdigit():
            最大 = max(最大, int(包名))
    return str(最大 + 1)


# ---------------- 路径与统计 ----------------

def 默认路径(规格, 包名):
    return os.path.join(数据根目录, 规格["目录"], 规格["前缀"] + 包名 + 规格["后缀"])


def _读行(路径):
    with open(路径, "r", encoding="utf-8-sig") as 文件:
        return [行.strip() for 行 in 文件]


def _非空行数(路径):
    return sum(1 for 行 in _读行(路径) if 行)


def _ART形状(路径):
    with open(路径, "r", encoding="utf-8-sig") as 文件:
        行列表 = [行 for 行 in 文件 if 行.strip()]
    if not 行列表:
        return 0, 0
    列数 = len([字段 for 字段 in 行列表[0].strip().split(",") if 字段.strip()])
    return len(行列表), 列数


def 条数(路径, 键):
    """文件不存在返回 None；ART 返回“行×列”；其余返回非空行数"""
    if not os.path.exists(路径):
        return None
    if 键 == "ART":
        行数, 列数 = _ART形状(路径)
        return "%d×%d" % (行数, 列数)
    return _非空行数(路径)


def 列出记忆包():
    """扫描 意识数据，返回 {包名: {"路径": {键: 路径}, "时间": 最后修改时间}}"""
    结果 = {}
    for 规格 in 类型规格:
        目录 = os.path.join(数据根目录, 规格["目录"])
        if not os.path.isdir(目录):
            continue
        for 文件名 in os.listdir(目录):
            if not (文件名.startswith(规格["前缀"]) and 文件名.endswith(规格["后缀"])):
                continue
            包名 = 文件名[len(规格["前缀"]):len(文件名) - len(规格["后缀"])]
            if not 包名:
                continue
            路径 = os.path.join(目录, 文件名)
            条目 = 结果.setdefault(包名, {"路径": {}, "时间": 0.0})
            条目["路径"][规格["键"]] = 路径
            try:
                条目["时间"] = max(条目["时间"], os.path.getmtime(路径))
            except OSError:
                pass
    return 结果


def 包内文件(包名, 覆盖路径=None):
    """导入用：逐类列出路径、是否存在、文件里的条数"""
    覆盖路径 = 覆盖路径 or {}
    结果 = []
    for 规格 in 类型规格:
        路径 = 覆盖路径.get(规格["键"]) or 默认路径(规格, 包名)
        存在 = os.path.exists(路径)
        结果.append({
            "键": 规格["键"],
            "名称": 规格["名称"],
            "路径": 路径,
            "存在": 存在,
            "条数": 条数(路径, 规格["键"]) if 存在 else None,
        })
    return 结果


def 导出预览(包名, 覆盖路径=None):
    """导出用：逐类列出目标路径、内存里条数、将新建还是覆盖"""
    覆盖路径 = 覆盖路径 or {}
    结果 = []
    for 规格 in 类型规格:
        键 = 规格["键"]
        路径 = 覆盖路径.get(键) or 默认路径(规格, 包名)
        存在 = os.path.exists(路径)
        if 键 == "ART":
            if 公共状态.art_model is None:
                内存条数, 状态 = "—", "跳过（模型未加载）"
            else:
                原型 = 公共状态.art_model.prototypes
                内存条数, 状态 = "%d×%d" % (len(原型), len(原型[0]) if len(原型) else 0), ("覆盖" if 存在 else "新建")
        else:
            内存条数 = len(getattr(公共状态, 规格["变量"], []) or [])
            状态 = "覆盖" if 存在 else "新建"
        结果.append({
            "键": 键,
            "名称": 规格["名称"],
            "路径": 路径,
            "存在": 存在,
            "条数": 内存条数,
            "状态": 状态,
        })
    return 结果


# ---------------- 解析 ----------------

def _概念列表(字段):
    return [片段 for 片段 in 字段.split("。") if 片段]


def _数字(字段):
    try:
        return float(字段)
    except (TypeError, ValueError):
        return None


def _整数(字段):
    数值 = _数字(字段)
    if 数值 is None or 数值 != int(数值):
        return None
    return int(数值)


def _解析_情绪(路径):
    列表, 坏行 = [], []
    for 行号, 行 in enumerate(_读行(路径), 1):
        if not 行:
            continue
        段 = 行.split("；")
        if len(段) != 2:
            坏行.append((行号, 行, "应为 2 段，实际 %d 段" % len(段)))
            continue
        强度 = _数字(段[1])
        if 强度 is None:
            坏行.append((行号, 行, "情绪强度不是数字"))
            continue
        列表.append([_概念列表(段[0]), int(强度) if 强度 == int(强度) else 强度])
    return 列表, 坏行


def _解析_行为空间(路径):
    return [行 for 行 in _读行(路径) if 行], []


def _解析_三列(路径):
    """行为习惯、自传体记忆：概念；概念；数值"""
    列表, 坏行 = [], []
    for 行号, 行 in enumerate(_读行(路径), 1):
        if not 行:
            continue
        段 = 行.split("；")
        if len(段) != 3:
            坏行.append((行号, 行, "应为 3 段，实际 %d 段" % len(段)))
            continue
        数值 = _数字(段[2])
        if 数值 is None:
            坏行.append((行号, 行, "价值不是数字"))
            continue
        列表.append([_概念列表(段[0]), _概念列表(段[1]), 数值])
    return 列表, 坏行


def _解析_状态转移(路径):
    列表, 坏行 = [], []
    for 行号, 行 in enumerate(_读行(路径), 1):
        if not 行:
            continue
        段 = 行.split("；")
        转移 = [_概念列表(段[0])]
        错误 = None
        for 后继字段 in 段[1:]:
            子段 = 后继字段.split("、")
            if len(子段) != 3:
                错误 = "转移应为 3 段，实际 %d 段" % len(子段)
                break
            概率 = _数字(子段[1])
            次数 = _整数(子段[2])
            if 概率 is None or 次数 is None:
                错误 = "转移的概率或次数不是数字"
                break
            转移.append([_概念列表(子段[0]), 概率, 次数])
        if 错误:
            坏行.append((行号, 行, 错误))
            continue
        列表.append(转移)
    return 列表, 坏行


def _解析_词典(路径):
    列表, 坏行 = [], []
    for 行号, 行 in enumerate(_读行(路径), 1):
        if not 行:
            continue
        段 = 行.split("；")
        if len(段) != 3:
            坏行.append((行号, 行, "应为 3 段，实际 %d 段" % len(段)))
            continue
        权重 = _数字(段[2])
        if 权重 is None:
            坏行.append((行号, 行, "权重不是数字"))
            continue
        列表.append([段[0], 段[1], 权重])
    return 列表, 坏行


解析器 = {
    "喜": _解析_情绪,
    "哀": _解析_情绪,
    "行为空间": _解析_行为空间,
    "行为习惯": _解析_三列,
    "自传体": _解析_三列,
    "状态转移": _解析_状态转移,
    "词典": _解析_词典,
    "词转移": _解析_词典,
}


# ---------------- 序列化 ----------------

def _数转文本(数值):
    if isinstance(数值, bool):
        return str(int(数值))
    if isinstance(数值, int):
        return str(数值)
    数值 = float(数值)
    if 数值 == int(数值):
        return str(int(数值))
    return repr(数值)#最短且能精确回读的写法


def _概念字段(概念):
    return "".join(str(单个) + "。" for 单个 in 概念)


def _序列化_情绪(列表):
    return "".join(_概念字段(概念) + "；" + _数转文本(值) + "\n" for 概念, 值 in 列表)


def _序列化_行为空间(列表):
    return "".join(str(行为) + "\n" for 行为 in 列表)


def _序列化_三列(列表):
    return "".join(_概念字段(前) + "；" + _概念字段(后) + "；" + _数转文本(值) + "\n"
                   for 前, 后, 值 in 列表)


def _序列化_状态转移(列表):
    输出 = ""
    for 转移 in 列表:
        行 = _概念字段(转移[0])
        for 后继 in 转移[1:]:
            行 += "；" + _概念字段(后继[0]) + "、" + _数转文本(后继[1]) + "、" + _数转文本(后继[2])
        输出 += 行 + "\n"
    return 输出


def _序列化_词典(列表):
    return "".join(str(词) + "；" + str(义) + "；" + _数转文本(权重) + "\n"
                   for 词, 义, 权重 in 列表)


def _序列化_ART(原型):
    行文本 = []
    for 行 in 原型:
        行文本.append(",".join("%.10g" % float(数值) for 数值 in 行))
    if not 行文本:
        return ""
    return "\n".join(行文本) + "\n"


序列化器 = {
    "喜": _序列化_情绪,
    "哀": _序列化_情绪,
    "行为空间": _序列化_行为空间,
    "行为习惯": _序列化_三列,
    "自传体": _序列化_三列,
    "状态转移": _序列化_状态转移,
    "词典": _序列化_词典,
    "词转移": _序列化_词典,
}


# ---------------- 导入 / 导出 ----------------

def 导入记忆包(包名, 覆盖路径=None, 跳过坏行=False, 提交=True):
    """读取一个记忆包。
    提交=True 且没有任何坏行时，才写入 公共状态（保证不会导入半个包）。
    返回 (成功, 报告, 错误列表)"""
    覆盖路径 = 覆盖路径 or {}
    暂存 = {}
    报告 = []
    错误 = []

    for 规格 in 类型规格:
        键 = 规格["键"]
        if 键 == "ART":
            continue
        路径 = 覆盖路径.get(键) or 默认路径(规格, 包名)
        if not os.path.exists(路径):
            暂存[规格["变量"]] = []
            报告.append({"键": 键, "名称": 规格["名称"], "路径": 路径,
                         "状态": "缺失（按空表导入）", "条数": 0, "坏行": []})
            continue
        列表, 坏行 = 解析器[键](路径)
        if 坏行 and not 跳过坏行:
            错误.append({"键": 键, "名称": 规格["名称"], "路径": 路径, "坏行": 坏行})
        暂存[规格["变量"]] = 列表
        报告.append({
            "键": 键,
            "名称": 规格["名称"],
            "路径": 路径,
            "状态": "已读取" if not 坏行 else "含坏行（已跳过 %d 行）" % len(坏行),
            "条数": len(列表),
            "坏行": 坏行,
        })

    if 错误:
        return False, 报告, 错误
    if not 提交:
        return True, 报告, []

    for 变量, 列表 in 暂存.items():
        setattr(公共状态, 变量, 列表)

    公共状态.当前记忆包 = 包名
    #ART 由 知觉分类模块 按这个路径加载
    公共状态.art原型路径 = 覆盖路径.get("ART") or 默认路径(
        [规格 for 规格 in 类型规格 if 规格["键"] == "ART"][0], 包名)
    return True, 报告, []


def 导出记忆包(包名, 覆盖路径=None):
    """把内存里的 9 类数据写成一个记忆包（两阶段写出，避免半个包）。
    返回 (成功, 报告, 错误信息)"""
    覆盖路径 = 覆盖路径 or {}
    待写 = []
    报告 = []

    for 规格 in 类型规格:
        键 = 规格["键"]
        路径 = 覆盖路径.get(键) or 默认路径(规格, 包名)
        if 键 == "ART":
            if 公共状态.art_model is None:
                报告.append({"键": 键, "名称": 规格["名称"], "路径": 路径,
                             "状态": "跳过（模型未加载）", "条数": "—"})
                continue
            内容 = _序列化_ART(公共状态.art_model.prototypes)
            if not 内容:
                报告.append({"键": 键, "名称": 规格["名称"], "路径": 路径,
                             "状态": "跳过（无原型）", "条数": "—"})
                continue
        else:
            内容 = 序列化器[键](getattr(公共状态, 规格["变量"], []) or [])
        待写.append((路径, 内容, 键, 规格["名称"]))
        报告.append({
            "键": 键,
            "名称": 规格["名称"],
            "路径": 路径,
            "状态": "覆盖" if os.path.exists(路径) else "新建",
            "条数": 内容.count("\n"),
        })

    临时文件 = []
    try:
        for 路径, 内容, 键, 名称 in 待写:
            目录 = os.path.dirname(路径)
            if 目录:
                os.makedirs(目录, exist_ok=True)
            临时 = 路径 + ".tmp"
            with open(临时, "w", encoding="utf-8", newline="") as 文件:
                文件.write(内容)
            临时文件.append((临时, 路径))
    except Exception as 异常:
        for 临时, 路径 in 临时文件:
            try:
                os.remove(临时)
            except OSError:
                pass
        return False, 报告, str(异常)

    for 临时, 路径 in 临时文件:
        os.replace(临时, 路径)

    公共状态.当前记忆包 = 包名
    return True, 报告, ""
