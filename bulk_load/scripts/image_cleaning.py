import os
import io
import logging
from glob import glob

from PIL import Image
 


def enhance_image(file_name):

    #resizing the image
    im = Image.open(file_name)
    #logging.info(f'Original Size:{im.size}')
    
    im2 = im.resize((min(4200, int(im.size[0]*2)), min(4200, int(im.size[1]*2))), Image.BICUBIC)
    
    #Improve the DPI to 1000 & save the enhanced image
    #target_file_name = '.'.join(file_name.split('.')[:-1]) + '_enhance' + '.jpg'
    target_file_name = '.'.join(file_name.split('.')[:-1])  + '.jpg'
    os.remove(file_name)
    im2.save(target_file_name,dpi=(300,300))

    return target_file_name
    
def rotate_image(file_name):

    #Target file
    target_file_name = '.'.join(file_name.split('.')[:-1]) + '_rotated' + '.jpg'

    #Read image
    img = cv2.imread(file_name, 0)
    #logging.info("Image Size: "+img.shape)

    #Flip the foreground
    gray = cv2.bitwise_not(img)
     
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    #cv2.imwrite('.'.join(file_name.split('.')[:-1]) + '_thresh' + '.jpg', thresh)
    
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
     
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)
     
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle

     
    logging.info(f'Angle:{angle}')
    if angle != 0.0:
        # rotate the image to deskew it
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        cv2.imwrite(file_name, rotated)
    
    else:
        #rotating by right angle - use pyttesseract to rotate landscape images
        try:
            a=(pytesseract.image_to_osd(file_name,output_type=pytesseract.Output.DICT))
            logging.info(f'Orientation:{a}')
            if(a["orientation"]==270):
                x=ndimage.rotate(img, 270)
                img=x
                logging.info('\nImage Rotated...\n')
            elif(a["orientation"]==90):
                x=ndimage.rotate(img,90)
                img=x
                logging.info('\nImage Rotated...\n')
            elif(a["orientation"]==180):
                x=ndimage.rotate(img,-90)
                img=x
                logging.info('\nImage Rotated...\n')
        except:
            img=img

        cv2.imwrite(file_name, img)
        #logging.info("Image Size: "+img.shape)
    return target_file_name

def remove_grain_noise(file_name):
    target_file_name = '.'.join(file_name.split('.')[:-1]) + '_grain_removed' + '.jpg'
    
    img = cv2.imread(file_name)
    
    kernel = np.ones((5, 5), np.uint8)
    #cv2.dilate(img, kernel, iterations = 1)
    
    kernel = np.ones((5, 5), np.uint8)
    #cv2.erode(img, kernel, iterations = 1)
    
    #bg_img =  cv2.medianBlur(img, 3)
    cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(target_file_name, img)
    
def remove_shadow(file_name):

    #Read image
    img = cv2.imread(file_name)
    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
        
#    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    target_file_name = '.'.join(file_name.split('.')[:-1]) + '_noshadow' + '.jpg'
    cv2.imwrite(target_file_name, result_norm)
    
    return target_file_name
    
def image_resize(file_name, height):

    #Read image
    image = cv2.imread(file_name, 0)
    #logging.info("Image Size: "+image.shape)

    #Resized image
    resized = imutils.resize(image, height=height)

    #logging.info("Image resize: "+resized.shape)
    target_file_name = '.'.join(file_name.split('.')[:-1]) + '_resize' + '.jpg'
    cv2.imwrite(target_file_name, resized)

    return target_file_name
    
def image_cleaning(img_path):
    
     
    img_names = glob(img_path+'/*')
    for filename in img_names:
        '''#enhance_image(filename)
        #remove_flicker(filename)
        remove_grain_noise(filename)
        remove_shadow(filename)
        rotate_image(filename)
        #image_resize(filename, height = 1024) '''
       
        #logging.info(filename)
        #inFile_resize = image_resize(filename, height = 1024)
        #logging.info('image_resize')
        inFile_enhance = enhance_image(filename)
        #logging.info('enhance_image')
        #inFile_edge = document_edge_detection(inFile_resize)
        #inFile_deflicker = remove_flicker(inFile_edge)
        #inFile_shadow = remove_shadow(inFile_enhance)
        #logging.info('remove_shadow')
        #inFile_rotate = rotate_image(inFile_shadow)
        #logging.info('rotate_image')
        #inFile_enhance = enhance_image(inFile_rotate)
        #logging.info('enhance_image')
        #inFile = image_resize(inFile_enhance, height = 1024) 
       
            