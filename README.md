## 西瓜视频百万英雄助手

本文的所有答案均来自百度知道的搜索，根据前两个投票最高的答案来，目前已经去除了广告，目前只支持android手机，程序运行时间是3秒左右（答题是10秒）。

本软件使用了`汉王云ocr`API，参考了[wuditken/MillionHeroes
](https://github.com/wuditken/MillionHeroes)项目，目前主要改进了广告和配置问题，提供免费的云api，不需要用户自己注册[汉王api](https://market.aliyun.com/products/57124001/cmapi011523.html?spm=5176.730005.0.0.B1mZNd#sku=yuncode552300000)，如果发现不可用请扫描二维码联系。

## 汉王OCR APPCode

**notice**: 第一次使用汉王阿里云只需要0.01元／100条，所以如果没有了，可以自己注册阿里云账号购买（[汉王](https://market.aliyun.com/products/57124001/cmapi011523.html?spm=5176.10695662.1996646101.searchclickresult.2d006e393rEVI7#sku=yuncode552300000)）。
- ~~714501eede0b4ac9a75a11af64b3b4d7~~

## release

- 20179/1/9: baiduzhi.com 答案获取bug，增加长文本信息摘要算法，增加免费的百度ocr

## 部署

1. 从python官网安装python3.6环境
2. pip install -r requirements.txt
3. 创建默认的临时文件夹mkdir -p screenshots
4. 修改默认的配置文件`config.py`,配置文件夹中可以配置临时数据目录和appcode


## ADB工具配置

以linux 为例：

1. 下载android-platform-tools,访问[google](https://developer.android.google.cn/studio/releases/platform-tools.html)下载，默认mac,windows,linux均支持
2. 配置环境变量，进入platform目录下面`export PATH=$(pwd):PATH`配置adb工具到系统的path下面
3. 手机打开开发者模式
4. 使用usb连接手机后信任，`adb devices`来检查是否有自己的设备，确认已经连接
5. 接下来就进入百万英雄，等待有题目的时候就运行`python main.py`即可

## 交流学习

想要交流学习或者联系充值汉王OCR的请扫描二维码联系(有效期7日)

![](./wechatcode/wechat.png)

qq: 294101042
