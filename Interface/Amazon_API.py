#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import re
import sys
import time
import urllib

from requests import request
from requests.exceptions import HTTPError
import define
import publog
#from util import amazon_conf
from util.xml_util import xml2dict


# from xml.dom.minidom import parse, parseString
# from xml.etree.ElementTree import fromstring
try:
    from xml.etree.ElementTree import ParseError as XMLError
except ImportError:
    from xml.parsers.expat import ExpatError as XMLError


reload(sys)
sys.setdefaultencoding('utf-8')

MARKETPLACES = {
    "A2EUQ1WTGCTBG2": "https://mws.amazonservices.ca",  # A2EUQ1WTGCTBG2
    "ATVPDKIKX0DER": "https://mws.amazonservices.com",  # ATVPDKIKX0DER",
    "A1AM78C64UM0Y8": "https://mws.amazonservices.com.mx",  # A1AM78C64UM0Y8
    "A1PA6795UKMFR9": "https://mws-eu.amazonservices.com",  # A1PA6795UKMFR9
    "A1RKKUPIHCS9HS": "https://mws-eu.amazonservices.com",  # A1RKKUPIHCS9HS
    "A13V1IB3VIYZZH": "https://mws-eu.amazonservices.com",  # A13V1IB3VIYZZH
    "A21TJRUUN4KGV": "https://mws.amazonservices.in",  # A21TJRUUN4KGV
    "APJ6JRA9NG5V4": "https://mws-eu.amazonservices.com",  # APJ6JRA9NG5V4
    "A1F83G8C2ARO7P": "https://mws-eu.amazonservices.com",  # A1F83G8C2ARO7P
    "A1VC38T7YXB528": "https://mws.amazonservices.jp",  # A1VC38T7YXB528
    "AAHKV2X7AFYLW": "https://mws.amazonservices.com.cn",  # AAHKV2X7AFYLW
}


class MWS(object):
    """ Base Amazon API class """

    # This is used to post/get to the different uris used by amazon per api
    # ie. /Orders/2011-01-01
    # All subclasses must define their own URI only if needed
    URI = "/"

    # The API version varies in most amazon APIs
    VERSION = "2009-01-01"

    # There seem to be some xml namespace issues. therefore every api subclass
    # is recommended to define its namespace, so that it can be referenced
    # like so AmazonAPISubclass.NS.
    # For more information see http://stackoverflow.com/a/8719461/389453
    NS = ''

    # Some APIs are available only to either a "Merchant" or "Seller"
    # the type of account needs to be sent in every call to the amazon MWS.
    # This constant defines the exact name of the parameter Amazon expects
    # for the specific API being used.
    # All subclasses need to define this if they require another account type
    # like "Merchant" in which case you define it like so.
    # ACCOUNT_TYPE = "Merchant"
    # Which is the name of the parameter for that specific account type.
    ACCOUNT_TYPE = "SellerId"

    def __init__(self, access_key, secret_key, account_id, mkplace_id='ATVPDKIKX0DER', MWSAuthToken=None,
                 domain='https://mws.amazonservices.com', uri="", version=""):
        self.access_key = access_key
        self.secret_key = secret_key
        self.account_id = account_id
        self.mkplace_id = mkplace_id
        #        if MWSAuthToken:
        self.MWSAuthToken = MWSAuthToken
        #        self.domain = domain
        self.domain = MARKETPLACES[mkplace_id]
        self.uri = uri or self.URI
        self.version = version or self.VERSION

    def make_request(self, extra_data, method="GET", **kwargs):
        """Make request to Amazon MWS API with these parameters
        """
        # Remove all keys with an empty value because
        # Amazon's MWS does not allow such a thing.
        # ffff = open('/home/ytroot/DeryAPP/fafafafafaafafafafaiiiiii.txt', 'aw')

        extra_data = remove_empty(extra_data)

        if self.MWSAuthToken:
            params = {
                'AWSAccessKeyId': self.access_key,
                self.ACCOUNT_TYPE: self.account_id,
                'SignatureVersion': '2',
                'MWSAuthToken': self.MWSAuthToken,
                'Timestamp': self.get_timestamp(),
                'Version': self.version,
                'SignatureMethod': 'HmacSHA256',
            }
        else:
            params = {
                'AWSAccessKeyId': self.access_key,
                self.ACCOUNT_TYPE: self.account_id,
                'SignatureVersion': '2',
                'Timestamp': self.get_timestamp(),
                'Version': self.version,
                'SignatureMethod': 'HmacSHA256',
            }
        params.update(extra_data)
        request_description = '&'.join(
            ['%s=%s' % (k, urllib.quote(params[k], safe='-_.~').encode('utf-8')) for k in sorted(params)])
        signature = self.calc_signature(method, request_description)

        url = '%s%s?%s&Signature=%s' % (
            self.domain, self.uri, request_description, urllib.quote(signature))
        #        print '-----------------华丽的分割线----------------------------------------------------'
        #        print '[url]:',url
        # print
        # '-----------------华丽的分割线----------------------------------------------------'
        headers = {'User-Agent': 'python-amazon-mws/0.0.1 (Language=Python)'}
        headers.update(kwargs.get('extra_headers', {}))
        #######################################################################
        try:
            # Some might wonder as to why i don't pass the params dict as the params argument to request.
            # My answer is, here i have to get the url parsed string of params in order to sign it, so
            # if i pass the params dict as params to request, request will repeat that step because it will need
            # to convert the dict to a url parsed string, so why do it twice if i can just pass the full url :).
            # print "okokokokokokokok"
            retry_number = 0
            while True and retry_number < define.RETRYTIME:
                retry_number = retry_number + 1
                try:
                    publog.info("request",method, url)
                    # proxies = {"http": "http://10.10.1.10:3128",
                    #           "https": "http://10.10.1.10:1080", }
                    #response = request(method, url, data=kwargs.get('body', ''), proxies=proxies, headers=headers, timeout=18)
                    response = request(method, url, data=kwargs.get(
                        'body', ''),  headers=headers, timeout=define.AMZ_TIMEOUT)
                    result = response.text
                    response.raise_for_status()
                    break
                except Exception, e:
                    # ffff.write(url+'\n')
                    #error_info = open(amazon_conf.ERROR_LOG_FILE, 'aw')
                    reson = str(e)
                    #@todo多一种情况要处理
            #         < ErrorResponse
            #         xmlns = "http://mws.amazonservices.com/Finances/2015-05-01" >
            #         < Error >
            #         < Type > Sender < / Type >
            #         < Code > InvalidRequestException < / Code >
            #         < Message > Token is not valid, token
            #         duration is 12
            #         minutes. < / Message >
            #     < / Error >
            #     < RequestId > 7
            #     a6fa25b - d991 - 41e2 - af5c - efe3322e1caa < / RequestId >
            # < / ErrorResponse >
            #         < ?xml
            #         version = "1.0"? >
            #         < ErrorResponse
            #         xmlns = "http://mws.amazonservices.com/schema/Finances/2015-05-01" >
            #         < Error >
            #         < Type > Sender < / Type >
            #         < Code > RequestExpired < / Code >
            #         < Message > Request
            #         signature is too
            #         far in the
            #         past and has
            #         expired.Timestamp
            #         date: 2017 - 05 - 22
            #         T13:45:45
            #         Z < / Message >
            #     < / Error >
            #     < RequestID > a27e75ec - 47
            #     d0 - 4517 - 8
            #     bf8 - e8317cad30ac < / RequestID >
            # < / ErrorResponse >
            #         < ErrorResponse
            #         xmlns = "http://mws.amazonservices.com/Finances/2015-05-01" >
            #         < Error >
            #         < Type > Sender < / Type >
            #         < Code > InvalidRequestException < / Code >
            #         < Message > Token is not valid, token
            #         duration is 4
            #         minutes. < / Message >
            #     < / Error >
            #     < RequestId > dc6ab995 - f288 - 4e2
            #     e - acff - 1
            #     ef749e4d7a4 < / RequestId >
            # < / ErrorResponse >

                    if reson == "400 Client Error: Bad Request":
                        publog.exception("严重错误.",result)
                        with open("errfile.log","wa") as f:
                            f.write("无法处理错误.%s"%str(extra_data))
                        break

                    publog.exception("amz接口访问异常",json.dumps({'url': url, 'reson': reson}))
                    #error_info.write(json.dumps({'url': url, 'reson': e}))
                    #print e, "hahhahahhahahahahahhahahhah"
                #import time
                #time.sleep(retry_number*10)
                publog.info("request失败重试",retry_number)
            # When retrieving data from the response object,
            # be aware that response.content returns the content in bytes while response.text calls
            # response.content and converts it to unicode.
            data = response.content

            # I do not check the headers to decide which content structure to server simply because sometimes
            # Amazon's MWS API returns XML error responses with "text/plain" as the Content-Type.
        #            try:
        #                parsed_response = DictWrapper(data, extra_data.get("Action") + "Result")
        #            except XMLError:
        #                parsed_response = DataWrapper(data, response.headers)

        except HTTPError, e:
            error = MWSError(str(e))
            error.response = e.response
            raise error

            # Store the response object in the parsed_response for quick access
        #        parsed_response.response = response
        return data

    ##########################################################################

    ##########GetServiceStatus API#################

    def get_service_status(self):
        """
            Returns a GREEN, GREEN_I, YELLOW or RED status.
            Depending on the status/availability of the API its being called from.
        """

        return self.make_request(extra_data=dict(Action='GetServiceStatus'))

    def calc_signature(self, method, request_description):
        """Calculate MWS signature to interface with Amazon
        """
        sig_data = method + '\n' + self.domain.replace('https://',
                                                       '').lower() + '\n' + self.uri + '\n' + request_description
        return base64.b64encode(hmac.new(str(self.secret_key), sig_data, hashlib.sha256).digest())

    ###########################################################################

    def get_timestamp(self):
        """
            Returns the current timestamp in proper format.
        """
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    ######################################################

    def enumerate_param(self, param, values):
        """
            Builds a dictionary of an enumerated parameter.
            Takes any iterable and returns a dictionary.
            ie.
            enumerate_param('MarketplaceIdList.Id', (123, 345, 4343))
            returns
            {
                MarketplaceIdList.Id.1: 123,
                MarketplaceIdList.Id.2: 345,
                MarketplaceIdList.Id.3: 4343
            }
        """
        params = {}
        if values is not None:
            if not param.endswith('.'):
                param = "%s." % param
            for num, value in enumerate(values):
                params['%s%d' % (param, (num + 1))] = value
        return params


#### Fulfillment APIs ####

class AuthToken(MWS):
    URI = "/Sellers/2011-07-01"
    VERSION = "2011-07-01"
    NS = '{https://mws.amazonservices.com/Sellers/2011-07-01}'

    def getAuthToken(self):
        data = dict(Action='GetAuthToken')
        return self.make_request(data, "POST")


class Amazon_Finance(MWS):
    """ Amazon MWS Products API """
    URI = '/Finances/2015-05-01'
    VERSION = '2015-05-01'
    NS = '{http://mws.amazonservices.com/schema/Finances/2015-05-01}'

    def list_finace_event_group(self, FinancialEventGroupStartedAfter, FinancialEventGroupStartedBefore):

        data = dict(Action='ListFinancialEventGroups',
                    FinancialEventGroupStartedAfter=FinancialEventGroupStartedAfter,
                    FinancialEventGroupStartedBefore=FinancialEventGroupStartedBefore,
                    )
        return self.make_request(data, 'POST')

    def list_finace_event(self, FinancialEventGroupId):
        """
        """
        data = dict(Action='ListFinancialEvents',
                    # PostedAfter=PostedAfter,
                    # PostedBefore=PostedBefore,
                    FinancialEventGroupId=FinancialEventGroupId,
                    # AmazonOrderId=AmazonOrderId,
                    )
        return self.make_request(data, 'POST')

    def list_finace_event_by_nextToken(self, NextToken):
        data = dict(Action='ListFinancialEventsByNextToken',
                    NextToken=NextToken,
                    )
        return self.make_request(data, 'POST')


def remove_namespace(xml):
    regex = re.compile(' xmlns(:ns2)?="[^"]+"|(ns2:)|(xml:)')
    return regex.sub('', xml)


def remove_empty(d):
    """
        Helper function that removes all keys from a dictionary (d),
        that have an empty value.
    """
    for key in d.keys():
        if not d[key]:
            del d[key]
    return d


def calc_md5(string):
    """Calculates the MD5 encryption for the given string
    """
    md = hashlib.md5()
    md.update(string)
    return base64.encodestring(md.digest()).strip('\n')


class DataWrapper(object):
    """
        Text wrapper in charge of validating the hash sent by Amazon.
    """

    def __init__(self, data, header):
        self.original = data
        if 'content-md5' in header:
            hash_ = calc_md5(self.original)
            if header['content-md5'] != hash_:
                raise MWSError("Wrong Contentlength, maybe amazon error...")

    @property
    def parsed(self):
        return self.original


class DictWrapper(object):
    def __init__(self, xml, rootkey=None):
        self.original = xml
        self._rootkey = rootkey
        self._mydict = xml2dict().fromstring(remove_namespace(xml))
        self._response_dict = self._mydict.get(self._mydict.keys()[0],
                                               self._mydict)

    @property
    def parsed(self):
        if self._rootkey:
            return self._response_dict.get(self._rootkey)
        else:
            return self._response_dict


class MWSError(Exception):
    """
        Main MWS Exception class
    """
    # Allows quick access to the response object.
    # Do not rely on this attribute, always check if its not None.
    response = None

#
# if __name__ == '__main__':
#
