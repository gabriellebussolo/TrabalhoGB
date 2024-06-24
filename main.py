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

# INICIO - OPCAO DE ENVIAR IMAGEM OU GRAVAR VIDEO
print("\n--------- BEM VINDO! --------- ")
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

    print('\nImagem adicionada!')
    img2 = img.copy()  

elif choice == '2':
    record_video()


#  ACOES - OPCAO DE COLAR STICKER OU ADICIONAR FILTRO
print('\nEscolha uma opcao:\n')
print('0 - Sair')
print('1 - Aplicar Filtro')
print('2 - Colar Sticker')

acao = input()

if acao == "1":

    print('\nEscolha uma opcao de filtro:\n')
    print('0 - Sair')
    print('1 - Grayscale')
    print('2 - Negativo')
    print('3 - Binarização') 
    print('4 - Quente')
    print('5 - Equalização de um histograma')

    opcao = input()

    if opcao == '1':
        img_cinza = ft.grayscale(img2)
        cv.imshow('Grayscale', img_cinza)
        k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
    elif opcao == '2':
        ft.negativo(img2)
        cv.imshow('Negativo', img2)
        k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
    elif opcao == '3':
        print('Insira o linear que deverá ser considerado:')
        l = int(input())
        ft.binarizacao(img2, l)
        cv.imshow('Binarizacao', img2)
        k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
    elif opcao == '4':
       cor = [240, 86, 86]
       ft.colorizacao(img2, cor)
       cv.imshow('Quente', img2)
       k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
    elif opcao == '5':
        equalizacao = ft.equalizacao_hist(img2)
        cv.imshow('Equalizacao de um histograma', equalizacao)
        k = cv.waitKey(0)
    #opcao = input()
elif acao == "2":
    print("sticker")