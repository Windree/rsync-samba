import os
import string
import subprocess
from random import random
from path import Path


class SshPoint:
    def __init__(self, url: Path, force_mount: bool):
        self.url = url
        random.choices(string.ascii_lowercase + string.digits, k=10)
        self.error = ""

    def _mount_cifs(self):
        if self.url.scheme == "smb":
            smb_options = []
            if self.url.port != None:
                smb_options.append("port=%s" % (self.url.port))
            if self.url.username != None:
                smb_options.append("username=%s" % (self.url.username))
            if self.url.password != None:
                os.environ["PASSWORD"] = self.url.password
            result = subprocess.run(
                [
                    "mount",
                    "-t",
                    "cifs",
                    "-o",
                    ";".join(smb_options),
                    "//%s/%s" % (self.path.host, self.path.path),
                ]
            )
            if not result.returncode:
                return True
            self.error = result.stderr
            return False
