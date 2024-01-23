from urllib.parse import urlparse, parse_qs
import Protocol

class Path:
    def __init__(self, arg):
        self._warnings = []
        url = urlparse(arg)
        qs = parse_qs(url.query)
        print(url.scheme)
        if url.scheme in Protocol.__members__:
            self.scheme = Protocol[url.scheme]
        else:
            self._warnings.append(
                "No supported scheme passed. Supported schemes are %s"
                % (", ".join(Protocol.__members__))
            )
        self.host = url.hostname
        self.port = url.port
        self.path = url.path
        self.user = url.username
        self.password = url.password
        self.credentials = qs["credentials"][0] if "credentials" in qs else None

    @property
    def warnings(self):
        return self._warnings
