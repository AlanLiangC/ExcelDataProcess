import sys
import numpy as np
import pandas as pd
import jieba
from DataProcess import Ui_DataProcess
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from PyQt5.QtCore import QStringListModel
import plotWordcloud



def get_stopwords(filename = "./stop_words.txt"):
    # stopwords_path = "./stop_words.txt"
    stopwords = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if len(line)>0:
                stopwords.append(line.strip())
    return stopwords

class MyPyQT_Form(QtWidgets.QWidget, Ui_DataProcess):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.excel_fileName = "./闽财指2021-424号：支付明细.xlsx"
        self.qList = None
        self.data = None
        self.index = None
        self.times = None
        self.money = None
        self.ratio_times = None
        self.ratio_money = None
        self.jingjiCls_labels = None
        self.words = None
        self.words_times = None
        self.stopwords = get_stopwords()
        self.setupUi(self)


    def OpenFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "选取文件",
                                                                "./",  # 起始路径
                                                                "All Files (*);;Text Files (*.xlsx)")  # 设置文件扩展名过滤,用双分号间隔

        if fileName_choose == "":
            print("\n取消选择")
            return
        self.ShowFilePath.setText(fileName_choose)
        self.excel_fileName = fileName_choose

    def load_data(self):
        slm = QStringListModel()  # 创建mode
        try:
            data = pd.read_excel(self.excel_fileName)
            self.data = data.loc[:, ["预算单位", "经济分类", "指标文号", "申请金额", "收款人名称", "支付日期", "支付摘要"]].dropna()

            self.qList = self.data["预算单位"].unique()
            slm.setStringList(self.qList)
            self.listView.setModel(slm)
            self.listView.clicked.connect(self.choose_index)
        except:
            QMessageBox.information(self, "文件不存在！")

    def choose_index(self, index):
        # QMessageBox.information(self, "ListView", "选择项是：%d" % (index.row()))
        self.Showlog.append("你选择了{}\n".format(self.qList[index.row()]))
        self.index = index.row()
        print(self.index)

    def jingjiCls(self):
        data2 = self.data.loc[self.data["预算单位"] == self.qList[self.index]]
        out = pd.value_counts(data2["经济分类"])
        self.Showlog.append(out.to_string())
        self.Showlog.append("\n")


    def allmoney(self):
        data2 = self.data.loc[self.data["预算单位"] == self.qList[self.index]]
        out = pd.value_counts(data2["经济分类"])
        self.jingjiCls_labels = out.index
        all_money = data2["申请金额"].sum()
        all_times = out.values.sum()
        times = []
        money = []
        ratio_times = []
        ratio_money = []
        for i in range(out.index.shape[0]):
            sub_data = data2.loc[data2["经济分类"] == out.index[i]]
            sub_time = out.values[i]
            sub_money = sub_data["申请金额"].sum()
            times.append(round(sub_time,2))
            money.append(round(sub_money,2))
            ratio_money.append(round(sub_money/all_money,4))
            ratio_times.append(round(sub_time/all_times,4))
        result = np.array([times,money,ratio_times,ratio_money])
        result = result.T
        result = pd.DataFrame(result,index=out.index,columns=["次数","金额","频次占比","金额占比"])
        self.Showlog.append(result.to_string())
        self.Showlog.append("\n")
        self.times = times
        self.money = money
        self.ratio_times = ratio_times
        self.ratio_money = ratio_money
        print(result)



    def barfig(self):
        fig,axes = plt.subplots(1,2)
        plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
        plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题
        axes[0].pie(self.ratio_times,labels = self.jingjiCls_labels,autopct='%3.1f%%')
        axes[0].set(title = "经济分类次数饼图")
        axes[1].pie(self.ratio_money,labels = self.jingjiCls_labels,autopct='%3.1f%%')
        axes[1].set(title = "经济分类金额饼图")
        plt.show()



    def words_freq(self):
        data2 = self.data.loc[self.data["预算单位"] == self.qList[self.index]]
        jieba.load_userdict('./userdict.txt') # 导入用户自定义词典
        wordcount = {}
        with open("./doc/{}.txt".format(self.qList[self.index]),"w") as f:
            for i in range(data2.shape[0]-1):
                words = data2.iloc[i+1,-1]
                f.write(words)
                f.write("\n")
                for word in jieba.cut(words):
                    if len(word) > 1 and word not in self.stopwords :
                        wordcount[word] = wordcount.get(word, 0)+1
        f.close()
        result = sorted(wordcount.items(), key=lambda x: x[1], reverse=True)[:10]
        labels = []
        times = []
        for i in result:
            labels.append(i[0])
            times.append(i[1])
            self.Showlog.append("({},{})".format(i[0],i[1]))
        self.words = labels
        self.words_times = times
        self.Showlog.append("\n")
        fig,axes = plt.subplots(1,1)
        plt.rcParams['font.sans-serif'] = ['SimHei']   #解决中文显示问题
        plt.rcParams['axes.unicode_minus'] = False    # 解决中文显示问题
        axes.pie(times,labels = labels,autopct='%3.1f%%')
        plt.show()

    def wordscloud(self):
        jieba.load_userdict('./userdict.txt') # 导入用户自定义词典
        text = open("./doc/{}.txt".format(self.qList[self.index])).read()
        jieba_word=jieba.cut(text,cut_all=False) # cut_all是分词模式，True是全模式，False是精准模式，默认False
        seg_list=' '.join(jieba_word)
        plotWordcloud.generate_wordcloud(seg_list)



    def school_freq(self):
        num = self.data["预算单位"].unique().shape[0]
        freq = []
        for i in range(num):
            data2 = self.data.loc[self.data["预算单位"] == self.qList[i]]
            freq.append(data2.shape[0])
        # print(freq)
        fig,axes = plt.subplots(1,1)
        plt.rcParams['font.sans-serif'] = ['SimHei'] 
        plt.rcParams['axes.unicode_minus'] = False 
        axes.pie(freq,labels = self.qList,autopct='%3.1f%%')
        axes.set(title = "各个机构的申请次数饼图")
        plt.show()
        

    def school_money(self):
        num = self.data["预算单位"].unique().shape[0]
        money = []
        for i in range(num):
            data2 = self.data.loc[self.data["预算单位"] == self.qList[i]]
            money.append(data2["申请金额"].sum())
        # print(freq)
        fig,axes = plt.subplots(1,1)
        plt.rcParams['font.sans-serif'] = ['SimHei'] 
        plt.rcParams['axes.unicode_minus'] = False 
        axes.pie(money,labels = self.qList,autopct='%3.1f%%')
        axes.set(title = "各个机构的申请金额饼图")
        plt.show()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
