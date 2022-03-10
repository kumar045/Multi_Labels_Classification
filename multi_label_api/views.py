from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from .serializers import MultiLabelSerializer
from .models import *
import itertools
from pandas import read_csv
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import cv2
import glob
import os
from keras import backend
from pathlib import Path
#from skimage import io

class RoadDetectionAPIView(CreateAPIView):
    serializer_class = MultiLabelSerializer
    queryset = MultiLabel.objects.all()

    def create(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            path_of_folder = self.request.data['path_of_folder']
            content = []

            path_of_folder = "C:\\Users\\Shivam\\Documents\\multi_label_api\\multi_label\\multi_label_api\\Photos\\"+str(path_of_folder)+"\\*.jpg"
            print("path_of_folder:::::", path_of_folder)
                            
            for name in glob.glob(path_of_folder):
                name_of_image=os.path.splitext(os.path.basename(name))[0]
                self.folder_creater_of_all_combination(name_of_image)

            # add result to the dictionary and revert as response
            mydict = {
                'status': True,
                'response':
                    {

                        'Image_Path_1':path_of_folder,

                    }
            }
            content.append(mydict)

            return Response(content, status=status.HTTP_200_OK)
        errors = serializer.errors

        response_text = {
            "status": False,
            "response": errors
        }
        return Response(response_text, status=status.HTTP_400_BAD_REQUEST)
    def folder_creater_of_all_combination(self,name_of_image):
                
        # load and prepare the image
        def load_image(filename):
            # load the image
            img = load_img(filename, target_size=(128, 128))
            # convert to array
            img = img_to_array(img)
            # reshape into a single sample with 3 channels
            img = img.reshape(1, 128, 128, 3)
            # center pixel data
            img = img.astype('float32')
            img = img - [123.68, 116.779, 103.939]
            return img

        # calculate fbeta score for multi-class/label classification
        def fbeta(y_true, y_pred, beta=2):
            # clip predictions
            y_pred = backend.clip(y_pred, 0, 1)
            # calculate elements
            tp = backend.sum(backend.round(backend.clip(y_true * y_pred, 0, 1)), axis=1)
            fp = backend.sum(backend.round(backend.clip(y_pred - y_true, 0, 1)), axis=1)
            fn = backend.sum(backend.round(backend.clip(y_true - y_pred, 0, 1)), axis=1)
            # calculate precision
            p = tp / (tp + fp + backend.epsilon())
            # calculate recall
            r = tp / (tp + fn + backend.epsilon())
            # calculate fbeta, averaged across each class
            bb = beta ** 2
            fbeta_score = backend.mean((1 + bb) * (p * r) / (bb * p + r + backend.epsilon()))
            return fbeta_score
          
        def create_tag_mapping1(mapping_csv1):
            # create a set of all known tags
            labels = set()
            for i in range(len(mapping_csv1)):
                # convert spaced separated tags into an array of tags
                tags = mapping_csv1['tags'][i].split(' ')
                # add tags to the set of known labels
                labels.update(tags)

            # convert set of labels to a list to list
            labels = list(labels)
            # order set alphabetically
            labels.sort()
            # dict that maps labels to integers, and the reverse
            labels_map = {labels[i]:i for i in range(len(labels))}
            inv_labels_map = {i:labels[i] for i in range(len(labels))}
            return labels_map, inv_labels_map

        # convert a prediction to tags
        def prediction_to_tags1(inv_mapping1, values):
            # round probabilities to {0, 1}
            #print(values)
            # collect all predicted tags
            tags = [inv_mapping1[i] for i in values]
            return tags
        
        def create_tag_mapping(mapping_csv):
            # create a set of all known tags
            labels = set()
            for i in range(len(mapping_csv)):
                # convert spaced separated tags into an array of tags
                tags = mapping_csv['tags'][i].split(' ')
                # add tags to the set of known labels
                labels.update(tags)
            # convert set of labels to a list to list
            labels = list(labels)
            # order set alphabetically
            labels.sort()
            # dict that maps labels to integers, and the reverse
            labels_map = {labels[i]:i for i in range(len(labels))}
            inv_labels_map = {i:labels[i] for i in range(len(labels))}
            return labels_map, inv_labels_map
        # convert a prediction to tags
        def prediction_to_tags(inv_mapping, prediction):
            # round probabilities to {0, 1}
            values = prediction.round()
            # collect all predicted tags
            tags = [inv_mapping[i] for i in range(len(values)) if values[i] == 1.0]
            return tags

        # load the mapping file
        filename = 'C:\\Users\\Shivam\\Documents\\multi_label_api\\multi_label\\multi_label_api\\Photos\\train_v2.csv'
        mapping_csv1 = read_csv(filename)
        # create a mapping of tags to integers
        _, inv_mapping1 = create_tag_mapping1(mapping_csv1)
        #print(inv_mapping)
        
        # load the image
        #	img = load_image('C:\\Users\\Shivam\\Downloads\\planet\\planet\\train-jpg\\train_1.jpg')
        img = load_image('C:\\Users\\Shivam\\Documents\\multi_label_api\\multi_label\\multi_label_api\\Photos\\test_images\\'+str(name_of_image)+'.jpg')
        # load model
        dependencies = { 'fbeta': fbeta}

        model = load_model('C:\\Users\\Shivam\\Documents\\multi_label_api\\multi_label\\multi_label_api\\Photos\\final_model.h5',custom_objects=dependencies)
        # predict the class
        result = model.predict(img)
        #print(result[0])

            # load the mapping file
        filename = 'C:\\Users\\Shivam\\Documents\\multi_label_api\\multi_label\\multi_label_api\\Photos\\train_v2.csv'
        mapping_csv = read_csv(filename)
        # create a mapping of tags to integers
        _, inv_mapping = create_tag_mapping(mapping_csv)
        # entry point, run the example
        #run_example(inv_mapping)
        # map prediction to tags
        tags = prediction_to_tags(inv_mapping, result[0])
        #print(tags)
        #	image=cv2.imread("C:\\Users\\Shivam\\Downloads\\planet\\planet\\train-jpg\\train_1.jpg")
        # font 
        font = cv2.FONT_HERSHEY_SIMPLEX 

        # org 
        org = (0, 30) 

        # fontScale 
        fontScale = 0.6

        # Blue color in BGR 
        color = (255, 255, 0) 

        # Line thickness of 2 px 
        thickness = 2

        image=cv2.imread('C:\\Users\\Shivam\\Documents\\multi_label_api\\multi_label\\multi_label_api\\Photos\\test_images\\'+str(name_of_image)+'.jpg')
        image=cv2.resize(image,(500,500))    
        #image = cv2.putText(image, str(tags), org, font,  
                            #fontScale, color, thickness, cv2.LINE_AA)
        stuff = [0,1, 2, 3,4,5,6,7,8,9,10]
        path="C:\\Users\\Shivam\\Documents\\multi_label_api\\multi_label"
        #os.chdir(path)
        for L in range(0, len(stuff)+1):
            for subset in itertools.combinations(stuff, L):
                my_tag=prediction_to_tags1(inv_mapping1,subset)
                #print(my_tag)
                my_tag.sort()
                tags.sort()
                if(my_tag==tags):
                    print("yes")
                    try:
                        if(not os.path.exists(str(tags))):
                            os.makedirs(str(tags)) 
                            print("Direcory '%s' created successfully")
                        path1=str(path)+'//'+str(tags)    
                        cv2.imwrite(os.path.join(path1,str(name_of_image)+".jpg"),image)
                    except OSError:
                        print("Directory '%s' is already created")
            