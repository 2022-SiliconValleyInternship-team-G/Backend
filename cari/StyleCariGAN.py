import os
import shutil
from PIL import Image

project_path = "/home/teamg/volume/CarryCARI-BE"
carigan_path = "/home/teamg/volume/CarryCARI-BE/ml/StyleCariGAN"

def make_input_directory():
        #StyleCariGAN/user_image
        dir_path = carigan_path + "/user_image"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        dir = 'user_image'
        parent_dir = carigan_path
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)
 

def make_output_directory():
        #StyleCariGAN/user_result
        dir_path = carigan_path + "/user_result"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        dir = 'user_result'
        parent_dir = carigan_path
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)


def make_final_output_directory():
        #StyleCariGAN/final_result
        dir_path = carigan_path + "/final_result"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        dir = 'final_result'
        parent_dir = carigan_path
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)


'''
def find_inputImg_1():
        os.chdir(carigan_path+"/user_image")
        
        url = "https://img.hankyung.com/photo/202111/p1065590921493731_758_thum.jpg"
        #url = "https://w7.pngwing.com/pngs/590/484/png-transparent-taeyeon-to-the-beautiful-you-girls-generation-tts-girls-generation-black-hair-photography-sooyoung-thumbnail.png"
        #url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgrBtgl7A9MUYAueWjBdK7SeJEEcVefSatJ9hlaSZj7YExWWyWADL4Wu-PJb6l_uoeiNCiq6yCf8TNW6JUuO5OjgMfaIhuX0NR2jzvufx7UScaTA41iK4idCDTxUMe7ZAtcuO8XbnQPJT8seZmy_zG2Ptq2_Q06kZc-7S8x8ZJ4r6G8v00z3GEwp1dm/s0/TAEYEON%20eZn%202022%20P05L.jpg"
        
        input_dir_path = carigan_path + "/user_image"
        os.system("wget " + url + " -P {input_dir_path}" +" -O photo.png --no-hsts") #이름만 png임
        
        #진짜 png로 변경
        im = Image.open('photo.png').convert('RGB')
        im.save('photo.png', 'png')
'''


def find_inputImg_2(user, user_id, emotion):
        if emotion == 0 : #func1
                file_name = user.user_img.name.split('/')[1] #ex) cat.png
                input_img = project_path + f"/assets/user_img/{user_id}/{file_name}"
        else : #func2
                #input_img = project_path + f"/assets/user_img_clip/user_{user_id}.jpg" #StyleCLIP의 결과물, user_{user_id}.jpg
                input_img = project_path + f"/ml/StyleCLIP-pytorch/user_result/clip_result.png"

        #input dir에 png로 바꿔서 photo.png로 저장
        os.chdir(carigan_path + "/user_image")
        im = Image.open(input_img).convert('RGB')
        im.save('photo.png', 'png')


def test():
        os.chdir(carigan_path)

        # python test.py --ckpt [CHECKPOINT_PATH]              --input_dir [INPUT_IMAGE_PATH] --output_dir [OUTPUT_CARICATURE_PATH] --invert_images
        os.system("python test.py --ckpt ./checkpoint/StyleCariGAN/001000.pt --input_dir ./user_image --output_dir ./user_result --invert_images")


def choose_8styles():
        style_list = [0, 12, 15, 17, 22, 47, 58, 61]

        for i in style_list:
            user_result_dir = './user_result/photo/' + str(i) + '.png'
            final_result_dir = './final_result'
            shutil.move(user_result_dir, final_result_dir)


def run_StyleCariGAN(user, user_id, emotion):
        make_input_directory()
        make_output_directory()
        make_final_output_directory()

        find_inputImg_2(user, user_id, emotion)

        test()
        choose_8styles()
