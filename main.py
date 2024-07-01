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
imgModificada = None
frameModificado = None
filtro = None

# Function to choose an image
def choose_image():
    Tk().withdraw()
    filename = askopenfilename()
    return filename

# Function to save image
def save_image(img, tipo):
    if tipo == 'imagem':
        print('\nVocê deseja salvar a imagem modificada?')
    else:
        print('\nVocê deseja salvar o último frame do vídeo?')
    print('1 - Sim')
    print('2 - Nao')
    salvar = input()

    if salvar == '1':
        print('Digite o nome do arquivo que será salvo:')
        arquivo = input()
        arquivo = arquivo + '.jpg'
        cv.imwrite(arquivo, img)
        print('Salvo!')

# Function to apply a filter to the image
def setFiltroImg(img, opcao):
    if opcao == '1':
        img_com_filtro = ft.grayscale(img)
        img_com_filtro = cv.cvtColor(img_com_filtro, cv.COLOR_GRAY2BGR) # converts the image back to BGR to have 3 channels
        print('Filtro de grayscale aplicado')

    elif opcao == '2':
        img_com_filtro = ft.negativo(img)
        print('Filtro negativo aplicado')

    elif opcao == '3':
        print('Insira o linear que deverá ser considerado:')
        l = int(input())
        img_com_filtro = ft.binarizacao(img, l)
        img_com_filtro = cv.cvtColor(img_com_filtro, cv.COLOR_GRAY2BGR) # converts the image back to BGR to have 3 channels
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
        img_com_filtro = cv.cvtColor(img_com_filtro, cv.COLOR_GRAY2BGR) #converts the image back to BGR to have 3 channels
        print('Filtro de detecção de bordas com Canny aplicado.')

    elif opcao == '9':
        img_com_filtro = ft.dilatacao_bordas(img)
        img_com_filtro = cv.cvtColor(img_com_filtro, cv.COLOR_GRAY2BGR) #converts the image back to BGR to have 3 channels
        print('Filtro de dilatação de bordas Canny aplicado.')

    else:
        img_com_filtro = ft.erosao(img)
        img_com_filtro = cv.cvtColor(img_com_filtro, cv.COLOR_GRAY2BGR) #converts the image back to BGR to have 3 channels
        print('Filtro de erosão das bordas aplicado.')

    return img_com_filtro

# Function to apply a filter to the video
def setFiltroVideo(frame, opcao):
    if opcao == '1':
        frame_com_filtro = ft.grayscale(frame)
        frame_com_filtro = cv.cvtColor(frame_com_filtro, cv.COLOR_GRAY2BGR) # converts the image back to BGR to have 3 channels

    elif opcao == '2':
        frame_com_filtro = ft.negativo(frame)

    elif opcao == '3':
        frame_com_filtro = ft.binarizacao(frame, l)
        frame_com_filtro = cv.cvtColor(frame_com_filtro, cv.COLOR_GRAY2BGR) #converts the image back to BGR to have 3 channels

    elif opcao == '4':
        cor = [242, 33, 33]
        frame_com_filtro = ft.colorizacao(frame, cor)

    elif opcao == '5':
        frame_com_filtro = ft.equalizacao_hist(frame)

    elif opcao == '6':
        frame_com_filtro = ft.average_blur(frame, kernel)
    
    elif opcao == '7':
        frame_com_filtro = ft.gaussian_blur(frame, kernel)

    elif opcao == '8':
        frame_com_filtro = ft.bordas_canny(frame)
        frame_com_filtro = cv.cvtColor(frame_com_filtro, cv.COLOR_GRAY2BGR) #converts the image back to BGR to have 3 channels

    elif opcao == '9':
        frame_com_filtro = ft.dilatacao_bordas(frame)
        frame_com_filtro = cv.cvtColor(frame_com_filtro, cv.COLOR_GRAY2BGR) #converts the image back to BGR to have 3 channels

    else:
        frame_com_filtro = ft.erosao(frame)
        frame_com_filtro = cv.cvtColor(frame_com_filtro, cv.COLOR_GRAY2BGR) #converts the image back to BGR to have 3 channels
   
    return frame_com_filtro

# Function that shows the filter options
def opcoesFiltro():
    print('\nEscolha uma opcao de filtro:\n')
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
    return opcao

# Function that shows the sticker options
def opcoesStickers():
    print("\nEscolha um sticker:\n")
    for i, (name, _) in enumerate(stickers):
        print(f"{i} - {name}")

    sticker_index = int(input())
    sticker = stickers[sticker_index][1]
    return sticker

# Function that shows the keyboard options to control the video
def opcoesVideo():
    print('\nPressione as seguintes teclas para continuar:')
    print('Q para encerrar as modificações no vídeo atual.')
    print('F para aplicar um filtro diferente no vídeo.')
    print('I para inserir um sticker no vídeo atual.')
    print('B para salvar o frame atual.')

# Function that shows the keyboard options to control the sticker on the video
def opcoesMovimentoSticker():
    print('A para mover o sticker para a esquerda')
    print('D para mover o sticker para a direita')
    print('W para mover o sticker para cima')
    print('S para mover o sticker para baixo\n')

# Function to check if the filter should also be applied to the sticker on the video
def addFilterToStickerVideo():
    print('\nVocê deseja aplicar o filtro no sticker também?')
    print('1 - Sim')
    print('2 - Não')
    opcao = input()
    return opcao

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

    # Image
    if choice == '1':

        # Add Filter #
        if acao == '1':
            filtro = opcoesFiltro()

            if isFirstTime == True:
                imgModificada = setFiltroImg(img, filtro)
                isFirstTime = False
            else:
                print('\nEscolha qual imagem quer aplicar o filtro:')
                print('1 - Original')
                print('2 - Modificada')

                tipoImagem = input()

                if tipoImagem == '1':
                    imgModificada = setFiltroImg(img, filtro)
                else:
                    imgModificada = setFiltroImg(imgModificada, filtro)
            
            print("\nPressione qualquer tecla para fechar a imagem.")

            cv.imshow('Imagem modificada', imgModificada)

            # Wait until a key is pressed to proceed
            cv.waitKey(0)

            # Verify if the user would like to save the image
            save_image(imgModificada, 'imagem')
            cv.destroyAllWindows()    

        # Add Sticker #
        else:
            sticker = opcoesStickers()

            if isFirstTime == True:
                print("\nClique na imagem para posicionar o sticker.")
                img2 = img.copy()
                cv.imshow('image', img2)
                cv.setMouseCallback('image', stk.mouse_click, {'img': img2, 'stickers': stickers, 'sticker': sticker})
                isFirstTime = False
                imgModificada = img2
            else:
                print('\nEscolha qual imagem você quer aplicar o filtro:')
                print('1 - Original')
                print('2 - Modificada')

                tipoImagem = input()

                print("\nClique na imagem para posicionar o sticker.")

                if tipoImagem == '1':
                    img2 = img.copy()
                    cv.imshow('image', img2)
                    cv.setMouseCallback('image', stk.mouse_click, {'img': img2, 'stickers': stickers, 'sticker': sticker})
                    imgModificada = img2
                else:
                    cv.imshow('image', imgModificada)
                    cv.setMouseCallback('image', stk.mouse_click, {'img': imgModificada, 'stickers': stickers, 'sticker': sticker})

            print("\nPressione qualquer tecla para fechar a imagem.")

            # Wait until a key is pressed to proceed
            cv.waitKey(0)

            # Verify if the user would like to save the image
            save_image(imgModificada, 'imagem')
            cv.destroyAllWindows()               
        
    # Video #
    else:
        # Add filter first#
        if acao == '1':
            
            filtro = opcoesFiltro()

            if filtro == '6' or filtro == '7':
                print('Escolha uma opcao de tamanho de kernel: (quanto maior, mais blur terá)')
                print('1 - 5x5')
                print('2 - 9x9')
                print('3 - 15x15')
                kernel = input()
            elif filtro == '3':
                print('Insira o linear que deverá ser considerado:')
                l = int(input())

            capture = cv.VideoCapture(0)
            if not capture.isOpened():
                print('Unable to open')
                exit(0)

            # Change the window size of the video
            capture.set(cv.CAP_PROP_FRAME_WIDTH, 800)
            capture.set(cv.CAP_PROP_FRAME_HEIGHT, 800)
                
            # Print the keyboard actions
            opcoesVideo()

            while True:
                ret, frame = capture.read()
                if frame is None:
                    break
                
                frameModificado = setFiltroVideo(frame, filtro)

                if sticker is None:
                    frameModificado = setFiltroVideo(frame, filtro)
                else:
                    # apply the filter to the sticker
                    if opcao == '1':
                        frameModificado = stk.overlay(frame, sticker, x, y)
                        frameModificado = setFiltroVideo(frameModificado, filtro)
                    # does not apply the filter to the sticker
                    else:
                        frameModificado = setFiltroVideo(frame, filtro)
                        frameModificado = stk.overlay(frameModificado, sticker, x, y)
                
                # Display the resulting frame
                cv.imshow('video', frameModificado)

                key = cv.waitKey(1) & 0xFF

                if key == ord('q'):
                    # erase the sticker and filter so it does not start in the next video
                    sticker = None
                    filtro = None
                    break
                elif key == ord('f'):
                    # Print the options of filters
                    filtro = opcoesFiltro()

                    if filtro == '6' or filtro == '7':
                        print('Escolha uma opcao de tamanho de kernel: (quanto maior, mais blur terá)')
                        print('1 - 5x5')
                        print('2 - 9x9')
                        print('3 - 15x15')
                        kernel = input()
                    elif filtro == '3':
                        print('Insira o linear que deverá ser considerado:')
                        l = int(input())

                    if sticker is not None:
                        # Ask if the filter should be applied to the sticker or not
                        opcao = addFilterToStickerVideo()
                        # Print the keyboard actions
                        opcoesVideo()
                        opcoesMovimentoSticker()
                    else:
                        # Print the keyboard actions
                        opcoesVideo()

                elif key == ord('b'):
                    save_image(frameModificado, 'video')
                    if sticker is not None:
                        # Print the keyboard actions
                        opcoesVideo()
                        opcoesMovimentoSticker()
                    else:
                        # Print the keyboard actions
                        opcoesVideo()

                elif key == ord('i'):
                    sticker = opcoesStickers()

                    # Ask if the filter should be applied to the sticker or not
                    opcao = addFilterToStickerVideo()

                    # Print the keyboard actions
                    opcoesVideo()
                    opcoesMovimentoSticker()

                # se clicar A, move o sticker para a esquerda
                elif key == ord('a'):
                    if sticker is not None and x-15 >= 0:
                        x -= 15
                # se clicar S, move o sticker para baixo
                elif key == ord('s'):
                    if sticker is not None and y+15 < 600:
                        y += 15
                # se clicar W, move o sticker para cima
                elif key == ord('w'):
                    if sticker is not None and y-15 >= 0:
                        y -= 15
                # se clicar D, move o sticker para a direita
                elif key == ord('d'):
                    if sticker is not None and x+15 < 800:
                        x += 15

            # After the loop release the cap object
            capture.release()
            # Verify if the user would like to save the last frame of the video
            save_image(frameModificado, 'video')
            # Destroy all windows
            cv.destroyAllWindows()
        
        # Add sticker first
        else:
            sticker = opcoesStickers()

            capture = cv.VideoCapture(0)
            if not capture.isOpened():
                print('Unable to open')
                exit(0)

            # Change the window size of the video
            capture.set(cv.CAP_PROP_FRAME_WIDTH, 800)
            capture.set(cv.CAP_PROP_FRAME_HEIGHT, 800)
                
            # Print the keyboard actions
            opcoesVideo()
            opcoesMovimentoSticker()

            while True:
                ret, frame = capture.read()
                if frame is None:
                    break
                
                if filtro is None:
                    frameModificado = stk.overlay(frame, sticker, x, y)
                else:
                    # apply the filter to the sticker
                    if opcao == '1':
                        frameModificado = stk.overlay(frame, sticker, x, y)
                        frameModificado = setFiltroVideo(frameModificado, filtro)
                    # does not apply the filter to the sticker
                    else:
                        frameModificado = setFiltroVideo(frame, filtro)
                        frameModificado = stk.overlay(frameModificado, sticker, x, y)

                # Display the resulting frame
                cv.imshow('video', frameModificado)

                key = cv.waitKey(1) & 0xFF

                if key == ord('q'):
                    # erase the sticker and filter so it does not start in the next video
                    sticker = None
                    filtro = None
                    break

                elif key == ord('f'):
                    # Print the options of filters
                    filtro = opcoesFiltro()

                    if filtro == '6' or filtro == '7':
                        print('Escolha uma opcao de tamanho de kernel: (quanto maior, mais blur terá)')
                        print('1 - 5x5')
                        print('2 - 9x9')
                        print('3 - 15x15')
                        kernel = input()
                    elif filtro == '3':
                        print('Insira o linear que deverá ser considerado:')
                        l = int(input())
                    
                    # Ask if the filter should be applied to the sticker or not
                    opcao = addFilterToStickerVideo()

                    # Print the keyboard actions
                    opcoesVideo()
                    opcoesMovimentoSticker()

                elif key == ord('b'):
                    save_image(frameModificado, 'video')
                    # Print the keyboard actions
                    opcoesVideo()
                    opcoesMovimentoSticker()

                elif key == ord('i'):
                    sticker = opcoesStickers()

                    if filtro is not None:
                        # Ask if the filter should be applied to the sticker or not
                        opcao = addFilterToStickerVideo()

                    opcoesVideo()
                    opcoesMovimentoSticker()

                # se clicar A, move o sticker para a esquerda
                elif key == ord('a'):
                    if sticker is not None and x-15 >= 0:
                        x -= 15
                # se clicar S, move o sticker para baixo
                elif key == ord('s'):
                    if sticker is not None and y+15 < 600:
                        y += 15
                # se clicar W, move o sticker para cima
                elif key == ord('w'):
                    if sticker is not None and y-15 >= 0:
                        y -= 15
                # se clicar D, move o sticker para a direita
                elif key == ord('d'):
                    if sticker is not None and x+15 < 800:
                        x += 15

            # After the loop release the cap object
            capture.release()
            # Verify if the user would like to save the last frame of the video
            save_image(frameModificado, 'video')
            # Destroy all windows
            cv.destroyAllWindows()
            
    # Actions - option to paste sticker or add filter
    print('\nEscolha uma opcao:\n')
    print('0 - Sair')
    print('1 - Aplicar Filtro')
    print('2 - Colar Sticker')

    acao = input()

       
