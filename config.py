# -*- coding:utf-8 -*-


data_directory = "screenshots"

### 默认百万，冲顶请调整为"cd"
screen_corp_mode = "bw"

### 1代表灰度处理， 2代表二值化处理，如果需要使用二值化，需要将2放到前面, 0不使用
image_compress_level = (1, 0, 2)

### 0 表示普通识别，配合compress_level 1使用
### 1 标识精确识别，精确识别建议配合image_compress_level 2使用
api_version = (0, 1)


### baidu orc
app_id = "10661627"
app_key = "h5xcL0m4TB8fiiFWoysn7uxt"
app_secret = "HGA1cgXzz80douKQUpII7K77TYWSGcfW"

### ocr.space
api_key = "6c851da45688957"

### 默认使用百度，每天封顶500次
### 如果你想要使用ocr.space的话，将ocrspace移动到前面,每个api_key每月支持25000次调用
prefer = ("baidu",  "ocrspace")

### enable chrome
enable_chrome = True
