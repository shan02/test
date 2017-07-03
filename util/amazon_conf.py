#!/usr/bin/env python
# -*- coding:utf-8 -*-
# STORE_ACCOUNT = {'access_key': '',
#                  'secret_key': '/',
#                  'account_id': '',
#                  'mkplace_id': '',
#                  'MWSAuthToken': ''}
# STORE_ACCOUNT = {
#     'store_name': "Acekool",
#     'access_key': 'AKIAI4QSPO5ISDC2GJYQ',
#     'secret_key': '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',
#     'account_id': 'A2K05V5ROM13ST',
#     'mkplace_id': 'ATVPDKIKX0DER',
#     'MWSAuthToken': 'amzn.mws.70aadedd-18a2-0444-e7c9-e7146e5766b2',
# }

CURRENT_CATALOG = './Result_group/'
RESULT_XML_FILE = './Result_xml/'
RESULT_GROUP = './Result_group/'
GROUP_LIST_FILE = './Result_data/groupid_list.txt'
CSV_DATA_FILE = './Result_data/CSV_data/'
TRANSFER_FILE = './Result_data/transfer.csv'
ERROR_LOG_FILE = './Result_data/error_info.txt'
AMAZON_ACCOUNT_FILE = './Result_data/amazon_account.csv'
# 'fulfillment','orderCity','orderState', 'orderPostal'
TITLE = ['datetime', 'settlement', 'type', 'account_id', 'orderID', 'sku', 'description', 'quantity', 'marketplace', 'fulfillment', 'productSales',
         'shippingCredits', 'giftWrapCredits', 'promotionalRebates', 'salesTaxCollected', 'sellingFees', 'fbaFees', 'otherTransactionFees', 'other', 'total', 'acount']

#GROUP_ID = ['2016268tlFYqFoxQeuZoMTh3xb7pw', '2016254Roaknb1HQSykzymzEU_How',
#            '2016240kKtDUcFCSxiTEmMLM2JJcg', '2016226cdDn3r1nRMqcltMh_4z0nA', '2016212jJuAsZDnTxSHkehtMRQGaA']
STORE_ACCOUNT_LIST = [
    "Wedbration",
    # "TomYStore",
    # "Minnesota",
    # "MyBarbie",
    # "KathyMall",
    # "Inmars",
    # "DaLian",
    # "F784",
    # "Berklee",
    # "Barclays",
    # "APPLUS",
    # "Albany",
    # "AKDSteel",
    # "Acekid",

    #"Mountain",
    #     "F784",
    #     "A3",
    #     "Los Angeles-WX",
    #     "PlymouthDE",
    #     "Barclays",
    #     "FTDSakiyr",
    #     "Acekool",
    #     "OberLin",
    #     "SongyeUK",
    #     "Mountain",
    #     "MyBarbie",
    #     "MoonSharon",
    #     "Albany",
    #     "Wisconsin",
    #     "GlasgowUK",
    #     "Michigan",
    #     "AKDSteel",
    #     "Chukoo",
    #     "DaLian",
    #     "Sakala",
    #     "LiverpoolUK",
    #     "VINCI",
    #     "TomYStore",
    #     "Acekid",
    #     "ZishiUS",
    #     "Lansing",
    #     "Louisiana",
    #     "Inmars",
    #     "hellotoysme",
    #     "Minnesota",
    #     "Utoys",
    #     "EdinburghDE",
    #     "Berklee",
    #     "Dapparel",
    #     "BelfastUK",
    #     "ZiningUS",
    #     "KathyMall",
    #     "Wedbration",
    #     "Hihoddy_UK",
    #     "Uleadingstar",
    #     "YihaiJP",
    #     "SongyeJP",
    #     "ZiningJP",
    #     "KCChuangJP",
    #     "ZiningUK",
    #     "TianJin",
    #     "Lightroom",
    #     "Amazbox",
    #     "APPLUS",
    #     "XiamoJP",
    #     "ShanTou",
    #     "ChrislyH",
    #     "Kroger",
    #     "Lukoil",
    #     "Calgary",
    #     "DYTesa",
    #     "VFclar",
    #     "LuomingUK",
    #     "leilanJP",
    #     "LanleiUS",

    #"NanJing"
    #     "Acekool",
    #     "AKDSteel",
    #     "Alfahome",
    #     "Amaz~box",
    #     "Ann's",
    #     "APPLUS",
    #     "Bay Toys and Electronics",
    #     "Best Garsnal",
    #     "CAROMIO",
    #     "Cascade Toys Plus",
    #     "ChrislyH",
    #     "Cute Pets Accessories",
    #     "Elecostart",
    #     "FairyStar Gifts",
    #     "Fashion Kitchen",
    #     "Fashion NOW",
    #     "Fastforward Technologies",
    #     "FidgetKool",
    #     "FTD Sakiyr",
    #     "Glamor House",
    #     "GlorySunshine",
    #     "GoGoFashion",
    #     "hellomeme",
    #     "hellotoysme",
    #     "HiQueen",
    #     "Hobbylane",
    #     "HONNY WEDDING",
    #     "Isafish",
    #     "Just Your Beauty",
    #     "KathyMall",
    #     "Kidlove",
    #     "Kinger Roger",
    #     "Leadingstar Fashion",
    #     "LuCubanStuff",
    #     "LUNSY",
    #     "MingMing88",
    #     "Moon Sharon Express",
    #     "Mounchain",
    #     "MrWonder",
    #     "MrWonder Store",
    #     "Olympia Commerce Express",
    #     "Playtime Store",
    #     "POR She Store",
    #     "Pretty Mall",
    #     "Running Experience",
    #     "Sakalaka",
    #     "Scott Treasure",
    #     "Tex Pets Express",
    #     "TomYStore",
    #     "Toys and Fashion Homes",
    #     "USqiuhan",
    #     "Wedding Decorations Favors",
    #     "Wedding Decorations Favors Accessories",
    #     "YesFashion",
    #     "Yiwa",
    #     "Young Horse Accessories",
    #     "YRLED",
    #     "Zachary Studio",
    #     "ZBL Industrial",
    #     "zishi",
]
g_InitStore = False
g_StoreInfo = {}
g_StoreNum = 0


def GetStoreAccount(store_name):
    return g_StoreInfo.get(store_name)


def GetAccountID(store_name):
    storeinfo = GetStoreAccount(store_name)
    return storeinfo["account_id"]


def GetStoreList():
    return g_StoreInfo.keys()


def InitStore():
    global g_InitStore, g_StoreInfo, g_StoreNum
    if g_InitStore:
        return
    with open(AMAZON_ACCOUNT_FILE) as amazac:
        amazac_list = amazac.readlines()
        for ama in amazac_list:
            a = ama.split(',')
            # print a, 222222222
            store_name = a[1].replace('"', '').replace('\n', '')
            if store_name not in STORE_ACCOUNT_LIST:
                continue
            print "load store", store_name
            store_info = {
                #'store_name': store_name,
                'access_key': a[2].replace('"', '').replace('\n', ''),
                'secret_key': a[3].replace('"', '').replace('\n', ''),
                'account_id': a[4].replace('"', '').replace('\n', ''),
                'mkplace_id': a[5].replace('"', '').replace('\n', ''),
                'MWSAuthToken': a[6].replace('"', '').replace('\n', '')}
            g_StoreInfo[store_name] = store_info
            g_StoreNum += 1
    g_InitStore = True


InitStore()
