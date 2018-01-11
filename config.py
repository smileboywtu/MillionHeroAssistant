# -*- coding:utf-8 -*-


data_directory = "screenshots"

### 1代表灰度处理， 2代表二值化处理，如果需要使用二值化，需要将2放到前面, 0不使用
image_compress_level = (1, 1, 2)

### 0 表示普通识别，配合compress_level 1使用
### 1 标识精确识别，精确识别建议配合image_compress_level 2使用
api_version = (0, 1)

## 设置baidu ocr
app_id = "10661627"
app_key = "h5xcL0m4TB8fiiFWoysn7uxt"
app_secret = "HGA1cgXzz80douKQUpII7K77TYWSGcfW"
