import pymssql #引入pymssql模块 



def ReadFiles():
    # index=1
    f = open('F:\周鑫\Project\GitHub\PythonHelper\importKnow\ms.txt', 'r',encoding='utf8')
    data= f.readlines()
    know=[]
    for item in data:
      if(len(item)<10):
          continue
      li=item.split('-')
    #  // i=li[0].split(".") 
    #  // numbers = [int(x) for x in i]     
      que={
          "index":li[0].replace(".",""),
          "ti":li[1].replace('\n',''),
          "id":'' if len(li)<3 else li[2].replace('\n',''),
      }
      know.append(que)   
    f.close()   
    for num in range(1,8):
        tempknow=[]
        for n in know:
            if(n['index'].startswith(str(num))):#第一层
                tempknow.append(n) 
        all= TakeChil(str(num),tempknow)
    index=1
    # index+=1
  


def TakeChil(parentId,data):#1,1  
    
    que={
        "name":'',
        "data":que
    }
    for item in data:        
        if(item['index'].startswith(parentId)and len(item['index'])==len(parentId)):            
            tempknow.append(item)           
        else:
            que={
                "data":TakeChil(item['index'],data)
            }
    que.name=item.ti
    que.data=tempknow
    return tempknow

ReadFiles()    