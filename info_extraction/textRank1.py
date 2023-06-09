from textrank4zh import TextRank4Keyword, TextRank4Sentence

def textR():
    text = "项目概况国家税务总局辽宁省税务局机房精密空调设备维保服务项目招标项目的潜在投标人应在乔泰工程管理集团有限公司（沈阳市浑南区高歌路5号）。获取招标文件，并于2023年06月05日14点00分（北京时间）前递交投标文件。一、项目基本情况项目编号：2022CG009/LNQT2022100801项目名称：国家税务总局辽宁省税务局机房精密空调设备维保服务项目预算金额：11.7800000万元（人民币）最高限价（如有）：1.4725000万元（人民币）采购需求：本项目为国家税务总局辽宁省税务局采购8台机房专用空调设备技术支持与维保服务项目。合同履行期限：服务期限自签订合同之日起36个月，每12个月为一个服务年度，共3个服务年度，每个服务年度签一次服务合同，视上年度合同执行情况，决定是否续签合同。本项目(不接受)联合体投标。二、申请人的资格要求：1.满足《中华人民共和国政府采购法》第二十二条规定；2.落实政府采购政策需满足的资格要求：本项目为专门面向中小企业采购的项目,供应商应为中小微企业、监狱企业、残疾人福利性单位。3.本项目的特定资格要求：（1）未被“信用中国”网站（www.creditchina.gov.cn）、中国政府采购网（http://www.ccgp.gov.cn/cr/list）列入失信被执行人、重大税收违法案件当事人名单、政府采购严重违法失信行为记录名单。三、获取招标文件时间：2023年05月15日至023年05月22日，每天上午8:30至11:30，下午12:30至16:00。（北京时间，法定节假日除外）地点：乔泰工程管理集团有限公司（沈阳市浑南区高歌路5号）。方式：现场领取/电子邮件方式，符合报名资格条件的供应商须将如下资料加盖公章扫描（PDF或JPG格式）发送至电子邮箱lnqt2018@163.com（发送资料后，请供应商及时联系代理机构）：(1)法人或者其他组织的营业执照等主体证明文件或自然人的身份证明复印件（自然人身份证明仅限在自然人作为招标主体时使用）；(2)法定代表人（或非法人组织负责人）身份证明书（自然人作为响应主体时不需提供）；(3)授权委托书复印件（法定代表人、非法人组织负责人、自然人本人领取招标文件的无需提供）；注：电子邮件名称应注明:“XX项目报名资料（报名单位+联系人+电话）”。售价：500元（售后不退）。售价：￥500.0元，本公告包含的招标文件售价总和四、提交投标文件截止时间、开标时间和地点提交投标文件截止时间：2023年06月05日14点00分（北京时间）开标时间：2023年06月05日14点00分（北京时间）地点：乔泰工程管理集团有限公司会议室（沈阳市浑南区高歌路5号）。五、公告期限自本公告发布之日起5个工作日。六、其他补充事宜1、项目基本情况预算金额：11.78万元/年（本价格为估算价格，具体以单价结算）单价最高限价：14725.00元/台2、申请人的资格要求本项目由符合国家有关法律规定、同时满足本项目资格要求、在中国境内（指关境内）注册的，具有履行项目服务能力的供应商作为投标人。3、开户行：招商银行沈阳华园东路支行账户名称：乔泰工程管理集团有限公司账号：124908422310855884、请各投标人随时关注政府部门疫情防控规定和要求，为加强个人防护工作，请到现场的投标人代表自行戴好口罩，配合现场工作人员登记问询工作。七、对本次招标提出询问，请按以下方式联系。1.采购人信息名称：国家税务总局辽宁省税务局地址：沈阳市沈河区青年大街256号联系方式：常老师024-231853172.采购代理机构信息名称：乔泰工程管理集团有限公司地址：沈阳市浑南区高歌路5号联系方式：刘桂君、朱頫来、郑陈旭024-23883380-8003、80043.项目联系方式项目联系人：刘桂君、朱頫来、郑陈旭电话：024-23883380-8003、8004"
    tr4w = TextRank4Keyword()

    tr4w.analyze(text=text, lower=True, window=2, vertex_source="all_filters")

    print( '关键词：' )
    for item in tr4w.get_keywords(20, word_min_len=2):
        print(item.word, item.weight)

    print()
    print( '关键短语：' )
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
        print(phrase)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')

    print()
    print( '摘要：' )
    for item in tr4s.get_key_sentences(num=8):
        print(item.index, item.weight, item.sentence)  # index是语句在文本中位置，weight是权重
    
    