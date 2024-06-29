import cv2 as cv
import sys
from metodos import filtros as ft
from metodos import sticker as stk
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import os

# Initialize global variables
img = None
sticker = None
x = 100
y = 50
texto = 'original'
isFirstTime = True

# Function to choose an image
def choose_image():
    Tk().withdraw()
    filename = askopenfilename()
    return filename

# Function to save image
def save_image(img, tipo):
    if tipo == 'imagem':
        print('Você deseja salvar a imagem modificada?')
    else:
        print('Você deseja salvar o último frame do vídeo?')
    print('1 - Sim')
    print('2 - Nao')
    salvar = input()

    if salvar == '1':
        print('Digite o nome do arquivo que será salvo:')
        arquivo = input()
        arquivo = arquivo + '.jpg'
        cv.imwrite(arquivo, img)
        print('Salvo!')

def setFiltroImg(img, opcao):
    if opcao == '1':
        img_com_filtro = ft.grayscale(img)
        print('Filtro de grayscale aplicado')

    elif opcao == '2':
        img_com_filtro = ft.negativo(img)
        print('Filtro negativo aplicado')

    elif opcao == '3':
        print('Insira o linear que deverá ser considerado:')
        l = int(input())
        img_com_filtro = ft.binarizacao(img, l)
        print('Filtro de binarização aplicado.')

    elif opcao == '4':
        cor = [242, 33, 33]
        img_com_filtro = ft.colorizacao(img, cor)
        print('Filtro rosado aplicado.')

    elif opcao == '5':
        img_com_filtro = ft.equalizacao_hist(img)
        print('Filtro de equalização de um histograma aplicado.')

    elif opcao == '6' or opcao == '7':
        print('Escolha uma opcao de tamanho de kernel: (quanto maior, mais blur terá)')
        print('1 - 5x5')
        print('2 - 9x9')
        print('3 - 15x15')
        kernel = input()

        if opcao == '6':
            img_com_filtro = ft.average_blur(img, kernel)
            print('Filtro de Average blur aplicado')
        else:
            img_com_filtro = ft.gaussian_blur(img, kernel)
            print('Filtro de Gaussian blur aplicado.')

    elif opcao == '8':
        img_com_filtro = ft.bordas_canny(img)
        print('Filtro de d eteccao de bordas com Canny aplicado.')

    elif opcao == '9':
        img_com_filtro = ft.dilatacao_bordas(img)
        print('Filtro de dilatacao de bordas Canny aplicado.')

    else:
        img_com_filtro = ft.erosao(img)
        print('Filtro de erosao das bordas aplicado.')

    return img_com_filtro

def setFiltroVideo(frame, opcao):
    if opcao == '1':
        frame_com_filtro = ft.grayscale(frame)
        print('Filtro de grayscale aplicado')


    elif opcao == '2':
        frame_com_filtro = ft.negativo(frame)
        print('Filtro negativo aplicado')

    elif opcao == '3':
        frame_com_filtro = ft.binarizacao(frame, l)
        print('Insira o linear que deverá ser considerado:')

    elif opcao == '4':
        cor = [242, 33, 33]
        frame_com_filtro = ft.colorizacao(frame, cor)
        print('Filtro rosado aplicado.')

    elif opcao == '5':
        frame_com_filtro = ft.equalizacao_hist(frame)
        print('Filtro de equalização de um histograma aplicado.')

    elif opcao == '6':
        frame_com_filtro = ft.average_blur(frame, kernel)
        print('Filtro de Average blur aplicado')
    elif opcao == '7':
        frame_com_filtro = ft.gaussian_blur(frame, kernel)
        print('Filtro de Gaussian blur aplicado')

    elif opcao == '8':
        frame_com_filtro = ft.bordas_canny(frame)
        print('Filtro de Deteccao de bordas com Canny aplicado')

    elif opcao == '9':
        frame_com_filtro = ft.dilatacao_bordas(frame)
        print('Filtro de Dilatacao de bordas Canny aplicado')

    else:
        frame_com_filtro = ft.erosao(frame)
        print('Filtro de Erosao das bordas aplicado')
   
    return frame_com_filtro


# Start - option to send image or record video
print("\n--------- BEM VINDO! --------- ")
print('Escolha uma opcao:\n')
print('1 - Escolher Imagem')
print('2 - Gravar Video')

choice = input()

# If user chooses 1, open an image
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

# Actions - option to paste sticker or add filter
print('\nEscolha uma opcao:\n')
print('0 - Sair')
print('1 - Aplicar Filtro')
print('2 - Colar Sticker')

acao = input()

stickers = stk.load_stickers()
sticker_index = 0

while acao != '0':

    if acao == '1':
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
        print('9 - Dilatação de bordas Canny')
        print('10 - Erosão das bordas')
        opcao = input()

        if choice == '1':
            if isFirstTime == True:
                img_com_filtro = setFiltroImg(img, opcao)
                isFirstTime = False
            else:
                print('\nEscolha qual imagem quer aplicar o filtro:')
                print('1 - Original')
                print('2 - Modificada')

                tipoImagem = input()

                if tipoImagem == '1':
                    img_com_filtro = setFiltroImg(img, opcao)
                else:
                    img_com_filtro = setFiltroImg(img_com_filtro, opcao)
        
            print("Pressione 'q' para fechar a imagem")
            # Displays the new image with the filter applied
            cv.imshow('Imagem modificada', img_com_filtro)
            k = cv.waitKey(0)

            # Verify if the user would like to save the image
            save_image(img_com_filtro, 'imagem')

            cv.destroyAllWindows()
        else:
            
            if opcao == '6' or opcao == '7':
                print('Escolha uma opcao de tamanho de kernel: (quanto maior, mais blur terá)')
                print('1 - 5x5')
                print('2 - 9x9')
                print('3 - 15x15')
                kernel = input()
            elif opcao == '3':
                print('Insira o linear que deverá ser considerado:')
                l = int(input())

            capture = cv.VideoCapture(0)
            if not capture.isOpened():
                print('Unable to open')
                exit(0)
            
            print("Pressione 'q' para fechar o video")

            while True:
                ret, frame = capture.read()
                if frame is None:
                    break

                if isFirstTime == True:
                    frame_com_filtro = setFiltroVideo(frame, opcao)
                    isFirstTime = False
                else:
                    print('\nEscolha qual video quer aplicar o filtro:')
                    print('1 - Original')
                    print('2 - Modificado')

                    tipoVideo = input()

                    if tipoVideo == '1':
                        frame_com_filtro = setFiltroVideo(frame, opcao)
                    else:
                        frame_com_filtro = setFiltroVideo(frame_com_filtro, opcao)
            
                # Display the resulting frame
                cv.imshow('video', frame_com_filtro)

                # the 'q' button is set as the
                # quitting button you may use any
                # desired button of your choice
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

            # Verify if the user would like to save the last frame of the video
            save_image(frame_com_filtro, 'video')

            # After the loop release the cap object
            capture.release()
            # Destroy all the windows
            cv.destroyAllWindows()

    elif acao == '2':
        print("\nEscolha um sticker:\n")
        for i, (name, _) in enumerate(stickers):
            print(f"{i} - {name}")

        sticker_index = int(input())
        sticker = stickers[sticker_index][1]
        print("Clique na imagem para posicionar o sticker.")

        if choice == '1':
            cv.imshow('image', img)
            cv.setMouseCallback('image', stk.mouse_click, {'img': img, 'stickers': stickers, 'sticker': sticker})

            print("Pressione 'q' para fechar a imagem")
            # Wait until a key is pressed to proceed
            cv.waitKey(0)
            cv.destroyAllWindows()

            # Verify if the user would like to save the image
            save_image(img, 'imagem')
        else:
            capture = cv.VideoCapture(0)

            print("Pressione 'q' para fechar o video")
            # Change the window size
            capture.set(cv.CAP_PROP_FRAME_WIDTH, 800)
            capture.set(cv.CAP_PROP_FRAME_HEIGHT, 800)

            if not capture.isOpened():
                print('Unable to open')
                exit(0)
            while True:
                ret, frame = capture.read()
                if frame is None:
                    break

                frame = stk.overlay(frame, sticker, x, y)
                cv.imshow('video', frame)
                
                key = cv.waitKey(1) & 0xFF
                #cv.setMouseCallback('video', stk.mouse_click, {'img': frame, 'stickers': stickers, 'sticker': sticker})

                if key == ord('q'):
                    break

                # se clicar A, move o sticker para a esquerda
                elif key == ord('a'):
                    if x-15 >= 0:
                        x -= 15
                # se clicar S, move o sticker para baixo
                elif key == ord('s'):
                    if y+15 < 600:
                        y += 15
                # se clicar W, move o sticker para cima
                elif key == ord('w'):
                    if y-15 >= 0:
                        y -= 15
                # se clicar D, move o sticker para a direita
                elif key == ord('d'):
                    if x+15 < 800:
                        x += 15

            # Verify if the user would like to save the last frame of the video
            save_image(frame_com_filtro, 'video')

            # After the loop release the cap object
            capture.release()
            # Destroy all the windows
            cv.destroyAllWindows()
            
    # Actions - option to paste sticker or add filter
    print('\nEscolha uma opcao:\n')
    print('0 - Sair')
    print('1 - Aplicar Filtro')
    print('2 - Colar Sticker')

    acao = input()

       
