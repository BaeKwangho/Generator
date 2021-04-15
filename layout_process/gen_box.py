# -*- coding: utf-8 -*-
import random
import copy
import PIL.Image as Image
import os
from trdg.generators import GeneratorFromStrings

def gen_box(dataloader, rects, title, count=40, contents_img_path="layout_process/contents_img"):
    text_list, palette = dataloader.use_set()
    palette = copy.deepcopy(palette)
    sentences = []
    
    # 제목 먼저 체크
    if(title is not None):
        # title이 만들어졌다면
        start_x = title['x1']
        start_y = title['y1']
        end_x = title['x2']
        end_y = title['y2']
        
        word = []
        sen_text = str()
        while(start_y <= end_y):
            if dataloader.gen_mode == True:
                default_space=5
                generator = GeneratorFromStrings(
                                [random.choice(text_list).replace('\n','') for _ in range(count)],
                                 blur=0,
                                 count=count,
                                 background_type=0,
                                 margins=(5, 5, 5, 5),
                                 language='ko',
                                 fonts=['../asset/fonts/ko/NanumBarunGothicUltraLight.ttf'],
                                 random_blur=False
                               )
                for text_img, text in generator:
                    if (end_x - start_x) >= text_img.width:
                        palette.paste(text_img, (start_x, start_y))
                        start_x += text_img.width + default_space
                        sen_text += text
                        word_dict = {
                                        'box' : {
                                            'x1' : start_x - text_img.width,
                                            'x2' : start_x,
                                            'y1' : start_y,
                                            'y2' : start_y + 32,
                                     },
                                     'word':text
                                 }
                        word.append(word_dict)
            else:
                for _ in range(len(text_list)):
                    text = random.choice(text_list)
                    if (end_x - start_x) >= text['width']:
                        text_img = Image.open(text['path'])
                        palette.paste(text_img, (start_x, start_y))
                        start_x += text['width']
                        sen_text += text['text']
                        word_dict = {
                                     'box':{
                                          'x1':start_x - text['width'],
                                          'x2':start_x,
                                          'y1':start_y,
                                          'y2':start_y + 32,
                                      },
                                      'word':text['text']
                                 }
                        word.append(word_dict)
            sen_dict = {
                    'box':{
                        'x1' : title['x1'],
                        'x2' : start_x,
                        'y1' : start_y,
                        'y2' : start_y + 32
                    },
                    'sentence' : sen_text,
                    'words' : word
            }     
            start_x = title['x1']
            #need to specify
            start_y += 32

            sentences.append(sen_dict)
            #add sentence box

            sen_y = start_y
                        
                        
    for layout in rects:
        start_x = layout['x1']
        start_y = layout['y1']
        end_x = layout['x2']
        end_y = layout['y2']
    
        # 문단에 글 대신 이미지도 넣기
        isImg = random.randint(6)
        if(isImg == 3):
            img_list = [files for files in os.listdir(contents_img_path) if ".png" in files] # 사진 파일들만 모으기
            img_name = random.choice(img_list)
            img_path = os.path.join(contents_img_path, img_name)
            
            contents_img = Image.open(img_path) # 랜덤 이미지 오픈
            contents_img = contents_img.resize((end_x - start_x, end_y - start_y)) # 문단 크기로 이미지 리사이즈
            palette.paste(contents_img, (start_x, start_y))
        
            continue # 이미지 넣었으면 그 문단은 패스
        
        # 여기서부터 텍스트 이미지
        trial = 0
        while True:
            trial += 1
            sen_x = start_x
            sen_text = str()
            word = []
            #print(f'gen_trial : {trial}')
            
            #if gen_mode is true
            if dataloader.gen_mode == True:
                word = []
                default_space=5
                generator = GeneratorFromStrings(
                                [random.choice(text_list).replace('\n','') for _ in range(count)],
                                blur=0,
                                count=count,
                                background_type=0,
                                margins=(5, 5, 5, 5),
                                language='ko',
                                fonts=['../asset/fonts/ko/NanumBarunGothicUltraLight.ttf'],
                                random_blur=False
                            )
                for text_img, text in generator:
                    if (end_x - start_x) >= text_img.width:
                        palette.paste(text_img, (start_x, start_y))
                        start_x += text_img.width + default_space
                        sen_text += text
                        word_dict = {
                                    'box' : {
                                        'x1' : start_x - text_img.width,
                                        'x2' : start_x,
                                        'y1' : start_y,
                                        'y2' : start_y + 32,
                                    },
                                    'word':text
                                }
                        word.append(word_dict)
            # if gen_mode is false use default dict shape dataset
            else:
                for _ in range(len(text_list)):
                    text = random.choice(text_list)
                    if (end_x - start_x) >= text['width']:
                        text_img = Image.open(text['path'])
                        palette.paste(text_img, (start_x, start_y))
                        start_x += text['width']
                        sen_text += text['text']
                        word_dict = {
                                    'box':{
                                        'x1':start_x - text['width'],
                                        'x2':start_x,
                                        'y1':start_y,
                                        'y2':start_y + 32,
                                    },
                                    'word':text['text']
                                }
                        word.append(word_dict)
            sen_dict = {
                'box':{
                    'x1' : layout['x1'],
                    'x2' : start_x,
                    'y1' : start_y,
                    'y2' : start_y + 32
                },
                'sentence' : sen_text,
                'words' : word
            }     
            start_x = layout['x1']
            #need to specify
            start_y += 32

            sentences.append(sen_dict)
            #add sentence box


            sen_y = start_y
            if start_y > end_y:
                break

    return sentences, palette
