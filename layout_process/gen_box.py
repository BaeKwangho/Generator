import random
import copy
import PIL.Image as Image
from trdg.generators import GeneratorFromStrings

def gen_box(dataloader,rects,count=40):
    
    text_list,palette = dataloader.use_set()
    palette = copy.deepcopy(palette)

    sentences = []
    for layout in rects:
        start_x = layout['x1']
        start_y = layout['y1']
        end_x = layout['x2']
        end_y = layout['y2']
    
    
        trial=0
        while True:
            trial+=1
            sen_x = start_x
            sen_text = str()
            word = []
            #print(f'gen_trial : {trial}')
            
            #if gen_mode is true
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
                    if (end_x-start_x) >= text_img.width:
                        palette.paste(text_img,(start_x,start_y))
                        start_x += text_img.width+default_space
                        sen_text += text
                        word_dict = {
                                    'box':{
                                        'x1':start_x-text_img.width,
                                        'x2':start_x,
                                        'y1':start_y,
                                        'y2':start_y + 32,
                                    },
                                    'word':text
                                }
                        word.append(word_dict)
            # if gen_mode is false use default dict shape dataset
            else:
                for _ in range(len(text_list)):
                    text = random.choice(text_list)
                    if (end_x-start_x) >= text['width']:
                        text_img = Image.open(text['path'])
                        palette.paste(text_img,(start_x,start_y))
                        start_x += text['width']
                        sen_text += text['text']
                        word_dict = {
                                'box':{
                                    'x1':start_x-text['width'],
                                    'x2':start_x,
                                    'y1':start_y,
                                    'y2':start_y + 32,
                                },
                                'word':text['text']
                            }
                        word.append(word_dict)

            sen_dict = {
                'box':{
                    'x1':layout['x1'],
                    'x2':start_x,
                    'y1':start_y,
                    'y2':start_y + 32
                },
                'sentence':sen_text,
                'words':word
            }     
            start_x = layout['x1']
            #need to specify
            start_y += 32

            sentences.append(sen_dict)
            #add sentence box


            sen_y = start_y
            if start_y>end_y:
                break

    return sentences, palette