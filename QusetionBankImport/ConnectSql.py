import pymssql #引入pymssql模块 


class ConnectSql():
    def ConnectMySql(self,ip,user,name,database):
         connect = pymssql.connect(ip, user, name, database) #服务器名,账户,密码,数据库名
         if connect:
             print("连接成功!")
             return connect 
 
        #  cursor = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
        #  sql = "sp_columns  ac_PaymentBooks_his"
        #  cursor.execute(sql)   #执行sql语句
        #  row = cursor.fetchone()  #读取查询结果,
        #  while row:              #循环读取所有结果
        #      row = cursor.fetchone()
        #      print(row)


# # 将SQL查询结果转换为PANDAS数据结构DataFrame
# import pandas as pd
# df = pd.read_sql(sql, connect) 