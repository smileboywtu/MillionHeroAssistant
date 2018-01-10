# -*- coding:utf-8 -*-


data_directory = "screenshots"

default_answer_number = 2

### ocr config
hanwan_appcode = "714501eede0b4ac9a75a11af64b3b4d7"

### baidu orc
app_id = "10661627"
app_key = "h5xcL0m4TB8fiiFWoysn7uxt"
app_secret = " HGA1cgXzz80douKQUpII7K77TYWSGcfW"

### 如果你想要使用汉王的话，将汉王移动到前面，默认使用百度，每天封顶500次
prefer = ("baidu", "hanwang")

text_summary = True

### 1代表灰度处理， 2代表二值化处理，如果需要使用二值化，需要将2放到前面
image_compress_level = (1, 2)

summary_sentence_count = 3
