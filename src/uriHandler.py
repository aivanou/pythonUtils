__author__ = 'aliaksandr'

import re


class UriHandler:
    def getAuthority(self, uri):
        scheme = self.getScheme(uri)
        schemeSeparator = self.getSchemeSeparator(uri)
        auth = uri[(len(scheme) + len(schemeSeparator)):]
        match = re.search('^[^#/\?]+([#/\?]|$)', auth)
        if not match:
            #throw error?
            return ''
        match = match.group(0)
        if match[-1] in ['?', '/', '#']:
            return match[:-1]
        return match

    def getHost(self, uri):
        auth = self.getAuthority(uri)
        userInf = self.getUserInformation(uri)
        if not auth:
            #throw error
            return ''
        if not userInf:
            host = auth
        else:
            host = auth[len(userInf) + 1:]
        colon = host.find(':')
        if colon == -1:
            return host
        return host[:colon]

    def getUserInformation(self, uri):
        auth = self.getAuthority(uri)
        if not auth:
            #throw error?
            return ''
        infIndex = auth.find('@')
        if infIndex == -1:
            return ''
        return auth[:infIndex]

    def getPort(self, uri):
        auth = self.getAuthority(uri)
        host = self.getHost(uri)
        userInf = self.getUserInformation(uri)
        if auth.endswith(host):
            return ''
        if userInf:
            userInf += '@'
        port = auth[(len(userInf) + len(host)):]
        if port.startswith(':'):
            return port[1:]
        return port

    def getScheme(self, uri):
        match = re.search('^[\w\+\.-]+:', uri.strip())
        if not match:
            return ""
        return match.group(0)[:-1]

    def getSchemeSeparator(self, uri):
        scheme = self.getScheme(uri)
        if not scheme:
            return ''
        separator = uri[len(scheme)]
        if uri[len(scheme) + 1:].startswith('//'):
            return separator + '//'
        return separator

    def getPath(self, uri):
        if not uri:
            return ''
        auth = self.getAuthority(uri)
        scheme = self.getScheme(uri)
        schemeSeparator = self.getSchemeSeparator(uri)
        path = uri[(len(auth) + len(scheme) + len(schemeSeparator)):]
        match = re.search('^[^#\?]+([#\?]|$)', path)
        if not match:
            #throw error?
            return ''
        path = match.group(0)
        if path[-1] in ['?', '#']:
            return path[:-1]
        return path

    def getQuery(self, uri):
        if not uri:
            return ''
        scheme = self.getScheme(uri)
        schemeSeparator = self.getSchemeSeparator(uri)
        auth = self.getAuthority(uri)
        path = self.getPath(uri)
        path = scheme + schemeSeparator + auth + path
        query = uri[len(path):]
        if not query:
            return ''
        if not qu
        return query

    def getFragment(sel, uri):
        pass

    def normalize(self, uri, domain):
        pass

    def appendQuery(self, uri, params):
        pass

    def getAbsoluteURI(self, uri, domain):
        pass


def main():
    print("test")


if __name__ == "__main__":
    main()


