import os
import string
import subprocess
from random import random
from path import Path


def build_ssh_arguments(self, source: Path, target: Path):
    arguments = []
    is_mount_source = source.scheme == "ssh" and target.scheme == "ssh"
    source_point = SshPoint(source, force_mount=is_mount_source)
    target_point = SshPoint(target)
    arguments.append(source_point.arguments)
    arguments.append(target_point.arguments)
    arguments.append(source_point.point)
    arguments.append(target_point.point)
    return arguments
