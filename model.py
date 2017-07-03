#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 制作:温赫男

'''数据对象
'''

from define import *
import define
import json
import publog

g_StoreInfo = {}  # 所有店铺信息


def GetStoreInfo(store_name):
    if 0:
        return CStoreInfo()
    return g_StoreInfo.get(store_name)


def GetAccountID(store_name):
    storeinfo = GetStoreInfo(store_name)
    return storeinfo.m_Account_ID


def InitStore():
    global g_StoreInfo
    with open(AMAZON_STORENAME_FILE) as amazac:
        amazac_list = amazac.readlines()
        for amastr in amazac_list:
            amastr = amastr.replace('"', '').replace('\n', '')
            if amastr=="":
                continue
            a = amastr.split(',')

            storeinfo = CStoreInfo(*a[1:])
            g_StoreInfo[storeinfo.m_StoreName] = storeinfo


class CStoreInfo(object):
    def __init__(self, storename, access_key, secret_key, account_id, mkplace_id, MWSAuthToken):
        self.m_StoreName = storename
        self.m_Access_Key = access_key
        self.m_Secret_Key = secret_key
        self.m_Account_ID = account_id
        self.m_Mkplace_ID = mkplace_id
        self.m_MWSAuthToken = MWSAuthToken

    def __str__(self):
        return "商铺<%s>" % self.m_StoreName

    def GetData(self):
        return {
            "access_key": self.m_Access_Key,
            "secret_key": self.m_Secret_Key,
            "account_id": self.m_Account_ID,
            "mkplace_id": self.m_Mkplace_ID,
            "MWSAuthToken": self.m_MWSAuthToken,
        }


def InitData():
    '''
    初始化数据 
    '''
    InitStore()


class CSaveData():
    c_StartTime = "2017-2-13"
    c_EndTime = "2017-2-28"
    #c_Cur_Store_Index = 0
    #c_Cur_GroupID_Index = 0
    c_SaveList = []
    c_StoreList = []  # 店铺列表
    c_GroupID_List = {}  # 分组编号信息

    @classmethod
    def GetStoreList(cls):
        return cls.c_StoreList

    @classmethod
    def DoSave(cls):
        data = {}
        data["starttime"] = cls.c_StartTime
        data["endtime"] = cls.c_EndTime
        #data["curstoreindex"] = cls.c_Cur_Store_Index
        #data["curgroupid"] = cls.c_Cur_GroupID_Index
        data["grouplist"] = cls.c_GroupID_List
        data["storelist"] = cls.c_StoreList
        data["savelist"] = cls.c_SaveList

        datastr = json.dumps(data,indent=1)

        with open(CONFIG_FILE, "w") as f:
            f.write(datastr)
        return  datastr

    @classmethod
    def SaveGroupInfo(cls,storename, groupid):
        key = (storename,groupid)
        if not key in cls.c_SaveList:
            cls.c_SaveList.append(key)

    @classmethod
    def GetGroupInfoList(cls):
        info = []
        for storename in cls.c_StoreList:
            for groupid in cls.c_GroupID_List[storename]:
                key = (storename, groupid)

                if key not in cls.c_SaveList:
                    info.append(key)
        return info

    @classmethod
    def Restart(cls):
        from datetime import datetime, timedelta
        import pytz, time
        day = 14
        now_time = datetime.now(pytz.UTC) - timedelta(days=day, hours=datetime.now(pytz.UTC).hour,
                                                      minutes=datetime.now(pytz.UTC).minute,
                                                      seconds=datetime.now(pytz.UTC).second)
        from_date = now_time.strftime('%FT%T')

        # @todo
        to_date = (now_time + timedelta(days=day)).strftime('%FT%T')
        print datetime.strptime("2012-5-12", "%Y-%m-%d").strftime('%FT%T')
        # .strftime("%Y-%m-%d")

        cls.c_StartTime = from_date
        cls.c_EndTime = to_date
        #cls.c_Cur_Store_Index = 0
        #cls.c_Cur_GroupID_Index = 0
        cls.c_GroupID_List = {}
        cls.c_StoreList = [
            "A3",
        ]
        cls.DoSave()

    @classmethod
    def SetGroupIDList(cls, storename, xmlinfo):
        from xml.dom import minidom
        doc = minidom.parseString(xmlinfo)
        root = doc.documentElement
        nodes = root.getElementsByTagName("FinancialEventGroupId")

        data = []
        cls.c_Cur_GroupID_Index = 0
        data = []

        for node in nodes:
            groupid = node.childNodes[0].data
            data.append(groupid)

        cls.c_GroupID_List[storename] = data

    @classmethod
    def ReadSaveData(cls):
        with open(CONFIG_FILE, "r") as f:
            try:
                datastr = f.read()
                data = json.loads(datastr)
            except Exception as e:
                publog.exception("配置文件解析错误", e, exc_info=1)
                return False
        data = json.loads(datastr)
        cls.c_StartTime = data["starttime"]
        cls.c_EndTime = data["endtime"]
        #cls.c_Cur_Store_Index = data["curstoreindex"]
        #cls.c_Cur_GroupID_Index = data["curgroupid"]
        cls.c_GroupID_List = data["grouplist"]
        savelist = data.get("savelist",[])

        cls.c_SaveList = []
        for saveinfo in savelist:
            cls.c_SaveList.append(tuple(saveinfo))

        cls.c_StoreList = []
        for storename in data["storelist"]:
            if storename in g_StoreInfo:
                cls.c_StoreList.append(storename)
            else:
                publog.info("发现异常帐号<%s>" % storename)
                #return False
        return True

    # @classmethod
    # def GetCurStoreName(cls):
    #     try:
    #         return cls.c_StoreList[cls.c_Cur_Store_Index]
    #     except:
    #         return None
    #
    # @classmethod
    # def GetCurGroupID(cls):
    #     storename = cls.GetCurStoreName()
    #     if storename:
    #         lst = cls.c_GroupID_List.get(storename)
    #         try:
    #             return lst[cls.c_Cur_GroupID_Index]
    #         except:
    #             return None
