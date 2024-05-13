import streamlit as st
from PIL import Image
from io import StringIO
from sidebar import sidebar 
import torch
from collections import OrderedDict 
from lib.networks import define_G
from transform import sketch2fashion,create_generator
# to run type python3.11 -m streamlit run main.py

models = {
    'unet': {'path': 'cyclegan-unet.pth', 'input_nc': 3, 'output_nc': 3, 'netG': "resnet_9blocks", 'norm': "instance", },
}
# set up generators
unet = create_generator(models['unet'])
# print("CycleGAN (Gen: unet): Ready", end='\n\n')



#Invokes sidebar and details
sidebar()

st.title(':red[Generating Clothing Visualization Using Sketches] :dress:')
st.subheader('Upload your sketch here or take a picture to see the results:exclamation::exclamation:')

uploaded_file = st.file_uploader(" ", type=['jpg','png','jpeg'])

picture = st.camera_input("Take a picture ! :camera_with_flash:")
count=1
if picture is not None and uploaded_file is None:
    #Sends picture to backend and preprocess
    types="unet"
    sketch2fashion(unet, picture, 1,count,types)
    count+=1




if uploaded_file is not None and picture is None:    
    #To download to system:
    # with open(os.path.join("C:/Users/hp/streamlit-test/",uploaded_file.name),"wb") as f:
    #        f.write(uploaded_file.getbuffer())
    types="unet"
    sketch2fashion(unet, uploaded_file, 1,count,types)
    count+=1
