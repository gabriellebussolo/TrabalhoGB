import cv2 as cv

def grayscale(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY) #converte a imagem para grayscale com um canal

def negativo(img):
    return cv.bitwise_not(img) #inverte cada bit da imagem

def binarizacao(img, l):
    gray = grayscale(img)
    for i in range(gray.shape[0]): # percorre as linhas
        for j in range(gray.shape[1]): # percorre as colunas
            # se menor que o meu linear, deixo como preto
            if gray[i, j] < l:
                gray[i, j] = 0 # canal azul - 0 - B
            else: # se for maior que o linear K, fica branco
                gray[i, j] = 255 # canal azul - 0 - B
    return gray

def colorizacao(img, cor):
    img2 = img.copy()
    for i in range(img2.shape[0]): # percorre as linhas
        for j in range(img2.shape[1]): # percorre as colunas
            img2.itemset((i,j,0),img2.item(i,j,0) | cor[0]) # canal azul - 0 - B
            img2.itemset((i,j,1),img2.item(i,j,1) | cor[1]) # canal verde - 1 - G
            img2.itemset((i,j,2),img2.item(i,j,2) | cor[2]) # canal vermelho - 2 - R
    return img2
            
def equalizacao_hist(img):
    cinza = grayscale(img)
    return cv.equalizeHist(cinza) # equaliza uma imagem que esta em grayscale e que tenha 1 canal apenas

def average_blur(img, opcao):
    if opcao == '1':
        return cv.blur(img, (5,5))
    elif(opcao == '2'):
        return cv.blur(img, (9,9))
    else:
        return cv.blur(img, (15,15))

def gaussian_blur(img, opcao):
    if opcao == '1':
        return cv.GaussianBlur(img, (5,5), 0) #colocando 0 o opencv calcula com base no kernel
    elif(opcao == '2'):
        return cv.GaussianBlur(img, (9,9), 0)
    else:
        return cv.GaussianBlur(img, (15,15), 0)

def bordas_canny(img):
    gray = grayscale(img)
    return cv.Canny(gray, 100, 200)

def dilatacao_bordas(img):
    bordas = bordas_canny(img)
    return cv.dilate(bordas,(9,9),iterations = 1)

def erosao(img):
    bordas = bordas_canny(img)
    return cv.erode(bordas,(15,15),iterations = 1)