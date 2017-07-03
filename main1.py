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
import define
import publog
import model
import trans
import get_info_save


def main():
    model.InitData()


    if not model.CSaveData.ReadSaveData():
        publog.error("需要初始化数据,请配置文件",define.CONFIG_FILE)
        #model.CSaveData.Restart()
        return
    #for storename in model.CSaveData.c_StoreList:
    # while True:
    #     storename = model.CSaveData.GetCurStoreName()
    #     if storename==None:
    #         break
    #
    #
    #     trans.Get_GroupIDList(storename)
    #     model.CSaveData.DoSave()
    #
    #     publog.info("获得店铺<%s>的groupid" % storename)
    #
    #     while True:
    #         groupid = model.CSaveData.GetCurGroupID()
    #         if groupid==None:
    #             break
    #         publog.info("下载报表成功" , storename,groupid)
    #         trans.Get_StoreXml(storename,groupid)
    #         model.CSaveData.c_Cur_GroupID_Index += 1
    #         model.CSaveData.DoSave()
    #     #处理下一家店
    #     model.CSaveData.c_Cur_Store_Index += 1
    #     model.CSaveData.DoSave()


    for storename in model.CSaveData.c_StoreList:
    #for storename in ["A3",]:
        trans.ClearCsvData(storename)
        trans.GetXmlData(storename)
        trans.Xml2Csv(storename)

if __name__ == "__main__":
    main()