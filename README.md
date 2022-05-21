## 20220513-数据分析使用指南



### 1 文件结构及说明

- 文件夹
  - doc：各机构的支付摘要，做词云时使用
  - font：词云字体，若修改请同时更改plotWordcloud.py程序
- 文件
  - alice.png：保存的词云图片
  - DataProcess.py：QT导出的界面程序
  - DataProcess.ui：UI界面
  - main.py：主程序
  - plotWordcloud.py：词云制作程序
  - stop_words.txt：中文停词，词频分析时使用，不希望”的、你、你好“等词汇被统计
  - userdict.txt：分词自定义设置，若有专业词汇或需要注意的词汇，自行输入，防止分词程序不满足用户需求



### 2 程序运行

- 命令行

  `python main.py`

- 程序依赖库
  - numpy
  - pandas 
  - jieba
  - PyQt5
  - matplotlib



### 3 程序测试

- 打开界面

![image-20220513193039464](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193039464.png)

- 导入数据 (excel文件已在主目录下，不需”导入文件“)

![image-20220513193142331](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193142331.png)

![image-20220513193214608](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193214608.png)

### 单样本（单机构）分析

- 经济分类总览

![image-20220513193342464](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193342464.png)

![image-20220513193356717](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193356717.png)



- 申请金额总览

![image-20220513193436238](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193436238.png)

![image-20220513193449807](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193449807.png)



- 饼状图分析

![image-20220513193517958](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193517958.png)

![image-20220513193531941](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193531941.png)



- 词频分析

![image-20220513193620381](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193620381.png)



- 词云显示

![image-20220513193656662](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193656662.png)

### 单样本（单机构）分析

- 申请频率

![image-20220513193736806](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193736806.png)

- 申请金额

![image-20220513193805090](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20220513193805090.png)