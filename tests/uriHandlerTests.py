import random
import unittest

import src.uriHandler as uhandler


class TestUriHandler(unittest.TestCase):
    def setUp(self):
        self.uriHandler = uhandler.UriHandler()

    def test_getSchemeSeparator(self):
        scheme = self.uriHandler.getSchemeSeparator('http://')
        self.assertEqual(scheme, "://")
        scheme = self.uriHandler.getSchemeSeparator('http:/')
        self.assertEqual(scheme, ":")
        scheme = self.uriHandler.getSchemeSeparator('http:')
        self.assertEqual(scheme, ":")
        scheme = self.uriHandler.getSchemeSeparator('http')
        self.assertEqual(scheme, "")

    def test_getHttpScheme(self):
        scheme = self.uriHandler.getScheme("http://testdomain.com")
        self.assertEqual(scheme, "http")
        scheme = self.uriHandler.getScheme("      http://netrnternetn     ")
        self.assertEqual(scheme, "http")
        scheme = self.uriHandler.getScheme("http://")
        self.assertEqual(scheme, "http")
        scheme = self.uriHandler.getScheme("http:")
        self.assertEqual(scheme, "http")

    def test_getComplexScheme(self):
        scheme = self.uriHandler.getScheme("test.-+-TEST://testdomain.com")
        self.assertEqual(scheme, "test.-+-TEST")
        scheme = self.uriHandler.getScheme("test.-+=;i,'ca-TEST://testdomain.com")
        self.assertEqual(scheme, "")

    def test_getIncorrectScheme(self):
        scheme = self.uriHandler.getScheme("      http ://netrnternetn     ")
        self.assertTrue(not scheme)
        scheme = self.uriHandler.getScheme("http")
        self.assertTrue(not scheme)
        scheme = self.uriHandler.getScheme("htt p")
        self.assertTrue(not scheme)

    def test_getFtpScheme(self):
        scheme = self.uriHandler.getScheme("ftp://domain.com")
        self.assertEqual(scheme, "ftp")

    def test_getMailScheme(self):
        scheme = self.uriHandler.getScheme("mailto:username@example.com?subject=Topic")
        self.assertEqual(scheme, "mailto")

    def test_getEmptyScheme(self):
        scheme = self.uriHandler.getScheme("domain.com/something")
        self.assertTrue(not scheme)
        scheme = self.uriHandler.getScheme("../something")
        self.assertTrue(not scheme)
        scheme = self.uriHandler.getScheme("127.0.0.1/something")
        self.assertTrue(not scheme)

    def test_getSchemeInAuthorityWithUserInf(self):
        scheme = self.uriHandler.getScheme("scheme:myusername:mypassword@domain.com:9000/path")
        self.assertEqual(scheme, "scheme")
        scheme = self.uriHandler.getScheme("scheme:mypassword@domain.com:9000/path")
        self.assertEqual(scheme, "scheme")

    def test_getEmptyAuthorityEmptyRequest(self):
        auth = self.uriHandler.getAuthority("")
        self.assertEqual(auth, "")
        auth = self.uriHandler.getAuthority("http:///path")
        self.assertEqual(auth, "")

    def test_getHttpAuthority(self):
        auth = self.uriHandler.getAuthority("http://testdomain.com/path")
        self.assertEqual(auth, "testdomain.com")
        auth = self.uriHandler.getAuthority("http://testdomain.com:9000/path")
        self.assertEqual(auth, "testdomain.com:9000")
        auth = self.uriHandler.getAuthority("http://127.0.0.1/path")
        self.assertEqual(auth, "127.0.0.1")
        auth = self.uriHandler.getAuthority("http://127.0.0.1:9000/path")
        self.assertEqual(auth, "127.0.0.1:9000")
        auth = self.uriHandler.getAuthority("http://[xh:ns:s2:32]:9000/path")
        self.assertEqual(auth, "[xh:ns:s2:32]:9000")
        auth = self.uriHandler.getAuthority(
            "http://errors.angularjs.org/1.2.28/$compile/tpload?p0=%2Fpartials%2Ftiles%2Ftile-m-02.html")
        self.assertEqual(auth, "errors.angularjs.org")

    def getIpV6Authority(self):
        auth = self.uriHandler.getAuthority('http://[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80/index.html')
        self.assertEqual(auth,'[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80')

    def test_getAuthorityWithUserInf(self):
        auth = self.uriHandler.getAuthority("scheme:myusername:mypassword@domain.com:9000/path")
        self.assertEqual(auth, "myusername:mypassword@domain.com:9000")
        auth = self.uriHandler.getAuthority("scheme:myusername@domain.com:9000/path")
        self.assertEqual(auth, "myusername@domain.com:9000")
        auth = self.uriHandler.getAuthority("scheme:MYTESTNAME@domain.com:9000/path")
        self.assertEqual(auth, "MYTESTNAME@domain.com:9000")

    def test_getEmptyUserInformation(self):
        inf = self.uriHandler.getUserInformation('http://domain.com/path')
        self.assertTrue(not inf)
        inf = self.uriHandler.getUserInformation('http://domain.com/path@path')
        self.assertTrue(not inf)

    def test_getUserInformation(self):
        inf = self.uriHandler.getUserInformation('http://test@domain.com/path')
        self.assertEqual(inf, 'test')
        inf = self.uriHandler.getUserInformation('http://test@domain.com/path@path')
        self.assertEqual(inf, 'test')


    def test_getMailUserInformation(self):
        inf = self.uriHandler.getUserInformation('mailto:testemail@testdomain.com')
        self.assertEqual(inf, 'testemail')

    def test_getUserInformationWithoutScheme(self):
        inf = self.uriHandler.getUserInformation('testemail@testdomain.com')
        self.assertEqual(inf, 'testemail')

    def test_getIpV6UserInformation(self):
        usefInf = self.uriHandler.getUserInformation('http://test@[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80/index.html')
        self.assertEqual(usefInf, 'test')
        usefInf = self.uriHandler.getUserInformation('http://[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80/index.html')
        self.assertEqual(usefInf, '')
        usefInf = self.uriHandler.getUserInformation('http://@[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80/index.html')
        self.assertEqual(usefInf, '')


    def test_getEmptyHostEmptyRequest(self):
        host = self.uriHandler.getHost('')
        self.assertTrue(not host)

    def test_getEmptyHost(self):
        host = self.uriHandler.getHost('scheme:///path')
        self.assertTrue(not host)

    def test_getHostInHttp(self):
        host = self.uriHandler.getHost('http://domain.com/path')
        self.assertEqual(host, 'domain.com')
        host = self.uriHandler.getHost('http://domain.com?query=12')
        self.assertEqual(host, 'domain.com')
        host = self.uriHandler.getHost('http://domain.com#fragment')
        self.assertEqual(host, 'domain.com')
        host = self.uriHandler.getHost('http://127.0.0.1/path')
        self.assertEqual(host, '127.0.0.1')
        host = self.uriHandler.getHost('http://127.0.0.1:9000?query=12')
        self.assertEqual(host, '127.0.0.1')

    def test_getIpV6Host(self):
        host = self.uriHandler.getHost('http://[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80/index.html')
        self.assertEqual(host,'FEDC:BA98:7654:3210:FEDC:BA98:7654:3210')


    def test_getHostInAuthority(self):
        host = self.uriHandler.getHost("scheme:MYTESTNAME@domain.com/path")
        self.assertEqual(host, "domain.com")
        host = self.uriHandler.getHost("scheme:myusername:mypassword@domain.com:9000/path")
        self.assertEqual(host, "domain.com")
        host = self.uriHandler.getHost("scheme:myusername@DOMAINdomain.com:9000/path")
        self.assertEqual(host, "DOMAINdomain.com")

    def test_getPort(self):
        host = self.uriHandler.getPort("scheme:MYTESTNAME@domain.com/path")
        self.assertEqual(host, "")
        host = self.uriHandler.getPort("scheme:myusername:mypassword@domain.com:9000/path")
        self.assertEqual(host, "9000")
        host = self.uriHandler.getPort("scheme:myusername@DOMAINdomain.com:9000/path")
        self.assertEqual(host, "9000")

    def test_getIpV6Port(self):
        port = self.uriHandler.getPort('http://[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:80/index.html')
        self.assertEqual(port, '80')

    def test_getEmptyPath(self):
        path = self.uriHandler.getPath('')
        self.assertTrue(not path)
        path = self.uriHandler.getPath('domain.com')
        self.assertTrue(not path)
        path = self.uriHandler.getPath('scheme://domain.com')
        self.assertTrue(not path)
        path = self.uriHandler.getPath('scheme://domain.com?query')
        self.assertTrue(not path)
        path = self.uriHandler.getPath('scheme://domain.com#fragment')
        self.assertTrue(not path)
        path = self.uriHandler.getPath('scheme:data@domain.com')
        self.assertTrue(not path)

    def test_getPath(self):
        path = self.uriHandler.getPath('domain.com/path')
        self.assertEqual(path, '/path')
        path = self.uriHandler.getPath('domain.com/root/child/file.ext')
        self.assertEqual(path, '/root/child/file.ext')
        path = self.uriHandler.getPath('scheme://domain.com/root/child/file.ext')
        self.assertEqual(path, '/root/child/file.ext')
        path = self.uriHandler.getPath('scheme:data@domain.com/root/child')
        self.assertEqual(path, '/root/child')
        path = self.uriHandler.getPath('/root/child')
        self.assertEqual(path, '/root/child')
        path = self.uriHandler.getPath('scheme:///root/child')
        self.assertEqual(path, '/root/child')
        path = self.uriHandler.getPath('scheme:/root/child')
        self.assertEqual(path, '/root/child')
        path = self.uriHandler.getPath(
            "http://errors.angularjs.org/1.2.28/$compile/tpload?p0=%2Fpartials%2Ftiles%2Ftile-m-02.html")
        self.assertEqual(path, "/1.2.28/$compile/tpload")

    def test_getPathQuery(self):
        path = self.uriHandler.getPath('scheme://domain.com/root/child?query')
        self.assertEqual(path, '/root/child')
        path = self.uriHandler.getPath('scheme://domain.com/root/child/file.ext?query')
        self.assertEqual(path, '/root/child/file.ext')

    def test_getPathFragment(self):
        path = self.uriHandler.getPath('scheme://domain.com/root/child#fragment')
        self.assertEqual(path, '/root/child')
        path = self.uriHandler.getPath('scheme://domain.com/root/child/file.ext#fragment')
        self.assertEqual(path, '/root/child/file.ext')

    def test_getEmptyStringQuery(self):
        query = self.uriHandler.getStringQuery('scheme://domain.com/root/child#fragment')
        self.assertTrue(not query)
        query = self.uriHandler.getStringQuery('scheme://domain.com/root/child/file.ext#fragment')
        self.assertTrue(not query)

    def test_getStringQuery(self):
        query = self.uriHandler.getStringQuery('scheme:///root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, 'p1=v1&p2=v2&p3=v3')
        query = self.uriHandler.getStringQuery('/root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, 'p1=v1&p2=v2&p3=v3')
        query = self.uriHandler.getStringQuery('scheme://domain.com/root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, 'p1=v1&p2=v2&p3=v3')
        query = self.uriHandler.getStringQuery('scheme://domain.com/root/child/file.ext?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, 'p1=v1&p2=v2&p3=v3')
        query = self.uriHandler.getStringQuery('root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, 'p1=v1&p2=v2&p3=v3')
        query = self.uriHandler.getStringQuery('scheme:usdata@domain:port/root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, 'p1=v1&p2=v2&p3=v3')
        query = self.uriHandler.getStringQuery(
            "http://errors.angularjs.org/1.2.28/$compile/tpload?p0=%2Fpartials%2Ftiles%2Ftile-m-02.html")
        self.assertEqual(query, "p0=%2Fpartials%2Ftiles%2Ftile-m-02.html")

    def test_getEmptyQuery(self):
        query = self.uriHandler.getQuery('scheme://domain.com/root/child#fragment')
        self.assertTrue(not query)
        query = self.uriHandler.getQuery('scheme://domain.com/root/child/file.ext#fragment')
        self.assertTrue(not query)

    def test_getgQuery(self):
        query = self.uriHandler.getQuery('scheme:///root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, {'p1': 'v1', 'p2': 'v2', 'p3': 'v3'})
        query = self.uriHandler.getQuery('/root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, {'p1': 'v1', 'p2': 'v2', 'p3': 'v3'})
        query = self.uriHandler.getQuery('scheme://domain.com/root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, {'p1': 'v1', 'p2': 'v2', 'p3': 'v3'})
        query = self.uriHandler.getQuery('scheme://domain.com/root/child/file.ext?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, {'p1': 'v1', 'p2': 'v2', 'p3': 'v3'})
        query = self.uriHandler.getQuery('root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, {'p1': 'v1', 'p2': 'v2', 'p3': 'v3'})
        query = self.uriHandler.getQuery('scheme:usdata@domain:port/root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(query, {'p1': 'v1', 'p2': 'v2', 'p3': 'v3'})

    def test_getFragment(self):
        frag = self.uriHandler.getFragment('scheme:///')
        self.assertEqual(frag, '')
        frag = self.uriHandler.getFragment('scheme:///#')
        self.assertEqual(frag, '')
        frag = self.uriHandler.getFragment('scheme:///root?p1=v1&p2=v2&p3=v3#fragment')
        self.assertEqual(frag, 'fragment')
        frag = self.uriHandler.getFragment('scheme:///#fragment')
        self.assertEqual(frag, 'fragment')

    def test_appendScheme(self):
        uri = self.uriHandler.appendScheme('', "http")
        self.assertEqual(uri, 'http://')
        uri = self.uriHandler.appendScheme('http://', "http")
        self.assertEqual(uri, 'http://')
        uri = self.uriHandler.appendScheme('domain.com', "http", ':')
        self.assertEqual(uri, 'http:domain.com')

    def test_appendAuthority(self):
        uri = self.uriHandler.appendAuthority("", "domain.com")
        self.assertEqual(uri, 'domain.com')
        uri = self.uriHandler.appendAuthority("http://", "domain.com")
        self.assertEqual(uri, 'http://domain.com')
        uri = self.uriHandler.appendAuthority("http:///path?query", "domain.com")
        self.assertEqual(uri, 'http://domain.com/path?query')
        uri = self.uriHandler.appendAuthority("http://mydomain/path?query", "domain.com")
        self.assertEqual(uri, 'http://mydomain/path?query')

    def test_appendPath(self):
        uri = self.uriHandler.appendPath('', '/path')
        self.assertEqual(uri, '/path')
        uri = self.uriHandler.appendPath('domain.com', '/path')
        self.assertEqual(uri, 'domain.com/path')
        uri = self.uriHandler.appendPath('scheme:', '/path')
        self.assertEqual(uri, 'scheme:/path')
        uri = self.uriHandler.appendPath('scheme://domian/root?query#fragment', '/path')
        self.assertEqual(uri, 'scheme://domian/root/path?query#fragment')
        uri = self.uriHandler.appendPath('?query', '/path')
        self.assertEqual(uri, '/path?query')

    def test_appendQuery(self):
        uri = self.uriHandler.appendQuery('', {'k1': 'v1', 'k2': 'v2'})
        queryParams = self.uriHandler.getQuery(uri)
        self.assertEqual(queryParams, {'k1': 'v1', 'k2': 'v2'})
        self.assertEqual(len(uri), len('?k1=v1&k2=v2'))
        uri = self.uriHandler.appendQuery('domain.com', {'k1': 'v1', 'k2': 42})
        queryParams = self.uriHandler.getQuery(uri)
        self.assertEqual(queryParams, {'k1': 'v1', 'k2': '42'})
        self.assertEqual(len(uri), len('domain.com?k1=v1&k2=42'))
        uri = self.uriHandler.appendQuery('domain.com?t1=42&t2=test', {'k1': 'v1', 'k2': 42})
        queryParams = self.uriHandler.getQuery(uri)
        self.assertEqual(queryParams, {'k1': 'v1', 'k2': '42', 't1': '42', 't2': 'test'})
        self.assertEqual(len(uri), len('domain.com?t1=42&t2=test&k1=v1&k2=42'))

    def test_appendFragment(self):
        uri = self.uriHandler.appendFragment('', 'fragment')
        self.assertEqual(uri, '#fragment')
        uri = self.uriHandler.appendFragment('domain', 'fragment')
        self.assertEqual(uri, 'domain#fragment')
        uri = self.uriHandler.appendFragment('domain#test', 'fragment')
        self.assertEqual(uri, 'domain#testfragment')

    def test_replaceScheme(self):
        uri = self.uriHandler.replaceScheme('', 'http', '://')
        self.assertEqual(uri, 'http://')
        uri = self.uriHandler.replaceScheme('scheme://domain.com', 'http', '://')
        self.assertEqual(uri, 'http://domain.com')
        uri = self.uriHandler.replaceScheme('scheme:domain.com', 'http', '://')
        self.assertEqual(uri, 'http://domain.com')
        uri = self.uriHandler.replaceScheme('scheme:domain.com', '')
        self.assertEqual(uri, 'domain.com')

    def test_replaceAuthority(self):
        uri = self.uriHandler.replaceAuthority('domain.com/path?query', 'username@newdomain.net')
        self.assertEqual(uri, 'username@newdomain.net/path?query')
        uri = self.uriHandler.replaceAuthority('scheme://domain.com/path?query', 'username@newdomain.net')
        self.assertEqual(uri, 'scheme://username@newdomain.net/path?query')
        uri = self.uriHandler.replaceAuthority('/path?query', 'username@newdomain.net')
        self.assertEqual(uri, 'username@newdomain.net/path?query')
        uri = self.uriHandler.replaceAuthority('', 'username@newdomain.net')
        self.assertEqual(uri, 'username@newdomain.net')
        uri = self.uriHandler.replaceAuthority('scheme:///path', 'username@newdomain.net')
        self.assertEqual(uri, 'scheme://username@newdomain.net/path')
        uri = self.uriHandler.replaceAuthority('scheme:///path', '')
        self.assertEqual(uri, 'scheme:///path')

    def test_replacePath(self):
        uri = self.uriHandler.replacePath('', '/newpath')
        self.assertEqual(uri, '/newpath')
        uri = self.uriHandler.replacePath('scheme://domain/path?query#frag', '/root/newpath')
        self.assertEqual(uri, 'scheme://domain/root/newpath?query#frag')
        uri = self.uriHandler.replacePath('scheme://domain/path?query#frag', '')
        self.assertEqual(uri, 'scheme://domain?query#frag')
        uri = self.uriHandler.replacePath('scheme://domain/path?query', '')
        self.assertEqual(uri, 'scheme://domain?query')

    def test_replaceQuery(self):
        uri = self.uriHandler.replaceQuery('', {'k1': 'v1', 'k2': 42})
        self.assertEqual(len(uri), len('?k1=v2&k2=42'))
        uri = self.uriHandler.replaceQuery('scheme://domain/path/path?a=1#fr', {'k1': 'v1', 'k2': 42})
        self.assertEqual(len(uri), len('scheme://domain/path/path?k1=v2&k2=42#fr'))
        uri = self.uriHandler.replaceQuery('scheme://domain/path/path?a=1&nn=11#fr', {})
        self.assertEqual(len(uri), len('scheme://domain/path/path#fr'))


# if __name__ == '__main__':
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestUriHandler)
#     unittest.TextTestRunner(verbosity=2).run(suite)
