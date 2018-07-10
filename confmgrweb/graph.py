# -*- coding:utf8 -*-
import confmgrweb.devicebase as devicebase
import IPy
import networkx
import matplotlib.pylab as plt


def isozmbiepolicy(checkfirewall,netaddrlist):
    print('begin' + checkfirewall.name + 'policycheck')
    print(checkfirewall.name + '######---独立存在的策略---######')
    # 遍历需要检测防火墙的原子策略表
    for checkpoliy in checkfirewall.policymiclist:
        issrcport = 0
        isdstport = 0
        # 不对未初始化的安全域策略检查
        for port in checkfirewall.portlink:
            if checkpoliy.srceth in port:
                issrcport = 1
            if checkpoliy.dsteth in port:
                isdstport = 1
        if issrcport == 0 or isdstport == 0:
            continue
        # 根据策略的源地址和目的地址 匹配拓扑网络区域地址
        for i in netaddrlist:
            if 1 == IPy.IP(i.netaddr).overlaps(checkpoliy.dstaddr):
                dstnet = i
                break
        for i in netaddrlist:
            if 1 == IPy.IP(i.netaddr).overlaps(checkpoliy.srcaddr):
                srcnet = i
                break
        # 根据策略的源区域和目的区域 确认策略路径 生成路径设备列表
        routelist = networkx.shortest_path(topology, source=srcnet, target=dstnet)
        iscontent = 0
        # 遍历路径设备列表
        for i in range(len(routelist)):
            # 设备与策略主机一致跳过
            if routelist[i] == firewall:
                pass
            # 如设备类型为防火墙
            elif routelist[i].type == 'firewall':
                # 根据上下游设备 确定检测策略经过本机的安全域或端口
                srceth = ''
                dsteth = ''
                for port in routelist[i].portlink:
                    if routelist[i - 1].name in port:
                        srceth = port.split('-')[0]
                    if routelist[i + 1].name in port:
                        dsteth = port.split('-')[0]
                # 遍历主机原子策略表，与经过的安全域策略比较是否有相应的策略
                for j in routelist[i].policymiclist:
                    if j.srceth == srceth and j.dsteth == dsteth:
                        iscontent = 1
                        if IPy.IP(checkpoliy.srcaddr).overlaps(j.srcaddr) == 1 or IPy.IP(j.srcaddr).overlaps(
                                checkpoliy.srcaddr) == 1:
                            if IPy.IP(checkpoliy.dstaddr).overlaps(j.dstaddr) == 1 or IPy.IP(j.dstaddr).overlaps(
                                    checkpoliy.dstaddr) == 1:
                                if checkpoliy.service == 'any' or j.service == 'any':
                                    # print("--------------------------------------------------------------")
                                    # checkpoliy.printpolicymic()
                                    # j.printpolicymic()
                                    iscontent = 2
                                    break
                                elif checkpoliy.service == j.service:
                                    # print("--------------------------------------------------------------")
                                    # checkpoliy.printpolicymic()
                                    # j.printpolicymic()
                                    iscontent = 2
                                    break
                # 标识  表示 1= 相关安全域策略未匹配 2= 匹配（存在相对应的策略）
                if iscontent == 1:
                    checkpoliy.printpolicymic()


def searchpolicy(topology,netaddrlist,srcaddr, dstaddr, service):
    searchpolicydic= {}
    dstnet = ""
    srcnet = ""

    for i in netaddrlist:
        if 1 == IPy.IP(i.netaddr).overlaps(dstaddr):
            dstnet = i
            break
    for i in netaddrlist:
        if 1 == IPy.IP(i.netaddr).overlaps(srcaddr):
            srcnet = i
            break
    # 根据策略的源区域和目的区域 确认策略路径 生成路径设备列表
    routelist = networkx.shortest_path(topology, source=srcnet, target=dstnet)
    # 遍历路径设备列表
    for i in range(len(routelist)):
        searchpolicylist = []
        if routelist[i].type == 'firewall':
            # 根据上下游设备 确定检测策略经过本机的安全域或端口
            srceth = ''
            dsteth = ''
            for port in routelist[i].portlink:
                if routelist[i - 1].name in port:
                    srceth = port.split('-')[0]
                if routelist[i + 1].name in port:
                    dsteth = port.split('-')[0]
            # 遍历主机原子策略表，与经过的安全域策略比较是否有相应的策略
            for j in routelist[i].policymiclist:
                if j.srceth == srceth and j.dsteth == dsteth:
                    if IPy.IP(srcaddr).overlaps(j.srcaddr) == 1 or IPy.IP(j.srcaddr).overlaps(
                            srcaddr) == 1:
                        if IPy.IP(dstaddr).overlaps(j.dstaddr) == 1 or IPy.IP(j.dstaddr).overlaps(
                                dstaddr) == 1:
                            if service == 'any' or j.service == 'any':
                                # print("--------------------------------------------------------------")
                                # checkpoliy.printpolicymic()
                                searchpolicylist.append(j)
                            elif service == j.service:
                                # print("--------------------------------------------------------------")
                                # checkpoliy.printpolicymic()
                                searchpolicylist.append(j)
        searchpolicydic.update({routelist[i].name:searchpolicylist})
    return searchpolicydic
