import os
from collections import OrderedDict
import torch
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
from lib.networks import define_G
from lib.util import tensor2im, save_image
from columns import columns


count=0
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

transform_without_grayscale = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

def create_generator(model,ngf=64):
    model_dict = torch.load(model['path'])
    new_dict = OrderedDict()
    for k, v in model_dict.items():
        new_dict[k] = v
    generator_model = define_G(input_nc=3, output_nc=3, netG=model['netG'],
                               norm=model['norm'], ngf=ngf, use_dropout=False, init_gain=0.02, gpu_ids=[])
    generator_model.load_state_dict(new_dict)

    # Set the model to evaluation mode
    generator_model.eval()

    return generator_model


def sketch2fashion(generator_model, input_image_path, output_image_path,count,types,grayscale=True):
    # print("model:",generator_model)

    input_image = Image.open(input_image_path).convert('RGB')
    image_size = input_image.size

    # Preprocess the input image
    input_tensor = transform(input_image).unsqueeze(0)

    if grayscale:
        input_tensor = transform(input_image).unsqueeze(0)
    else:
        input_tensor = transform_without_grayscale(input_image).unsqueeze(0)
        
    # Pass the input image through the generator model
    with torch.no_grad():
        output_tensor = generator_model(input_tensor)
    
    # Postprocess the output image

    output_image_unet = tensor2im(output_tensor)
    # print(type(output_image_unet))
    output_image_unet = Image.fromarray(output_image_unet)
    output_image_unet = output_image_unet.resize(image_size)
            #Invoke Columns and output
    columns(input_image,output_image_unet,count,types)
    
    