def grayscale(img):
    for i in range(img.shape[0]): # percorre as linhas
        for j in range(img.shape[1]): # percorre as colunas
            # são os canais (RGB mas aqui é invertido, fica BGR)
            media = img[i, j, 0] * 0.33 + img[i, j, 1] * 0.33 + img[i, j, 2] * 0.33
            img[i, j, 0] = media # canal azul - 0 - B
            img[i, j, 1] = media # canal verde - 1 - G
            img[i, j, 2] = media # canal vermelho - 2 - R

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
