import os
import json
import numpy as np
import shutil
JSONPATH='images/Annotations/coco_info.json'
IMAGE_PATH='images\\Images'
SAVE_PATH = 'dataset'
TRAINIMAGE_PATH ='images'
LABEL_PATH = 'labels'
TRAIN_PATH='train'
VAL_PATH='val'
TEST_PATH='test'
CATEGORIES_TXT = 'categories.txt'
wd = os.getcwd()

with open(JSONPATH, 'r', encoding='utf-8') as f:
    idx2label = f.read()
idx2label = json.loads(idx2label)
categories = idx2label['categories']
images = idx2label['images']

np.random.seed(10101)
np.random.shuffle(images)
np.random.seed(None)


annotations = idx2label['annotations']
if os.path.exists(SAVE_PATH) == False:
    os.mkdir(SAVE_PATH)
labelpath = os.path.join(SAVE_PATH, LABEL_PATH)
if os.path.exists(labelpath) == False:
    os.mkdir(labelpath)
imagepath = os.path.join(SAVE_PATH, TRAINIMAGE_PATH)
if os.path.exists(imagepath) == False:
    os.mkdir(imagepath)

def createCategoriesTxt():
    if os.path.exists(CATEGORIES_TXT) == True:
        os.remove(CATEGORIES_TXT)
    save_txt=open(CATEGORIES_TXT,'w', encoding='utf-8')
    for item in categories:
        temp = str(item['id'])+': '+item['name']
        save_txt.write('  '+temp)
        save_txt.write('\n')
    save_txt.close()

def handle():
    trainpath = os.path.join(SAVE_PATH, TRAINIMAGE_PATH, TRAIN_PATH)
    valpath = os.path.join(SAVE_PATH, TRAINIMAGE_PATH, VAL_PATH)
    testpath = os.path.join(SAVE_PATH, TRAINIMAGE_PATH, TEST_PATH)
    trainlabel = os.path.join(SAVE_PATH, LABEL_PATH, TRAIN_PATH)
    vallabel = os.path.join(SAVE_PATH, LABEL_PATH, VAL_PATH)
    testlabel = os.path.join(SAVE_PATH, LABEL_PATH, TEST_PATH)
    if os.path.exists(trainpath) == True:
        shutil.rmtree(trainpath)
    os.mkdir(trainpath)
    if os.path.exists(valpath) == True:
        shutil.rmtree(valpath)
    os.mkdir(valpath)
    if os.path.exists(testpath) == True:
        shutil.rmtree(testpath)
    os.mkdir(testpath)
    if os.path.exists(trainlabel) == True:
        shutil.rmtree(trainlabel)
    os.mkdir(trainlabel)
    if os.path.exists(vallabel) == True:
        shutil.rmtree(vallabel)
    os.mkdir(vallabel)
    if os.path.exists(testlabel) == True:
        shutil.rmtree(testlabel)
    os.mkdir(testlabel)

    imageNum = len(images)
    k=0
    for item in images:
        filename=str(k)+'.jpg'
        sourcePath = os.path.join(IMAGE_PATH, item['file_name'])
        if k<imageNum*0.6:
            targetPath = os.path.join(trainpath, filename)
            writeLabel(item, trainlabel, filename)
            
        elif k>=imageNum*0.6 and k<imageNum*0.8:
            targetPath = os.path.join(valpath, filename)
            writeLabel(item, vallabel, filename)
            # shutil.copy(sourcePath, targetPath)
        else:
            targetPath = os.path.join(testpath,filename)
            writeLabel(item, testlabel, filename)
            # shutil.copy(sourcePath, targetPath)
        if os.path.exists(sourcePath) == True:
            shutil.copy(sourcePath, targetPath)
        k = k +1

def getAnnotations(id):
    bbox=[]
    temp = {}
    for item in annotations:
        if item['image_id']==id:
            temp['bbox'] = item['bbox']
            temp['category_id'] = item['category_id']
            bbox.append(temp)
    return bbox

def writeLabel(item, path, filename):
    bbox = getAnnotations(item['id'])
    name, _ = os.path.splitext(filename)
    tempPath = os.path.join(path, name+'.txt')
    tempTxt=open(tempPath,'w')
    width=item['width']
    height=item['height']
    for box in bbox:
        x,y,w,h = box['bbox']
        x=round((x+w)/2/width, 6)
        y=round((y+h)/2/height, 6)
        w=round(w/width, 6)
        h=round(h/height, 6)
        categoryId = box['category_id']
        content = str(categoryId)+' '+str(x)+' '+str(y)+' '+str(w)+' '+str(h)
        tempTxt.write(content)
        tempTxt.write('\n')
    tempTxt.close()


handle()
createCategoriesTxt()


    

