#记忆管理（记忆的扫描、导入、导出；本模块不弹任何命令行输入，交互全部交给界面）
import os

import 公共状态


DATA_ROOT = "意识数据"

#自动保存固定用这个版本号：每回合覆盖，只保留最近一回合，不会动用户导入的版本
AUTO_SAVE_NAME = "自动保存"

#9 类意识数据的规格
#  key：内部标识
#  name：界面显示名
#  dir：意识数据下的子目录
#  prefix/suffix：文件名 = prefix + 版本号 + suffix
#  var：对应 公共状态 里的变量（ART 单独处理）
TYPE_SPECS = [
    {"key": "喜",       "name": "喜习惯列表",      "dir": os.path.join("情绪习惯列表", "喜习惯列表"), "prefix": "喜习惯列表",      "suffix": ".txt", "var": "haphablist"},
    {"key": "哀",       "name": "哀习惯列表",      "dir": os.path.join("情绪习惯列表", "哀习惯列表"), "prefix": "哀习惯列表",      "suffix": ".txt", "var": "sadhablist"},
    {"key": "行为空间", "name": "行为空间",        "dir": "行为空间",         "prefix": "行为空间",        "suffix": ".txt", "var": "allact"},
    {"key": "行为习惯", "name": "行为习惯列表",    "dir": "行为习惯列表",     "prefix": "行为习惯列表",    "suffix": ".txt", "var": "acthablist"},
    {"key": "自传体",   "name": "自传体记忆",      "dir": "自传体记忆",       "prefix": "自传体记忆",      "suffix": ".txt", "var": "memorylist"},
    {"key": "状态转移", "name": "状态转移概率矩阵", "dir": "状态转移概率矩阵", "prefix": "状态转移概率矩阵", "suffix": ".txt", "var": "transmatrix"},
    {"key": "词典",     "name": "词典",            "dir": "词典",             "prefix": "词典",            "suffix": ".txt", "var": "dictionary"},
    {"key": "词转移",   "name": "词转移概率矩阵",  "dir": "词转移概率矩阵",   "prefix": "词转移概率矩阵",   "suffix": ".txt", "var": "word_trans_matrix"},
    {"key": "ART",      "name": "ART原型",         "dir": "ART",              "prefix": "ART",             "suffix": ".csv", "var": None},
]

# ---------------- 版本号 ----------------

ILLEGAL_CHARS = set('\\/:*?"<>|')


def normalize_version(version):
    """版本号（文件名里“前缀”和扩展名之间的部分）→ 版本号；不合法时返回 (None, 原因)。
    沿用原有意识数据的命名习惯：100、研究者_v1、螺旋藻v2_2 都可以。"""
    version = (version or "").strip()
    if not version:
        return None, "请填写版本号"
    for char in version:
        if char in ILLEGAL_CHARS:
            return None, "版本号中不能包含 \\ / : * ? \" < > | 等字符"
    return version, ""


# ---------------- 路径与统计 ----------------

def default_path(spec, memory):
    return os.path.join(DATA_ROOT, spec["dir"], spec["prefix"] + memory + spec["suffix"])


def _read_lines(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return [hang.strip() for hang in file]


def _count_nonempty(path):
    return sum(1 for hang in _read_lines(path) if hang)


def _art_shape(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        rows = [hang for hang in file if hang.strip()]
    if not rows:
        return 0, 0
    columns = len([field for field in rows[0].strip().split(",") if field.strip()])
    return len(rows), columns


def count_rows(path, key):
    """文件不存在返回 None；ART 返回“行×列”；其余返回非空行数"""
    if not os.path.exists(path):
        return None
    if key == "ART":
        rows, columns = _art_shape(path)
        return "%d×%d" % (rows, columns)
    return _count_nonempty(path)


def list_memories():
    """扫描 意识数据，返回 {版本号: {"paths": {key: 路径}, "mtime": 最后修改时间}}"""
    result = {}
    for spec in TYPE_SPECS:
        folder = os.path.join(DATA_ROOT, spec["dir"])
        if not os.path.isdir(folder):
            continue
        for filename in os.listdir(folder):
            if not (filename.startswith(spec["prefix"]) and filename.endswith(spec["suffix"])):
                continue
            memory = filename[len(spec["prefix"]):len(filename) - len(spec["suffix"])]
            if not memory:
                continue
            path = os.path.join(folder, filename)
            entry = result.setdefault(memory, {"paths": {}, "mtime": 0.0})
            entry["paths"][spec["key"]] = path
            try:
                entry["mtime"] = max(entry["mtime"], os.path.getmtime(path))
            except OSError:
                pass
    return result


def memory_files(memory, overrides=None):
    """导入用：逐类列出路径、是否存在、文件里的条数"""
    overrides = overrides or {}
    result = []
    for spec in TYPE_SPECS:
        path = overrides.get(spec["key"]) or default_path(spec, memory)
        exists = os.path.exists(path)
        result.append({
            "key": spec["key"],
            "name": spec["name"],
            "path": path,
            "exists": exists,
            "count": count_rows(path, spec["key"]) if exists else None,
        })
    return result


def export_preview(memory, overrides=None):
    """导出用：逐类列出目标路径、内存里条数、将新建还是覆盖"""
    overrides = overrides or {}
    result = []
    for spec in TYPE_SPECS:
        key = spec["key"]
        path = overrides.get(key) or default_path(spec, memory)
        exists = os.path.exists(path)
        if key == "ART":
            if 公共状态.art_model is None:
                count, status = "—", "跳过（模型未加载）"
            else:
                prototypes = 公共状态.art_model.prototypes
                count = "%d×%d" % (len(prototypes), len(prototypes[0]) if len(prototypes) else 0)
                status = "覆盖" if exists else "新建"
        else:
            count = len(getattr(公共状态, spec["var"], []) or [])
            status = "覆盖" if exists else "新建"
        result.append({
            "key": key,
            "name": spec["name"],
            "path": path,
            "exists": exists,
            "count": count,
            "status": status,
        })
    return result


# ---------------- 解析 ----------------

def _concept_list(field):
    return [part for part in field.split("。") if part]


def _to_number(field):
    try:
        return float(field)
    except (TypeError, ValueError):
        return None


def _to_int(field):
    number = _to_number(field)
    if number is None or number != int(number):
        return None
    return int(number)


def _parse_emotion(path):
    items, bad_lines = [], []
    for line_no, hang in enumerate(_read_lines(path), 1):
        if not hang:
            continue
        parts = hang.split("；")
        if len(parts) != 2:
            bad_lines.append((line_no, hang, "应为 2 段，实际 %d 段" % len(parts)))
            continue
        strength = _to_number(parts[1])
        if strength is None:
            bad_lines.append((line_no, hang, "情绪强度不是数字"))
            continue
        items.append([_concept_list(parts[0]), int(strength) if strength == int(strength) else strength])
    return items, bad_lines


def _parse_action_space(path):
    return [line for line in _read_lines(path) if line], []


def _parse_three_columns(path):
    """行为习惯、自传体记忆：概念；概念；数值"""
    items, bad_lines = [], []
    for line_no, hang in enumerate(_read_lines(path), 1):
        if not hang:
            continue
        parts = hang.split("；")
        if len(parts) != 3:
            bad_lines.append((line_no, hang, "应为 3 段，实际 %d 段" % len(parts)))
            continue
        v = _to_number(parts[2])
        if v is None:
            bad_lines.append((line_no, hang, "价值不是数字"))
            continue
        items.append([_concept_list(parts[0]), _concept_list(parts[1]), v])
    return items, bad_lines


def _parse_transition(path):
    items, bad_lines = [], []
    for line_no, hang in enumerate(_read_lines(path), 1):
        if not hang:
            continue
        parts = hang.split("；")
        transition = [_concept_list(parts[0])]
        error = None
        for successor_field in parts[1:]:
            sub_parts = successor_field.split("、")
            if len(sub_parts) != 3:
                error = "转移应为 3 段，实际 %d 段" % len(sub_parts)
                break
            chance = _to_number(sub_parts[1])
            times = _to_int(sub_parts[2])
            if chance is None or times is None:
                error = "转移的概率或次数不是数字"
                break
            transition.append([_concept_list(sub_parts[0]), chance, times])
        if error:
            bad_lines.append((line_no, hang, error))
            continue
        items.append(transition)
    return items, bad_lines


def _parse_dictionary(path):
    items, bad_lines = [], []
    for line_no, hang in enumerate(_read_lines(path), 1):
        if not hang:
            continue
        parts = hang.split("；")
        if len(parts) != 3:
            bad_lines.append((line_no, hang, "应为 3 段，实际 %d 段" % len(parts)))
            continue
        weight = _to_number(parts[2])
        if weight is None:
            bad_lines.append((line_no, hang, "权重不是数字"))
            continue
        items.append([parts[0], parts[1], weight])
    return items, bad_lines


PARSERS = {
    "喜": _parse_emotion,
    "哀": _parse_emotion,
    "行为空间": _parse_action_space,
    "行为习惯": _parse_three_columns,
    "自传体": _parse_three_columns,
    "状态转移": _parse_transition,
    "词典": _parse_dictionary,
    "词转移": _parse_dictionary,
}


# ---------------- 序列化 ----------------

def _number_text(value):
    if isinstance(value, bool):
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    value = float(value)
    if value == int(value):
        return str(int(value))
    return repr(value)#最短且能精确回读的写法


def _concept_field(concept):
    return "".join(str(item) + "。" for item in concept)


def _serialize_emotion(items):
    return "".join(_concept_field(concept) + "；" + _number_text(value) + "\n"
                   for concept, value in items)


def _serialize_action_space(items):
    return "".join(str(action) + "\n" for action in items)


def _serialize_three_columns(items):
    return "".join(_concept_field(first) + "；" + _concept_field(second) + "；" + _number_text(v) + "\n"
                   for first, second, v in items)


def _serialize_transition(items):
    content = ""
    for transition in items:
        line = _concept_field(transition[0])
        for successor in transition[1:]:
            line += "；" + _concept_field(successor[0]) + "、" + _number_text(successor[1]) + "、" + _number_text(successor[2])
        content += line + "\n"
    return content


def _serialize_dictionary(items):
    return "".join(str(word) + "；" + str(meaning) + "；" + _number_text(weight) + "\n"
                   for word, meaning, weight in items)


def _serialize_art(prototypes):
    lines = []
    for row in prototypes:
        lines.append(",".join("%.10g" % float(value) for value in row))
    if not lines:
        return ""
    return "\n".join(lines) + "\n"


SERIALIZERS = {
    "喜": _serialize_emotion,
    "哀": _serialize_emotion,
    "行为空间": _serialize_action_space,
    "行为习惯": _serialize_three_columns,
    "自传体": _serialize_three_columns,
    "状态转移": _serialize_transition,
    "词典": _serialize_dictionary,
    "词转移": _serialize_dictionary,
}


# ---------------- 导入 / 导出 ----------------

def import_memory(memory, overrides=None, skip_bad_lines=False, commit=True):
    """读取一个记忆。
    commit=True 且没有任何坏行时，才写入 公共状态（保证不会导入半个包）。
    返回 (成功, 报告, 错误列表)"""
    overrides = overrides or {}
    staged = {}
    report = []
    errors = []

    for spec in TYPE_SPECS:
        key = spec["key"]
        if key == "ART":
            continue
        path = overrides.get(key) or default_path(spec, memory)
        if not os.path.exists(path):
            staged[spec["var"]] = []
            report.append({"key": key, "name": spec["name"], "path": path,
                           "status": "缺失（按空表导入）", "count": 0, "bad_lines": []})
            continue
        items, bad_lines = PARSERS[key](path)
        if bad_lines and not skip_bad_lines:
            errors.append({"key": key, "name": spec["name"], "path": path, "bad_lines": bad_lines})
        staged[spec["var"]] = items
        report.append({
            "key": key,
            "name": spec["name"],
            "path": path,
            "status": "已读取" if not bad_lines else "含坏行（跳过 %d 行）" % len(bad_lines),
            "count": len(items),
            "bad_lines": bad_lines,
        })

    if errors:
        return False, report, errors
    if not commit:
        return True, report, []

    for var, items in staged.items():
        setattr(公共状态, var, items)

    公共状态.current_memory = memory
    #ART 由 知觉分类模块 按这个路径加载
    公共状态.art_path = overrides.get("ART") or default_path(
        [spec for spec in TYPE_SPECS if spec["key"] == "ART"][0], memory)
    return True, report, []


def export_memory(memory, overrides=None):
    """把内存里的 9 类数据写成一个记忆（两阶段写出，避免半个包）。
    返回 (成功, 报告, 错误信息)"""
    overrides = overrides or {}
    pending = []
    report = []

    for spec in TYPE_SPECS:
        key = spec["key"]
        path = overrides.get(key) or default_path(spec, memory)
        if key == "ART":
            if 公共状态.art_model is None:
                report.append({"key": key, "name": spec["name"], "path": path,
                               "status": "跳过（模型未加载）", "count": "—"})
                continue
            content = _serialize_art(公共状态.art_model.prototypes)
            if not content:
                report.append({"key": key, "name": spec["name"], "path": path,
                               "status": "跳过（无原型）", "count": "—"})
                continue
        else:
            content = SERIALIZERS[key](getattr(公共状态, spec["var"], []) or [])
        pending.append((path, content, key, spec["name"]))
        report.append({
            "key": key,
            "name": spec["name"],
            "path": path,
            "status": "覆盖" if os.path.exists(path) else "新建",
            "count": content.count("\n"),
        })

    temp_files = []
    try:
        for path, content, key, name in pending:
            folder = os.path.dirname(path)
            if folder:
                os.makedirs(folder, exist_ok=True)
            temp = path + ".tmp"
            with open(temp, "w", encoding="utf-8", newline="") as file:
                file.write(content)
            temp_files.append((temp, path))
    except Exception as error:
        for temp, path in temp_files:
            try:
                os.remove(temp)
            except OSError:
                pass
        return False, report, str(error)

    for temp, path in temp_files:
        os.replace(temp, path)

    公共状态.current_memory = memory
    return True, report, ""
