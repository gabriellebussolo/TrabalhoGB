import cv2 as cv
import sys
from metodos import filtros as ft

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np

def choose_image():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    return filename

def record_video():
    cap = cv.VideoCapture(0)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv.imshow('Recording Video', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv.destroyAllWindows()

# Choose image or record video
print('Escolha uma opcao:\n')
print('1 - Escolher Imagem')
print('2 - Gravar Video')

choice = input()

if choice == '1':
    img_path = choose_image()
    if not img_path:
        print('Nenhuma imagem escolhida')
        sys.exit()

    img = cv.imread(img_path)
    if img is None:
        print('Erro ao carregar imagem')
        sys.exit()

    img2 = img.copy()  # cria uma copia da original


print('Escolha uma opcao de filtro:\n')
print('0 - Sair')
print('1 - Grayscale')
print('2 - Negativo')
print('3 - Binarização')

opcao = input()

if opcao == '1':
    ft.grayscale(img2)
    cv.imshow('Grayscale', img2)
    k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
elif opcao == '2':
    ft.negativo(img2)
    cv.imshow('Negativo', img2)
    k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
elif opcao == '3':
    print('Insira o linear que deverá ser considerado:')
    l = int(input())
    ft.binarizacao(img2, l)
    cv.imshow('binarizacao', img2)
    k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
opcao = input()
