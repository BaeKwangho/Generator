import PIL.Image as Image
import os

class DataLoader(object):
    def __init__(self, text_dir, bg_file):
        if text_dir==None:
            self.gen_mode = True
            with open('./asset/dict/ko_word.txt','r') as f:
                self.text_list = f.readlines()
            self.bg_file = self.prepare_bg(bg_file)
        else:
            self.gen_mode = False
            self.text_list = self.prepare_text(text_dir)
            self.bg_file = self.prepare_bg(bg_file)

    def prepare_text(self,text_dir):
        text_list = []
        for i,text in enumerate(os.listdir(text_dir)):
            text_img_path = os.path.join(text_dir,text)
            if os.path.isdir(text_img_path):
                continue
            text_img = Image.open(text_img_path)
            word = text.split('.')[0].split('_')[0].replace(' ','')
            cache = {
                'path':text_img_path,
                'text':word,
                'width':text_img.width,
                'height':text_img.height,
            }
            text_list.append(cache)
        return text_list
    
    def prepare_bg(self,bg_file):
        return Image.open(bg_file)
    
    def use_set(self):
        return self.text_list, self.bg_file