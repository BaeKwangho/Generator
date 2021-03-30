import random
import copy
import PIL.Image as Image

def gen_box(dataloader,rects):
    
    text_list,palette = dataloader.use_set()
    palette = copy.deepcopy(palette)

    sentences = []
    for layout in rects:
        start_x = layout['x1']
        start_y = layout['y1']
        end_x = layout['x2']
        end_y = layout['y2']

        switch = 1
        while switch:
            sen_x = start_x
            sen_text = str()
            word = []
            for _ in range(len(text_list)):
                text = random.choice(text_list)
                if (end_x-start_x) >= text['width']:
                    text_img = Image.open(text['path'])
                    text_img.save('/root/storage/Experiments/vision/Generator/asset/text/out/test.png')
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