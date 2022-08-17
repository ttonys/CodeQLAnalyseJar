import argparse


def parse():
    usage = "CodeQL Analysis Jar[options]"
    parser = argparse.ArgumentParser(prog='CodeQLAnalysisJar', usage=usage)
    parser.add_argument('-jar', dest='jar_path', action='store', required=True,
                        help='指定jar包路径')
    parser.add_argument('-out', dest='out_path', action='store', required=True,
                        help='指定输出文件路径')
    parser.add_argument('-tomcat', dest='tomcat_path', action='store', required=False,
                        default=False, help='引入tomcat相关jar, 如:/usr/local/apache-tomcat-8.5.75, default: false')
    parser.add_argument('-xml', dest='build_xml', action='store_false', required=False,
                        help='自动生成build.xml文件, default: true')
    args = parser.parse_args()
    return args.__dict__
