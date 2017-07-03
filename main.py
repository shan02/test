#!/usr/bin/env python
# -*- coding:utf-8 -*-
#制作:温赫男

'''
'''


import os
import logging
def initenv():
    import sys
    sys.path.append("config")
    import define
    if not os.path.exists(define.RESULT_PATH):
        os.mkdir(define.RESULT_PATH)

    if not os.path.exists(define.XML_RESULT_PATH):
        os.mkdir(define.XML_RESULT_PATH)
    if not os.path.exists(define.OUTPUT_PATH):
        os.mkdir(define.OUTPUT_PATH)


    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)
initenv()
import publog
import model
import trans
import json
import define
def Haha():
    try:
        1/0
    except Exception as e:
        print e
        logging.exception("sdf",exc_info=1)
        #import  traceback
        #traceback.print_exc()

def ColorPrint(*args):
    print '\033[1;31;40m'
    print ",".join([str(i) for i in args])
    print '\033[0m'

def main():
    model.InitData()
    # model.CSaveData.Restart()
    # model.CSaveData.c_StartTime = "2017-05-11T00:00:00"
    # model.CSaveData.c_EndTime = "2017-05-20T00:00:00"
    # trans.Get_GroupIDList("A3")
    # model.CSaveData.DoSave()
    # return

    if not model.CSaveData.ReadSaveData():
        publog.error("需要初始化数据,请配置文件",define.CONFIG_FILE)
        #model.CSaveData.Restart()
        return
    #model.CSaveData.DoSave()
    #while True:6
    #print model.CSaveData.c_SaveList
    #print model.CSaveData.GetGroupInfoList()
    #sdf
        #= model.CSaveData.GetGroupInfoList()
    if 0:
        for storename in model.CSaveData.c_StoreList:
            #storename = model.CSaveData.GetCurStoreName()
            # if storename!="A3":
            #     break

            #if storename==None:
            #    break


            trans.Get_GroupIDList(storename)
            # print "测试",storename
            # model.CSaveData.c_Cur_Store_Index += 1
            # continue
            model.CSaveData.DoSave()

            ColorPrint("获得店铺<%s>的groupid" % storename)
    allct = 0
    while True:
        groupinfolist = model.CSaveData.GetGroupInfoList()
        if not groupinfolist:
            break
        ct = 0
        all = len(groupinfolist)
        for storename,groupid in groupinfolist:
            if trans.Get_StoreXml(storename,groupid):
                model.CSaveData.SaveGroupInfo(storename,groupid)
                ColorPrint("下载报表成功", storename, groupid,"完成%s/%s"%( ct, all))
                ct+=1
            model.CSaveData.DoSave()
        allct +=1
        ColorPrint("完成遍历<%s>"%allct,"完成%s/%s"%( ct, all))

    #处理下一家店
    # model.CSaveData.c_Cur_Store_Index += 1
    # model.CSaveData.DoSave()


if __name__ == "__main__":
    main()