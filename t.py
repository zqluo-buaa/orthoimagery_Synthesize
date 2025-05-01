import os
from PIL import Image
if __name__ == '__main__':
    input_dir_A = '/media/ziqing/S1/ANU_data_test/streetview/'
    input_dir_B = '/media/ziqing/S1/ANU_data_test/polar/'
    output_dir_A1 = '/media/ziqing/S1/ANU_data_test/A1/test/'
    output_dir_A2 = '/media/ziqing/S1/ANU_data_test/A2/test/'
    output_dir_B = '/media/ziqing/S1/ANU_data_test/B/test/'
    images = os.listdir(input_dir_A)
    #le = len(images)
    for index, img in enumerate(images):
        if index >= 1000:
            break
       # print(img)
        grd_img = Image.open(input_dir_A + img)
        sat_img = Image.open(input_dir_B + img.replace('grdView.jpg','satView_polish.png'))
        image_B = sat_img
        #signal = np.flip(signal , 0)
        #
        image_A1 = grd_img.resize([512,256])
        image_A2 = grd_img.resize([256,256])
        #print(type(image_A1))
        #image = image.astype(np.uint8)
        image_A1.save(output_dir_A1 + img.replace('jpg','png'))
        image_A2.save(output_dir_A2 + img.replace('jpg','png'))
        image_B.save(output_dir_B + img.replace('jpg','png'))
        
        if index%100 == 0:
            print('index = ',index, 'total = ',1000)
    

#python datasets/combine_A_and_B.py --fold_A /media/ziqing/S1/ANU_data_test/A1 --fold_B /media/ziqing/S1/ANU_data_test/B --fold_AB /media/ziqing/S1/ANU_data_test/512AB          
#python test.py --dataroot /media/ziqing/S1/small_2/256AB --direction AtoB --model pix2pix --name rev_pix2pix_14
