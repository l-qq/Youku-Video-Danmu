# Youku Video Danmu

### 使用说明：

1. 运行`get_vurls.py`生成视频地址

2. 使用`you-get`下载视频

3. 运行`get_vdanmu_xml.py`生成弹幕XML

4. 使用[bilibili ASS 弹幕在线转换](https://tiansh.github.io/us-danmaku/bilibili/)或[danmaku-to-ass](https://github.com/otakustay/danmaku-to-ass)转换成ASS

   > danmaku-to-ass安装使用参考：
   >
   > https://www.npmjs.com/package/node-gyp
   >
   > https://github.com/Automattic/node-canvas/wiki/Installation---Windows
   >
   > http://cnodejs.org/topic/505080cb5aa28e09430d89b0
   >
   > `(for %i in (*.xml) do @echo danmaku --font-size=18,25,36 --out-dir=../ASS ./"%i") > mylist.txt`

5. 运行`use_ffmpeg.py`生成批处理命令，无损封装`ffmpeg -i input.mp4 -i input.ass -c copy output.mkv`

   > `for %i in (*.mp4) do ffmpeg -i "%i" -c copy "%~ni.flv"`
   >
   > `(for %i in (*.mp4) do @echo ffmpeg -i "%i" -i "%~ni.ass" -c copy "%~ni.mkv") > mylist.txt`


