import cv2 as cv

def grayscale(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def negativo(img):
    # muda a cor de pixel a pixel
    for i in range(img.shape[0]): # percorre as linhas
        for j in range(img.shape[1]): # percorre as colunas
            # Negativo
            img[i, j, 0] = img[i, j, 0] ^ 255 # canal azul - 0 - B
            img[i, j, 1] = img[i, j, 1] ^ 255 # canal verde - 1 - G
            img[i, j, 2] = img[i, j, 2] ^ 255 # canal vermelho - 2 - R

def binarizacao(img, l):
    # Binarização - pego a média porque primeiro passo pra grayscale. Senão, uso só um canal
    for i in range(img.shape[0]): # percorre as linhas
        for j in range(img.shape[1]): # percorre as colunas
            media = img[i, j, 0] * 0.33 + img[i, j, 1] * 0.33 + img[i, j, 2] * 0.33

            img[i, j, 0] = media # canal azul - 0 - B
            img[i, j, 1] = media # canal verde - 1 - G
            img[i, j, 2] = media # canal vermelho - 2 - R

            # se menor que o meu linear, deixo como preto
            if img[i, j, 0] < l:
                img[i, j, 0] = 0 # canal azul - 0 - B
                img[i, j, 1] = 0 # canal verde - 1 - G
                img[i, j, 2] = 0 # canal vermelho - 2 - R
            else: # se for maior que o linear K, fica branco
                img[i, j, 0] = 255 # canal azul - 0 - B
                img[i, j, 1] = 255 # canal verde - 1 - G
                img[i, j, 2] = 255 # canal vermelho - 2 - R

def colorizacao(img, cor):
    for i in range(img.shape[0]): # percorre as linhas
        for j in range(img.shape[1]): # percorre as colunas
            img.itemset((i,j,0),img.item(i,j,0) | cor[0]) # canal azul - 0 - B
            img.itemset((i,j,1),img.item(i,j,1) | cor[1]) # canal verde - 1 - G
            img.itemset((i,j,2),img.item(i,j,2) | cor[2]) # canal vermelho - 2 - R
            
def equalizacao_hist(img):
    cinza = grayscale(img)
    return cv.equalizeHist(cinza) # equaliza uma imagem que esta em grayscale e que tenha 1 canal apenas