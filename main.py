import cv2 as cv
import sys
from metodos import filtros as ft

from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np

import numpy as np
import cv2 as cv


def choose_image():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    return filename

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

#  ACOES - OPCAO DE COLAR STICKER OU ADICIONAR FILTRO
print('\nEscolha uma opcao:\n')
print('0 - Sair')
print('1 - Aplicar Filtro')
print('2 - Colar Sticker')

acao = input()
texto = 'original'

while(acao != '0'):
    
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
            if opcao == '1':
                img_com_filtro = ft.grayscale(img)
                texto = 'Grayscale'
                
            elif opcao == '2':
                img_com_filtro = ft.negativo(img)
                texto = 'Negativo'
                
            elif opcao == '3':
                print('Insira o linear que deverá ser considerado:')
                l = int(input())
                img_com_filtro = ft.binarizacao(img, l)
                texto = 'Binarizacao'
                
            elif opcao == '4':
                cor = [242, 33, 33]
                img_com_filtro = ft.colorizacao(img, cor)
                texto = 'Rosado'
                
            elif opcao == '5':
                img_com_filtro = ft.equalizacao_hist(img)
                texto = 'Equalizacao de um histograma'
                
            elif opcao == '6' or opcao == '7':
                print('Escolha uma opcao de tamanho de kernel: (quanto maior, mais blur terá)')
                print('1 - 5x5')
                print('2 - 9x9')
                print('3 - 15x15') 
                kernel = input()
                
                if opcao == '6':
                    img_com_filtro = ft.average_blur(img, kernel)
                    texto = 'Average blur'
                else:
                    img_com_filtro = ft.gaussian_blur(img, kernel)
                    texto = 'Gaussian blur'
                        
            elif opcao == '8':
                img_com_filtro = ft.bordas_canny(img)
                texto = 'Deteccao de bordas com Canny'
            
            elif opcao == '9':
                img_com_filtro = ft.dilatacao_bordas(img)
                texto = 'Dilatacao de bordas Canny'
                
            else:
                img_com_filtro = ft.erosao(img)
                texto = 'Erosao das bordas'
            
            cv.imshow(texto, img_com_filtro)
            k = cv.waitKey(0)

            print('Você deseja salvar essa foto?')
            print('1 - Sim')
            print('2 - Nao')
            salvar = input()

            if salvar == '1':
                print('Digite o nome do arquivo que será salvo:')
                arquivo = input()
                arquivo = arquivo + '.jpg'
                cv.imwrite(arquivo, img_com_filtro)
                print('Salvo!')

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
            while True:
                ret, frame = capture.read()
                if frame is None:
                    break

                if opcao == '1':
                    frame_com_filtro = ft.grayscale(frame)
                    texto = 'Grayscale'
                
                elif opcao == '2':
                    frame_com_filtro = ft.negativo(frame)
                    texto = 'Negativo'
                    
                elif opcao == '3':
                    frame_com_filtro = ft.binarizacao(frame, l)
                    texto = 'Binarizacao'
                    
                elif opcao == '4':
                    cor = [242, 33, 33]
                    frame_com_filtro = ft.colorizacao(frame, cor)
                    texto = 'Rosado'
                    
                elif opcao == '5':
                    frame_com_filtro = ft.equalizacao_hist(frame)
                    texto = 'Equalizacao de um histograma'
                    
                elif opcao == '6':
                    frame_com_filtro = ft.average_blur(frame, kernel)
                    texto = 'Average blur'
                elif opcao == '7':
                    frame_com_filtro = ft.gaussian_blur(frame, kernel)
                    texto = 'Gaussian blur'
                            
                elif opcao == '8':
                    frame_com_filtro = ft.bordas_canny(frame)
                    texto = 'Deteccao de bordas com Canny'
                
                elif opcao == '9':
                    frame_com_filtro = ft.dilatacao_bordas(frame)
                    texto = 'Dilatacao de bordas Canny'
                    
                else:
                    frame_com_filtro = ft.erosao(frame)
                    texto = 'Erosao das bordas'
                # Display the resulting frame
                cv.imshow(texto, frame_com_filtro)

                # the 'q' button is set as the
                # quitting button you may use any
                # desired button of your choice
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

            print('Você deseja salvar o último frame do vídeo?')
            print('1 - Sim')
            print('2 - Nao')
            salvar = input()

            if salvar == '1':
                print('Digite o nome do arquivo que será salvo:')
                arquivo = input()
                arquivo = arquivo + '.jpg'
                cv.imwrite(arquivo, frame_com_filtro)
                print('Salvo!')

            # After the loop release the cap object
            capture.release()
            # Destroy all the windows
            cv.destroyAllWindows()
        
    elif acao == '2':
        print("sticker")

    #  ACOES - OPCAO DE COLAR STICKER OU ADICIONAR FILTRO
    print('\nEscolha uma opcao:\n')
    print('0 - Sair')
    print('1 - Aplicar Filtro')
    print('2 - Colar Sticker')  
    
    acao = input()