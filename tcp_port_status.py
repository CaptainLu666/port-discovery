#!/usr/bin/env python
# encoding: utf-8
import commands
import re

##########返回命令执行结果
def getComStr(comand):
    try:
        stat, proStr = commands.getstatusoutput(comand)
    except:
        print "command %s execute failed, exit" % comand
    #将字符串转化成列表
    #proList = proStr.split("\n")
    return proStr

##########获取系统服务名称和监听端口
def filterList():
    tmpStr = getComStr("ss -lnt")
    tmpList = tmpStr.split("\n")
    #删除前面两行
    del tmpList[0]
    newList = []
    for i in tmpList:
        val = i.split()
        del val[0:3]
        #提取端口号
        valTmp = val[0].split(":")
        val[0] = valTmp[-1]
        newList.append(val[0])
    portList = list(set(newList))
    portList.sort(key=newList.index)
    return portList

def main():
    netInfo = filterList()
    #格式化成适合zabbix lld的json数据
    json_data = "{\n" + "\t" + '"data":[' + "\n"
    #print netInfo
    for net in netInfo:
        if net != netInfo[-1]:
            json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#PORT}":"' + str(net) + "\"},\n"
        else:
            json_data = json_data + "\t\t" + "{" + "\n" + "\t\t\t" + '"{#PORT}":"' + str(net) + "\"}]}"
    print json_data

if __name__ == "__main__":
    main()
