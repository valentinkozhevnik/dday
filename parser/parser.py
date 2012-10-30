# --*-- coding: utf-8 --*--

import datetime
import grab
from domains.models import ProxyList

class Parser(object):
    name = None
    str = ''
    model = None
    date = ''
    date_today = datetime.date.today()

    def __init__(self, name=None, str='', model=None):
        self.name = name
        self.str = str
        self.model = model

    def parse(self, name):
        try:
            print "<---- seach"
#            print self.model.objects.count()
            obj = self.model.objects.get(name=name)
#            obj.google_dir = self.get_google_dir(site_names=name)
#            obj.dmoz = self.get_dmoz(site_names=name)
#            print self.get_create_years(name)

#            print "get_google_rp ->", self.GetPageRank(name)
#            print "get_google_link ->", self.get_google_link(site_names=name)
#            print "get_create_years ->", self.get_create_years(site_names=name)
#            print "get_dmoz ->", self.get_dmoz(site_names=name)
#            print "get_google_dir ->", self.get_google_dir(site_names=name)
#            print "get_age_history ->", self.get_age_history(site_names=name)
#            print "get_alexa_rank ->", self.get_alexa_rank(site_names=name)
#            obj.save()
            print "%d - iter %s" % (obj.id, obj.name)
        except self.model.DoesNotExist:
            obj = self.model(name=name)
            obj.date_valid = datetime.date.today()
            print "get_google_rp ->", self.GetPageRank(name)
            print "get_google_link ->", self.get_google_link(site_names=name)
#            print "get_create_years ->", self.get_create_years(site_names=name)
            print "get_dmoz ->", self.get_dmoz(site_names=name)
            print "get_google_dir ->", self.get_google_dir(site_names=name)
            print "get_age_history ->", self.get_age_history(site_names=name)
            print "get_alexa_rank ->", self.get_alexa_rank(site_names=name)
            obj.save()
            print "%d - created %s" % (obj.id,obj.name)
        return True

    def splitInfo(self, str=''):
        list_param = self.str.split('|')
        result_str = str.split(list_param[0])[int(list_param[1])]
        return result_str

    def openFile(self, name):
        f = open(name)
        while True:
            str = f.readline()
            if str != 'END\n':
                self.parse(name=self.splitInfo(str))
            else:
                break
        return "END"

    def scanFolder(self, date=''):
        pass

    def clearTable(self):
        pass

    def get_google_link(self, site_names=''):
        site_name = site_names
        grab_file = grab.Grab()
        grab_file.setup(url="https://www.google.com.ua/search?q=link:%s" % site_name)
        grab_request = grab_file.request()
        try:
            strs = grab_file.xpath('//*[@id="resultStats"]').text_content()
            try:
                res = str(strs.split(' ')[3].replace(u'\xa0', ''))
            except IndexError:
                res = 0
        except grab.DataNotFound:
            res =0
        return res

    def get_google_dir(self, site_names=''):
        site_name = site_names
        grab_file = grab.Grab()
        grab_file.setup(url="http://dir.search.yahoo.com/search?p="\
        + site_name)
        grab_request = grab_file.request()
        strs = grab_file.xpath('//*[@id="resultCount"]').text_content()
        if strs == "0":
            return False
        else:
            return True

    def get_dmoz(self, site_names=''):
        site_name = site_names
        grab_file = grab.Grab()
        grab_file.setup(url="http://www.dmoz.org/search/?q="\
        + site_name)
        grab_request = grab_file.request()
        try:
            strs = grab_file.xpath('//*[@id="bd-cross"]/h3[1]/strong').text_content()
            return True
        except grab.DataNotFound:
            return False

    def get_age_history(self, site_names=''):
        site_name = site_names
        grab_file = grab.Grab()
        grab_file.setup(url="http://wayback.archive.org/web/*/http://"\
        + site_name)#, proxy=ProxyList.objects.order_by('?')[0].ip)
        try:
            grab_request = grab_file.request()
            date_year = grab_file.xpath('//*[@id="wbMeta"]/p[1]/a[2]').text_content()
            count = grab_file.xpath('//*[@id="wbMeta"]/p[1]/strong').text_content()
            print count, date_year
            res1 = datetime.date.today().year - int(date_year.split(' ')[2])
            res2 = int(count.split(' ')[0].replace(',', ''))
            return res1, res2
        except grab.DataNotFound:
            return 0, 0
        except (grab.GrabTimeoutError, grab.GrabNetworkError):
            print "recurs"
            self.get_age_history(site_names)


    prhost='toolbarqueries.google.com'
    prpath='/tbr?client=navclient-auto&ch=%s&features=Rank&q=info:%s'

    # Function definitions
    def GetHash (self, query):
        SEED = "Mining PageRank is AGAINST GOOGLE'S TERMS OF SERVICE. Yes, I'm talking to you, scammer."
        Result = 0x01020345
        for i in range(len(query)) :
            Result ^= ord(SEED[i%len(SEED)]) ^ ord(query[i])
            Result = Result >> 23 | Result << 9
            Result &= 0xffffffff
        return '8%x' % Result

    def GetPageRank (self, query):
        import httplib
        conn = httplib.HTTPConnection(self.prhost)
        hash = self.GetHash(query)
        path = self.prpath % (hash,query)
        conn.request("GET", path)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data.split(":")[-1].replace('\n', '')

    def get_proxy_list(self, name_file='', model=''):
        f = open(name_file)
        while True:
            str = f.readline()
            if str != 'END\n' and str != 'END':
                print str
                try:
                    obj = model.objects.get(ip=str)
                except model.DoesNotExist:
                    obj = model(ip = str)
                    obj.save()
            else:
                break

    def get_create_years(self, site_names=''):
        site_name = site_names
        grab_file = grab.Grab()
        try:
            grab_file.setup(url="http://who.is/whois/"\
                                + site_name)#, proxy=ProxyList.objects.order_by('?')[0].ip)
            grab_request = grab_file.request()
            date_year = grab_file.xpath('//*[@id="registry_whois"]/div/div[2]/table/tbody/tr[2]/td/span')
            return date_year.text.split(' ')[-1]
        except grab.DataNotFound:
            return 0

    def get_alexa_rank(self, site_names=''):
        site_name = site_names
        grab_file = grab.Grab()
        try:
            grab_file.setup(url="http://data.alexa.com/data/?cli=10&url="\
                                + site_name)#, proxy=ProxyList.objects.order_by('?')[0].ip)
            grab_request = grab_file.request()
            return grab_file.xml_tree.xpath('/ALEXA/SD/POPULARITY')[0].get('TEXT')
        except IndexError:
            return 0
