# python3 coding:utf-8
# 生成视频弹幕XML文件
import urllib.request
import re
import json
import os.path
import random

# root_url = "http://www.soku.com/search_video/q_%E7%81%AB%E5%BD%B1"
#抓取火影241-320集网页源代码中的视频ID信息
with open("./videos_source.html", "r", encoding="utf-8") as fin:
    data = fin.read()
results = re.findall("id_.*html", data)

"""
抓取对应URL中视频的弹幕json数据
弹幕请求地址示例 https://service.danmu.youku.com/list?mat=6&mcount=1&ct=1001&iid=132171946
个人的猜想：参数mat为视频弹幕的分片数，一集火影估计最大25左右
            参数mcount为每次分片弹幕可以取到的最大弹幕数量，测试发现最大取值为5，即可以取到5*360=1800条弹幕
            参数ct为弹幕样式，有3002,3001,4002,7002，1001等
            参数iid为视频ID，即视频网页源代码中的videoId
"""
for i in results:
    flag = False    #标志此次弹幕信息抓取是否成功
    while not flag:
        try:
            url = "https://v.youku.com/v_show/" + i
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
            response = urllib.request.urlopen(req)
            res = response.read().decode("utf-8")
            titles = re.findall("<title>.*</title>", res)
            print(titles)
            title = titles[0][7:-36]
            iids = re.findall(" videoId: \&#39;\d*\&", res)
            print(iids)
            iid = iids[0][15:-1]
            #根据获取到的视频ID请求弹幕json
            filename = "./XML/" + title + ".xml"
            if os.path.exists(filename):
                print("已经存在xml文件......Skipping......")
            else:
                with open(filename, "w", encoding='utf-8') as fout:
                    fout.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    fout.write('<i>\n')
                    for mat in range(26):
                        req = urllib.request.Request("https://service.danmu.youku.com/list?mat=" + str(mat) + "&mcount=1&ct=1001&iid=" + iid)
                        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
                        response = urllib.request.urlopen(req)
                        print("\t" + "https://service.danmu.youku.com/list?mat=" + str(mat) + "&mcount=1&ct=1001&iid=" + iid)
                        danmu = json.loads(response.read().decode("utf-8"))
                        # print(type(danmu))
                        # print(json.dumps(danmu, sort_keys=True, indent=2))
                        """
                        开始将弹幕字典数据生成类似B站的.xml文件
                        // Bilibili的弹幕XML结构如下：
                        //
                        // ```xml
                        // <?xml version="1.0" encoding="UTF-8"?>
                        // <i>
                        //     <chatserver>chat.bilibili.com</chatserver>
                        //     <chatid>747601</chatid>
                        //     <mission>0</mission>
                        //     <maxlimit>3000</maxlimit>
                        //     <max_count>3000</max_count>
                        //     <d p="42.442,4,25,65280,1430559225,0,ff5d0daf,886337510">WTF?</d>
                        //     ...
                        // </i>
                        // ```
                        //
                        // 其中每个`<d>`节点是一条弹幕，`p`属性是弹幕的信息，节点内容是弹幕的内容。`p`属性以逗号分隔分别为以下属性：
                        //
                        // 1. 弹幕发送时间，相对于视频开始时间，以秒为单位
                        // 2. 弹幕类型，1-3为滚动弹幕、4为底部、5为顶端、6为逆向、7为精确、8为高级
                        // 3. 字体大小，25为中，18为小，当前Bilibili只有这2个字号
                        // 4. 弹幕颜色，RGB颜色转为十进制后的值
                        // 5. 弹幕发送时间
                        // 6. 弹幕池，0为普通，1为字幕，2为特殊
                        // 7. 发送人的cid
                        // 8. 弹幕id
                        //
                        // 转换时只需要使用前4项即可
                        """
                        print("\t\tjson-info//count:" + str(danmu["count"]) + "    filtered:" + str(danmu["filtered"]) + "    result:" + str(len(danmu["result"])))
                        for i in range(len(danmu["result"])):
                            illegal = False #标志是否有非法XML字符
                            for char in ["<", ">", "&", "\u0000"]:
                                if char in danmu["result"][i]["content"]:
                                    illegal = True
                                    break
                            if illegal:
                                continue
                            playat = danmu["result"][i]["playat"]/1000  #弹幕发送时间
                            ct = random.randint(1, 5)   #弹幕样式
                            size = random.randint(11, 17)   #字体大小
                            # 获取颜色
                            if "color" in danmu["result"][i]["propertis"]:
                                propertis = json.loads(danmu["result"][i]["propertis"])
                                color = propertis["color"]
                            else:
                                color = 16777215
                            content = danmu["result"][i]["content"] #弹幕内容
                            fout.write('<d p="' + str(playat) + ',' + str(ct) +',' + str(size) + ',' + str(color) + '">' + content + '</d>\n')
                    fout.write('</i>')
            flag = True #抓取成功
        except:
            print("！！！Error：正在尝试重连......")