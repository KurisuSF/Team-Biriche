import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
from network import Network
import torch
from utils import to_numpy, get_transforms, add_img_text
from dataset import EMOTIONS_MAP
import pathlib

file_path = pathlib.Path(__file__).parent.absolute()

def load_img(path):
    assert os.path.isfile(path), f"El archivo {path} no existe"
    img = cv2.imread(path)
    val_transforms, unnormalize = get_transforms("test", img_size = 48)
    tensor_img = val_transforms(img)
    denormalized = unnormalize(tensor_img)
    return img, tensor_img, denormalized

def predict(img_title_paths):
    '''
        Hace la inferencia de las imagenes
        args:
        - img_title_paths (dict): diccionario con el titulo de la imagen (key) y el path (value)
    '''
    # Cargar el modelo
    modelo = Network(48, 7)
    modelo.load_model("model_1.pt")
    for path in img_title_paths:
        # Cargar la imagen
        # np.ndarray, torch.Tensor
        im_file = (file_path / path).as_posix()
        original, transformed, denormalized = load_img(im_file)

        # Inferencia
        # TODO: Para la imagen de entrada, utiliza tu modelo para predecir la clase mas probable
        modelo.eval()
        pred, x = modelo(transformed.unsqueeze(0))
        pred = torch.argmax(pred, dim=1).item()
        pred_label = EMOTIONS_MAP[pred]
        
        # Original / transformada
        # pred_label (str): nombre de la clase predicha
        h, w = original.shape[:2]
        resize_value = 300
        img = cv2.resize(original, (w * resize_value // h, resize_value))
        img = add_img_text(img, f"Pred: {pred_label}")

        # Mostrar la imagen
        denormalized = to_numpy(denormalized)
        denormalized = cv2.resize(denormalized, (resize_value, resize_value))
        cv2.imshow("Predicción - original", img)
        cv2.imshow("Predicción - transformed", denormalized)
        cv2.waitKey(0)

if __name__=="__main__":
    # Direcciones relativas a este archivo
    img_paths = ["./test_imgs/happy.png", "./test_imgs/happy_a.jpg", "./test_imgs/sad_a.jpg", "./test_imgs/anger_a.jpg", "./test_imgs/surprise_a.jpg", "./test_imgs/disgust_a.jpg", "./test_imgs/fear_a.jpg", "./test_imgs/neutral_a.jpg"
                 , "./test_imgs/happy_f.jpg", "./test_imgs/sad_f.jpg", "./test_imgs/anger_f.jpg", "./test_imgs/surprise_f.jpg", "./test_imgs/disgust_f.jpg", "./test_imgs/fear_f.jpg", "./test_imgs/neutral_f.jpg"
                 , "./test_imgs/happy_c.jpg", "./test_imgs/sad_c.jpg", "./test_imgs/anger_c.jpg", "./test_imgs/surprise_c.jpg", "./test_imgs/disgust_c.jpg", "./test_imgs/fear_c.jpg", "./test_imgs/neutral_c.jpg"]
    predict(img_paths)