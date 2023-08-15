import sys
import re
from recognize_contact import get_man_org
import pymysql as pmq



con_mysql = pmq.connect(host='101.36.73.80',user='root',password='4b4767af8182be0e',database='pm345')
cursor_mysql = con_mysql.cursor()
sql1=''
try:
    id = 1620750
    sql = "select id, gglx,url,fb_day,created_at,content from jdggxq where id >={} and id <={}".format(int(id), int(id))  
    # sql = "select id, gglx,url,fb_day,created_at,content from jdggxq where id >={} and id <={}".format(int(id), int(id)+3000)  

    res = cursor_mysql.execute(sql)
    ans = cursor_mysql.fetchall()
    for line in ans:
        id = line[0]
        print(str(id)+":"+line[2]) 
        info = get_man_org(line[5])
        print(info)
        #res = ''
        # try:
        #     #for k in info:
        #     #    res = k+":"+str(info[k])+'\t'+res
        #     #print(res+'\t'+str(line[0])+'\t'+line[2])
        #     #if info['delivery_time'] !='' and info['delivery_address'] !='':
        #     #    print(str(id)+":"+str(line[2]))
        #     #    print(info)
        #     print(info)
        # except Exception as e:
        #     print(str(id)+":2222 "+line[2])
        #     print(info)
        #     print(str(e))
        #     break
    cursor_mysql.close()
    con_mysql.close()
except Exception as e:
    print(str(e))
    print("ddddddddddddddddddddddd")

