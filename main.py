import os

from utils.parser import parse
from utils.system_call import *
from utils.build_xml import build_ant_xml


if __name__ == '__main__':
    # todo suppose mac/win
    check()
    cmd_parse = parse()
    jar_path = cmd_parse["jar_path"]
    out_path = cmd_parse["out_path"]
    tomcat_path = cmd_parse["tomcat_path"]
    build_xml = cmd_parse["build_xml"]

    if os.path.isabs(jar_path) is False:
        jar_path = os.path.abspath(jar_path)
    if os.path.isabs(out_path) is False:
        out_path = os.path.abspath(out_path)

    java_decompiler_path = os.path.abspath(os.path.join("jar", "java-decompiler.jar"))
    procyon_decompile_path = os.path.abspath(os.path.join("jar", "procyon-decompiler-0.6.0.jar"))
    zip_path = os.path.abspath(os.path.join(out_path, os.path.basename(jar_path)))
    xml_path = os.path.abspath("build.xml")

    status, out = procyon_decompile(procyon_decompile_path, jar_path, os.path.join(out_path, "src1"))
    if status is False:
        log.info("procyon decompile error!")
        log.error(out)
        exit()
    log.info("procyon decompile successful!")

    status, out = java_decompiler(java_decompiler_path, jar_path, out_path)
    if status is False:
        log.info("java decompile error!")
        log.error(out)
        exit()
    log.info("java decompile successful!")

    unzip(zip_path)

    if build_xml is not True:
        build_ant_xml(xml_path, out_path, tomcat_path)
    # ant_build()




