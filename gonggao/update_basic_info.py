import sys
import re
import os
from recognize_basic_info import get_basic_info
import pymysql as pmq
from tqdm import tqdm

con_mysql = pmq.connect(host='101.36.73.80', user='root', password='4b4767af8182be0e', database='pm345')
cursor_mysql = con_mysql.cursor()
sql1=''
try:
    # sql = "select id,gglx,url,content from jdggxq where  gglx = 26 and id>=2200000 and id <= 2244339  and url like '%mil%'"
    #sql = "select id,gglx,url,content from jdggxq where  gglx = 26 and id=2101412"
    sql = "select id,gglx,url,content from jdggxq where id=2327285"
    res = cursor_mysql.execute(sql)
    ans = cursor_mysql.fetchall()
    for line in tqdm(ans):
        id = line[0]
        #result = get_baoming_info_index_upg(clear_baoming_info(line[3]))
        #print(result)
        print("result: "+str(id)+"\t"+line[2])
        info = get_basic_info(line[3])
        print(info)
        if info['xmbh'] == '':
            print("不一样的我："+str(id) + "\t"+str(info)+line[2])
        # if info['tbr_zgtj'] != '' and info['bm_flow'] == '':
        #     print("不一样的我："+str(id)+str(info)+line[2])

    cursor_mysql.close()
    con_mysql.close()
except Exception as e:
    print(str(e))
    print(sql1)
    print("ddddddddddddddddddddddd")

