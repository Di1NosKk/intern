import re
import jionlp
from collections import defaultdict

p = re.compile( '<[^>]+>' )

schema = ['预算金额','预算总金额','预算总额：','预算:','预算：','预算', '报价限额：','最高限价','投标限价','采购预算','金额(元)','最高价','总价(元)','限价（万元）','控制价：','项目概算（万元）','项目总投资：','预算价','总保险费用约','合同估算价：','采购总额','采购总预算','采购产品金额','合同金额','总投资额：','总控制价','控制价为','项目预算：','预算总价','项目预算']
 
    
"""filter info"""
def filter_zgtj(content):
    lst1 = []
    lst_index = []
    for j in range(len(zgtj)): 
        index1 = content.find(zgtj[j])
        if index1 != -1: 
            lst1.append(index1+len(zgtj[j]))
            lst_index.append(index1-2)
            
    return lst1,lst_index

def filter_fbqd(content):
    lst1 = []
    lst_index = []
    for j in range(len(fbqd)): 
        index1 = content.find(fbqd[j])
        if index1 != -1: 
            lst1.append(index1+len(fbqd[j]))
            lst_index.append(index1-2)
            
    return lst1,lst_index

def filter_end(content, xy):
    lst1 = []
    if xy in zgtj_end:
        ij = zgtj_end.index(xy) + 1
    else:
        ij = 0
    while ij < len(zgtj_end):
        index1 = content.find(zgtj_end[ij])
        if index1 != -1: 
            lst1.append(index1)
        ij += 1
    return lst1


def filter_end1(content, xy):
    lst1 = []
    if xy in zgtj_end1:
        ij = zgtj_end1.index(xy) + 1
    else:
        ij = 0
    while ij < len(zgtj_end1):
        index1 = content.find(zgtj_end1[ij])
        if index1 != -1: 
            lst1.append(index1)
        ij += 1
    return lst1

def clear_baoming_info(content: str) -> str:
    content = jionlp.remove_html_tag(content)
    pattern1 = r'\{[^{}]*?\}'
    pattern2 = r'\<[^<>]*?\>'
    content = re.compile(pattern2).sub('', content)
    content = re.compile(pattern1).sub('', content)
    content = content.replace("\xa02", "").replace("\xa01", "").replace("\xa0", "").replace(" ", "").replace(";",
                                                                                                             "").replace(
        "\u3000", "").replace("&nbsp", "").replace("■", "").replace("★", "").replace("_", "").replace("\\t", "").split(
        "\\n")
    content = [item for item in content if item != '' or "notice" not in item or "font" not in item]
    return "".join(content)

def handle_delivery_outside(original_content, keywords):
    try:
        table_start = original_content.find("<table ")
        table_end = original_content.find("</table>") + len("</table>")
        table_content = original_content[table_start:table_end]
        # print(table_content)
        
        lst_tr_start = []
        lst_tr_end = []
        tr_start = 0
        tr_end = 0
        tr_content = []
        
        # 取table每一行的信息
        while table_content.find("<tr", tr_start) != -1:
            lst_tr_start.append(table_content.find("<tr", tr_start))
            lst_tr_end.append(table_content.find("</tr>", tr_end) + len("</tr>")) 
            tr_start = table_content.find("<tr", tr_start) + 1
            tr_end = table_content.find("</tr>", tr_end) + 1
        for i in range(len(lst_tr_start)):
            tr_content.append(table_content[lst_tr_start[i]:lst_tr_end[i]])
        
        tr_content = [p.sub('', tr_cont) for tr_cont in tr_content]
        for tr_cont in tr_content:
            for keyword in keywords:
                if keyword in tr_cont:
                    index = tr_cont.find(keyword) + len(keyword)
                    return tr_cont[index + 1:].replace("\n", "").replace("&nbsp", "").replace(";", "")
    except Exception as e:
        print(e)
        
def handle_table_info(original_content, keywords):
    try:
        table_start = original_content.find("<table ")
        table_end = original_content.find("</table>") + len("</table>")
        table_content = original_content[table_start:table_end]
        
        lst_tr_start = []
        lst_tr_end = []
        tr_start = 0
        tr_end = 0
        tr_content = []
        
        # 取table每一行的信息
        while table_content.find("<tr", tr_start) != -1:
            lst_tr_start.append(table_content.find("<tr", tr_start))
            lst_tr_end.append(table_content.find("</tr>", tr_end) + len("</tr>")) 
            tr_start = table_content.find("<tr", tr_start) + 1
            tr_end = table_content.find("</tr>", tr_end) + 1
        for i in range(len(lst_tr_start)):
            tr_content.append(table_content[lst_tr_start[i]:lst_tr_end[i]])

        td_content = []
        price_content = []
        combine = False
        # 取每一行中单元格的信息
        for i in range(len(tr_content)):
            lst_td_start = []
            lst_td_end = []
            td_start = 0
            td_end = 0
            if "<th" in tr_content[i]:
                while tr_content[i].find("<th", td_start) != -1:
                    colspan_content = tr_content[i][td_end:]
                    if tr_content[i].find("<th", td_start) <  (tr_content[i].find("<th", td_end)+colspan_content.find("colspan=")) < tr_content[i].find("</th>", td_end) and colspan_content.find("colspan=") != -1:
                        colspan = int(colspan_content[colspan_content.find("colspan=") + len("colspan=") + 1])
                        if colspan == len(td_content):
                            combine = True
                        for j in range(colspan):
                            lst_td_start.append(tr_content[i].find("<th", td_start))
                            lst_td_end.append(tr_content[i].find("</th>", td_end) + len("</th>"))
                    else: 
                        lst_td_start.append(tr_content[i].find("<th", td_start))
                        lst_td_end.append(tr_content[i].find("</th>", td_end) + len("</th>"))
                    td_start = (tr_content[i].find("<th", td_start)) + 1
                    td_end = (tr_content[i].find("</th>", td_end)) + 1
            elif "<td" in tr_content[i]:
                while tr_content[i].find("<td", td_start) != -1:
                    colspan_content = tr_content[i][td_end:]
                    if tr_content[i].find("<td", td_start) < (tr_content[i].find("<td", td_end)+colspan_content.find("colspan=")) < tr_content[i].find("</td>", td_end) and colspan_content.find("colspan=") != -1:
                        colspan = int(colspan_content[colspan_content.find("colspan=") + len("colspan=") + 1])
                        if colspan == len(td_content):
                            combine = True
                        for j in range(colspan):
                            lst_td_start.append(tr_content[i].find("<td", td_start))
                            lst_td_end.append(tr_content[i].find("</td>", td_end) + len("</td>"))
                    else: 
                        lst_td_start.append(tr_content[i].find("<td", td_start))
                        lst_td_end.append(tr_content[i].find("</td>", td_end) + len("</td>"))
                    td_start = (tr_content[i].find("<td", td_start)) + 1
                    td_end = (tr_content[i].find("</td>", td_end)) + 1
                    
            if i == 0:
                for j in range(len(lst_td_start)):
                    td_content.append(tr_content[0][lst_td_start[j]:lst_td_end[j]])
            if combine is False:
                if i == 1:
                    for j in range(len(lst_td_start)):
                        price_content.append(tr_content[1][lst_td_start[j]:lst_td_end[j]])
            if combine is True:
                if i == 2:
                    for j in range(len(lst_td_start)):
                        price_content.append(tr_content[2][lst_td_start[j]:lst_td_end[j]])

        # 判断关键词是否在列表里
        index_price = -1
        td_content = [p.sub('', td_cont) for td_cont in td_content]
        price_content = [p.sub('', price_cont) for price_cont in price_content]
        td_content = [td_cont.replace("\n", "").replace(";", "").replace("&nbsp", "").replace(" ","") for td_cont in td_content]
        price_content = [price_cont.replace("\n", "").replace("&nbsp", "").replace(";", "").replace(" ","") for price_cont in price_content]
        for i in range(len(td_content)):
            for key in keywords:
                if key in td_content[i]:
                    index_price = i
        if index_price == -1:
            return ""
        if price_content == []:
            return ""
        return str(price_content[index_price]).replace("\n","").replace("&nbsp", "").replace(";", "")
    except Exception as e:
        print(e)
        
    
def handle_table(original_content):
    try:
        ans = defaultdict(list)
        table_start = original_content.find("<table ")
        table_end = original_content.find("</table>") + len("</table>")
        table_content = original_content[table_start:table_end]
        
        lst_tr_start = []
        lst_tr_end = []
        tr_start = 0
        tr_end = 0
        tr_content = []
        
        # 取table每一行的信息
        while table_content.find("<tr", tr_start) != -1:
            lst_tr_start.append(table_content.find("<tr", tr_start))
            lst_tr_end.append(table_content.find("</tr>", tr_end) + len("</tr>")) 
            tr_start = table_content.find("<tr", tr_start) + 1
            tr_end = table_content.find("</tr>", tr_end) + 1
        for i in range(len(lst_tr_start)):
            tr_content.append(table_content[lst_tr_start[i]:lst_tr_end[i]])

        td_content = []
        price_content = []
        combine = False
        # 取每一行中单元格的信息
        for i in range(len(tr_content)):
            total_content = []
            lst_td_start = []
            lst_td_end = []
            td_start = 0
            td_end = 0
            if "<th" in tr_content[i]:
                while tr_content[i].find("<th", td_start) != -1:
                    colspan_content = tr_content[i][td_end:]
                    if tr_content[i].find("<th", td_start) <  (tr_content[i].find("<th", td_end)+colspan_content.find("colspan=")) < tr_content[i].find("</th>", td_end) and colspan_content.find("colspan=") != -1:
                        colspan = int(colspan_content[colspan_content.find("colspan=") + len("colspan=") + 1])
                        if colspan == len(td_content):
                            combine = True
                        for j in range(colspan):
                            lst_td_start.append(tr_content[i].find("<th", td_start))
                            lst_td_end.append(tr_content[i].find("</th>", td_end) + len("</th>"))
                    else: 
                        lst_td_start.append(tr_content[i].find("<th", td_start))
                        lst_td_end.append(tr_content[i].find("</th>", td_end) + len("</th>"))
                    td_start = (tr_content[i].find("<th", td_start)) + 1
                    td_end = (tr_content[i].find("</th>", td_end)) + 1
            elif "<td" in tr_content[i]:
                while tr_content[i].find("<td", td_start) != -1:
                    colspan_content = tr_content[i][td_end:]
                    if tr_content[i].find("<td", td_start) < (tr_content[i].find("<td", td_end)+colspan_content.find("colspan=")) < tr_content[i].find("</td>", td_end) and colspan_content.find("colspan=") != -1:
                        colspan = int(colspan_content[colspan_content.find("colspan=") + len("colspan=") + 1])
                        if colspan == len(td_content):
                            combine = True
                        for j in range(colspan):
                            lst_td_start.append(tr_content[i].find("<td", td_start))
                            lst_td_end.append(tr_content[i].find("</td>", td_end) + len("</td>"))
                    else: 
                        lst_td_start.append(tr_content[i].find("<td", td_start))
                        lst_td_end.append(tr_content[i].find("</td>", td_end) + len("</td>"))
                    td_start = (tr_content[i].find("<td", td_start)) + 1
                    td_end = (tr_content[i].find("</td>", td_end)) + 1
                    
            if i == 0:
                for j in range(len(lst_td_start)):
                    td_content.append(tr_content[0][lst_td_start[j]:lst_td_end[j]])
            else:
                for j in range(len(lst_td_start)):
                    total_content.append(tr_content[i][lst_td_start[j]:lst_td_end[j]])
            price_content.append(total_content)
        price_content = price_content[1:]
        # print(price_content)
        # 判断关键词是否在列表里
        index_price = -1
        td_content = [p.sub('', td_cont) for td_cont in td_content]
        for i in range(len(price_content)):
            for j in range(len(price_content[i])):
                price_content[i][j] = p.sub('', price_content[i][j])

        td_content = [td_cont.replace("\n", "").replace(";", "").replace("&nbsp", "").replace(" ","") for td_cont in td_content]
        for i in range(len(price_content)):
            for j in range(len(price_content[i])):
                price_content[i][j] = price_content[i][j].replace("\n", "").replace("&nbsp", "").replace(";", "").replace(" ","") 

        for i in range(len(td_content)):
            for j in range(len(price_content)):
                if len(price_content[j]) < len(td_content):
                    price_content[j] += [""] * (len(td_content)-len(price_content[j]))
                
                ans[td_content[i]].append(price_content[j][i])
        return dict(ans)
    except Exception as e:
        print(e)


zgtj_end = ['一、','二、','三、', '四、', '五、', '六、', '七、', '八、','九、','十、','十一、','十二、','十三、','十四、']
zgtj_end1 = ['1.', '2.', '3.', '4.', '5.','6.','7.','8.','9.','10.','11.','12.','13.','14.']
zgtj = ['项目情况：', '项目概况：','项目概况', '采购内容', '采购需求：', '服务内容及相关要求：', '初步技术参数', '交付条件','项目内容', '项目基本情况：','采购项目基本内容']
tmp_zgtj = ["、申请人资格要求","、投标单位资格条件","、供应商资格条件","、供应商应具备的资格","、供应商资格要求","、投标资格能力要求","、竞优人资格条件","、投标人的资格条件", "、报价人资格条件", '、申请人的资格要求', "、投标人资格要求",
                         "、投标人的资格要求", "、合格投标人资格", "、投标供应商资格条件", "、供应商的资格条件","、投标人资质要求",
                         ".投标人资格要求","、合格投标人的资格要求","、报价供应商资格条件","、磋商供应商资格要求", "、投标人资格条件", "、企业资格要求","、供应商的资格要求", 
                         "、投标人资格","、报价方资格要求","资格预审：", "投标人资格要求"]
fbqd = ['信息发布渠道','采购信息发布','本项目相关信息','本采购项目相关信息','发布公告的媒介','发布公告媒介','网上公告媒体查询：']
result = {
    "summary": "",
    "baoshu":"",
    "project_shuoming":"",
    "is_accept":"",
    "accept_number":"",
    "project_name": "",
    "delivery_time": "",
    "delivery_address": "",
    "quantity": "",
    "unit_price": "",
    "release_address": ""
}

def get_release_address(content):
    try:
        content = clear_baoming_info(content)
        ls,ls_index = filter_fbqd(content)
        if ls != []:
            cont = content[min(ls):]
        else: 
            cont = ""
        if ls_index != []:
            xy = content[min(ls_index):min(ls_index)+2]

        # 申请人资格要求字段填写
        if cont != "":
            ls_tmp = filter_end(cont, xy)
            if ls_tmp != []:
                new_cont = cont[:min(ls_tmp)]
            else:
                ls_num = filter_end1(cont, xy)
                if ls_num != []:
                    new_cont = cont[:min(ls_num)]
                else:
                    new_cont = cont
            new_cont = new_cont.replace("&nbsp", "").replace("\n", "").replace(" ","").replace("\t","")
            new_cont = new_cont[:new_cont.find("。")+1]
            pattern = r"(?:https?://)?(?:www\.)?[\w.-]+\.[a-zA-Z]{2,6}(?:/[\w.-]*)*(?:\?[^\s]*)?|https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
            links = re.findall(pattern, new_cont)
            if len(links) > 0:
                address = ", ".join(links)
            else: 
                address = new_cont
            return address
        else:
            return ""
    except Exception as e:
        print(e)
        
def first_table(content, t): 
    try:
        ls,ls_index = filter_zgtj(content)
        if ls != []:
            cont = content[min(ls):]
        else: 
            cont = ""
        if ls_index != []:
            xy = content[min(ls_index):min(ls_index)+2]
            symbol = content[min(ls_index)+1:min(ls_index)+2]
            global zgtj_end1
            for i in range(len(zgtj_end1)):
                zgtj_end1[i] = zgtj_end1[i].replace(".", symbol)
        if cont != "":
            ls_tmp = filter_end(cont, xy)
            if ls_tmp != []:
                new_cont = cont[:min(ls_tmp)]
            else:
                ls_num = filter_end1(cont, xy)
                if ls_num != []:
                    new_cont = cont[:min(ls_num)]
                else:
                    new_cont = cont
            
            if t is True:
                for value in tmp_zgtj:
                    if value in new_cont:
                        stop = new_cont.find(value)
                        new_cont = new_cont[:stop]
                        break
                    
            if "联合体" in content:
                result["is_accept"] = "否"
            
            # 供应商中标情况
            gys_bid = ["供应商中标","供应商成交"]
            gys_start = ["本项目"]
            gys_end = -1
            for key in gys_bid:
                number_index = content.rfind(key)
                if number_index != -1:
                    gys_end = number_index + len(key)
            gys_ilst = []
            for s in gys_start:
                number_index = content[:gys_end].rfind(s)
                if number_index != -1:
                    gys_ilst.append(number_index)
            if gys_end == -1 or gys_ilst == []:
                result["accept_number"] = "1家"
            else: 
                result["accept_number"] = content[max(gys_ilst):gys_end]
            result['delivery_address'] = new_cont.replace("&nbsp", "").replace("\n", "").replace(" ","").replace("\t","")
            result['delivery_address'] = result['delivery_address'][0:254]
            result['delivery_time'] = result['delivery_time'][0:254]
            result["project_name"] = result["project_name"][0:254]
            result["quantity"] = result["quantity"][0:254]
            result["unit_price"] = result["unit_price"][0:254].replace("\\","")
            result["accept_number"] = result["accept_number"][0:254]
            result["project_shuoming"] = result["project_shuoming"][0:254]
            return result
        else: 
            return result
    except Exception as e: 
        print(e)

def get_table_info(content):
    try:
        result["release_address"] = get_release_address(content)[0:255]
        original_content = content
        content = clear_baoming_info(content)
        
        if "<table" in original_content[0:10]:
            return first_table(content, False)
        
        name = ['名称','内容']
        time = ['交货时间','交付时间', '期限','交货期','服务期','项目完成时间', '服务时间',"供货期"]
        address = ['地点']
        quantity = ['数量']
        price = schema
        result['summary'] = handle_table(original_content)
        if result["summary"] == dict():
            result["baoshu"] = "1"
        else: 
            
            result["baoshu"] = str(len(result["summary"][list(result["summary"].keys())[0]]) - 1)
            if len(result["summary"][list(result["summary"].keys())[0]]) - 1 > 200:
                result["baoshu"] = "1"
        ## 提取项目概况 说明一栏
        index = -1
        for value in result["summary"].values():
            for i in range(len(value)):
                if "说明" in value[i]:
                    index = i
            if index != -1:
                result["project_shuoming"] = value[index]
        if index == -1:
            result["project_shuoming"] = ""
            
        result['project_name'] = handle_table_info(original_content, name)
        result['delivery_time'] = handle_table_info(original_content, time)
        result['delivery_address'] = handle_table_info(original_content, address)
        result['quantity'] = handle_table_info(original_content, quantity)
        result['unit_price'] = handle_table_info(original_content, price)
        # print(result)
        
        # 表格内第三行之后存在交货时间和地点的情况下
        if result['delivery_time'] == "" or result['delivery_time'] is None:
            result['delivery_time'] = handle_delivery_outside(original_content, time)
        if result['delivery_address'] == "" or result['delivery_address'] is None:
            result['delivery_address'] = handle_delivery_outside(original_content, address)
        # print(result)
        # 表格之外存在交货时间和地点的情况下
        time_outside = ["交付时间：", "交货时间：", "交付时限：", "交货期：", "供货期："]
        address_outside = ["交货/改造地点：", "交货地点：", "交付地点：", "供货地点："]
        if result['delivery_time'] == "" or result['delivery_time'] is None:
            for w in time_outside:
                if content.find(w) != -1:
                    start1 = content.find(w) + len(w)
                    tmp = content[start1:]
                    end1 = start1 + tmp.find("。")
                    end3 = start1 + tmp.find("；")
                    result['delivery_time'] = content[start1:min(end1,end3)]
        if result['delivery_address'] == "" or result['delivery_address'] is None:
            for w in address_outside:
                if content.find(w) != -1:
                    start2 = content.find(w) + len(w)
                    tmp = content[start2:]
                    end2 = start2 + tmp.find("。")
                    end4 = start2 + tmp.find("；")
                    result['delivery_address'] = content[start2:min(end2, end4)]
        
        # 联合体谈判 接受/不接受
        if "联合体" in content:
            result["is_accept"] = "否"
        
        # 供应商中标情况
        gys_bid = ["供应商中标","供应商成交"]
        gys_start = ["本项目"]
        gys_end = -1
        for key in gys_bid:
            number_index = content.rfind(key)
            if number_index != -1:
                gys_end = number_index + len(key)
        gys_ilst = []
        for s in gys_start:
            number_index = content[:gys_end].rfind(s)
            if number_index != -1:
                gys_ilst.append(number_index)
        if gys_end == -1 or gys_ilst == []:
            result["accept_number"] = "1家"
        else: 
            result["accept_number"] = content[max(gys_ilst):gys_end]
                
        for i in result.items():
            if i[1] == None:
                result[i[0]] = ""
            elif i[0] == "summary":
                continue
            else:
                result[i[0]] = result[i[0]].replace("&nbsp", "").replace("\n", "").replace(" ","").replace("\t","").replace("\r", "")

        check = 0
        for i in result.items():
            if i[0] != "release_address" or i[0] != "summary" or i[0] != "baoshu":
                if i[1] == "":
                    check += 1

        if check == len(result)-1: 
            return first_table(content, True)

        result['delivery_address'] = result['delivery_address'][0:255]
        result['delivery_time'] = result['delivery_time'][0:255]
        result["project_name"] = result["project_name"][0:255]
        result["quantity"] = result["quantity"][0:255]
        result["unit_price"] = result["unit_price"][0:255].replace('\\','')
        result["accept_number"] = result["accept_number"][0:254]
        result["project_shuoming"] = result["project_shuoming"][0:254]
        return result
    except Exception as e:
        print(e)

