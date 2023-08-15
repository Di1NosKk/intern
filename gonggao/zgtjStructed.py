# -*- coding: utf-8 -*-
import re
# re 需补充标题、
# SPLIST_LIST = ['\d+\、+[^\d]','\d+\丶+[^\d]', '\d+\.+[^\d]', '\（\d\）', '\(\d\)','\d+\.+\d+[^\d]', '\d+\.+\d+\.+\d+[^\d]']
# SPLIST_LIST = ['\d+\、+[^\d]','\d+\丶+[^\d]', '\d+\.+[^\d]', '\（\d\）', '\(\d\)','\d+\.+\d+[^\d]', '\d+\.+\d+\.+\d+[^\d]', '（[一|二|三|四|五|六]）','\([一|二|三|四|五|六|七]\)']
# SPLIST_LIST = ['\d+\、+[^\d]','\d+\丶+[^\d]', '\（\d\）', '\(\d\)','[1-9]{1}.{1}[1-9]{0,1}.{0,1}[1-9]','（[一|二|三|四|五|六]）','[1-9]{1}）','（[一|二|三|四|五|六]）','\([一|二|三|四|五|六|七]\)']
# SPLIST_LIST = [r'\d{1}[.]{1}[^\d]', r'\d+\、+[^\d]', '\d+\丶+[^\d]', r'\（\d\）', r'\(\d\)',r'[1-9]{1}[\.]{1}[1-9]{0,1}[\.]{0,1}[1-9]',r'（[一|二|三|四|五|六]）',r'[1-9]{1}）',r'（[一|二|三|四|五|六]）',r'\([一|二|三|四|五|六|七]\)']

SPLIST_LIST = [r"\d{1}[．]{1}[^\d]",r'\d{1}[.]{1}[^\d]', r'\d+\、+[^\d]', '\d+\丶+[^\d]', r'\（\d\）', r'\(\d\)',r'[1-9]{1}[\.]{1}[1-9]{0,1}[\.]{0,1}[1-9]',r'（[一|二|三|四|五|六]）',r'（[一|二|三|四|五|六]）',r'\([一|二|三|四|五|六|七]\)',r'[1-9]{1}）']
# SPLIST_LIST = [r'\d{1}[.]{1}[^\d]', r'\d+\、+[^\d]', '\d+\丶+[^\d]', r'\（\d\）', r'\(\d\)',r'[1-9]{1}[\.]{1}[1-9]{0,1}[\.]{0,1}[1-9]',r'（[一|二|三|四|五|六]）',r'（[一|二|三|四|五|六]）',r'\([一|二|三|四|五|六|七]\)',r'[1-9]{1}）']

def structurize_text(text: str):
    re_local = dict()
    for item in SPLIST_LIST:
        result = re.finditer(string=text, pattern=item)
        
        for item_2 in result:
            if item_2.span()[0]-1 not in re_local.keys() and item_2.span()[0]+3 not in re_local.keys()and item_2.span()[0]+2 not in re_local.keys():
                re_local[item_2.span()[0]] = item
            # re_local[item_2.span()[0]] = item
    if re_local == dict():
        print("zgtj re question, please check!!!")
        return dict()
    sorted_dict = dict(sorted(re_local.items(), key=lambda x: x[0]))
    return recur(text=text, re_local_dict=sorted_dict, relocal_dict_or=sorted_dict)

def recur(text:str, re_local_dict, relocal_dict_or)->dict:
    # 构建 返回值 形式
    result = {"children":[]}
    # len_re_local_dict = len(re_local_dict)
    # 找到 与首元素 value 相同值 所在 的 位置
    same_lab_local_list = match_first_local(my_dict=re_local_dict)
    # 循环递归
    re_local_dict_key_list = list(re_local_dict.keys())
    re_local_dict_key_list_or = list(relocal_dict_or.keys())
    for index in range(len(same_lab_local_list)-1):
        # 判断当前位置的内容是否存在多级标签

        try:
            if same_lab_local_list[index + 1] - same_lab_local_list[index] == 1:
                # 不存在多级标签

                result["children"].append({"name": text[re_local_dict_key_list[same_lab_local_list[index]]:
                                                        re_local_dict_key_list[same_lab_local_list[index + 1]]]})
                pass
            else:
                # 存在多级标签 截取 多级 标签 的 位置
                # 这里start_position index+1了注意
                tranc_re_local_dict = tranc_dict_local(my_dict=re_local_dict,
                                                       start_position=same_lab_local_list[index]+1,
                                                       end_position=same_lab_local_list[index + 1])
                recur_result = recur(text=text,re_local_dict=tranc_re_local_dict,relocal_dict_or=relocal_dict_or)
                result["children"].append({"name":text[re_local_dict_key_list[same_lab_local_list[index]]:re_local_dict_key_list[same_lab_local_list[index]+1]], list(recur_result)[0]:recur_result.get(list(recur_result)[0]) })
                # result["children"]["children"].append(recur(text=text, re_local_dict=tranc_re_local_dict))
        except IndexError as f:
            print(f)
            pass
    # 剩下最后一位 不放在异常里面了
    len_same_lab = len(same_lab_local_list)
    re_local_len = len(re_local_dict)
    if same_lab_local_list[-1] + 1 == re_local_len:
        try:
            result["children"].append({"name": text[re_local_dict_key_list[same_lab_local_list[len_same_lab-1]]:re_local_dict_key_list_or[re_local_dict_key_list_or.index(re_local_dict_key_list[same_lab_local_list[len_same_lab-1]])+1]]})
        except Exception:
            result["children"].append({"name": text[re_local_dict_key_list[same_lab_local_list[len_same_lab-1]]:]})
    else:
        # 这里start_position index+1了注意
        tranc_re_local_dict = tranc_dict_local(my_dict = re_local_dict,
                                                   start_position = same_lab_local_list[-1]+1,
                                                   end_position = re_local_len)

        recur_result = recur(text=text, re_local_dict = tranc_re_local_dict, relocal_dict_or=relocal_dict_or)
        result["children"].append({"name": text[re_local_dict_key_list[same_lab_local_list[-1]]:
                                                re_local_dict_key_list[same_lab_local_list[-1]+1]],
                                   list(recur_result)[0]: recur_result.get(list(recur_result)[0])})
    # print(result)
    return result
def tranc_dict_local(my_dict:dict,start_position:int, end_position:int)->dict:
    # 获取字典的键值对列表
    items = list(my_dict.items())
    # 截取指定位置的元素
    sliced_items = items[start_position:end_position]

    # 将截取后的元素转换为字典
    sliced_dict = dict(sliced_items)
    # return sliced_dict, end_item
    return sliced_dict
def match_first_local(my_dict:dict):
    # 获取首个元素的值
    first_value = list(my_dict.values())[0]
    # 遍历字典的键值对列表
    matching_positions = []
    index = 0
    for key, value in my_dict.items():
        if value == first_value:
            # matching_positions.append(key)
            matching_positions.append(index)
        index=index+1
    # print(matching_positions)
    return matching_positions #返回首元素位置
if __name__ == "__main__":
    text='资格条件：1.营业执照（三证合一）；2.质量认证体系；3.代理商需提供代理资质；4.近两年类似我司产品成交业绩。'
    text='资格条件：1.营业执照（三证合一）；2.质量认证体系；3.代理商需提供代理资质；4.近两年类似我司产品成交业绩。'
    print(text)
    print("-------------------")
    result = structurize_text(text=text)
    print("----------------------")
    print(result)
