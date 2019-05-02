# id3_tag_downloader

This tool is used for adding ID3 tags to mp3 files from netease cloud music according to music ID.

这个工具用于根据音乐 ID 为来自网易云音乐的 mp3 文件自动添加 ID3 tag （包含封面）。

**IMPORTANT NOTE**: 本工具需要配合 [More Sound 魔声](http://moresound.tk) 使用.

开发初衷是针对网易云音乐，目前并没有找到一个非常完美的既能下载 **所有** 高品质音乐，同时还能添加好 ID3 信息的工具。[More Sound 魔声](http://moresound.tk) 提供了非常强大的下载服务，但是得到的音频文件既没有可读的文件名，也没有 ID3 信息（自动改名虽然能保证文件名可读，但还是缺少 ID3 信息）。本工具配合 [More Sound 魔声](http://moresound.tk) ，可以获得“完美”的 mp3 文件。

## 使用步骤

1. 新建一个网易云音乐歌单（或者使用已有歌单），添加所有希望下载的音乐。
2. 前往 [More Sound 魔声](http://moresound.tk) ，先在右下角切换到 `手动改名` 模式，然后左上角将搜索模式设置为 `网易云批量`，填入账号 ID 搜索, 打开需要下载的歌单。
3. 在歌单界面，点击 `批量获取链接`，再选择需要的音质（目前只支持 mp3），弹出下载地址列表。
4. **【重要】** 复制列表中所有链接地址，保存为 `url_list.txt`, 放置在下载目录中。
5. **【重要】** 使用下载工具批量下载所有音频文件，注意保持文件名不变。比如对于地址：

   > http://m10.music.126.net/20190502105454/644187324c19b54c6266783f8ef451b3/ymusic/b9dc/f825/7b56/547ee7fa34594054111a87c5931e0986.mp3?&suffix=mp3&id=39311959

   文件名应当为 `547ee7fa34594054111a87c5931e0986.mp3`.

   （我在实际操作中发现 IDM 对个别文件命名不正确，可能会多加前面的部分（ `/` 替换为 `_` ），变成 `b9dc_f825_7b56_547ee7fa34594054111a87c5931e0986.mp3`. 遇到这种情况请见[下一部分](#1)。

6. 运行本工具，将自动下载并添加 ID3 信息。具体用法：

   On Windows:

   ```
   python main.py -d DIRECTORY
   ```

   On Linux / Mac OS:

   ```
   python3 main.py -d DIRECTORY
   ```

   `DIRECTORY` 是你的下载目录。

   任务完成后，工具会在该目录下输出 `id3_tag_downloader.log`, 内含经修改的 mp3 文件的 Music ID 和新文件名。

<span id="1"></span>

## 文件名含有 `/` 前部分的处理

在运行工具前，拷贝本项目中的 `remove_prefix.py` 到下载目录，执行一次后删除。

## 致谢

- 本项目的 API 部分参考了 [codezjx](https://github.com/codezjx) 的项目 [netease-cloud-music-dl](https://github.com/codezjx/netease-cloud-music-dl).
- [More Sound 魔声](http://moresound.tk)

## License

[The MIT License](LICENSE).
