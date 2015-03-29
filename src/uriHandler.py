__author__ = 'aliaksandr'

import re

#TODO: implement validation error


class UriHandler:
    """
    Retrieves the authority from the URI, as described in RFC3986,
     Authority consists of userinformation@host:port and placed after scheme
    """

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

    """
    Retrieves the host from the authority. The host is one of: IPv4, IPv6 or domain name.
    The port can be set ater the host, e.g.: testdomain:9000
    """

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
        if host.startswith('['):
            endIndex = host.find(']')
            if endIndex == -1:
                return ''
            return host[1:endIndex]
        colon = host.find(':')
        if colon == -1:
            return host
        return host[:colon]

    def __hasIpV6Host(self, uri):
        auth = self.getAuthority(uri)
        userInf = self.getUserInformation(uri)
        if not auth:
            #throw error
            return ''
        if not userInf:
            host = auth
        else:
            host = auth[len(userInf) + 1:]
        return host.startswith('[')

    """
    Gets the user information from the uri.
    As described in RFC3986, user information is first part of the authority,
    separated by the '@' symbol.
    Example: testname@testdomain.ext => testname is a user information
    """

    def getUserInformation(self, uri):
        auth = self.getAuthority(uri)
        if not auth:
            #throw error?
            return ''
        infIndex = auth.find('@')
        if infIndex == -1:
            return ''
        return auth[:infIndex]

    """
        retrieves tne port from the URI
        the port is separated with ':' symbol.
        also supports the IPv6 format
    """
    def getPort(self, uri):
        auth = self.getAuthority(uri)
        host = self.getHost(uri)
        userInf = self.getUserInformation(uri)
        if auth.endswith(host):
            return ''
        if userInf:
            userInf += '@'
        if self.__hasIpV6Host(uri):
            port = auth[(len(userInf) + len(host)+2):]
        else:
            port = auth[(len(userInf) + len(host)):]
        if port.startswith(':'):
            return port[1:]
        return port

    """
        retrieves and returnes scheme of the uri,
        if no scheme specified returns empty string
        Accorting to RFC3986, scheme is a string until delimiter(which is ';' or '://')
    """
    def getScheme(self, uri):
        match = re.search('^[\w\+\.-]+:', uri.strip())
        if not match:
            return ""
        return match.group(0)[:-1]

    """
        returns the separator between sheme and authority,
        if no scheme specified returns empty string
    """
    def getSchemeSeparator(self, uri):
        scheme = self.getScheme(uri)
        if not scheme:
            return ''
        separator = uri[len(scheme)]
        if uri[len(scheme) + 1:].startswith('//'):
            return separator + '//'
        return separator

    """
        returns the path of the URI
        the path starts directly after authority with the symbol '/' and ends
        when with '?,#, or end string'
        if no uri specified, returns empty string
    """
    def getPath(self, uri):
        if not uri:
            return ''
        auth = self.getAuthority(uri)
        scheme = self.getScheme(uri)
        schemeSeparator = self.getSchemeSeparator(uri)
        path = uri[(len(auth) + len(scheme) + len(schemeSeparator)):]
        match = re.search('^[^#\?]+([#\?]|$)', path)
        if not match:
            #Todo: throw an error
            return ''
        path = match.group(0)
        if path[-1] in ['?', '#']:
            return path[:-1]
        return path

    """
        Returns the query part of URI as a string.
        if no URI specified returns empty string
        if no query found in URI returns empty string
        otherwise returns query.
        According to RFC3986, the query follows after the path(which can be empty),
            it starts with '?' and finised with '# or end of the string'
    """
    def getStringQuery(self, uri):
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
        match = re.search('^\?([^#]+)([#]|$)', query)
        if not match:
            return ''
        return match.group(1)

    """
        Returns query as a dictionary
        if no query is specified, returns empty string
        According to RFC3986, the query follows after the path(which can be empty),
            it starts with '?' and finised with '# or end of the string'
    """
    def getQuery(self, uri):
        query = self.getStringQuery(uri)
        if not query:
            return {}
        params = {}
        for part in re.split('[;&]', query):
        #TODO: cach exception
            (key, value) = part.split('=')
            params[key] = value
        return params

    """
        Returns the fragment or empty string
    """
    def getFragment(self, uri):
        match = re.search('#([\w]*)', uri)
        if not match:
            return ''
        return match.group(1)

    def normalize(self, uri, authority='', scheme=''):
        pass

    def getAbsoluteURI(self, uri, domain):
        pass


    """
        Appends scheme to the current URI.
        if empty scheme , appends nothing
        Second argument is optional separator, default is '://'
    """
    def appendScheme(self, uri, scheme, separator="://"):
        currScheme = self.getScheme(uri)
        if not currScheme:
            return scheme + separator + uri
            #throw error?
        return uri

    """
        Appends authority to the uri if URI has no authority,
        otherwise doing nothing
    """
    def appendAuthority(self, uri, auth):
        currAuthority = self.getAuthority(uri)
        if not currAuthority:
            scheme = self.getScheme(uri)
            separator = self.getSchemeSeparator(uri)
            return scheme + separator + auth + uri[len(scheme + separator):]
        return uri


    """
        Appends path to the URI.
        If path was already specified, adds new path to the current path
    """
    def appendPath(self, uri, path):
        currPath = self.getPath(uri)
        newPath = currPath + path
        partialUri = self.getScheme(uri) + self.getSchemeSeparator(uri) + self.getAuthority(uri)
        return partialUri + newPath + uri[(len(partialUri) + len(currPath)):]

    """
        appends query to the uri
        params is a dictionary of values
        delimiter is an optional parameter that delimits the query pairs
    """
    def appendQuery(self, uri, params, delimiter='&'):
        query = self.queryToString(params, delimiter)
        currQuery = self.getStringQuery(uri)
        partialUri = self.getScheme(uri) + self.getSchemeSeparator(uri) + self.getAuthority(uri) + self.getPath(uri)
        if currQuery:
            query = '?' + currQuery + delimiter + query
            postfixPosition = len(partialUri) + len(currQuery) + 1
        else:
            query = '?' + query
            postfixPosition = len(partialUri)
        return partialUri + query + uri[postfixPosition:]

    """
        Appends fragment to the URI
    """
    def appendFragment(self, uri, fragment):
        if not self.getFragment(uri):
            return uri + '#' + fragment
        return uri + fragment

    def replaceScheme(self, uri, newScheme, schemeSeparator="://"):
        currScheme = self.getScheme(uri)
        currSeparator = self.getSchemeSeparator(uri)
        newUri = uri[(len(currScheme) + len(currSeparator)):]
        if not newScheme:
            return newUri
        return newScheme + schemeSeparator + newUri

    def replaceAuthority(self, uri, newAuth):
        currScheme = self.getSchemeWithSeparator(uri)
        currAuth = self.getAuthority(uri)
        return currScheme + newAuth + uri[(len(currScheme) + len(currAuth)):]

    def replacePath(self, uri, newPath):
        currPath = self.getPath(uri)
        currScheme = self.getSchemeWithSeparator(uri)
        currAuth = self.getAuthority(uri)
        return currScheme + currAuth + newPath + uri[(len(currScheme) + len(currAuth) + len(currPath)):]

    def replaceQuery(self, uri, params):
        newQuery = self.queryToStringWithSeparator(params)
        currPath = self.getPath(uri)
        currScheme = self.getSchemeWithSeparator(uri)
        currAuth = self.getAuthority(uri)

        return currScheme + currAuth + currPath + newQuery + self.getFragmentWithSeparator(uri)

    def buildUri(self, scheme='', shcemeSeparator='://', auth='', path='', query='', fragment=''):
        return scheme + shcemeSeparator + auth + path + '?' + query + '#' + fragment

    def buildAuthority(self, userInf, host, port):
        auth = ''
        if userInf:
            auth = auth + userInf + '@'
        if host:
            auth = auth + host
        if port:
            auth = auth + ':' + port
        return auth

    def queryToString(self, query, delimiter='&'):
        qString = ''
        for key in query:
            qString += key + '=' + str(query[key]) + delimiter
        return qString[:-1]

    def getSchemeWithSeparator(self, uri):
        return self.getScheme(uri) + self.getSchemeSeparator(uri)

    def getFragmentWithSeparator(self, uri):
        fr = self.getFragment(uri)
        if not fr:
            return ''
        return '#' + fr

    def queryToStringWithSeparator(self, params, delimiter='&'):
        query = self.queryToString(params)
        if not query:
            return ''
        return '?' + query


def main():
    print("test")


if __name__ == "__main__":
    main()


