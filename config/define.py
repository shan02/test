#!/usr/bin/env python
# -*- coding:utf-8 -*-
#制作:温赫男

'''常量定义
'''
RETRYTIME = 3#重试此时
AMZ_TIMEOUT = 30#文件下载超市时间
RESULT_PATH = './result/'
XML_RESULT_PATH = './result/xml/'
OUTPUT_PATH = "./result/csv/"
GROUPID_LIST_FILE = "./result/group_id_list.csv"
LOG_FILE = "./result/log.txt"
AMAZON_STORENAME_FILE = './config/amazon_account.csv'
CONFIG_FILE = "./config/config.json"
#CURRENT_CATALOG = './Result_group/'
#RESULT_XML_FILE = './Result_xml/'
#RESULT_GROUP = './Result_group/'
#GROUP_LIST_FILE = './Result_data/groupid_list.txt'
#CSV_DATA_FILE = './Result_data/CSV_data/'
#TRANSFER_FILE = './Result_data/transfer.csv'
#ERROR_LOG_FILE = './Result_data/error_info.txt'
#AMAZON_ACCOUNT_FILE = './Result_data/amazon_account.csv'
# 'fulfillment','orderCity','orderState', 'orderPostal'
TITLE = ['datetime', 'settlement', 'type', 'account_id', 'orderID', 'sku', 'description', 'quantity', 'marketplace', 'fulfillment', 'productSales',
         'shippingCredits', 'giftWrapCredits', 'promotionalRebates', 'salesTaxCollected', 'sellingFees', 'fbaFees', 'otherTransactionFees', 'other', 'total', 'acount']

import enum

class _FINANCE_DEFINE(str):
    def __new__(cls, fieldname,desc,outname):
        define = str.__new__(cls, fieldname)
        define.m_FieldName = fieldname
        define.m_Desc = desc
        define.m_OutName = outname
        return define

class FINANCE(_FINANCE_DEFINE,enum.Enum):
    DATETIME = ('datetime', "时间", 'datetime')
    SETTLEMENT = ('settlement', "结算id", 'settlement')
    TYPE = ('type', "类型", 'type')
    ACCOUNT_ID = ('account_id', "", 'account_id')
    ORDERID = ('orderID', "订单号", 'orderID')
    SKU = ('sku', "外部sku", 'sku')
    DESCRIPTION = ('description', "", 'description')
    QUANTITY = ('quantity', "数量", 'quantity')
    MARKETPLACE = ('marketplace', "市场", 'marketplace')
    FULFILLMENT = ('fulfillment', "实现", 'fulfillment')
    PRODUCTSALES = ('productSales', "产品售价", 'productSales')
    SHIPPINGCREDITS = ('shippingCredits', "运费", 'shippingCredits')
    GIFTWRAPCREDITS = ('giftWrapCredits', "礼物包装", 'giftWrapCredits')
    PROMOTIONALREBATES = ('promotionalRebates', "促销折扣", 'promotionalRebates')
    SALESTAXCOLLECTED = ('salesTaxCollected', "税", 'salesTaxCollected')
    SELLINGFEES = ('sellingFees', "平台费", 'sellingFees')
    FBAFEES = ('fbaFees', "FBA费", 'fbaFees')
    OTHERTRANSACTIONFEES = ('otherTransactionFees', "其他交易费用", 'otherTransactionFees')
    OTHER = ('other', "其他", 'other')
    TOTAL = ('total', "汇总", 'total')


OLD_TITLE_LIST = [
    FINANCE.DATETIME,
    FINANCE.SETTLEMENT,
    FINANCE.TYPE,
    FINANCE.ACCOUNT_ID,
    FINANCE.ORDERID,
    FINANCE.SKU,
    FINANCE.DESCRIPTION,
    FINANCE.QUANTITY,
    FINANCE.MARKETPLACE,
    FINANCE.FULFILLMENT,
    FINANCE.PRODUCTSALES,
    FINANCE.SHIPPINGCREDITS,
    FINANCE.GIFTWRAPCREDITS,
    FINANCE.PROMOTIONALREBATES,
    FINANCE.SALESTAXCOLLECTED,
    FINANCE.SELLINGFEES,
    FINANCE.FBAFEES,
    FINANCE.OTHERTRANSACTIONFEES,
    FINANCE.OTHER,
    FINANCE.TOTAL,
]