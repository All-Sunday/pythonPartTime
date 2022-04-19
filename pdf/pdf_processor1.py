# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/4/10 15:38
# @File : pdf_processor.py
# import re
#
# import pdfplumber
# import pandas as pd

# with pdfplumber.open("2005-2009真题(英语一二通用).pdf") as pdf:
#     page_count = len(pdf.pages)
#     print(page_count)  # 得到页数
#     for page in pdf.pages[1:2]:
#         print('---------- 第[%d]页 ----------' % page.page_number)
#         # 获取当前页面的全部文本信息，包括表格中的文字
#         print(page.extract_text())
#         # l = page.extract_text().split('.')
#         # for i in l:
#         #     print(i)
#         # pattern = re.compile(r'[A-Za-z]+[A-Za-z0-9_,\"#;.() \\s]*[.]$')   # 查找数字
#         # result1 = pattern.findall(page.extract_text(), re.M)
#         # print(result1)
#         list_ret = list()
#
#         for s_str in page.extract_text().split('.'):   #对输入进行处理  (用英文结尾句号.来划分句子)
#             s_str = s_str.replace('\n','')      #去掉句子中的\n换行
#
#             if '?' in s_str:
#                 list_ret.extend(s_str.split('?'))
#             elif '!' in s_str:
#                 list_ret.extend(s_str.split('!'))
#             else:
#                 list_ret.append(s_str)
#
#         for s_str in list_ret:
#             #print(s_str+".\n")
#             s_str=s_str+".\n"         #每一个完整英语句子加上句号“.”，然后加个换行
#             print(s_str)



import urllib
import importlib,sys
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


def parse(DataIO, save_path):

    #用文件对象创建一个PDF文档分析器
    parser = PDFParser(DataIO)
    #创建一个PDF文档
    doc = PDFDocument()
    #分析器和文档相互连接
    parser.set_document(doc)
    doc.set_parser(parser)
    #提供初始化密码，没有默认为空
    doc.initialize()
    #检查文档是否可以转成TXT，如果不可以就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        #创建PDF资源管理器，来管理共享资源
        rsrcmagr = PDFResourceManager()
        #创建一个PDF设备对象
        laparams = LAParams()
        #将资源管理器和设备对象聚合
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        #创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmagr, device)

        #循环遍历列表，每次处理一个page内容
        #doc.get_pages()获取page列表
        for page in doc.get_pages():
            interpreter.process_page(page)
            #接收该页面的LTPage对象
            layout = device.get_result()
            #这里的layout是一个LTPage对象 里面存放着page解析出来的各种对象
            #一般包括LTTextBox，LTFigure，LTImage，LTTextBoxHorizontal等等一些对像
            #想要获取文本就得获取对象的text属性
            for x in layout:
                try:
                    if(isinstance(x, LTTextBoxHorizontal)):
                        with open('%s' % (save_path), 'a') as f:
                            result = x.get_text()
                            print (result)
                            f.write(result + "\n")
                except:
                    print("Failed")


if __name__ == '__main__':
    #解析本地PDF文本，保存到本地TXT
    with open(r'2005-2009真题(英语一二通用).pdf','rb') as pdf_html:
        parse(pdf_html, r'd.txt')

    #解析网络上的PDF，保存文本到本地
    # url = "https:"
    # pdf_html = urllib.urlopen(url).read()
    # DataIO = StringIO(pdf_html)
    # parse_pdf(DataIO, r'E:\parse_pdf')
