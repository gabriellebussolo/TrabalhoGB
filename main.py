import cv2 as cv
import sys
from metodos import filtros as ft

## TODO - fazer a parte que escolhe imagem e grava video

img = cv.imread('imagem-teste.png')
img2 = img.copy() # cria uma copia da original

print('Escolha uma opcao de filtro:\n')
print('0 - Sair')
print('1 - Grayscale\n')
print('2 - Negativo')

opcao = input()

while(opcao != '0'):
    if opcao == '1':
        ft.grayscale(img2)
        cv.imshow('Grayscale', img2)
        k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
    elif opcao == '2':
        ft.negativo(img2)
        cv.imshow('Negativo', img2)
        k = cv.waitKey(0) # faz com que se eu clicar em qualquer tecla a imagem feche
    opcao = input()
