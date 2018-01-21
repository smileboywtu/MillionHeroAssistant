# -*- coding:utf-8 -*-


import yaml

with open("config.yaml", "rb") as reader:
    config = yaml.safe_load(reader.read())

    data_directory = config["data_directory"]

    ### 1代表灰度处理， 2代表二值化处理，如果需要使用二值化，需要将2放到前面, 0不使用
    image_compress_level = config["image_compress_level"]

    ### 0 表示普通识别，配合compress_level 1使用
    ### 1 标识精确识别，精确识别建议配合image_compress_level 2使用
    api_version = config["api_version"]

    ## 图像比例裁剪区域, (left, top, right, bottom)
    ## 最终裁剪区域可表示为 (image_width * left, image_height * top, image_width * right, image_height * bottom)
    crop_areas = config["crop_areas"]

    ### baidu orc
    app_id = config["app_id"]
    app_key = config["app_key"]
    app_secret = config["app_secret"]

    ### ocr.space
    api_key = config["api_key"]

    ### 默认使用百度，每天封顶500次
    ### 如果你想要使用ocr.space的话，将ocrspace移动到前面,每个api_key每月支持25000次调用
    prefer = config["prefer"]

    ### enable chrome
    enable_chrome = config["enable_chrome"]

    ### 是否使用夜神模拟器
    use_monitor = config["use_monitor"]

    ### 是否图片缩放
    enable_scale = config["enable_scale"]