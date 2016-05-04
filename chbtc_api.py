﻿
import json, urllib.request, hashlib, struct, time, sys


class chbtc_api:
    def __init__(self, mykey, mysecret):
        self.mykey = mykey
        self.mysecret =  mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in range(len(slist)):
            slist[index] = chr(slist[index] ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb = struct.pack("%ds" % len(aKey), aKey.encode())
        value = struct.pack("%ds" % len(aValue), aValue.encode())
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad.encode())
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad.encode())
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value = struct.pack("%ds" % len(aValue), aValue.encode())
        # print value
        h = hashlib.sha1()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params=''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time() * 1000)
            params += '&sign=%s&reqTime=%d' % (sign, reqTime)
            url = 'https://trade.chbtc.com/api/' + path + '?' + params
            # request = urllib.request(url)
            response = urllib.request.urlopen(url, timeout=2)
            doc = json.loads(response.read().decode())
            return doc
        except Exception as ex:
            # print >> sys.stderr, 'chbtc request ex: ', ex
            raise ex
            #  return None

    def query_account(self):
        try:
            params = "method=getAccountInfo&accesskey=" + self.mykey
            path = 'getAccountInfo'

            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            # print >> sys.stderr, 'chbtc query_account exception,', ex
            return None

    def __make_order(self, price, amount, tradeType, currency):
        try:
            params = "method=order&accesskey=" + self.mykey + "&price=" + price + \
                     "&amount=" + amount + "&tradeType=" + tradeType + "&currency=" + currency
            path = 'order'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            # print >> sys.stderr, 'chbtc make_order_api exception,', ex
            raise ex
            # return None

    def make_buy(self, price, amount):
        self.__make_order(price, amount, "1", "btc")

    def make_sell(self, price, amount):
        self.__make_order(price, amount, "0", "btc")

    def get_order(self, id, currency='btc'):
        try:
            params = "method=getOrder&accesskey=" + self.mykey + "&id=" + id + \
                     "&currency=" + str(currency)
            path = 'getOrder'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            print >> sys.stderr, 'chbtc get_order exception,', ex
            raise ex
            # return None


    def __get_order_list(self, tradeType, currency, pageIndex):
        try:
            params = "method=getOrders&accesskey=" + self.mykey + "&tradeType=" + tradeType + \
                     "&currency=" + str(currency) + "&pageIndex=" + str(pageIndex)
            path = 'getOrders'
            obj = self.__api_call(path, params)
            # print obj
            return obj
        except Exception as ex:
            print >> sys.stderr, 'chbtc get_order_list exception,', ex
            raise ex
            # return None

#
# if __name__ == '__main__':
#     access_key = 'accesskey'
#     access_secret = 'secretkey'
#
#     api = chbtc_api(access_key, access_secret)
#
#     print api.query_account()
