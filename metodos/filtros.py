
def grayscale(img):
    for i in range(img.shape[0]): # percorre as linhas
        for j in range(img.shape[1]): # percorre as colunas
            # sao os canais (RGB mas aqui é invertido, fica BGR)
            media = img.item(i,j,0) * 0.33 + img.item(i,j,1) * 0.33 + img.item(i,j,2) * 0.33
            img.itemset((i,j,0),media) # canal azul - 0 - B
            img.itemset((i,j,1),media) # canal verde - 1 - G
            img.itemset((i,j,2),media) # canal vermelho - 2 - R

def negativo(img):
    # muda a cor de pixel a pixel
    for i in range(img.shape[0]): # percorre as linhas
        for j in range(img.shape[1]): # percorre as colunas
            # Negativo
            img.itemset((i,j,0),img.item(i,j,0) ^ 255) # canal azul - 0 - B
            img.itemset((i,j,1),img.item(i,j,1) ^ 255) # canal verde - 1 - G
            img.itemset((i,j,2),img.item(i,j,2) ^ 255) # canal vermelho - 2 - R