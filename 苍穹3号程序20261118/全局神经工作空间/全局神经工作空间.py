#全局神经工作空间GW
import copy
import os
import time
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

    varcb自动保存=IntVar()
    cb自动保存=Checkbutton(root,text="每回合自动保存到当前记忆包",variable=varcb自动保存,onvalue=1,offvalue=0)
    cb自动保存.grid(row=12,column=1)
    btn记忆包=Button(root,text="记忆包…（导出）",command=lambda: 打开记忆包窗口("导出"))
    btn记忆包.grid(row=13,column=1)


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
    公共状态.varcb自动保存=varcb自动保存



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



#============================ 记忆包窗口（导入/导出） ============================

class 记忆包窗口:
    """一个窗口两种模式：启动时导入、运行中导出。
    两种模式不能在这个窗口里直接切换：导入会替换内存、导出会写盘，时机不同。
    “一键模式”= 只填一个版本号，9 行文件路径自动拼出；
    “逐文件模式”= 在同一张文件明细表里单独指定某几行的路径。"""

    def __init__(self, 父窗口, 模式):
        self.父窗口 = 父窗口
        self.模式 = 模式
        self.覆盖路径 = {}
        self._静默 = False

        self.窗口 = Toplevel(父窗口)
        self.窗口.title("记忆包 · " + 模式)
        self.窗口.geometry("1120x740")
        self.窗口.transient(父窗口)
        self.窗口.protocol("WM_DELETE_WINDOW", self._关闭)

        self._建界面()
        self._预填()
        self._刷新已有()
        self._刷新明细()
        self._校验()
        try:
            self.窗口.grab_set()
        except Exception:
            self.窗口.after(100, self._重新抓取)

    def _重新抓取(self):
        try:
            self.窗口.grab_set()
        except Exception:
            pass

    def 等待关闭(self):
        self.窗口.wait_window(self.窗口)

    # ---------------- 界面 ----------------

    def _建界面(self):
        self.版本号 = StringVar()
        self.包名 = StringVar()
        self.状态 = StringVar(value="")

        顶部 = Frame(self.窗口)
        顶部.pack(fill=X, padx=10, pady=(10, 2))
        Label(顶部, text="记忆包", font=("Microsoft YaHei", 14, "bold")).pack(side=LEFT)
        Label(顶部, text="  导入：启动时选择记忆包        导出：把当前心智内容写成记忆包",
              fg="#666").pack(side=LEFT)

        模式行 = Frame(self.窗口)
        模式行.pack(fill=X, padx=10, pady=(2, 6))
        for 名称 in ("导入", "导出"):
            当前 = (名称 == self.模式)
            标签 = Label(模式行, text=名称, width=8, padx=8, pady=3,
                         relief=SUNKEN if 当前 else RIDGE,
                         bg="#cfe3ff" if 当前 else "#efefef")
            标签.pack(side=LEFT, padx=(0, 6))
            if not 当前:
                标签.bind("<Button-1>", lambda 事件, 名=名称: self._提示不能切换(名))
        Label(模式行, text="（导入只在启动时、导出只在运行中，不能在这里直接切换）",
              fg="#999").pack(side=LEFT, padx=6)

        查询行 = Frame(self.窗口)
        查询行.pack(fill=X, padx=10, pady=3)
        Label(查询行, text="版本号").pack(side=LEFT)
        self.版本号框 = Entry(查询行, textvariable=self.版本号, width=16)
        self.版本号框.pack(side=LEFT, padx=(2, 10))
        Button(查询行, text="查找", width=6, command=self._查找).pack(side=LEFT)
        Label(查询行, text="（只需输入一个版本号；也可在下方列表双击已有的记忆包）",
              fg="#999").pack(side=LEFT, padx=8)
        self.版本号框.bind("<Return>", lambda 事件: self._查找())

        包名行 = Frame(self.窗口)
        包名行.pack(fill=X, padx=10, pady=3)
        Label(包名行, text="记忆包").pack(side=LEFT)
        self.包名框 = Entry(包名行, textvariable=self.包名, width=32)
        self.包名框.pack(side=LEFT, padx=(2, 8))
        #包名由版本号自动生成（或由列表双击选中），不需要手动填写
        self.包名框.config(state="readonly")
        self.提示标签 = Label(包名行, textvariable=self.状态, fg="#0a58ca")
        self.提示标签.pack(side=LEFT, padx=6)

        Label(self.窗口, text="已有版本（双击选中）").pack(anchor=W, padx=10, pady=(8, 2))
        表框 = Frame(self.窗口)
        表框.pack(fill=X, padx=10)
        列 = ("包名",) + tuple(规格["名称"][:4] for 规格 in 记忆管理.类型规格) + ("修改时间",)
        self.已有表 = ttk.Treeview(表框, columns=列, show="headings", height=8)
        for 名称 in 列:
            self.已有表.heading(名称, text=名称)
            self.已有表.column(名称, width=105 if 名称 == "包名" else 62,
                            anchor="w" if 名称 == "包名" else "center", stretch=False)
        滚动 = Scrollbar(表框, orient=VERTICAL, command=self.已有表.yview)
        self.已有表.configure(yscrollcommand=滚动.set)
        self.已有表.pack(side=LEFT, fill=X, expand=True)
        滚动.pack(side=RIGHT, fill=Y)
        self.已有表.bind("<<TreeviewSelect>>", self._选中已有)
        self.已有表.bind("<Double-1>", self._选中已有)

        Label(self.窗口, text="文件明细（一键=9 行自动填满；逐文件=单独指定某行）").pack(anchor=W, padx=10, pady=(8, 2))
        明细框 = Frame(self.窗口)
        明细框.pack(fill=BOTH, expand=True, padx=10)
        列2 = ("类型", "文件", "条数", "状态")
        self.明细表 = ttk.Treeview(明细框, columns=列2, show="headings", height=9)
        for 名称, 宽 in (("类型", 150), ("文件", 660), ("条数", 80), ("状态", 160)):
            self.明细表.heading(名称, text=名称)
            self.明细表.column(名称, width=宽, anchor="w" if 名称 == "文件" else "center")
        滚动2 = Scrollbar(明细框, orient=VERTICAL, command=self.明细表.yview)
        self.明细表.configure(yscrollcommand=滚动2.set)
        self.明细表.pack(side=LEFT, fill=BOTH, expand=True)
        滚动2.pack(side=RIGHT, fill=Y)

        按钮行 = Frame(self.窗口)
        按钮行.pack(fill=X, padx=10, pady=8)
        Button(按钮行, text="单独指定所选行…", command=self._选择文件).pack(side=LEFT)
        Button(按钮行, text="恢复自动", command=self._恢复自动).pack(side=LEFT, padx=6)
        self.确认按钮 = Button(按钮行, width=12, command=self._确认, state=DISABLED,
                            text=("确认导入" if self.模式 == "导入" else "确认导出"))
        self.确认按钮.pack(side=RIGHT)
        Button(按钮行, text=("退出" if self.模式 == "导入" else "关闭"), width=8,
               command=self._关闭).pack(side=RIGHT, padx=6)

        self.版本号.trace_add("write", self._输入变化)

    # ---------------- 事件 ----------------

    def _提示不能切换(self, 名称):
        messagebox.showinfo(
            "不能直接切换",
            "导入只在启动时进行，导出只在运行中进行，不能在这个窗口里直接切换。\n\n"
            "要导入：关闭本窗口，重新启动程序。\n"
            "要导出：关闭本窗口，在运行中的主界面点“记忆包…（导出）”。",
            parent=self.窗口)

    def _预填(self):
        if self.模式 == "导入":
            if 公共状态.当前记忆包:
                self.包名.set(公共状态.当前记忆包)
            return
        self.版本号.set(记忆管理.建议版本号())

    def _输入变化(self, *参数):
        if self._静默:
            return
        包名, 错误 = 记忆管理.规范化包名(self.版本号.get())
        self._静默 = True
        if self.模式 == "导入":
            #导入：输入合法版本号就自动切换包名；输入了非法内容则清空，避免误导入
            if not 错误:
                self.包名.set(包名)
            elif self.版本号.get().strip():
                self.包名.set("")
        else:
            self.包名.set(包名 or "")
        self._静默 = False
        if self.模式 == "导入":
            self._刷新已有()
        self._刷新明细()
        self._校验()

    def _查找(self):
        self._刷新已有()
        项目 = self.已有表.get_children()
        if len(项目) == 1:
            self.已有表.selection_set(项目[0])
            self._选中已有()

    def _刷新已有(self):
        for 项目 in self.已有表.get_children():
            self.已有表.delete(项目)
        版本号 = self.版本号.get().strip() if self.模式 == "导入" else ""
        包们 = 记忆管理.列出记忆包()
        for 包名 in sorted(包们):
            if 版本号 and 版本号 not in 包名:
                continue
            值 = [包名]
            for 规格 in 记忆管理.类型规格:
                路径 = 包们[包名]["路径"].get(规格["键"])
                数量 = 记忆管理.条数(路径, 规格["键"]) if 路径 else None
                值.append("—" if 数量 is None else 数量)
            值.append(time.strftime("%Y-%m-%d %H:%M", time.localtime(包们[包名]["时间"])))
            self.已有表.insert("", END, iid=包名, values=值)

    def _选中已有(self, 事件=None):
        选中 = self.已有表.selection()
        if not 选中:
            return
        if self.模式 != "导入":
            self.状态.set("提示：导出只需填版本号；选中已有包不会改动它")
            return
        #双击列表可以选中旧命名的记忆包（如 研究者_v1、张毅），导入时仍然兼容
        self._静默 = True
        self.包名.set(选中[0])
        self._静默 = False
        self._刷新明细()
        self._校验()

    def _刷新明细(self):
        for 项目 in self.明细表.get_children():
            self.明细表.delete(项目)
        if self.模式 == "导入":
            包名 = self.包名.get().strip()
            if not 包名:
                return
            for 行 in 记忆管理.包内文件(包名, self.覆盖路径):
                if 行["存在"]:
                    状态 = "存在"
                else:
                    状态 = "缺失（ART置空）" if 行["键"] == "ART" else "缺失（按空表）"
                if 行["键"] in self.覆盖路径:
                    状态 += "（手动指定）"
                条数文本 = "—" if 行["条数"] is None else str(行["条数"])
                self.明细表.insert("", END, iid=行["键"],
                                 values=(行["名称"], 行["路径"], 条数文本, 状态))
        else:
            包名 = self.包名.get().strip() or "未命名"
            for 行 in 记忆管理.导出预览(包名, self.覆盖路径):
                状态 = 行["状态"]
                if 行["键"] in self.覆盖路径:
                    状态 += "（手动指定）"
                self.明细表.insert("", END, iid=行["键"],
                                 values=(行["名称"], 行["路径"], str(行["条数"]), 状态))

    def _校验(self):
        有效 = False
        提示 = ""
        if self.模式 == "导出":
            包名, 错误 = 记忆管理.规范化包名(self.版本号.get())
            if 错误:
                提示 = 错误
            else:
                总数 = sum(len(getattr(公共状态, 规格["变量"], []) or [])
                          for 规格 in 记忆管理.类型规格 if 规格["变量"])
                提示 = "将导出为：%s（%d 条记录）" % (包名, 总数)
                有效 = True
        else:
            包名 = self.包名.get().strip()
            if not 包名:
                提示 = "请输入版本号，或在下方列表双击选择记忆包"
            else:
                找到 = 0
                for 规格 in 记忆管理.类型规格:
                    路径 = self.覆盖路径.get(规格["键"]) or 记忆管理.默认路径(规格, 包名)
                    if os.path.exists(路径):
                        找到 += 1
                if 找到 == 0:
                    提示 = "未找到该记忆包的任何文件"
                else:
                    提示 = "找到 %d/9 类文件" % 找到
                    有效 = True
        self.确认按钮.config(state=NORMAL if 有效 else DISABLED)
        self.状态.set(提示)
        return 有效

    # ---------------- 执行 ----------------

    def _确认(self):
        if not self._校验():
            messagebox.showwarning("无法继续", "输入尚不完整或无效，请先补全。", parent=self.窗口)
            return
        if self.模式 == "导入":
            self._执行导入()
        else:
            self._执行导出()

    def _执行导入(self):
        包名 = self.包名.get().strip()
        跳过坏行 = False
        成功, 报告, 错误 = 记忆管理.导入记忆包(包名, self.覆盖路径, 跳过坏行=False, 提交=False)
        if not 成功 and 错误:
            文本 = []
            for 项 in 错误[:6]:
                坏 = 项["坏行"][0]
                文本.append("· %s：%d 行无法解析，例如第 %d 行（%s）" %
                          (项["名称"], len(项["坏行"]), 坏[0], 坏[2]))
            if not messagebox.askyesno(
                    "存在无法解析的行",
                    "以下文件里有无法解析的行：\n\n" + "\n".join(文本) +
                    "\n\n是否跳过这些坏行继续导入？", parent=self.窗口):
                return
            跳过坏行 = True
            成功, 报告, 错误 = 记忆管理.导入记忆包(包名, self.覆盖路径, 跳过坏行=True, 提交=False)
            if not 成功:
                self._显示错误(错误)
                return

        汇总 = "、".join("%s %s 条" % (项["名称"], 项["条数"]) for 项 in 报告)
        缺失 = [项["名称"] for 项 in 报告 if 项["状态"].startswith("缺失")]
        提示 = "将从记忆包「%s」导入：\n\n%s\n\n当前内存中的心智内容会被替换。" % (包名, 汇总)
        if 缺失:
            提示 += "\n\n以下类型没有文件，将按空表导入：\n" + "、".join(缺失)
        自传体条数 = next((项["条数"] for 项 in 报告 if 项["键"] == "自传体"), 0)
        行为空间条数 = next((项["条数"] for 项 in 报告 if 项["键"] == "行为空间"), 0)
        if 自传体条数 < 5:
            提示 += "\n\n注意：自传体记忆只有 %d 条（程序需要至少 5 条）。" % 自传体条数
        if 行为空间条数 == 0:
            提示 += "\n\n注意：行为空间为空，运行中调整行为习惯时可能出错。"
        提示 += "\n\n导入后若勾选了“每回合自动保存”，本回合的改动会写回该记忆包。"
        if not messagebox.askyesno("确认导入", 提示 + "\n\n确定导入吗？", parent=self.窗口):
            return

        成功, 报告, 错误 = 记忆管理.导入记忆包(包名, self.覆盖路径,
                                              跳过坏行=跳过坏行, 提交=True)
        if not 成功:
            self._显示错误(错误)
            return
        messagebox.showinfo("导入完成", "记忆包「%s」已导入。" % 包名, parent=self.窗口)
        self.窗口.destroy()

    def _执行导出(self):
        包名, 错误 = 记忆管理.规范化包名(self.版本号.get())
        if 错误:
            messagebox.showwarning("无法导出", 错误, parent=self.窗口)
            return
        已存在 = 包名 in 记忆管理.列出记忆包()
        提示 = "将把当前心智内容导出为记忆包「%s」（9 类文件）。" % 包名
        if 已存在:
            提示 += "\n\n注意：该记忆包已存在，同名文件会被覆盖。"
        if len(公共状态.memorylist) < 5:
            提示 += "\n\n注意：当前自传体记忆只有 %d 条（程序需要至少 5 条）。" % len(公共状态.memorylist)
        if not 公共状态.allact:
            提示 += "\n\n注意：当前行为空间为空，导入后调整行为习惯时可能出错。"
        if not messagebox.askyesno("确认导出", 提示 + "\n\n确定导出吗？", parent=self.窗口):
            return

        成功, 报告, 错误 = 记忆管理.导出记忆包(包名, self.覆盖路径)
        if not 成功:
            messagebox.showerror("导出失败", "写入失败：%s" % 错误, parent=self.窗口)
            return
        跳过 = [项["名称"] for 项 in 报告 if 项["状态"].startswith("跳过")]
        汇总 = "、".join(
            "%s %s" % (项["名称"], "（跳过）" if str(项["条数"]) == "—" else "%s 条" % 项["条数"])
            for 项 in 报告)
        消息 = "已导出到记忆包「%s」：\n\n%s" % (包名, 汇总)
        if 跳过:
            消息 += "\n\n未写入：\n" + "、".join(跳过)
        messagebox.showinfo("导出完成", 消息, parent=self.窗口)
        self._刷新已有()
        self._刷新明细()
        self._校验()

    def _选择文件(self):
        选中 = self.明细表.selection()
        if not 选中:
            messagebox.showinfo("提示", "请先在下面的文件明细里选中一行。", parent=self.窗口)
            return
        键 = 选中[0]
        规格 = [项 for 项 in 记忆管理.类型规格 if 项["键"] == 键][0]
        当前 = self.覆盖路径.get(键) or 记忆管理.默认路径(规格, self.包名.get().strip() or "未命名")
        初始目录 = os.path.dirname(os.path.abspath(当前))
        if not os.path.isdir(初始目录):
            初始目录 = os.getcwd()
        if self.模式 == "导入":
            路径 = filedialog.askopenfilename(
                parent=self.窗口, title="选择「%s」文件" % 规格["名称"],
                initialdir=初始目录,
                filetypes=[("文本文件", "*.txt"), ("CSV文件", "*.csv"), ("所有文件", "*.*")])
        else:
            路径 = filedialog.asksaveasfilename(
                parent=self.窗口, title="「%s」导出到" % 规格["名称"],
                initialdir=初始目录, initialfile=os.path.basename(当前),
                defaultextension=规格["后缀"])
        if not 路径:
            return
        self.覆盖路径[键] = os.path.normpath(路径)
        self._刷新明细()
        self._校验()

    def _恢复自动(self):
        选中 = self.明细表.selection()
        if not 选中:
            messagebox.showinfo("提示", "请先在下面的文件明细里选中一行。", parent=self.窗口)
            return
        键 = 选中[0]
        if 键 in self.覆盖路径:
            del self.覆盖路径[键]
        self._刷新明细()
        self._校验()

    def _关闭(self):
        if self.模式 == "导入":
            if 公共状态.当前记忆包 is None:
                if not messagebox.askyesno("退出程序",
                                           "还没有导入记忆包，关闭后程序将退出。\n\n确定吗？",
                                           parent=self.窗口):
                    return
            else:
                if not messagebox.askyesno("关闭", "关闭记忆包窗口，进入主程序？",
                                           parent=self.窗口):
                    return
        self.窗口.destroy()


def 打开记忆包窗口(模式="导出"):
    """打开记忆包窗口。导入模式会阻塞到窗口关闭（供启动时使用）；
    导出模式同样阻塞，避免导出过程中主循环改动内存。"""
    if 公共状态.root is None:
        return
    已有 = 公共状态.记忆包窗口
    if 已有 is not None:
        try:
            if 已有.窗口.winfo_exists():
                已有.窗口.lift()
                已有.窗口.focus_force()
                return
        except Exception:
            pass
    窗口 = 记忆包窗口(公共状态.root, 模式)
    公共状态.记忆包窗口 = 窗口
    try:
        窗口.等待关闭()
    finally:
        公共状态.记忆包窗口 = None
