import re
import jionlp
from collections import defaultdict

p = re.compile( '<[^>]+>' )


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

        td_content = [td_cont.replace("\n", "").replace(";", "").replace("&nbsp", "").replace(" ","").replace("\xa0","").replace("\t","") for td_cont in td_content]
        for i in range(len(price_content)):
            for j in range(len(price_content[i])):
                price_content[i][j] = price_content[i][j].replace("\n", "").replace("&nbsp", "").replace(";", "").replace("\t","").replace(" ","").replace("\xa0","")

        for i in range(len(td_content)):
            for j in range(len(price_content)):
                if len(price_content[j]) < len(td_content):
                    price_content[j] += [""] * (len(td_content)-len(price_content[j]))
                
                ans[td_content[i]].append(price_content[j][i])
        return dict(ans)
    except Exception as e:
        print(e)

def get_index(table, lst):
    index = -1
    for i in range(len(table.keys())):
        for element in lst:
            if element in list(table.keys())[i]:
                index = i
    return index
        
def get_gys_info(value_list, index, ind):
    if index != -1:
        gys_info = value_list[index][ind]
    else:
        gys_info = ""
    return gys_info

def get_hittable(content):
    ans = []
    # content = clear_baoming_info(content)
    table = handle_table(content)
    if table == dict():
        return {}
    # print(table)
    gys_name_list = ["供应商名称","投标人名称","候选人名称","单位名称"]
    gys_address_list = ["供应商地址","地址"]
    gys_price_list = ["单价", "金额","报价","总价"]
    gys_discount_list = ["折扣率","下浮率"]
    gys_score_list = ["得分"]
    gys_phone_list = ["电话"]
    
    gys_name_index = get_index(table, gys_name_list)
    gys_address_index = get_index(table, gys_address_list)
    gys_price_index = get_index(table, gys_price_list)
    gys_discount_index = get_index(table, gys_discount_list)
    gys_score_index = get_index(table, gys_score_list)
    gys_phone_index = get_index(table, gys_phone_list)
    
    value_list = list(table.values())
    
    
    for j in range(len(value_list[0])):
        
        gys_name = get_gys_info(value_list, gys_name_index, j)
        gys_address = get_gys_info(value_list, gys_address_index, j)
        gys_price = get_gys_info(value_list, gys_price_index, j)
        gys_discount = get_gys_info(value_list, gys_discount_index, j)
        gys_score = get_gys_info(value_list, gys_score_index, j)
        gys_phone = get_gys_info(value_list, gys_phone_index, j)
            
        new_entry = {"gys_name": gys_name,
                "gys_address": gys_address, 
                "gys_price": gys_price,
                "gys_discount": gys_discount,
                "gys_score": gys_score,
                "gys_phone": gys_phone
                }
        
        ans.append(new_entry)

    # print(ans)
    return ans
    
    
