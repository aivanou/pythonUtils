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

# if __name__ == '__main__':
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestUriHandler)
#     unittest.TextTestRunner(verbosity=2).run(suite)
