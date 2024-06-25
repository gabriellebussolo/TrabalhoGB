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

elif choice == '2':
    record_video()


#  ACOES - OPCAO DE COLAR STICKER OU ADICIONAR FILTRO
print('\nEscolha uma opcao:\n')
print('0 - Sair')
print('1 - Aplicar Filtro')
print('2 - Colar Sticker')

acao = input()

while(acao != '0'):
    
    if acao == "1":

        print('\nEscolha uma opcao de filtro:\n')
        print('0 - Sair')
        print('1 - Grayscale')
        print('2 - Negativo')
        print('3 - Binarização') 
        print('4 - Tom rosado')
        print('5 - Equalização de um histograma')
        print('6 - Blur usando média da vizinhança')
        print('7 - Gaussian Blur')
        print('8 - Detecção de bordas com Canny')
        opcao = input()

        if opcao == '1':
            img_cinza = ft.grayscale(img)
            cv.imshow('Grayscale', img_cinza)
            k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
            
        elif opcao == '2':
            neg = ft.negativo(img)
            cv.imshow('Negativo', neg)
            k = cv.waitKey(0)
            
        elif opcao == '3':
            print('Insira o linear que deverá ser considerado:')
            l = int(input())
            binarizada = ft.binarizacao(img, l)
            cv.imshow('Binarizacao', binarizada)
            k = cv.waitKey(0)
            
        elif opcao == '4':
            cor = [242, 33, 33]
            vermelho = ft.colorizacao(img, cor)
            cv.imshow('Rosado', vermelho)
            k = cv.waitKey(0)
            
        elif opcao == '5':
            equalizacao = ft.equalizacao_hist(img)
            cv.imshow('Equalizacao de um histograma', equalizacao)
            k = cv.waitKey(0)
            
        elif opcao == '6' or opcao == '7':
            print('Escolha uma opcao de tamanho de kernel: (quanto maior, mais blur terá)')
            print('1 - 5x5')
            print('2 - 9x9')
            print('3 - 15x15') 
            kernel = input()
            if opcao == '6':
                blurred = ft.average_blur(img, kernel)
                cv.imshow('Average blur', blurred)
                k = cv.waitKey(0)
            else:
                blurred_gaussian = ft.gaussian_blur(img, kernel)
                cv.imshow('Gaussian blur', blurred_gaussian)
                k = cv.waitKey(0)
                
        elif opcao == '8':
            bordas = ft.bordas_canny(img)
            cv.imshow('Detecção de bordas com Canny', bordas)
            k = cv.waitKey(0)
                
    elif acao == "2":
        print("sticker")
    
    cv.destroyAllWindows()
    #  ACOES - OPCAO DE COLAR STICKER OU ADICIONAR FILTRO
    print('\nEscolha uma opcao:\n')
    print('0 - Sair')
    print('1 - Aplicar Filtro')
    print('2 - Colar Sticker')  
    
    acao = input()