# PIMGenerator

* thanks to https://github.com/Belval/TextRecognitionDataGenerator

개발단계입니다.

---

## Requirement

* trdg
* PIL.Image

## Run
* ```python run.py```
* ```python run.py -t ./sample_text_imgs``` (if you have text image files with trdg)

## Image file dir
* You need to fill follow directory with image files.
    - ```smaple_text_imgs/data``` : text images using [text generator](https://github.com/Belval/TextRecognitionDataGenerator)
    - ```layout_process/contents_img``` (unconditionally) : ```original_background``` images in [DDI-100 dataset](https://github.com/machine-intelligence-laboratory/DDI-100) (+ We use image crop, but there is no image crop code here.) (Or any image you need)
