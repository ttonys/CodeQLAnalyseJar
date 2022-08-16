import argparse


def parse():
    usage = "CodeQL Analysis Jar[options]"
    parser = argparse.ArgumentParser(prog='CodeQLAnalysisJar', usage=usage)
    parser.add_argument('-jar', dest='jar_path', action='store', required=True,
                        help='指定jar包路径')
    parser.add_argument('-out', dest='out_path', action='store', required=True,
                        help='指定输出文件路径')

    args = parser.parse_args()
    return args.__dict__
