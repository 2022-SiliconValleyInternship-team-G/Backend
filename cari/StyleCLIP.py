import sys
sys.path.append('/home/teamg/volume/CarryCARI-BE/ml/StyleCLIP-pytorch')

import os
import shutil
import clip
import numpy as np
import PIL.Image
import torch
from PIL import Image
from embedding import get_delta_t
from manipulator import Manipulator
from mapper import get_delta_s
from wrapper import Generator


# prompt engineering
templates = [
    'a bad photo of a {}.',
    'a photo of the hard to see {}.',
    'a low resolution photo of the {}.',
    'a rendering of a {}.',
    'graffiti of a {}.',
    'a bad photo of the {}.',
    'a cropped photo of the {}.',
    'a photo of a hard to see {}.',
    'a bright photo of a {}.',
    'a photo of a clean {}.',
    'a photo of a dirty {}.',
    'a dark photo of the {}.',
    'a drawing of a {}.',
    'a photo of my {}.',
    'a photo of the cool {}.',
    'a close-up photo of a {}.',
    'a black and white photo of the {}.',
    'a painting of the {}.',
    'a painting of a {}.',
    'a pixelated photo of the {}.',
    'a sculpture of the {}.',
    'a bright photo of the {}.',
    'a cropped photo of a {}.',
    'a jpeg corrupted photo of a {}.',
    'a blurry photo of the {}.',
    'a photo of the {}.',
    'a good photo of the {}.',
    'a rendering of the {}.',
    'a close-up photo of the {}.',
    'a photo of a {}.',
    'a low resolution photo of a {}.',
    'a photo of the clean {}.',
    'a photo of a large {}.',
    'a photo of a nice {}.',
    'a blurry photo of a {}.',
    'a cartoon {}.',
    'art of a {}.',
    'a good photo of a {}.',
    'a photo of the nice {}.',
    'a photo of the small {}.',
    'a photo of the weird {}.',
    'art of the {}.',
    'a drawing of the {}.',
    'a photo of the large {}.',
    'a dark photo of a {}.',
    'graffiti of the {}.',
]


project_path = "/home/teamg/volume/CarryCARI-BE"
styleclip_path = "/home/teamg/volume/CarryCARI-BE/ml/StyleCLIP-pytorch"


def make_input_directory():
        #StyleCariGAN/user_image
        dir_path = styleclip_path + "/user_image"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        dir = 'user_image'
        parent_dir = styleclip_path
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)


def make_output_directory():
        #StyleCariGAN/user_result
        dir_path = styleclip_path + "/user_result"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        dir = 'user_result'
        parent_dir = styleclip_path
        path = os.path.join(parent_dir, dir)
        os.mkdir(path)


def find_inputImg_1():
        os.chdir(styleclip_path+"/user_image")
        
        #url = "https://img.hankyung.com/photo/202111/p1065590921493731_758_thum.jpg"
        url = "https://w7.pngwing.com/pngs/590/484/png-transparent-taeyeon-to-the-beautiful-you-girls-generation-tts-girls-generation-black-hair-photography-sooyoung-thumbnail.png"
        #url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgrBtgl7A9MUYAueWjBdK7SeJEEcVefSatJ9hlaSZj7YExWWyWADL4Wu-PJb6l_uoeiNCiq6yCf8TNW6JUuO5OjgMfaIhuX0NR2jzvufx7UScaTA41iK4idCDTxUMe7ZAtcuO8XbnQPJT8seZmy_zG2Ptq2_Q06kZc-7S8x8ZJ4r6G8v00z3GEwp1dm/s0/TAEYEON%20eZn%202022%20P05L.jpg"
        
        input_dir_path = styleclip_path + "/user_image"
        os.system("wget " + url + " -P {input_dir_path}" +" -O photo.png --no-hsts") #이름만 png임
        
        #진짜 png로 변경
        im = Image.open('photo.png').convert('RGB')
        im.save('photo.png', 'png')


def find_inputImg_2(user, user_id):
        file_name = user.user_img.name.split('/')[1] #ex) cat.png
        input_img = project_path + f"/assets/user_img/{user_id}/{file_name}"
       
        #input dir에 png로 바꿔서 photo.png로 저장
        os.chdir(styleclip_path + "/user_image")
        im = Image.open(input_img).convert('RGB')
        im.save('photo.png', 'png')


def select_emotion(emotion) :
    # text direction : neutral -> target
    # neutral = 'young face'
    # target = 'old face'

    # 4가지 emotion과 integer mapping
    global neutral
    global target
    emotion_mapping = ['smile', 'sad', 'surprised', 'angry'] #emotion = 1, 2, 3, 4
    input_emotion = emotion_mapping[emotion - 1]
    neutral='face' 
    target= input_emotion + ' face' 


def test():
    # GPU device
    device = torch.device('cuda:1')
    # pretrained ffhq generator
    ckpt = 'pretrained/ffhq.pkl'
    G = Generator(ckpt, device)
    # CLIP
    model, preprocess = clip.load("ViT-B/32", device=device)
    # global image direction
    fs3 = np.load('tensor/fs3.npy')


    manipulator = Manipulator(G, device)


    # test image dir path
    # imgdir = 'samples'
    imgdir = 'user_image'

    # manipulator mode
    # inv_mode : inversion mode
        # 'w' : use w projector proposed by Karras et al.
        # 'w+' : use e4e encoder (only implemented for ffhq1024 now)
    # pti_mode : pivot tuning mode
        # 'w' : W latent space pivot tuning
        # 's' : Style space pivot tuning
    manipulator.set_real_img_projection(imgdir, inv_mode='w+', pti_mode='s')


    # beta_threshold : Determines the degree of disentanglement, # channels manipulated
    beta_threshold = 0.10

    classnames=[neutral, target]
    # get delta_t in CLIP text space
    delta_t = get_delta_t(classnames, model)
    # get delta_s in global image directions and text directions that satisfy beta threshold
    delta_s, num_channel = get_delta_s(fs3, delta_t, manipulator, beta_threshold=beta_threshold)
    print(f'{num_channel} channels will be manipulated under the beta threshold {beta_threshold}')

    # alpha_threshold : Determines the degree of manipulation
    lst_alpha = [-3] #-3이 적당한 듯
    manipulator.set_alpha(lst_alpha)


    # manipulate styles
    styles = manipulator.manipulate(delta_s)

    # synthesis images from manipulated styles
    all_imgs = manipulator.synthesis_from_styles(styles, 0, manipulator.num_images)


    # visualize
    lst = []
    for imgs in all_imgs:
        lst.append((imgs.permute(0,2,3,1)*127.5+128).clamp(0,255).to(torch.uint8).numpy())

    H,W = (256,256)
    gw, gh = (manipulator.num_images, 1)

    for i, alpha in enumerate(lst_alpha):
        print(alpha)
        imgs = lst[i]
        imgs_ = []
        for img in imgs:
            imgs_.append( np.asarray( PIL.Image.fromarray(img, 'RGB').resize((H,W),PIL.Image.LANCZOS)))
        imgs_ = np.stack(imgs_)
        imgs_ = imgs_.reshape(gh,gw,H,W,3)
        imgs_ = imgs_.transpose(0,2,1,3,4)
        imgs_ = imgs_.reshape(gh*H, gw*W, 3)
        imgs = PIL.Image.fromarray(imgs_, 'RGB')

        os.chdir(styleclip_path + "/user_result")
        imgs.save(f"clip_result.png") #우리는 한장만 뽑을거라서 이렇게 저장
        #imgs.save(f"test-{i}-{alpha}.png")
        #display(PIL.Image.fromarray(imgs_, 'RGB'))


def run_StyleCLIP(user, user_id, emotion):
    make_input_directory()
    make_output_directory()

    select_emotion(emotion)
    print("변경하고 싶은 표정: " + target)

    #find_inputImg_1()
    find_inputImg_2(user, user_id)

    os.chdir(styleclip_path)
    test()


# run_StyleCLIP(user, user_id, emotion)
#run_StyleCLIP("", "", 2)