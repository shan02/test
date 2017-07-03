#!/usr/bin/env python
# -*- coding:utf-8 -*-
#制作:温赫男

'''传输数据模块
'''

import publog
import model
from define import *
from Interface.amazom_interface import AmazonFinancial
import xmltodict
from xml.dom.minidom import parseString
from util.xml_util import get_element_by_tag
import get_info_save

def Get_GroupIDList(storename):
    '''
    获得groupid
    :param storename: 
    :return: 
    '''
    from_date = model.CSaveData.c_StartTime
    to_date = model.CSaveData.c_EndTime
    storeinfo = model.GetStoreInfo(storename)


    group_xml_file = XML_RESULT_PATH + storename + '.xml'

    # with open(group_xml_file, 'r') as groupxml:
    #      model.CSaveData.SetGroupIDList(storename, groupxml.read())
    # return

    amaz = AmazonFinancial(storeinfo.GetData())
    groupObj = amaz.list_finace_eventgroup(from_date, to_date)
    if groupObj["result"]:
        group_xml_file = XML_RESULT_PATH +storename + '.xml'
        with open(group_xml_file, 'w') as groupxml:
            groupxml.write(str(groupObj['group_xml']))
            model.CSaveData.SetGroupIDList(storename, groupObj['group_xml'])

    else:
        publog.exception("获取groupid失败",groupObj["message"],exc_info=1)



def Get_StoreXml(storename,groupid):
    '''
    
    :param storename: 
    :param groupid: 
    :return: 
    '''

    import os
    storeinfo = model.GetStoreInfo(storename)
    amaz = AmazonFinancial(storeinfo.GetData())

    xls = amaz.list_finace_event(groupid)
    path = os.path.join(XML_RESULT_PATH , storename )
    if not os.path.exists(path):
        os.mkdir(path)
    filename = os.path.join(path, storename + ': ' + groupid + '.xml')
    publog.info("尝试下载",filename,xls["result"])

    if xls["result"]:
        with open(filename, 'w') as groupxml:
            groupxml.write(str(xls['finance_event_group_obj']))


    else:
        publog.exception("获取详细数据失败",xls["message"],storename,groupid,exc_info=1)
        return False

    nextToken = xls.get('NextToken')
    if nextToken:
        return Get_StoreXmlNext(storename,groupid,nextToken)
    return True

def Get_StoreXmlNext(storename, groupid, nextToken):
    '''

    :param storename: 
    :param groupid: 
    :return: 
    '''

    import os
    storeinfo = model.GetStoreInfo(storename)
    amaz = AmazonFinancial(storeinfo.GetData())

    xls = amaz.list_finace_event_by_nextToken(nextToken)
    path = os.path.join(XML_RESULT_PATH, storename)
    #if os.path.exists(path):
    #        os.rmdir(path)
    if not os.path.exists(path):
        os.mkdir(path)

    index = 1
    while True:
        filename = os.path.join(path, storename + ': ' + groupid+"_%d"%index + '.xml')
        if not os.path.exists(filename):
            break
        index+=1
    publog.info("尝试下载", filename,nextToken)

    if xls["result"]:
        response  = str(xls['finance_event_group_obj'])
        group = xmltodict.parse(xls['finance_event_group_obj'], encoding='utf-8')
        if group.get("ErrorResponse"):
            publog.info("错误记录,",group["ErrorResponse"])
            return False

        with open(filename, 'w') as groupxml:
            groupxml.write(response)

        dom = parseString(response)
        try:
            nextToken = get_element_by_tag(dom, "NextToken")
            if nextToken:
                return Get_StoreXmlNext(storename, groupid, nextToken)
        except Exception as e:
            publog.info("没有NextToken需要解析",exc_info=1)
            return False
    else:

        publog.exception("获取NextToken详细数据失败", xls["message"], storename, groupid, exc_info=1)
        return False
    return True

def ClearCsvData(storename):
    with open(OUTPUT_PATH + storename + '.csv', 'w') as csvfile:
        data = []
        for key in TITLE:
            data.append(key)

        csvfile.write('\t'.join(data)+"\n")

def GetXmlData(storename):
    import os

    rootpath =os.path.join(XML_RESULT_PATH +storename)

    _allct = 0
    _rightct = 0

    for group_xmls in os.listdir(rootpath):
        xmlfile = os.path.join(rootpath , group_xmls)

        xmldata = ""
        if os.path.isdir(xmlfile):
            continue
        print xmlfile,222222222
        with open(xmlfile, 'r') as f:
            xmldata = f.read()


        with open(OUTPUT_PATH + storename + '.csv', 'a') as csvfile:
            group = xmltodict.parse(xmldata, encoding='utf-8')
            account_id = model.GetAccountID(storename)

            try:
                eventGroupList = group['ListFinancialEventGroupsResponse'][
                    'ListFinancialEventGroupsResult']['FinancialEventGroupList']['FinancialEventGroup']
                trans_list = []
                try:
                    for eventGroup in eventGroupList:
                        trans_fee = eventGroup['OriginalTotal']['CurrencyAmount']
                        trans_time = eventGroup['FinancialEventGroupStart']
                        trans_time = str(trans_time).replace(
                            'T', ' ').replace('Z', '')
                        info_list = [trans_time, '', 'Transfer', account_id, '', '', '', '', '',
                                     'Amazon', '', '', '', '', '', '', '', '', '', trans_fee, trans_fee]
                        trans_list.append(info_list)
                        # trans_list.append('\n')
                except Exception as e:
                    trans_fee = eventGroupList['OriginalTotal']['CurrencyAmount']
                    trans_time = eventGroupList['FinancialEventGroupStart']
                    trans_time = str(trans_time).replace(
                        'T', ' ').replace('Z', '')
                    info_list = [trans_time, '', 'Transfer', account_id, '', '', '', '', '',
                                 'Amazon', '', '', '', '', '', '', '', '', '', trans_fee, trans_fee]
                    trans_list.append(info_list)



                for sub_list in trans_list:
                    sub_list[0] = sub_list[0].replace(" ",":")
                    csvfile.write('\t'.join(str(s) for s in sub_list if isinstance(sub_list, list)) )

                flag = True
                _rightct+=1
            except:
                flag = False
            publog.debug("处理文件", xmlfile,flag)
            _allct +=1

    publog.info("处理基本信息", storename,"完成%d/%d"%(_rightct,_allct) )

def _GetUSTime(txt):
    import time, datetime
    newtime = datetime.datetime.strptime(txt, '%Y-%m-%dT%H:%M:%S')
    return newtime - datetime.timedelta(hours=7)

def CsvSetDateTime(storename):
    import time,datetime
    from django.utils import timezone
    #storename = "APPLUS"
    print "处理",storename
    with open(OUTPUT_PATH + storename + '.csv', 'r') as csvfile:
        allinfotxt = csvfile.read()
    #allinfo =
    #from_date = model.CSaveData.c_StartTime
    from_date = "2017-05-30T00:00:00"
    from_date = datetime.datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')
    to_date = "2017-06-02T00:00:00"
    to_date = datetime.datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')
    #print from_date,type(from_date)
    #sdf

    alllines = allinfotxt.splitlines()

    alldata = [alllines.pop(0)]
    for line in alllines:
        info = line.split()

        try:
            subtime = info[0]
            #subtime = "2017-05-01T12:40:52"
            ustime = _GetUSTime(subtime)
        except:
            continue
        if (ustime-from_date).days <0:
             continue
        if (ustime - to_date).days >= 0:
             continue
        info[0] = ustime.strftime("%b %d %Y %I:%M:%S %p %Z")
        alldata.append("\t".join(info))
        #print ustime,(ustime - to_date).days,(ustime - to_date).days > 0

        #
        # if (to_date - ustime).days > 0:
        #     continue

        #May 1, 2017 5:40:52 AM PDT

        #print curtime,curtime - datetime.timedelta(hours=7)
        #print ustime.strftime("%b %d, %Y %I:%M:%S %p %Z")
    #sadf
    with open(OUTPUT_PATH +"new" + storename + '.csv', 'w') as csvfile:
        csvfile.write("\n".join(alldata))

# def Csv2Xls():
#     import csv
#     import xlwt
#     #新建excel文件
#     myexcel = xlwt.Workbook()
#     #新建sheet页
#     mysheet = myexcel.add_sheet("testsheet")
#     #打开csv文件，事实证明file和open 效果一样的，网上建议用open打开
#     csvfile = file("test.csv","rb")
#     #csvfile = open("test.csv","rb")
#
#     #读取文件信息
#     reader = csv.reader(csvfile)
#     l = 0
#     #通过循环获取单行信息
#     for line in reader:
#         r = 0
#         #通过双重循环获取单个单元信息
#         for i in line:
#             print l,r
#             #通过双重循环写入excel表格
#             mysheet.write(l,r,i)
#             r=r+1
#         l=l+1
#     #最后保存到excel
#     myexcel.save("myexcel.xls")

def Xml2Csv(storename):
    import os
    _rightct, _allct = 0,0
    rootpath =os.path.join(XML_RESULT_PATH +storename)
    allinfo = []
    for group_xmls in os.listdir(rootpath):

        xmlfile = os.path.join(rootpath , group_xmls)

        xmldata = ""
        if os.path.isdir(xmlfile):
            continue
        with open(xmlfile, 'r') as f:
            xmldata = f.read()

            group = xmltodict.parse(xmldata, encoding='utf-8')
            account_id = model.GetAccountID(storename)
            fee_group_data = xmltodict.parse(xmldata, encoding='utf-8')
            try:
                info = get_info_save.get_data_to_save_db(fee_group_data, account_id)
                _rightct += 1
            except Exception, e:
                info = []
                publog.debug("get_info_save.get_data_to_save_db----wrong",exc_info=1)


            for fee_dict in info:
                fee_dict['datetime'] = fee_dict['datetime'].replace(" ","T")


                info = []
                for key in TITLE:
                    info.append(str(fee_dict[key]))

                allinfo.append(info)
        _allct += 1
        publog.debug("处理文件", xmlfile)

    with open(OUTPUT_PATH + storename + '.csv', 'a') as csvfile:
        alldata = []
        def _my_cmp(ls1, ls2):
            return cmp(ls1[0], ls2[0])

        allinfo.sort(_my_cmp)
        for info in allinfo:
            if info[0]< model.CSaveData.c_StartTime:
                continue
            newinfo = '\t'.join(info)

            if newinfo in alldata:
                continue
            alldata.append(newinfo)
        #print "\n".join(alldata),2222222
        csvfile.write("\n".join(alldata))


    publog.info("处理详细信息", storename, "完成%d/%d" % (_rightct, _allct))
