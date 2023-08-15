import sys
import re
import os
from recognize_gaikuang import get_table_info, get_release_address
import pymysql as pmq

con_mysql = pmq.connect(host='101.36.73.80', user='root', password='4b4767af8182be0e', database='pm345')
cursor_mysql = con_mysql.cursor()
sql1=''
try:
    sql = "select id,gglx,url,content from jdggxq where  gglx = 26 and id=1963296"
    #1776747   1775891   1785398    1785493
    # 1775581 http://plap.mil.cn/freecms/site/juncai/ggxx/info/2023/6CA8E645E1EC428785ECB235740C04D7.html
    # 1777042 http://plap.mil.cn/freecms/site/juncai/ggxx/info/2023/26E9E3263F824C46BF34E2D92BB62CB6.html
    # 1777152 http://plap.mil.cn/freecms/site/juncai/ggxx/info/2023/6A3B3B8667AB46DFA705B9AE8014B732.html
    # 1780731 http://plap.mil.cn/freecms/site/juncai/ggxx/info/2023/693FD5A8323C4570B77553A801394D27.html
    # sql = "select id,gglx,url,content from jdggxq where  gglx = 26 and id>=1875000 and id <= 2064152 and url like '%mil%'"

    res = cursor_mysql.execute(sql)
    ans = cursor_mysql.fetchall()
    for line in ans:
        id = line[0]
        print("result: "+str(id)+"\t"+line[2])
        project_summary = get_table_info(line[3])
        print(project_summary)
        
        #if  project_summary['summary'] != dict():
            #print(project_summary)
        # if  project_summary['accept_number'] == "":
        #     print("result: "+str(id)+"\t"+line[2])
            # print("inside")

    cursor_mysql.close()
    con_mysql.close()
except Exception as e:
    print(str(e))
    print(sql1)
    print("ddddddddddddddddddddddd")

