## ssl context factory helper library
#
# Copyright (c) 2008, 2009 Adam Marshall Smith
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Idea:
# - allow anyone who's cert verifies
# - verify people using ONLY our single CA
# - log everyone who comes by

from OpenSSL import SSL, crypto

class ServerContextFactory(object):
    def __init__(self, myKey, trustedCA):
        self.myKey = myKey
        self.trustedCA = trustedCA

    def _verify(self, connection, x509, errnum, errdepth, ok):
        dude = x509.get_subject().commonName
        if ok:
            print 'Allowing SSL connection from', dude
        else:
            print 'Blocking SSL connection from', dude
        return ok

    def getContext(self):
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_certificate_file(self.myKey)
        ctx.use_privatekey_file(self.myKey)
        ctx.load_client_ca(self.trustedCA)
        ctx.load_verify_locations(self.trustedCA)
        ctx.set_verify(SSL.VERIFY_PEER |  SSL.VERIFY_FAIL_IF_NO_PEER_CERT, self._verify)
        ctx.set_verify_depth(1)
        return ctx
