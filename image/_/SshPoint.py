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

    def _mount_ssh(self):
        sshfs_options = []
        sshfs_arguments = []
        sshfs_remote = []
        if self.url.port != None:
            sshfs_arguments.append("-p")
            sshfs_arguments.append(self.url.port)
        if self.url.username != None:
            smb_options.append("username=%s" % (self.url.username))
        if self.url.password != None:
            os.environ["PASSWORD"] = self.url.password
        result = subprocess.run(
            [
                "sshfs",
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
    1  apt update && apt install -y sshfs
    2  apt install -y sshfsa
    3  apt install -y sshfs
    4  history
    5  mount -t sshfs 10.22.0.8 /mnt
    6  mount -t sshfs ssh://10.22.0.8 /mnt
    7  sudo modprobe fuse
    8  modprobe fuse
    9  sshfs ssh_home@10.22.0.8/home /mnt
   10  sshfs ssh://ssh_home@10.22.0.8/home /mnt
   11  history 