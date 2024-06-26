import cv2 as cv
import sys
from metodos import filtros as ft
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
import os

# Path to the stickers directory
STICKERS_DIR = 'stickers/'  # Ensure this path is correct
STICKER_MAX_SIZE = 50  # Define the maximum size for the larger dimension of the stickers

# Function to load and resize stickers while maintaining the aspect ratio
def load_stickers():
    stickers = []
    for filename in os.listdir(STICKERS_DIR):
        if filename.endswith(".png"):
            sticker_path = os.path.join(STICKERS_DIR, filename)
            sticker = cv.imread(sticker_path, cv.IMREAD_UNCHANGED)
            if sticker is not None:
                # Calculate the scaling factor to maintain the aspect ratio
                h, w = sticker.shape[:2]
                scaling_factor = STICKER_MAX_SIZE / max(h, w)
                new_size = (int(w * scaling_factor), int(h * scaling_factor))
                sticker = cv.resize(sticker, new_size, interpolation=cv.INTER_AREA)
                stickers.append((filename, sticker))
    return stickers

# Function to choose an image
def choose_image():
    Tk().withdraw()
    filename = askopenfilename()
    return filename

# Function to overlay stickers on the image
def overlay(background, foreground, x_offset=None, y_offset=None):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    # Center the sticker by default
    if x_offset is None: x_offset = (bg_w - fg_w) // 2
    if y_offset is None: y_offset = (bg_h - fg_h) // 2

    # Ensure x_offset and y_offset are within the bounds of the background image
    x_start = max(0, x_offset)
    y_start = max(0, y_offset)
    x_end = min(bg_w, x_offset + fg_w)
    y_end = min(bg_h, y_offset + fg_h)

    # Calculate the region of interest for the foreground and background images
    fg_roi = foreground[y_start - y_offset:y_end - y_offset, x_start - x_offset:x_end - x_offset]
    bg_roi = background[y_start:y_end, x_start:x_end]

    # Separate alpha and color channels from the foreground image
    foreground_colors = fg_roi[:, :, :3]
    alpha_channel = fg_roi[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # Construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # Combine the background with the overlay image weighted by alpha
    composite = bg_roi * (1 - alpha_mask) + foreground_colors * alpha_mask

    # Overwrite the section of the background image that has been updated
    background[y_start:y_end, x_start:x_end] = composite
    return background

def mouse_click(event, x, y, flags, param):
    global img, sticker, stickers

    if event == cv.EVENT_LBUTTONDOWN:
        if sticker is not None:
            img = overlay(img, sticker, x, y)
            cv.imshow('image', img)

# Initialize global variables
img = None
sticker = None

# Start - option to send image or record video
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

# Actions - option to paste sticker or add filter
print('\nEscolha uma opcao:\n')
print('0 - Sair')
print('1 - Aplicar Filtro')
print('2 - Colar Sticker')

acao = input()
texto = 'original'

stickers = load_stickers()
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
        print("\nEscolha um sticker:\n")
        for i, (name, _) in enumerate(stickers):
            print(f"{i} - {name}")

        sticker_index = int(input())
        sticker = stickers[sticker_index][1]

        print("Clique na imagem para posicionar o sticker.")
        cv.imshow('image', img)
        cv.setMouseCallback('image', mouse_click)

        
        # Wait until a key is pressed to proceed
        cv.waitKey(0)
        cv.destroyAllWindows()

    # Actions - option to paste sticker or add filter
    print('\nEscolha uma opcao:\n')
    print('0 - Sair')
    print('1 - Aplicar Filtro')
    print('2 - Colar Sticker')

    acao = input()

       
