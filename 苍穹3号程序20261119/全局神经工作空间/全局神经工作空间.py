#全局神经工作空间GW
import copy
import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog

import 公共状态
import 记忆管理.记忆管理 as 记忆管理


#可视化界面初始化
def 初始化界面():
    root=Tk()
    root.title("苍穹3号")
    root.geometry('1000x800')


    lbGW=Label(root,text="全局神经工作空间GW")
    lbGW.grid(row=0,column=1)



    lbsenpart=Label(root,text="知觉分类模块")
    lbsenpart.grid(row=1,column=0)

    lbinputsentence=Label(root,text="输入句（一句自然语言（由句号分隔的））")
    lbinputsentence.grid(row=2,column=0)
    entinputsentence=Entry(root,width=40)
    entinputsentence.grid(row=3,column=0)

    varcbinputsentence1=IntVar()
    varcbinputsentence2=IntVar()
    cbinputsentence1=Checkbutton(root,text="输入句准备完毕",variable=varcbinputsentence1,onvalue=1,offvalue=0)
    cbinputsentence1.grid(row=4,column=0)
    cbinputsentence2=Checkbutton(root,text="提交输入句",variable=varcbinputsentence2,onvalue=1,offvalue=0)
    cbinputsentence2.grid(row=5,column=0)

    lbinputsen=Label(root,text="输入当前知觉概念列表,各知觉概念之间用空格隔开。（若输入：想+某行为，系统将会输出该行为）")
    lbinputsen.grid(row=6,column=0)
    entinputsen=Entry(root,width=40)
    entinputsen.grid(row=7,column=0)

    varcbinputsen1=IntVar()
    varcbinputsen2=IntVar()
    cbinputsen1=Checkbutton(root,text="知觉概念列表准备完毕",variable=varcbinputsen1,onvalue=1,offvalue=0)
    cbinputsen1.grid(row=8,column=0)
    cbinputsen2=Checkbutton(root,text="提交知觉概念列表",variable=varcbinputsen2,onvalue=1,offvalue=0)
    cbinputsen2.grid(row=9,column=0)

    lbsenlist=Label(root,text="知觉概念列表：扩展前（当前从环境中获得的知觉内容）")
    lbsenlist.grid(row=10,column=0)
    txsenlist=Text(root,width=40,height=5)
    txsenlist.grid(row=11,column=0)

    lbextended_senlist=Label(root,text="知觉概念列表：扩展后（既是注意力选择后的结果，也模拟工作记忆的内容）")
    lbextended_senlist.grid(row=12,column=0)
    txextended_senlist=Text(root,width=40,height=5)
    txextended_senlist.grid(row=13,column=0)


    lbmemorypart=Label(root,text="记忆模块")
    lbmemorypart.grid(row=1,column=1)
    lbmemorylist=Label(root,text="自传体记忆")
    lbmemorylist.grid(row=2,column=1)
    txmemorylist=Text(root,width=20,height=5)
    txmemorylist.grid(row=3,column=1)



    lbvalpart=Label(root,text="价值分类记忆与价值系统")
    lbvalpart.grid(row=1,column=2)
    lbhapsum=Label(root,text="喜的值:")
    lbhapsum.grid(row=2,column=2)
    lbsadsum=Label(root,text="哀的值:")
    lbsadsum.grid(row=3,column=2)
    lbvsum=Label(root,text="总价值:")
    lbvsum.grid(row=4,column=2)
    lbhapsadhablist=Label(root,text="情绪习惯列表")
    lbhapsadhablist.grid(row=5,column=2)
    lbhaphablist=Label(root,text="喜习惯列表")
    lbhaphablist.grid(row=6,column=2)
    txhaphablist=Text(root,width=20,height=5)
    txhaphablist.grid(row=7,column=2)
    lbsadhablist=Label(root,text="哀习惯列表")
    lbsadhablist.grid(row=8,column=2)
    txsadhablist=Text(root,width=20,height=5)
    txsadhablist.grid(row=9,column=2)



    lbworldmodel=Label(root,text="世界模型")
    lbworldmodel.grid(row=4,column=1)
    lbtransmatrix=Label(root,text="状态转移概率矩阵")
    lbtransmatrix.grid(row=5,column=1)
    txtransmatrix=Text(root,width=40,height=5)
    txtransmatrix.grid(row=6,column=1)
    lbpredict_state_chance=Label(root,text="接下来各状态发生概率为：")
    lbpredict_state_chance.grid(row=7,column=1)
    txpredict_state_chance=Text(root,width=20,height=5)
    txpredict_state_chance.grid(row=8,column=1)
    lbpredict_max_state=Label(root,text="接下来最可能发生的状态为:")
    lbpredict_max_state.grid(row=9,column=1)
    lbpredict_max_chance=Label(root,text="发生概率为:")
    lbpredict_max_chance.grid(row=10,column=1)



    lbactpart=Label(root,text="行为与计划模块")
    lbactpart.grid(row=1,column=3)
    lbacthablist=Label(root,text="行为习惯列表")
    lbacthablist.grid(row=2,column=3)
    txacthablist=Text(root,width=40,height=10)
    txacthablist.grid(row=3,column=3)
    lbactlist=Label(root,text="当前精神图景下最优行为：")
    lbactlist.grid(row=4,column=3)
    txactlist=Text(root,width=40,height=5)
    txactlist.grid(row=5,column=3)
    lbcounts=Label(root,text="行为的分解次数：（输入一个>=0的整数）")
    lbcounts.grid(row=6,column=3)
    entcounts=Entry(root,width=10)
    entcounts.grid(row=7,column=3)
    varcbcounts1=IntVar()
    varcbcounts2=IntVar()
    cbcounts1=Checkbutton(root,text="行为分解次数输入完毕",variable=varcbcounts1,onvalue=1,offvalue=0)
    cbcounts1.grid(row=8,column=3)
    cbcounts2=Checkbutton(root,text="提交行为分解次数",variable=varcbcounts2,onvalue=1,offvalue=0)
    cbcounts2.grid(row=9,column=3)
    lbact_detail_list=Label(root,text="行为细化后：")
    lbact_detail_list.grid(row=10,column=3)
    txact_detail_list=Text(root,width=40,height=5)
    txact_detail_list.grid(row=11,column=3)
    lbnloutput=Label(root,text="自然语言输出：")
    lbnloutput.grid(row=12,column=3)
    txnloutput=Text(root,width=40,height=3)
    txnloutput.grid(row=13,column=3)

    #自动保存常开：固定写到记忆「自动保存」，只保留最近一回合，导入时选它即可恢复
    lb_autosave=Label(root,text="每回合自动保存到版本号：自动保存",fg="#666")
    lb_autosave.grid(row=12,column=1)
    btn_memory=Button(root,text="记忆…（导出）",command=lambda: open_memory_window("导出"))
    btn_memory.grid(row=13,column=1)


    #将控制流中需要访问的控件存入公共状态
    公共状态.root=root
    公共状态.entinputsentence=entinputsentence
    公共状态.varcbinputsentence1=varcbinputsentence1
    公共状态.varcbinputsentence2=varcbinputsentence2
    公共状态.entinputsen=entinputsen
    公共状态.varcbinputsen1=varcbinputsen1
    公共状态.varcbinputsen2=varcbinputsen2
    公共状态.txsenlist=txsenlist
    公共状态.txextended_senlist=txextended_senlist
    公共状态.txmemorylist=txmemorylist
    公共状态.lbhapsum=lbhapsum
    公共状态.lbsadsum=lbsadsum
    公共状态.lbvsum=lbvsum
    公共状态.txhaphablist=txhaphablist
    公共状态.txsadhablist=txsadhablist
    公共状态.txtransmatrix=txtransmatrix
    公共状态.txpredict_state_chance=txpredict_state_chance
    公共状态.lbpredict_max_state=lbpredict_max_state
    公共状态.lbpredict_max_chance=lbpredict_max_chance
    公共状态.txacthablist=txacthablist
    公共状态.txactlist=txactlist
    公共状态.entcounts=entcounts
    公共状态.varcbcounts1=varcbcounts1
    公共状态.varcbcounts2=varcbcounts2
    公共状态.txact_detail_list=txact_detail_list
    公共状态.txnloutput=txnloutput



#扩展知觉概念列表senlist
def extend_senlist():

    #1、extended_senlist=pactlist（上一回合的行为概念列表）+senlist（本回合知觉概念列表）+其他
    #其他包含内省出来的内容
    qita=公共状态.introcontent
    extended_senlist=公共状态.pactlist+公共状态.senlist+qita
    #2、增强或抑制知觉概念
	#1）若pactlist中的行为概念就是知觉概念，表示对该知觉概念的增强
		#在1中已经添加入extended_senlist中了，不需要作额外处理
	#2）若pactlist中的行为概念是知觉概念前面加一个英文减号“-”，表示对该知觉概念的减弱
		#删除该行为概念，在extended_senlist中删除1次其对应的知觉概念
    extended_senlist1=copy.deepcopy(extended_senlist)
    for i in extended_senlist:
        if i[0]=="-":
            extended_senlist1.remove(i)
            if i[1:] in extended_senlist1:
                extended_senlist1.remove(i[1:])
    extended_senlist=extended_senlist1

    #3、若extended_senlist为空列表，往extended_senlist中添加“空闲”
    if extended_senlist==[]:
        extended_senlist.append("空闲")

    return extended_senlist



#============================ 模式设置 ============================

class ModeSettings(Frame):
    """启动时的模式与参数设置。
    可单独使用，也可以嵌在导入窗口顶部，和“导入记忆”共用一个界面。"""

    def __init__(self, parent):
        super().__init__(parent)

        self.mode=StringVar(value="2")
        self.sleeptime=StringVar(value="2")
        self.imgsource=StringVar(value="1")
        self.add_actlist=IntVar(value=0)
        self.randforget=IntVar(value=0)
        self.adjust_hapsad=IntVar(value=1)
        self.adjust_acthab=IntVar(value=1)
        self.hapsum_threshold=StringVar(value="2")
        self.sadsum_threshold=StringVar(value="2")
        self.v_acthab_threshold=StringVar(value="1")
        self.v_adjustact_threshold=StringVar(value="2")

        Label(self,text="模式",font=("Microsoft YaHei",11,"bold")).grid(row=0,column=0,sticky="w")
        modes=Frame(self)
        modes.grid(row=0,column=1,columnspan=2,sticky="w",padx=8)
        #四种模式对应原来的 1/2/3/0
        for text,value in (("不可变模式","1"),("默认模式","2"),("自主模式","3"),("自定义","0")):
            Radiobutton(modes,text=text,variable=self.mode,value=value,
                        command=self._rebuild).pack(side=LEFT,padx=(0,10))

        self.params=LabelFrame(self,text="参数")
        self.params.grid(row=1,column=0,columnspan=3,sticky="we",pady=6)
        self._rebuild()

    def _entry(self,row,column,label,var,width=8):
        Label(self.params,text=label).grid(row=row,column=column*2,sticky="e",padx=(8,4),pady=4)
        Entry(self.params,textvariable=var,width=width).grid(row=row,column=column*2+1,sticky="w",pady=4)

    def _rebuild(self):
        #按模式切换参数区：预设模式不需要填写，自主模式要间隔和图像来源，自定义要各项开关
        for child in self.params.winfo_children():
            child.destroy()
        current=self.mode.get()
        if current in ("1","2"):
            Label(self.params,text="使用预设参数，无需填写。").grid(row=0,column=0,sticky="w",padx=10,pady=8)
        elif current=="3":
            self._entry(0,0,"每回合之间的睡眠时间（秒）",self.sleeptime)
            Label(self.params,text="图像来源").grid(row=1,column=0,sticky="e",padx=(8,4),pady=4)
            frame=Frame(self.params)
            frame.grid(row=1,column=1,sticky="w",pady=4)
            Radiobutton(frame,text="摄像头",variable=self.imgsource,value="1").pack(side=LEFT)
            Radiobutton(frame,text="截屏（左半边屏幕）",variable=self.imgsource,value="2").pack(side=LEFT,padx=8)
        else:
            Checkbutton(self.params,text="上一回合的行为概念加入下一回合的知觉概念列表",
                        variable=self.add_actlist).grid(row=0,column=0,columnspan=2,sticky="w",padx=10,pady=2)
            Checkbutton(self.params,text="激活随机遗忘机制",
                        variable=self.randforget).grid(row=1,column=0,columnspan=2,sticky="w",padx=10,pady=2)
            Checkbutton(self.params,text="允许调整情绪习惯列表",
                        variable=self.adjust_hapsad).grid(row=2,column=0,columnspan=2,sticky="w",padx=10,pady=2)
            self._entry(3,0,"喜的价值分类记忆激活阈值",self.hapsum_threshold)
            self._entry(3,1,"哀的价值分类记忆激活阈值",self.sadsum_threshold)
            Checkbutton(self.params,text="允许调整行为习惯列表",
                        variable=self.adjust_acthab).grid(row=4,column=0,columnspan=2,sticky="w",padx=10,pady=2)
            self._entry(5,0,"行为固定化阈值",self.v_acthab_threshold)
            self._entry(5,1,"行为调整激活阈值",self.v_adjustact_threshold)

    def _read_threshold(self,var,label):
        #阈值按原版范围 0-5 校验
        try:
            value=int(var.get().strip())
        except ValueError:
            raise ValueError(label+"请填写 0-5 的整数")
        if value<0 or value>5:
            raise ValueError(label+"请填写 0-5 的整数")
        return value

    def read(self):
        """校验并返回设置；不合法时抛 ValueError。"""
        current=self.mode.get()
        values={"mode":current,"sleeptime":None,"imgsource":self.imgsource.get(),
                "add_actlist":self.add_actlist.get(),"randforget":self.randforget.get(),
                "adjust_hapsad":self.adjust_hapsad.get(),"adjust_acthab":self.adjust_acthab.get()}
        thresholds={}
        if current=="3":
            try:
                sleep_value=int(self.sleeptime.get().strip())
            except ValueError:
                raise ValueError("睡眠时间请填写非负整数")
            if sleep_value<0:
                raise ValueError("睡眠时间请填写非负整数")
            values["sleeptime"]=sleep_value
        elif current=="0":
            if values["adjust_hapsad"]==1:
                thresholds["hap"]=self._read_threshold(self.hapsum_threshold,"喜的阈值")
                thresholds["sad"]=self._read_threshold(self.sadsum_threshold,"哀的阈值")
            if values["adjust_acthab"]==1:
                thresholds["v_acthab"]=self._read_threshold(self.v_acthab_threshold,"行为固定化阈值")
                thresholds["v_adjustact"]=self._read_threshold(self.v_adjustact_threshold,"行为调整阈值")
        values["thresholds"]=thresholds
        return values

    def apply(self,values):
        """把设置写入公共状态。"""
        公共状态.mode=values["mode"]
        if values["mode"]=="3":
            公共状态.sleeptime=values["sleeptime"]
            公共状态.imgsource=values["imgsource"]
        elif values["mode"]=="0":
            公共状态.senlist_add_actlist=str(values["add_actlist"])
            公共状态.randforget=str(values["randforget"])
            公共状态.adjust_hapsadhablist=str(values["adjust_hapsad"])
            公共状态.adjust_acthablist=str(values["adjust_acthab"])
            thresholds=values["thresholds"]
            if "hap" in thresholds:
                公共状态.hapsum_mem_threshold=thresholds["hap"]
                公共状态.sadsum_mem_threshold=thresholds["sad"]
            if "v_acthab" in thresholds:
                公共状态.v_acthab_threshold=thresholds["v_acthab"]
                公共状态.v_adjustact_threshold=thresholds["v_adjustact"]


#============================ 记忆窗口（导入/导出） ============================

class MemoryWindow:
    """一个窗口两种模式：启动时导入、运行中导出。
    “一键”= 只填一个版本号，9 类文件路径自动拼出（默认）；
    “逐文件导入”= 勾选后每个类型行右侧出现“选择文件…”，单独指定读哪个文件。"""

    def __init__(self, parent, mode, with_settings=False):
        self.parent = parent
        self.mode = mode
        self.with_settings = with_settings and mode == "导入"
        self.overrides = {}
        self._silent = False

        self.win = Toplevel(parent)
        if self.with_settings:
            self.win.title("苍穹3号 · 设置与导入")
        else:
            self.win.title("导入记忆" if mode == "导入" else "导出记忆")
        self.win.geometry("1120x900" if self.with_settings else "1120x740")
        self.win.transient(parent)
        self.win.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._refresh_versions()
        self._refresh_detail()
        self._validate()
        try:
            self.win.grab_set()
        except Exception:
            self.win.after(100, self._grab_again)

    def _grab_again(self):
        try:
            self.win.grab_set()
        except Exception:
            pass

    def wait_closed(self):
        self.win.wait_window(self.win)

    # ---------------- 界面 ----------------

    def _build_ui(self):
        self.version = StringVar()
        self.memory = StringVar()
        self.status = StringVar(value="")
        is_import = self.mode == "导入"

        if self.with_settings:
            #模式设置和导入放在同一个界面
            self.settings = ModeSettings(self.win)
            self.settings.pack(fill=X, padx=12, pady=(10, 0))

        header = Frame(self.win)
        header.pack(fill=X, padx=12, pady=(12, 2))
        Label(header, text="导入记忆" if is_import else "导出记忆",
              font=("Microsoft YaHei", 15, "bold")).pack(side=LEFT)
        Label(header, text="  输入要导入的版本号" if is_import else "  输入要导出的版本号",
              fg="#666").pack(side=LEFT)

        row = Frame(self.win)
        row.pack(fill=X, padx=12, pady=8)
        Label(row, text="版本号", font=("Microsoft YaHei", 11)).pack(side=LEFT)
        self.version_box = ttk.Combobox(row, textvariable=self.version, width=26)
        self.version_box.pack(side=LEFT, padx=6)
        Label(row, text="（如 张三、123、研究者_v1）" if is_import else "（如 张三、123、研究者_v1）",
              fg="#999").pack(side=LEFT)

        self.tip_label = Label(self.win, textvariable=self.status, fg="#0a58ca", anchor="w")
        self.tip_label.pack(fill=X, padx=12)

        Label(self.win, text="9 类文件").pack(anchor=W, padx=12, pady=(10, 0))

        self.per_file = IntVar(value=0)
        options = Frame(self.win)
        options.pack(fill=X, padx=12, pady=(2, 4))
        if is_import:
            #默认一键导入；勾选后才逐行单独指定文件
            Checkbutton(options, text="逐文件导入", variable=self.per_file,
                        command=self._toggle_per_file).pack(side=LEFT)
            self.reset_btn = Button(options, text="全部恢复", state=DISABLED,
                                    command=self._reset_overrides)
            self.reset_btn.pack(side=LEFT, padx=10)
        else:
            Label(options, text="一键导出", fg="#999").pack(side=LEFT)

        table = Frame(self.win)
        table.pack(fill=BOTH, expand=True, padx=12)
        head = Frame(table)
        head.pack(fill=X)
        Label(head, text="类型", width=26, anchor="w",
              font=("Microsoft YaHei", 9, "bold")).grid(row=0, column=0, sticky="w")
        Label(head, text="条数", width=10, anchor="center",
              font=("Microsoft YaHei", 9, "bold")).grid(row=0, column=1)
        Label(head, text="状态", anchor="w",
              font=("Microsoft YaHei", 9, "bold")).grid(row=0, column=2, sticky="w")

        body = Frame(table)
        body.pack(fill=BOTH, expand=True)
        body.columnconfigure(2, weight=1)
        self.rows = {}
        for index, spec in enumerate(记忆管理.TYPE_SPECS):
            key = spec["key"]
            type_label = Label(body, text=spec["name"], width=26, anchor="w")
            count_label = Label(body, text="—", width=10, anchor="center")
            status_label = Label(body, text="", anchor="w")
            pick_btn = Button(body, text="选择文件…", width=11,
                              command=lambda key=key: self._pick_file(key))
            type_label.grid(row=index, column=0, sticky="w", pady=2)
            count_label.grid(row=index, column=1, pady=2)
            status_label.grid(row=index, column=2, sticky="we", padx=(4, 6), pady=2)
            pick_btn.grid(row=index, column=3, padx=(0, 4), pady=2)
            pick_btn.grid_remove()
            self.rows[key] = {"type": type_label, "count": count_label,
                              "status": status_label, "pick": pick_btn}

        buttons = Frame(self.win)
        buttons.pack(fill=X, padx=12, pady=10)
        self.confirm_btn = Button(buttons, width=12, command=self._on_confirm,
                                  state=DISABLED,
                                  text="开始" if self.with_settings
                                  else ("确认导入" if is_import else "确认导出"))
        self.confirm_btn.pack(side=RIGHT)
        Button(buttons, text="退出" if is_import else "关闭", width=8,
               command=self._on_close).pack(side=RIGHT, padx=6)

        self.version.trace_add("write", self._on_input)

    # ---------------- 事件 ----------------

    def _refresh_versions(self):
        if self.mode == "导入":
            self.version_box["values"] = sorted(记忆管理.list_memories())

    def _on_input(self, *args):
        if self._silent:
            return
        memory, error = 记忆管理.normalize_version(self.version.get())
        self._silent = True
        self.memory.set(memory or "")
        self._silent = False
        self._refresh_detail()
        self._validate()

    def _refresh_detail(self):
        if self.mode == "导入":
            memory = self.memory.get().strip()
            if not memory:
                for row in self.rows.values():
                    row["count"].config(text="—")
                    row["status"].config(text="")
                if hasattr(self, "reset_btn"):
                    self.reset_btn.config(state=NORMAL if self.overrides else DISABLED)
                return
            for item in 记忆管理.memory_files(memory, self.overrides):
                row = self.rows[item["key"]]
                row["count"].config(text="—" if item["count"] is None else str(item["count"]))
                if item["key"] in self.overrides:
                    text = "手动指定：%s" % os.path.basename(self.overrides[item["key"]])
                elif item["exists"]:
                    text = "自动：%s" % os.path.basename(item["path"])
                else:
                    text = "缺失"
                row["status"].config(text=text)
        else:
            memory = self.memory.get().strip() or "未命名"
            for item in 记忆管理.export_preview(memory, self.overrides):
                row = self.rows[item["key"]]
                row["count"].config(text=str(item["count"]))
                row["status"].config(text=item["status"])
        if hasattr(self, "reset_btn"):
            self.reset_btn.config(state=NORMAL if self.overrides else DISABLED)

    def _validate(self):
        valid = False
        tip = ""
        if self.mode == "导出":
            memory, error = 记忆管理.normalize_version(self.version.get())
            if error:
                tip = error
            else:
                total = sum(len(getattr(公共状态, spec["var"], []) or [])
                            for spec in 记忆管理.TYPE_SPECS if spec["var"])
                tip = "要导出的版本号：%s（共 %d 条）" % (memory, total)
                valid = True
        else:
            memory = self.memory.get().strip()
            if not memory:
                tip = "请输入版本号"
            else:
                found = 0
                for spec in 记忆管理.TYPE_SPECS:
                    path = self.overrides.get(spec["key"]) or 记忆管理.default_path(spec, memory)
                    if os.path.exists(path):
                        found += 1
                if found == 0:
                    tip = "没有找到该版本号的文件"
                else:
                    tip = "已找到 %d/9 类文件" % found
                    valid = True
        self.confirm_btn.config(state=NORMAL if valid else DISABLED)
        self.status.set(tip)
        return valid

    # ---------------- 执行 ----------------

    def _on_confirm(self):
        if not self._validate():
            messagebox.showwarning("无法继续", "请先补全输入。", parent=self.win)
            return
        if self.mode == "导入":
            self._do_import()
        else:
            self._do_export()

    def _do_import(self):
        memory = self.memory.get().strip()
        settings = None
        if self.with_settings:
            #先校验模式和参数，再检查记忆文件
            try:
                settings = self.settings.read()
            except ValueError as error:
                messagebox.showerror("设置", str(error), parent=self.win)
                return
        skip_bad_lines = False
        ok, _, errors = 记忆管理.import_memory(
            memory, self.overrides, skip_bad_lines=False, commit=False)
        if not ok and errors:
            lines = []
            for item in errors[:6]:
                bad = item["bad_lines"][0]
                lines.append("· %s：%d 行无法解析（如第 %d 行：%s）" %
                             (item["name"], len(item["bad_lines"]), bad[0], bad[2]))
            if not messagebox.askyesno(
                    "存在无法解析的行",
                    "\n".join(lines) + "\n\n跳过这些行继续导入？", parent=self.win):
                return
            skip_bad_lines = True
            ok, _, errors = 记忆管理.import_memory(
                memory, self.overrides, skip_bad_lines=True, commit=False)
            if not ok:
                self._show_errors(errors)
                return

        if not messagebox.askyesno("确认导入", "确定导入这些记忆吗？", parent=self.win):
            return

        ok, _, errors = 记忆管理.import_memory(
            memory, self.overrides, skip_bad_lines=skip_bad_lines, commit=True)
        if not ok:
            self._show_errors(errors)
            return
        if self.with_settings:
            self.settings.apply(settings)
        messagebox.showinfo("导入成功——————————————", "已导入版本号：%s。" % memory, parent=self.win)
        self.win.destroy()

    def _do_export(self):
        memory, error = 记忆管理.normalize_version(self.version.get())
        if error:
            messagebox.showwarning("无法导出", error, parent=self.win)
            return
        exists = memory in 记忆管理.list_memories()
        text = "保存到版本号：%s（9 类文件）。" % memory
        if exists:
            text += "\n\n同名文件会被覆盖。"
        if len(公共状态.memorylist) < 5:
            text += "\n\n注意：自传体记忆只有 %d 条（至少需要 5 条）。" % len(公共状态.memorylist)
        if not 公共状态.allact:
            text += "\n\n注意：行为空间为空。"
        if not messagebox.askyesno("确认导出", text + "\n\n确定导出？", parent=self.win):
            return

        ok, report, error = 记忆管理.export_memory(memory, self.overrides)
        if not ok:
            messagebox.showerror("导出失败", "写入失败：%s" % error, parent=self.win)
            return
        skipped = [item["name"] for item in report if item["status"].startswith("跳过")]
        summary = "、".join(
            "%s %s" % (item["name"], "（跳过）" if str(item["count"]) == "—" else "%s 条" % item["count"])
            for item in report)
        text = "保存到版本号：%s\n\n%s" % (memory, summary)
        if skipped:
            text += "\n\n未写入：" + "、".join(skipped)
        messagebox.showinfo("导出成功——————————————", text, parent=self.win)
        self._refresh_versions()
        self._refresh_detail()
        self._validate()

    def _toggle_per_file(self):
        """勾选“逐文件导入”后显示每行的“选择文件…”；取消则回到一键并清空手动指定。"""
        show = bool(self.per_file.get())
        if not show:
            self.overrides.clear()
        for row in self.rows.values():
            if show:
                row["pick"].grid()
            else:
                row["pick"].grid_remove()
        if hasattr(self, "reset_btn"):
            self.reset_btn.config(state=NORMAL if self.overrides else DISABLED)
        self._refresh_detail()
        self._validate()

    def _pick_file(self, key):
        spec = [item for item in 记忆管理.TYPE_SPECS if item["key"] == key][0]
        current = self.overrides.get(key) or 记忆管理.default_path(
            spec, self.memory.get().strip() or "未命名")
        folder = os.path.dirname(os.path.abspath(current))
        if not os.path.isdir(folder):
            folder = os.getcwd()
        path = filedialog.askopenfilename(
            parent=self.win, title="选择「%s」文件" % spec["name"],
            initialdir=folder,
            filetypes=[("文本文件", "*.txt"), ("CSV文件", "*.csv"), ("所有文件", "*.*")])
        if not path:
            return
        self.overrides[key] = os.path.normpath(path)
        self._refresh_detail()
        self._validate()

    def _reset_overrides(self):
        self.overrides.clear()
        self._refresh_detail()
        self._validate()

    def _show_errors(self, errors):
        lines = ["%s：%d 行无法解析" % (item["name"], len(item["bad_lines"])) for item in errors]
        messagebox.showerror("导入失败", "\n".join(lines), parent=self.win)

    def _on_close(self):
        if self.mode == "导入":
            if 公共状态.current_memory is None:
                if not messagebox.askyesno("退出程序", "还没有导入记忆，关闭后程序将退出。\n\n确定吗？",
                                           parent=self.win):
                    return
            elif not messagebox.askyesno("关闭", "关闭记忆窗口，进入主程序？", parent=self.win):
                return
        self.win.destroy()


def open_memory_window(mode="导出", with_settings=False):
    """打开记忆窗口。导入模式会阻塞到窗口关闭（供启动时使用）；
    导出模式同样阻塞，避免导出过程中主循环改动内存。
    with_settings=True 时，模式设置与导入共用一个界面。"""
    if 公共状态.root is None:
        return
    existing = 公共状态.memory_window
    if existing is not None:
        try:
            if existing.win.winfo_exists():
                existing.win.lift()
                existing.win.focus_force()
                return
        except Exception:
            pass
    window = MemoryWindow(公共状态.root, mode, with_settings)
    公共状态.memory_window = window
    try:
        window.wait_closed()
    finally:
        公共状态.memory_window = None
