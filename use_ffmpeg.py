#基于python 3
import os

s = set()
#获取当前目录下所有文件及文件夹名称
dirs = os.listdir('D:\\NARUTO -ナルト- 疾風伝')
#存入集合
for file in dirs:
   s.add(file[0:-3])
#集合set排序
l = list(s)
l.sort()
#生成.bat文件内容
print("生成的bat文件内容：..........................")
for file in l:
    print("ffmpeg -i \"" + file + "mp4\"" + " -i \"" + file + "ass\"" + " -c copy \"" + file + "mkv\"")
    # print("del \"" + file + "mp4\" \"" + file + "ass\"")