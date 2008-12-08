## ssl context factory helper library
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
