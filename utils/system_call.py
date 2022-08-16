import os
import zipfile
import subprocess
from utils.logger import log


def check():
    if check_cmd(["java", "-h"]) is False:
        log.error("java command not exists")
        exit()
    if check_cmd(["ant", '-h']) is False:
        log.warning("ant command not exists")


def check_cmd(command):
    try:
        null = open(os.devnull, 'w')
        subprocess.call(command, stderr=subprocess.STDOUT, stdout=null)
        return True
    except OSError:
        return False


def system_call(command):
    res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = res.communicate()
    if res.poll() == 0:
        return True, output
    else:
        return False, error


def procyon_decompile(decompiler_path, jar_path, out_path):
    cmd = ["java", "-jar", decompiler_path, "-dgs=true", jar_path, "-o", out_path]
    return system_call(cmd)


def java_decompiler(decompiler_path, jar_path, out_path):
    cmd = ["java", "-cp", decompiler_path, "org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler",
           "-dgs=true", jar_path, out_path]
    return system_call(cmd)


def unzip(zip_path):
    zip_file = zipfile.ZipFile(zip_path)
    zip_list = zip_file.namelist()
    for f in zip_list:
        zip_file.extract(f, os.path.join(os.path.dirname(zip_path), "src2"))
    zip_file.close()


def ant_build():
    exit()


