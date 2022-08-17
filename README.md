## Info

反编译Jar包脚本，基于Apache Ant构建CodeQL数据库

## Todo

- [x] 反编译jar文件
- [x] 构造build.xml文件
- [ ] 自动优化编译失败文件

## Usage
```
(CodeQLAnalysisJar) ➜  CodeQLAnalysisJar python main.py -h
usage: CodeQL Analysis Jar[options]

optional arguments:
  -h, --help           show this help message and exit
  -jar JAR_PATH        指定jar包路径
  -out OUT_PATH        指定输出文件路径
  -tomcat TOMCAT_PATH  引入tomcat相关jar, 如:/usr/local/apache-tomcat-8.5.75, default: false
  -xml                 自动生成build.xml文件, default: false
```

所需工具：

- Python3

- Java:1.8
- Ant:https://ant.apache.org/

使用：

1、反编译jar包，生成ant配置文件

```shell
python main.py -jar java-sec.jar -out java-sec-decompile -tomcat /usr/local/apache-tomcat-8.5.75 -xml
```

2、进入生成目录，执行`ant -f build.xml`，仅测试，可跳过

3、构建codeql数据库

```shell
codeql database create tmp-database --language=java --command="ant -f build.xml" --source-root ./
```

