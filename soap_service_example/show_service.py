from spyne import ServiceBase, Application, rpc, Integer, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class NumberConversion(ServiceBase):
 
    @rpc(Integer, _returns=String)
    def NumberToWords(self, num):
        d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
            6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
            11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
            15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
            19 : 'nineteen', 20 : 'twenty',
            30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
            70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
        k = 1000
        m = k * 1000
        b = m * 1000
        t = b * 1000

        assert(0 <= num)

        if (num < 20):
            return d[num]

        if (num < 100):
            if num % 10 == 0: return d[num]
            else: return d[num // 10 * 10] + '-' + d[num % 10]

        if (num < k):
            if num % 100 == 0: return d[num // 100] + ' hundred'
            else: 
                return d[num // 100] + ' hundred and ' + self.NumberToWords(num % 100)

        if (num < m):
            if num % k == 0: return self.NumberToWords(num // k) + ' thousand'
            else:
                return self.NumberToWords(num // k) + ' thousand, ' + self.NumberToWords(num % k)

        if (num < b):
            if (num % m) == 0: return self.NumberToWords(num // m) + ' million'
            else:
                return self.NumberToWords(num // m) + ' million, ' + self.NumberToWords(num % m)

        if (num < t):
            if (num % b) == 0: return self.NumberToWords(num // b) + ' billion'
            else:
                return self.NumberToWords(num // b) + ' billion, ' + self.NumberToWords(num % b)

        if (num % t == 0): return self.NumberToWords(num // t) + ' trillion'
        else: 
            return self.NumberToWords(num // t) + ' trillion, ' + self.NumberToWords(num % t)

application = Application([NumberConversion], 'my.soap.app',
        in_protocol=Soap11(),
        out_protocol=Soap11(),
    )
 
wsgi_app = WsgiApplication(application)
server = make_server('127.0.0.1', 7789, wsgi_app)
 
print ("listening to http://127.0.0.1:7789")
print ("wsdl is at: http://www.dataaccess.com/webservicesserver/numberconversion.wso?WSDL")
 
server.serve_forever()