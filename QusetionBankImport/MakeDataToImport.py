import pymssql #引入pymssql模块 
import json
import re
import lxml
from ConnectSql import ConnectSql
from bs4 import BeautifulSoup


def AnalyData():
    Connectsql=ConnectSql()
    connectmysql=Connectsql.ConnectMySql('119.23.152.14:1999','sa','Ylm123456','YLM_AFT')    
    cursor = connectmysql.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
    sql="select  * from Tb_KnowledgeQuestion_Article where jsonContent is not null and jsonContent!=''"#高中
    cursor.execute(sql)   #执行sql语句
    rows=cursor.fetchall()   
    queList=[]
    for i in rows:
        # aa=json.loads(i[22])
        # soup = BeautifulSoup(i[22],'html.parser').get_text(strip=True) #去除HTML  
        ss=json.loads(i[22])
        # que=ss.get("public_question")#问题
        # analysis=ss.get("public_analysis")#分析
        asks= ss.get("sub_question")#问题        
        askList=[]
        for ask in asks:            
            # askque=StringConfiom(ask.get("question").get("question"))#题目
            # askanswer=StringConfiom(ask.get("answer"))#答案
            # askany=StringConfiom(ask.get("analysis"))# 题目分析
            askoption=ask.get("question").get("option")#选项
            options=[] #选项
            for option in askoption: 
                option={
                    "index":BeautifulSoup(TakeOptionIndex(option),'html.parser').get_text(strip=True) ,
                    "Text":BeautifulSoup(TakeOptionText(option),'html.parser').get_text(strip=True) 
                }
                options.append(option)
                # options=options+","+('{"index":"'+TakeOptionIndex(option)+'","Text":"'+TakeOptionText(option)+'"}')
                # index=TakeOptionIndex(option)
                # text=TakeOptionText(option)    
            # jsonOptions=json.dumps(options, ensure_ascii=False)    #选项Json  
            sub_question={
                "question":StringConfiom(BeautifulSoup(ask.get("question").get("question"),'html.parser').get_text(strip=True)),
                "answer":StringConfiomAns(BeautifulSoup(ask.get("answer"),'html.parser').get_text(strip=True)),
                "askany":StringConfiom(BeautifulSoup(ask.get("analysis"),'html.parser').get_text(strip=True).replace("</div","")),
                "option":options
            }
            askList.append(sub_question)
            #askList=askList+","+'{"question":"'+StringConfiom(ask.get("question").get("question"))+'","answer":"'+StringConfiom(ask.get("answer"))+'","askany":"'+StringConfiom(ask.get("analysis"))+'","option":['+options+']}'
        #askList="["+askList[1::]+"]"
        #jsonAsk= json.dumps(askList,ensure_ascii=False)
        # print(askList)
        #    ss = json.dumps(dict(zip(columnNames, list_)))
        que={
            "public_question":BeautifulSoup(ss.get("public_question"),'html.parser').get_text(strip=True),
            "public_analysis":BeautifulSoup(ss.get("public_analysis"),'html.parser').get_text(strip=True),
            "year":i[5],
            "degree":i[8],
            "subject":i[2],
            "Unid":i[1],
            "sub_question":askList
        }                
        jd=transferContent(json.dumps(que,ensure_ascii=False))
        sql = "update Tb_KnowledgeQuestion_Article set dataother='{}' where IdKey={}".format(jd,i[0])
        cursor.execute(sql)
        connectmysql.commit() 
       # queList.append(que)
        #queList.extend() #批量添加
        # queList=queList+","+'{"public_question":"'+ss.get("public_question")+'","public_analysis":"'+ss.get("public_analysis")+'","sub_question":"['+askList[1::]+']}'
    # queList=queList[1::]
    cursor.close()
    connectmysql.close()
    # jsondata=json.dumps(queList,ensure_ascii=False)#吧python转换成Json字符串    
    # data=json.loads(jsondata)#把Json字符串转换为Python对象
    # for item in data:
    #     #print(item.get("public_question"))
    #     print(f'------{item.get("public_question")}------')
    
#删除字符串中的【小题1】标示
def StringConfiom(text):    
    startIndx= text.find("【") 
    if(startIndx!=-1):#存在
         endIndex=text.find("】") 
         return text[endIndex+1::]
    return text
def StringConfiomAns(text): 
    text=text.replace(" ", "")   
    startIndx= text.find("【") 
    if(startIndx!=-1):#存在
         endIndex=text.find("】") 
         return text[endIndex+1:endIndex+2:]
    return text
#选项分离出ABCD 
def TakeOptionIndex(text):
    string=text.strip()
    return text.strip()[0:1:1]
#选项分离出文字
def TakeOptionText(text):
    string=text.strip()
    return text.strip()[2::].strip()

def transferContent(content):
        if content is None:
            return None
        else:
            string = ""
            for c in content:
                # if c == '"':
                #     string += '\\\"'
                if c == "'":
                    string += "''"
                # elif c == "\\":
                #     string += "\\\\"
                else:
                    string += c
            return string
AnalyData()