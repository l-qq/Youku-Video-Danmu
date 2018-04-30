# python3 coding:utf-8
# 抓取视频URL
import re

# root_url = "http://www.soku.com/search_video/q_%E7%81%AB%E5%BD%B1"
#抓取火影241-320集网页源代码中的视频ID信息
with open("./videos_source.html", "r", encoding="utf-8") as fin:
    data = fin.read()
results = re.findall("id_.*html", data)

with open("./videos_urls_out.html", "w", encoding='utf-8') as fout:
    fout.write("<html>")
    fout.write("<body>")
    fout.write("<table>")
    for i in results:
        i = "https://v.youku.com/v_show/" + i
        fout.write("<tr>")
        fout.write("<td><a href=%s>%s</a></td>"%(i,i))
        fout.write("</tr>")
    fout.write("</table>")
    fout.write("</body>")
    fout.write("</html>")