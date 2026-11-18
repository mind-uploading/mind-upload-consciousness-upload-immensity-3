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
    “一键模式”= 只填一个版本号，9 类文件路径自动拼出（默认）；
    “逐文件导入”= 勾选后每个类型行右侧出现“选择文件…”，单独指定该类型读哪个文件。"""

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
        self._刷新版本列表()
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
        顶部.pack(fill=X, padx=12, pady=(12, 2))
        Label(顶部, text=("导入记忆包" if self.模式 == "导入" else "导出记忆包"),
              font=("Microsoft YaHei", 15, "bold")).pack(side=LEFT)
        Label(顶部, text=("  选择已有版本，或直接输入版本号" if self.模式 == "导入"
                          else "  填写新版本号，把当前心智内容写成一包"),
              fg="#666").pack(side=LEFT)

        输入行 = Frame(self.窗口)
        输入行.pack(fill=X, padx=12, pady=8)
        Label(输入行, text="版本号", font=("Microsoft YaHei", 11)).pack(side=LEFT)
        #导入时可以下拉选已有版本；导出时直接输入新版本号
        self.版本号框 = ttk.Combobox(输入行, textvariable=self.版本号, width=26)
        self.版本号框.pack(side=LEFT, padx=6)
        Label(输入行, text="（如 100、研究者_v1）" if self.模式 == "导入" else "（如 104）",
              fg="#999").pack(side=LEFT)

        self.提示标签 = Label(self.窗口, textvariable=self.状态, fg="#0a58ca", anchor="w")
        self.提示标签.pack(fill=X, padx=12)

        Label(self.窗口, text="这一包的 9 类文件").pack(anchor=W, padx=12, pady=(10, 0))

        self.逐文件 = IntVar(value=0)
        选项行 = Frame(self.窗口)
        选项行.pack(fill=X, padx=12, pady=(2, 4))
        if self.模式 == "导入":
            #默认一键导入：9 类文件全部按版本号自动拼路径；勾选后才逐行单独指定
            Checkbutton(选项行, text="逐文件导入（勾选后可单独指定每个类型的文件）",
                        variable=self.逐文件,
                        command=self._切换逐文件).pack(side=LEFT)
            self.恢复全部按钮 = Button(选项行, text="全部恢复自动", state=DISABLED,
                                      command=self._恢复全部)
            self.恢复全部按钮.pack(side=LEFT, padx=10)
        else:
            Label(选项行, text="默认一键导出 9 类文件", fg="#999").pack(side=LEFT)

        表框 = Frame(self.窗口)
        表框.pack(fill=BOTH, expand=True, padx=12)
        表头 = Frame(表框)
        表头.pack(fill=X)
        Label(表头, text="类型", width=26, anchor="w",
              font=("Microsoft YaHei", 9, "bold")).grid(row=0, column=0, sticky="w")
        Label(表头, text="条数", width=10, anchor="center",
              font=("Microsoft YaHei", 9, "bold")).grid(row=0, column=1)
        Label(表头, text="状态", anchor="w",
              font=("Microsoft YaHei", 9, "bold")).grid(row=0, column=2, sticky="w")

        行区域 = Frame(表框)
        行区域.pack(fill=BOTH, expand=True)
        行区域.columnconfigure(2, weight=1)
        self.明细行 = {}
        for 序号, 规格 in enumerate(记忆管理.类型规格):
            键 = 规格["键"]
            类型标签 = Label(行区域, text=规格["名称"], width=26, anchor="w")
            条数标签 = Label(行区域, text="—", width=10, anchor="center")
            状态标签 = Label(行区域, text="", anchor="w")
            按钮 = Button(行区域, text="选择文件…", width=11,
                         command=lambda 键=键: self._选择文件(键))
            类型标签.grid(row=序号, column=0, sticky="w", pady=2)
            条数标签.grid(row=序号, column=1, pady=2)
            状态标签.grid(row=序号, column=2, sticky="we", padx=(4, 6), pady=2)
            按钮.grid(row=序号, column=3, padx=(0, 4), pady=2)
            按钮.grid_remove()
            self.明细行[键] = {"类型": 类型标签, "条数": 条数标签,
                             "状态": 状态标签, "按钮": 按钮}

        按钮行 = Frame(self.窗口)
        按钮行.pack(fill=X, padx=12, pady=10)
        self.确认按钮 = Button(按钮行, width=12, command=self._确认, state=DISABLED,
                            text=("确认导入" if self.模式 == "导入" else "确认导出"))
        self.确认按钮.pack(side=RIGHT)
        Button(按钮行, text=("退出" if self.模式 == "导入" else "关闭"), width=8,
               command=self._关闭).pack(side=RIGHT, padx=6)

        self.版本号.trace_add("write", self._输入变化)

    # ---------------- 事件 ----------------

    def _切换逐文件(self):
        """勾选“逐文件导入”后，每个类型行右侧出现“选择文件…”按钮；
        取消勾选即回到一键导入，之前单独指定的文件作废。"""
        显示 = bool(self.逐文件.get())
        if not 显示:
            self.覆盖路径.clear()
        for 行控件 in self.明细行.values():
            if 显示:
                行控件["按钮"].grid()
            else:
                行控件["按钮"].grid_remove()
        if hasattr(self, "恢复全部按钮"):
            self.恢复全部按钮.config(state=NORMAL if self.覆盖路径 else DISABLED)
        self._刷新明细()
        self._校验()

    def _预填(self):
        if self.模式 == "导入":
            return
        self.版本号.set(记忆管理.建议版本号(公共状态.当前记忆包))

    def _刷新版本列表(self):
        """导入时把已有版本放进下拉框，导出时不需要"""
        if self.模式 == "导入":
            self.版本号框["values"] = sorted(记忆管理.列出记忆包())

    def _输入变化(self, *参数):
        if self._静默:
            return
        包名, 错误 = 记忆管理.规范化包名(self.版本号.get())
        self._静默 = True
        self.包名.set(包名 or "")
        self._静默 = False
        self._刷新明细()
        self._校验()

    def _刷新明细(self):
        if self.模式 == "导入":
            包名 = self.包名.get().strip()
            if not 包名:
                for 行控件 in self.明细行.values():
                    行控件["条数"].config(text="—")
                    行控件["状态"].config(text="")
                return
            for 行 in 记忆管理.包内文件(包名, self.覆盖路径):
                行控件 = self.明细行[行["键"]]
                行控件["条数"].config(
                    text="—" if 行["条数"] is None else str(行["条数"]))
                if 行["键"] in self.覆盖路径:
                    状态 = "手动指定：%s" % os.path.basename(self.覆盖路径[行["键"]])
                elif 行["存在"]:
                    状态 = "自动：%s" % os.path.basename(行["路径"])
                else:
                    状态 = "缺失（ART置空）" if 行["键"] == "ART" else "缺失（按空表）"
                行控件["状态"].config(text=状态)
        else:
            包名 = self.包名.get().strip() or "未命名"
            for 行 in 记忆管理.导出预览(包名, self.覆盖路径):
                行控件 = self.明细行[行["键"]]
                行控件["条数"].config(text=str(行["条数"]))
                if 行["键"] in self.覆盖路径:
                    状态 = "手动指定：%s" % os.path.basename(self.覆盖路径[行["键"]])
                else:
                    状态 = 行["状态"]
                行控件["状态"].config(text=状态)
        if hasattr(self, "恢复全部按钮"):
            self.恢复全部按钮.config(state=NORMAL if self.覆盖路径 else DISABLED)

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
                提示 = "请选择或输入版本号"
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
        self._刷新版本列表()
        self._刷新明细()
        self._校验()

    def _选择文件(self, 键):
        """逐文件导入：为某个类型单独挑选文件（其余类型仍按版本号自动拼）"""
        规格 = [项 for 项 in 记忆管理.类型规格 if 项["键"] == 键][0]
        当前 = self.覆盖路径.get(键) or 记忆管理.默认路径(规格, self.包名.get().strip() or "未命名")
        初始目录 = os.path.dirname(os.path.abspath(当前))
        if not os.path.isdir(初始目录):
            初始目录 = os.getcwd()
        路径 = filedialog.askopenfilename(
            parent=self.窗口, title="选择「%s」文件" % 规格["名称"],
            initialdir=初始目录,
            filetypes=[("文本文件", "*.txt"), ("CSV文件", "*.csv"), ("所有文件", "*.*")])
        if not 路径:
            return
        self.覆盖路径[键] = os.path.normpath(路径)
        self._刷新明细()
        self._校验()

    def _恢复全部(self):
        self.覆盖路径.clear()
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
