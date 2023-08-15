import os
import jionlp
import re
import datetime
import jieba
from paddlenlp import Taskflow
import paddlenlp
import json
# from similar_par import unify_vocab, tb_method_determineBybid_file_place_or_tb_method, bm_fangshi2bm_fangshi,bm_fangshi2bm_fangshi_2
from similar_par import *
from zgtjStructed import structurize_text
from datetime import datetime as datatime_son
import datetime as datatime_fat

path1 = "/home/albay/fl_test/"

reg_condition_keys_path = path1+ "data/0606_reg_condition_keys.txt"
credentials_condition_keys_path = path1+ "data/0606_credentials_vocab_keys.txt"

# schema = ["开标时间","开标地点"]
schema = ["tb_start_time","tb_place","tb_method","bid_open_time"]
ie_2 = Taskflow("information_extraction", schema=schema, task_path = path1 + "data/model/tb_best_model")

schema = ["bm_kaishi","bm_jieshu","am_begin_time","am_end_time","pm_begin_time","pm_end_time","bid_file_place","bm_fangshi"]
ie_3 = Taskflow("information_extraction",schema= schema,task_path  = path1 + "data/model/bm_best_model" )

# 相似度 判断 
KEYS_LIST_DICT = {
    "项目名称": ["、项目名称", ".项目名称", "项目名称："],
    "项目编号": ["、项目编号", ".项目编号","项目编号："],
    "项目基本情况": ["、项目概况", '、项目基本情况',
                    "、项目名称及编号", ".项目概况", 
                    "、招标内容", "、项目概况","项目概况："],
    "申请人的资格要求": [ "、合格企业资格要求","、外协报名单位资格要求","、资格要求","、申请人资格要求","、投标单位资格条件","、供应商资格条件","、供应商应具备的资格","、供应商资格要求","、投标资格能力要求","、竞优人资格条件","、投标人的资格条件", "、报价人资格条件", '、申请人的资格要求', "、投标人资格要求",
                         "、投标人的资格要求", "、合格投标人资格", "、投标供应商资格条件","、外协报名单位资格要求", 
                         "、供应商的资格条件","、投标人资质要求","、报名人资格条件","、报价单位资格要求",
                         ".投标人资格要求","、合格投标人的资格要求","、磋商供应商资格要求", 
                         "、投标人资格条件", "、企业资格要求","、供应商的资格要求", 
                         "、投标人资格","、报价方资格要求",
                         "．投标人资格要求","资格预审：",
                         "投标供应商资格条件"],
    # "招标文件售价":[".招标文件售价",],
    
    "报名材料清单及要求": ["、报名材料清单及要求"],
    "获取招标文件": ["、采购文件的获取","、招标文件获取时间、方式及地址","、获取招标文件","、发售招标文件具体要求","、《招标文件》发售时间", "、询价文件发售时间", "、招标文件发售", 
                     "、购买招标文件时间和地点", "、招标文件发放时间","、招标文件申领时间、地点、方式",
                     "、谈判文件发售时间、地点、方式及售价","、公告发布及获取招标文件获取时间","、招标文件获取",
                     "、谈判文件申领时间、地点、方式","、获取公开招标文件的地点、方式、期限及售价",
                     "、招标文件申领时间", "、采购文件的发售", "、竞争性磋商文件的发售时间及地点", ".公告发布及文件发售", ".招标文件的获取", "、招标文件的获取","招标文件申领时间、地点及方式:",
                     ".发售招标文件时间和地点", "、报名登记时间", "、获取征集文件",
                     "、获取采购文件","、报价文件获取时间","、询价文件申领时间、地点、方式",
                     "、报名及招标文件发售时间、地点、方式、售价","、报名及采购文件获取","、报名及采购文件的获取",
                     "、获取时间、方式","、领取招标文件",
                     ".发售招标文件时间",".发售招标文件时间和地点",".报名及招标文件发售时间、地点、方式、售价",
                     "．招标文件的获取",".购买招标文件时间和地点",
                     ".投标报名及资格初审，招标文件领取",
                     "招标文件发售与投标文件递交：",
                     "招标文件申领时间、地点、方式"],

    "提交投标文件": ["、投标截止时间和地点","、投标起止时间","、投标文件递交截止时间及地点",
                    "、投标文件递交截止时间及地点","、投标文件递交",
                    "、报价截止时间及地点", '、提交投标文件', "、响应文件提交截止时间","、报价文件递交时间、地点及方式",
                    '、开启', "、投标截止时间及地点","、投标保证金缴纳截止时间、方式",
                    "、投标开始时间","、报价文件接收开始和截止接收时间及地点、方式",
                    "、响应文件提交截止时间","、投标文件和样机的递交",
                    "、报价文件接受开始和截止接受时间及地点、方式",
                    "、报价文件递交截止时间","、报价文件递交开始和截止时间及地点、方式",
                    "、投标文件的递交","、投标文件接收信息","、提交投标文件截止时间、开标时间和地点",
                    "．投标文件的递交",
                    "、投标开始和截止时间及地点", ".投标截止时间", 
                    "、投标文件的递交时间及地点","开标时间:",
                    ".投标文件的递交",
                    "投标文件递交时间、地点、方式：",".投标截止时间及地点",
                    # "、询价方法及预算"
                    "投标开始和截止时间及地点、方式"
                    ],
    "公告期限": ['、公告期限',
                '、其他补充事宜',"、公告公布媒介及公告期限"],
    "对本次招标提出询问": ['、对本次招标提出询问'],
    "对本次采购提出": ['、对本次采购提出'],
    "招标文件售价": ['、招标文件售价'],
    "开标时间及地点": ["、开标时间及地点","、开标时间",
                "、谈判时间、地点","、开标信息","、开标",
                "、谈判时间、地点",".开标时间及地点开标时间：",
                ".开标时间及地点","开标时间、地点"],
    "发布媒介": ["、发布媒介", ".发布公告的媒介","、发布公告的媒介","、公告发布媒介"],
    "公示时间": ["、公示时间"],
    "报名方式":["、报名方式"],
    "联系方式": ["、招标代理机构联系方式招标代理机构",
                "、联系方式联系人", 
                "、采购机构联系方式", ".招标人联系方式采购人", 
                "、联系事项",
                ".联系方式","．联系方式",
                 "、招标人及招标代理机构联系方式","联系方法："],
    "其他补充事宜": ["、其他补充事宜"],
    "项目最高限价": ["、项目最高限价"],
    "监督部门联系方式": ["、监督部门联系方式"],
    "纪检部门联系方式": ["、纪检部门联系方式"],
    "项目相关信息": ["、本采购项目相关信息"],
    "疑问": ["、凡对本次采购提出疑问"]
}

"""recognize needed info from short sentences"""
account_name = ['账户公司名称', '收款单位', '开户单位']
schema1 = account_name  # Define the schema for entity extraction
ie1 = Taskflow('information_extraction', schema=schema1, task_path=path1 + "data/model/information_extraction/uie-base")
schema2 = ['开户银行']
ie2 = Taskflow('information_extraction', schema=schema2, task_path=path1 + "data/model/information_extraction/uie-base")
schema3 = ['银行账号']
ie3 = Taskflow('information_extraction', schema=schema3, task_path=path1 + "data/model/information_extraction/uie-base")

account = ['银行账户：', '账户名称：', '账户名称:', '收款人全称：', '开户名：', '开户名称：', '收款单位：', '收款名称：',
           '单位名称：', '开户单位名称：', '开户单位：', '公司名称：', '户名：', '收款人：', '账户信息：', '单位名称:']
bank = ['开户行：', '开户银行：', '保证金交纳银行：', '开户银行名称：', '开户行名称：', '开户银行（']
bank_account = ['银行账号：', '账号：', '开户账号：']

# 报名条件映射值
bm_tiaojian = []
# 资质映射值
slcl = []

def hand_tbr_zgtj(tbr_zgtj:str)->list:
    """
    对投标人资格条件进行二次处理，主要 是 分行 处理 存入list中返回
    """
    result = list()
    return result
def clear_baoming_info(content: str) -> str:
    content = jionlp.remove_html_tag(content)
    pattern1 = r'\{[^{}]*?\}'
    pattern2 = r'\<[^<>]*?\>'
    content = re.compile(pattern2).sub('', content)
    content = re.compile(pattern1).sub('', content)
    content = content.replace("\xa02", "").replace("\xa01", "").replace("\xa0", "").replace(" ", "").replace(";","").replace(
        "\u3000", "").replace("&nbsp", "").replace("■", "").replace("★", "").replace("_", "").replace("\\t", "").split(
        "\\n")
    content = [item for item in content if item != '' or "notice" not in item or "font" not in item]
    return "".join(content)


def clear_paddle_IE(paddle_data) -> dict:
    """清洗paddlepaddle解析文件
    经多层嵌套的list 简单保留name:text
    """
    result = dict()
    for item in paddle_data[0]:
        result[item] = paddle_data[0].get(item)[0]["text"]
    return result


"""filter info"""
def filter_key(content):
    lst1 = []
    for ij in range(len(bank_account)):
        index1 = content.rfind(bank_account[ij])
        if index1 != -1:
            lst1.append(index1)
    for ik in range(len(bank)):
        index2 = content.rfind(bank[ik])
        if index2 != -1:
            lst1.append(index2)
    for il in range(len(account)):
        index3 = content.rfind(account[il])
        if index3 != -1:
            lst1.append(index3)
    return lst1


def get_info(content):
    res = {"bank_name": "", "account_name": "", "account_number": ""}

    if content != 0:

        result1 = clear_paddle_IE(ie1(content))
        result2 = clear_paddle_IE(ie2(content))
        result3 = clear_paddle_IE(ie3(content))

        result1.get('账户公司名称')
        result1.get('收款单位')
        result1.get('开户单位')
        result2.get('开户银行')
        result3.get('开户账号')

        res["bank_name"] = result2.get('开户银行')

        if result1.get('账户公司名称') is not None:
            res["account_name"] = result1.get('账户公司名称')
        elif result1.get('收款单位') is not None:
            res["account_name"] = result1.get('收款单位')
        elif result1.get('开户单位') is not None:
            res["account_name"] = result1.get('开户单位')
        else:
            res["account_name"] = ""

        res["account_number"] = result3.get('银行账号')

        if res["bank_name"] is None:
            res["bank_name"] = ""
        if res["account_name"] is None:
            res["account_name"] = ""
        if res["account_number"] is None:
            res["account_number"] = ""

    else:

        res["bank_name"] = ""
        res["account_name"] = ""
        res["account_number"] = ""

    return res


def handle_content(content):
    res = None
    try:
        ls = filter_key(content)
        if ls != []:
            cont = content[min(ls):]
        else:
            cont = 0
        res = get_info(cont)
    except Exception as e:
        print("Error: ", e)
        

    return res


def get_baoming_info_index_upg(content: str) -> dict:
    """
    升级版
    """
    result = {item: [] for item in KEYS_LIST_DICT}  # 构建返回值类型
    for item in KEYS_LIST_DICT:
        count = False
        for value in KEYS_LIST_DICT.get(item):
            index = content.find(value)
            if index != -1:
                result.get(item).append({"index": index})
                count = True
            if count:
                break

        if count is False:
            result.pop(item)
    result = dict(sorted(result.items(), key=lambda x: x[1][0]['index']))  # 排序
    keys_list = list(result.keys())
    for i in range(len(result)):
        try:
            seq = result.get(keys_list[i])[0].get("index")
            end = result.get(keys_list[i + 1])[0].get("index")
            content_index = content[seq:end - 2]
        except IndexError:
            content_index = content[seq:]
        result.get(keys_list[i]).append({keys_list[i]: content_index})
    return result



def get_format_time(time_string:str):
    """
    时间格式化
    2023年8月10日

    Args:
        time_string (str): result中获取的时间

    Returns:
        _type_: 标准 的 %Y-%m-%d 格式的时间
    """
    try:
        pattern = r"\d{2,4}[年-]\d{1,2}[月-]\d{1,2}|\d{1,2}[月-]\d{1,2}"
        # pattern = r"\d{1,2}[月-]\d{1,2}"
        if time_string:
            time_re = re.findall(pattern=pattern, string=time_string)[0]
            if time_re:
                time_re = time_re.replace("年", "-").replace("月", "-").replace("日", "")
                # 解决年分位数不问题 例如023 按照 当前 年份 的 前两位 进行填充
                year = time_re.split("-")[0] if len(time_re.split("-"))==3 else None
                if year and len(year) < 4:
                    YEAR =str(datatime_fat.datetime.now().year)
                    time_re = "-".join(["".join([YEAR[:2], year[-2:]]), "-".join(time_re.split("-")[-2:])])
                if year:
                    parsed_time = datatime_son.strptime(time_re, "%Y-%m-%d")
                    time_re = parsed_time.strftime("%Y-%m-%d")
                else:
                    parsed_time = datatime_son.strptime(time_re, "%m-%d")
                    time_re = parsed_time.strftime("%m-%d")
                return time_re
    except Exception as e:
        pass
    
    return ""

#todo get_format_time_min get_format_time_hour_min时间格式化暂未实现
def get_format_time_min(time_string:str):
    pass
def get_format_time_hour_min(time_string:str):
    if "秒" in time_string:
        second_index1 = time_string.find("秒")
        second_index2 = time_string.rfind("秒")
        if second_index1 == second_index2:
            time_str = time_string[:time_string.find("分")]
            time_str = time_str.replace("年","-").replace("月","-").replace("日"," ").replace("点",":").replace("分","").replace("时",":").replace("至","-").replace("到","-").replace("号"," ")
        else:
            time_str = time_string[:time_string.find("分")] + time_string[second_index1 + 1:time_string.rfind("分")]
            time_str = time_str.replace("年","-").replace("月","-").replace("日"," ").replace("点",":").replace("分","").replace("时",":").replace("至","-").replace("到","-").replace("号"," ")
    else:
        time_str = time_string.replace("年","-").replace("月","-").replace("日"," ").replace("点",":").replace("分","").replace("时",":").replace("至","-").replace("到","-").replace("号"," ")
    
    if time_str[-1] == ":":
        time_str = time_str[:-1]
    return time_str

def clear_paddle_IE(paddle_data) -> dict:
    """清洗paddlepaddle解析文件
    经多层嵌套的list 简单保留name:text
    """
    result = dict()
    for item in paddle_data[0]:
        result[item] = paddle_data[0].get(item)[0]["text"]
    return result


def get_exit_vocab(content: str, vocab_list: list) -> list:
    """
    实现vocab中的list一定程度的被模糊在content中查询
    呼叫.{0,8}?资质
    """
    if content is None or vocab_list is None:
        return []
    result = []
    for item in vocab_list:
        pattern = ".{0,20}"
        if len(item) > 6:
            # ****修改了匹配的前长度
            pattern = item[0:3] + pattern + item[-3:]
            if re.findall(pattern, content):
                result.append(item)
        elif len(item)>3:
            pattern = item[0] + pattern + item[-2:]
            if re.findall(pattern, content):
                result.append(item)
        else:
            # todo 小于3暂时没想好怎么匹配
            pass
    return result


def get_exit_app(content: str) -> list:
    "实现对报名方式的查找"
    result = []
    app_dict = {
        "注册报名": ["网上报名", "注册报名", "网上确认","供应商注册",
                     "线上招标", "不见面方式开标", "数字认证证书", 
                     "不见面网上开标", "下载招标文件", "微信获取",
                     "上传投标文件", "网上汇款成功截图", "在线下载", 
                     "注册及购买标书流程", "网络报名","线上获取","在线售卖",
                     "网上支付方式购买招标文件", "在线获取"],
        "邮件报名": ["邮件报名", "邮寄递交", 
                     "邮箱进行登记", "电子邮件",
                     "邮箱发送","邮箱获取"],
        "现场报名": ["现场报名", "现场提交", 
                     "现场提供", "现场获取", "线下集中购标", "现场领取", "携带法人授权书原件",
                     "携带身份证", "至某某公司", "现场购买","线下获取"],
        "邮寄报名": ["邮寄报名"] #TODO 需要 补充
    }
    no_list = '(不|无需|不需要|不可以|不接受)' # TODO 待补充
    pattern = ".{0,10}"
    for item in list(app_dict.keys()):
        pattern_result = ""
        item_c = app_dict.get(item)
        for item_d in item_c:
            # pattern_result =pattern_result +'(?<!不接受)'+ item_d[0:2] + pattern + item_d[-2:] + "|"
            pattern_result =pattern_result +item_d[0:2] + pattern + item_d[-2:] + "|"
        pattern_result = pattern_result.strip("|")
        pattern_result_no = no_list+'.{0,6}'+'('+pattern_result+')'
        if re.findall(pattern_result, content) and not re.findall(pattern_result_no, content):
            result.append(item)
    
    return result

zgtj_end = ['一、','二、','三、', '四、', '五、', '六、', '七、']
zgtj_end1 = ['1.', '2.', '3.', '4.', '5.','6.','7.']
zgtj = ['、资格条件','申请人的资格条件','、投标供应商资格要求','申请人的资格要求：',"合格的投标人","供应商的资格条件","投标供应商资格条件", '供应商资格条件', '候选供应商资格能力条件：','投标人资格条件','投标人资格要求','投标资格能力要求：','投标单位资格条件','投标单位资格要求：','申请人的资格要求','资格条件：']
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

def get_bidopen_bidInformation(context):
    """
    获取 开标时间 投标地点 是否 现场投标字段
	抽取字段： tb_start_time  tb_place tb_method   
	开始时间 暂不获取
	开标方式 先不判断 暂定判断逻辑 如果开标地点是 物理地点 则是现场透投标 

    Args:
        context: content_index.get("开标时间及地点")

    Returns:
        tb_start_time, tb_place, tb_method
    """
    # print("".join("".join(list(context[1].values())).split()))
    
    item = clear_paddle_IE(ie_2(list(context[1].values())))
    
    return item

def get_zgtj(curr_context):
    """_summary_
    zgtj字段获取
    #todo slcl
    Args:
        curr_context (_type_): content_index.get("申请人的资格要求")
    """
    result = "".join(list(curr_context[1].values()))[1:].replace(
                "Normal07.8磅02falsefalsefalseEN-USZH-CNX-NONE/*StyleDefinitions*/table.MsoNormalTable1", "").replace(
                "Normal07.8磅02falsefalsefalseEN-USZH-CNX-NONE/*StyleDefinitions*/table.MsoNormalTable", "").replace(
                "\t", "").replace("\n","")
    result = result.replace("Normal07.8磅02falsefalsefalseEN-USZH-CNX-NONE/*StyleDefinitions*/table.MsoNormalTable","")
    result = structurize_text(text=result)
    if result != dict():
        result=list(result.values())[0]
    return result
def get_vocab(path:str):
    """ 获取txt文件中的vocab
        vocab按照行进行分开

    Args:
        path (str): 文件路径

    Returns:
        _type_: vocab list
    """
    with open(path, "r", encoding="utf-8") as f:
        vocab_list = f.readlines()
    vocab_list = [item.replace("\n", "").split(" ")[0] for item in vocab_list]
    while '' in vocab_list:
        vocab_list.remove('')
    return vocab_list
    
def get_baoming(curr_context):
    """获取标签
    bm_kaishi 报名开始时间
    bm_jieshu 报名结束时间
    am_begin_time 上午开始时间
    am_end_time   上午结束时间
    pm_begin_time 下午开始时间
    pm_end_time   下午结束时间
    bid_file_place 招标文件申领地点
    bm_fangshi  报名方式 
    bm_tiaojian 报名材料 #还是使用原来全局搜索的方式进行抽取
    bm_flow 报名流程 #todo
    招标文件售价 pass
    八个实体UIE应该OK（不包含报名材料）
    Args:
        curr_context (_type_): content_index.get("获取招标文件") 
    """
    result = clear_paddle_IE( ie_3( list( curr_context[1].values() ) ) )
    return result
fangshi = ["领取招标文件","申领程序","申领方式","报名方式","报名流程","标书流程","招标文件获取","领取流程","发售方式","方式：","方式或事项"]

def get_bm_flow(context, check):
    """
    利用re获取报名流程
    获取报名流程
    Args:
        context (str): _description_
    Returns:
        _type_: _description_
    """
    if check is True:
        index = []
        for element in fangshi:
            if context.rfind(element) == -1:
                continue
            index.append(context.rfind(element)+len(element))
            
        if index != []:
            return context[min(index):]
        else:
            return context
    else:
        pattern = r"(申领方式|报名方式|报名流程|报名方式|发售方式).{2,300}.((?=[一|二|三|四|五|六])|。)"
        result = re.search(pattern=pattern, string=context)
        if result:
            return result.group()[:-1]
        else:
            return ""

def get_baoming_info(content: str):
    """
    content:文本内容
    """
    # 定义返回值形状
    result = {
        "bm_tiaojian": [], # 报名条件
        "slcl": [], # 审核条件
        "bm_fangshi": "", # 报名方式
        "start_date": "", # 获取招标文件开始时间
        "bm_kaishi": "", # 报名开始时间
        "bm_jieshu": "", # 获取招标文件结束时间
        "bid_file_place": "", # 获取 招标文件 地点
        "bid_open_time": "", # 开标 时间
        "tbr_zgtj": "",  # 申请人 资格 条件
        "tb_place": "",  # 开标 地点
        "tb_start_time":"", # 投标 开始 时间
        "tb_method":"", # 投标方式 现场/网上 
        
        "am_begin_time" :"", #上午开始时间
        "am_end_time" :"",#上午结束时间
        "pm_begin_time" :"", #下午开始时间
        "pm_end_time": "",   #下午结束时间
        "bm_flow": "", # 报名流程
        "bank_name" :"",
        "account_name" : "",
        "account_number" : ""
    }
    
    content = clear_baoming_info(content)
    # result["bm_flow"]=get_bm_flow(context=content)
    if len(content) < 10:
        print("content内容太短")
        return result
    try:
        res1 = handle_content(content)
        result["bank_name"] = res1["bank_name"]
        result["account_name"] = res1["account_name"]
        result["account_number"] = res1["account_number"]
    except Exception as e:
        print(e)
    content_index = get_baoming_info_index_upg(content)
    cer_vocab_list = get_vocab(path=path1 + "data/0517_credentials_vocab.txt")
    # 存在的报名材料字段 
    reg_vocab_list = get_vocab(path=path1 + "data/0518_reg_condition.txt")
    # 申请人资格要求字段填写
    reg_exit_remove=None
    if content_index.get("申请人的资格要求") is not None:
        result["tbr_zgtj"]=get_zgtj(curr_context=content_index.get("申请人的资格要求"))
        # reg_exit_remove = get_exit_vocab(content=content, vocab_list=reg_vocab_list)
        # reg_exit_remove = unify_vocab(reg_exit_remove, reg_condition_keys_path)
    curr_result = None # 记录当前的返回值
    exit_app=None
    if content_index.get("获取招标文件") is not None:
        curr_result = get_baoming(content_index.get("获取招标文件"))
        exit_app = get_exit_app(list(content_index.get("获取招标文件")[1].values())[0]) # 关键字抽取 报名方式
    if content_index.get("获取招标文件") is None and content_index.get("公示时间") is not None:
        curr_result = get_baoming(content_index.get("公示时间"))
        exit_app = get_exit_app(list(content_index.get("公示时间")[1].values())[0]) # 关键字抽取 报名方式
    if curr_result is None and content_index.get("项目基本情况") is not None:
        curr_result = get_baoming(content_index.get("项目基本情况"))
    # 字段赋值
    #todo 报名方式 需要进行相似度映射 时间 需要 处理 成 指定格式
    if curr_result is not None:
        result.update(curr_result)
    
    curr_result = dict()
    if content_index.get("开标时间及地点") is not None:
        try:
            curr_result.update(get_bidopen_bidInformation(content_index.get("开标时间及地点")))
        except Exception as e:
            print(e)
        
    # if content_index.get("提交投标文件") is not None and content_index.get("开标时间及地点") is None:
    if content_index.get("提交投标文件")is not None:
        try:
            curr_result.update(get_bidopen_bidInformation(content_index.get("提交投标文件")))
        except Exception as e:
            print(e)
    if curr_result:
        result.update(curr_result)
   
        
    
    

    cer_exit = get_exit_vocab(content=content, vocab_list=cer_vocab_list)
    cer_exit =unify_vocab(cer_exit, credentials_condition_keys_path)
    if content_index.get("申请人的资格要求") is not None:
        reg_exit = get_exit_vocab(content=content.replace(list(content_index.get("申请人的资格要求")[1].values())[0],""), vocab_list=reg_vocab_list)
    else:
        reg_exit = get_exit_vocab(content=content, vocab_list=reg_vocab_list)

    reg_exit = unify_vocab(reg_exit, reg_condition_keys_path)
    
    
    # 报名开始时间 与报名结束时间进行 格式进行 优化
    if result["bm_kaishi"]:
        result["bm_kaishi"] = get_format_time(result["bm_kaishi"])
    if result["bm_jieshu"]:
        result["bm_jieshu"] = get_format_time(result["bm_jieshu"])
     # 获取tbmethod
    if result["tb_method"]:
        result["tb_method"]=tb_method_determineBybid_file_place_or_tb_method(result["tb_method"])
    elif result["tb_place"]:
        # result["tb_method"] = tb_method_determineBybid_file_place_or_tb_method(result["tb_place"])
        # result["tb_method"] = answer(clueAI_input_change(result["tb_place"])) 
        result["tb_method"] = tb_method_determin(result["tb_place"])

    


    result["bm_tiaojian"] = cer_exit
    result["slcl"] = reg_exit
    for key in result:
        if key == 'tbr_zgtj':
            continue
        if isinstance(result[key], str):
            result[key] = result[key].replace('\'', '').replace('\\', '')
        else:
            for value in result[key]:
                value = value.replace('\'', '').replace('\\', '')
    if result["bm_kaishi"]:
        result["start_date"] = result["bm_kaishi"]
    if result["bid_open_time"] ==''and result["tb_start_time"]:
        result["bid_open_time"]=result["tb_start_time"]

    if result["bid_file_place"]==""and result["tb_place"]:
        result["bid_file_place"] = result["tb_place"]
    if content_index.get("获取招标文件") is not None:
        flow_cont = content_index.get("获取招标文件")
        flow_content = "".join(list(flow_cont[1].values())).replace("星期六","")
        if flow_content.find("售价：") != -1:
            flow_content = flow_content[:flow_content.find("售价：")]
        flow_start = content.find(flow_content) - 1
        flow_start_number = content[flow_start:flow_start+2]
        lst = []
        lst = filter_end(flow_content, flow_start_number)
        if lst != []:
            flow_content = flow_content[:min(lst)]
        result["bm_flow"]=get_bm_flow(context=flow_content, check=True)[0:511]
    else:
        result["bm_flow"]=get_bm_flow(context=content, check=False)[0:511]
    if result["tb_start_time"] == "" and result["bm_jieshu"]:
        result["tb_start_time"] = result["bm_jieshu"]
        
        
    if exit_app:
        if "邮件报名" in exit_app and "注册报名" in exit_app:
            exit_app.remove("注册报名")
        result["bm_fangshi"] = ",".join(exit_app)
    elif result["bid_file_place"]:
        result["bm_fangshi"]=tb_method_determin(result["bid_file_place"])
        if result["bm_fangshi"]=="现场投标":
            result["bm_fangshi"]="现场报名"
        else:
            result ["bm_fangshi"] = "注册报名"
    else:
        result["bm_fangshi"]="其他"
    # 邮件报名
    topic = ["邮件主题：", "供应商的邮件标题为："]
    if "邮件报名" in result["bm_fangshi"]:
        flow_content = result["bm_flow"]
        try:
            # 邮件主题
            mail_topic_index = min([flow_content.find(item) + len(item) for item in topic if flow_content.find(item) != -1])
            if mail_topic_index == -1:
                result["bm_flow"] = flow_content
            else: 
                mail_topic = "邮件主题：" + flow_content[mail_topic_index:mail_topic_index+min(flow_content[mail_topic_index:].find("；")+1 if flow_content[mail_topic_index:].find("；")+1 != 0 else 99999999, flow_content[mail_topic_index:].find("。")+1 if flow_content[mail_topic_index:].find("。")+1 != 0 else 99999999 )].replace("。","；")
                # 邮件内容
                mail_content_index = flow_content.find("邮件内容") + len("邮件内容")
                if mail_content_index == -1: 
                    mail_content = "邮件内容： ；"
                else: 
                    mail_content = "邮件内容：" + flow_content[mail_content_index:mail_content_index+min(flow_content[mail_content_index:].find("；")+1 if flow_content[mail_content_index:].find("；")+1 != 0 else 99999999, flow_content[mail_content_index:].find("。")+1 if flow_content[mail_content_index:].find("。")+1 != 0 else 99999999 )].replace("。","；").replace("：","")
                
                # 邮件附件
                mail_attach = "邮件附件：报名材料"
                
                # 邮箱
                mail_re = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
                if re.findall(mail_re, flow_content) != []:
                    mail_address = "邮箱：" + re.findall(mail_re, flow_content)[0] + "；"
                    result["bm_flow"] = mail_address + mail_topic + mail_content + mail_attach
                else: 
                    result["bm_flow"] = flow_content
        except Exception as e:
            result["bm_flow"] = flow_content

    if "现场报名" == result["bm_fangshi"]:
        result["bm_flow"] = ""
        
    for item in result.keys():
        if "time" in item:
            result[item]=get_format_time_hour_min(result[item])if result[item] else ""
    result['bid_open_time'] = result['bid_open_time'][:22]
    if result["bm_flow"]:
        result["bm_flow"]=" ".join(result["bm_flow"].split())
    return result


if __name__ == "__main__":
    # result = get_baoming_info_index_upg()    
    pass
