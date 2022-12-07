'''
Some crude test for REST calls for sites.
'''
import unittest
from WMCore.Services.Requests import JSONRequests, Requests


class RESTSites_t(unittest.TestCase):


    def setUp(self):
        self.goodurls = [('/hello/', {'rows': ['world']})]
        self.meantime = [('/repack_mean_time/?run=341169', {'rows': ['world']})]
        self.badurls = [('/wronghello/', {})]

    def testGoodGetJSON(self):
        headers={"Accept": "application/json"}
        json = JSONRequests('localhost:8308')
        self.runReq(self.goodurls, json, 200)

    def testGoodGetDefault(self):
        req = Requests('localhost:8308')
        self.runReq(self.goodurls, req, 200)

    def testBaadGetJSON(self):
        headers={"Accept": "application/json"}
        json = JSONRequests('localhost:8308')
        self.runReq(self.badurls, json, 400)

    def testBaadGetDefault(self):
        req = Requests('localhost:8308')
        self.runReq(self.badurls, req, 400)

    def testMeanTime(self):
        req = Requests('localhost:8308')
        self.runReq(self.meantime, req, 400)

    def runReq(self, urls, req, code):
        #TODO: check keys returned are good
        for u in urls:
            u[0]
            result = req.get(u[0], data=u[1])
            assert result[1] == code, 'got %s instead of %s for %s: %s' % (
                                                                    result[1],
                                                                    code,
                                                                    u[0],
                                                                    result[0])

if __name__ == "__main__":
    unittest.main()
