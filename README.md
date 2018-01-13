
## 西瓜视频百万英雄助手

参考了微信跳一跳助手的思路，通过截取手机上面的题目识别问题和答案。
支持使用[汉王云 OCR ](https://market.aliyun.com/products/57124001/cmapi011523.html?spm=5176.730005.0.0.B1mZNd#sku=yuncode552300000)和[百度文字识别](https://cloud.baidu.com/product/ocr/general)。


移动端支持 Android / IOS 手机，程序运行时间是3秒左右（答题是10秒）。

# 只有 IPHONE, 没有 android 手机怎么办？

其中一种方法是你可以使用 `ios` 分支，更加简单和靠谱的办法是使用模拟器。

1. 首先还是要下载adb工具，下文有介绍
2. 下载[夜神](https://www.yeshen.com/)模拟器并安装
3. 安装完成后，打开 cmd, 检查是否有模拟器设备 `adb devices`
4. 在模拟器中安装答题应用
5. 运行答题辅助脚本`python main.py`,如果有问题下文有解决办法，请参照安装步骤

## **支持捐赠**

- [微信入口](./wechatcode/wechatpay.png)
- [支付宝](./wechatcode/alipay.png)

捐赠后请给我留言，如下福利：

- 项目结束后，整体讲解
- 免安装版提供支持，目前开发中
- 无责任辅助安装包



## Release

>- 2018/1/12: 更改搜索策略，自动决策，减少python依赖
>- 2018/1/11: 结巴分词预编译和多核分词优化
>- 2018/1/10： 增加ios分支，修复master文本摘要bug
>- 2018/1/9： 修复答案获取bug，增加长文本信息摘要算法，增加百度OCR
>- 2018/1/9： 使用相似度猜测答案，请切换分支使用

## 运行

![](./wechatcode/run-1.png)
![](./wechatcode/run-2.png)
![](./wechatcode/run-3.png)
![](./wechatcode/run-4.png)

## 汉王OCR 百度OCR

**notice**: 第一次使用汉王阿里云只需要0.01元／100条，所以如果没有了，可以自己注册阿里云账号购买（[汉王](https://market.aliyun.com/products/57124001/cmapi011523.html?spm=5176.10695662.1996646101.searchclickresult.2d006e393rEVI7#sku=yuncode552300000)）。百度的注册开发者后创建应用就可以看见自己的 key 和 secret 。

## 分支说明

- master: 主要是 Android 手机使用，支持汉王 / 百度识别 / ocrspace
- knearby: 根据文本关联度思想，答案更加清晰，目前只支持百度识别
- iso: 主要是苹果手机使用，支持百度和汉王 

## V2 文本关联相似度分析

对于答题这样的项目，首先一个问题，然后有三个答案可以选择，能不能通过分别统计问题与三个答案的关联度来选择出正确的答案，由于数据采集是来自百度的，可能会受到部分广告数据的影响，但是在集合相当大的情况下，关联度还是会呈现正相关。

假设题目是： 

*中国历史上著名的科举制度开始于那个朝代？*
- 汉朝
- 唐朝
- 隋朝

我们先用百度分别搜索`汉朝`，`唐朝`，`隋朝`，得到如下数据：

朝代 | 搜索出的数量（来自百度为您找到相关结果约）
---- | ------------------------------------------
汉朝 | 17900000
唐朝 | 30500000
隋朝 | 16600000

然后我们在用`题目` + 答案的方式，搜索示例：

`中国历史上著名的科举制度开始于那个朝代？ 汉朝` 得到三次的搜索结果：

 关键字  | 搜索出的数量（来自百度为您找到相关结果约）
-------- | ------------------------------------------
Q + 汉朝 | 602000
Q + 唐朝 | 837000
Q + 隋朝 | 658000

关联度计算方式：

``` shell
K = count(Q&A) / (count(Q) * count(A))
```

关联度如下：

答案 | 关联度
---- | ------
汉朝 | 0.0336
唐朝 | 0.0274
隋朝 | 0.0396


## 部署

1. 从python官网安装python3.6环境
2. pip install -r requirements.txt
3. 创建默认的临时文件夹mkdir -p screenshots
4. 修改默认的配置文件`config.py`,配置文件夹中可以配置临时数据目录和appcode


## ADB工具配置

以 linux 为例：

1. 下载 android-platform-tools，访问[google](https://developer.android.google.cn/studio/releases/platform-tools.html)下载，默认 mac，windows， linux 均支持
2. 配置环境变量，进入 platform 目录下面`export PATH=$(pwd):PATH`配置 adb 工具到系统的 path 下面
3. 手机打开开发者模式
4. 使用usb连接手机后信任，`adb devices`来检查是否有自己的设备，确认已经连接
5. 接下来就进入百万英雄，等待有题目的时候就运行`python main.py`即可


## 贡献者（不分先后）

- [uniqhj](https://github.com/UniqHu)
- wangfpp
- [using1174](https://github.com/Using1174)
- [kakalote2008	](https://github.com/kakalote2008)
- [lonelam](https://github.com/lonelam)
- [sjm1992st](https://github.com/sjm1992st)

## 参考项目

- [wuditken/MillionHeroes](https://github.com/wuditken/MillionHeroes)
- [lingfengsan/MillionHero](https://github.com/lingfengsan/MillionHero)
- [SnakeHacker/QA-Snake](https://github.com/SnakeHacker/QA-Snake)

## 交流学习

想要交流学习请添加我的 wechat ,
群已经满了200人了，需要邀请进群。
请优先加入qq群，很重要的改进可以加weixin:

![](./wechatcode/qqcode.png)

请加wexin后邀请：

![](./wechatcode/wechat-1.png)

qq: 294101042
