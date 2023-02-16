import hd_model as hd
# ################ Exemplos e utilizaçãp
# # Exemplo 1 - Titanio
# # Entrada
# M       = 'Titânio Gr1'
# E       = 72000                                     #{MPa] Módulo de Elasticidade
# Sy      = 183                                       #[MPa] Limite de Escoamento
# Sut     = 287                                       #[MPa] Tensão máxima a tração
# emax    = 40                                        #[%]   Deformação onde ocorre o Sut
# pontos_multi = [4,5,7,10,20,28]                     #Pontos para o modelo multilinear
# Nome_imagem, formato = ['Modelos','.png']
# h       = Hardening(M,E,Sy,Sut,emax)                  # define as constantes do material
# exp     = h.Experimental('ensaio_longitudinal_titanio.txt') # puxa os dados do experimental Stress vs Strain, pode usar o método Abrir_Arquivos
# #exp     = h.Experimental(h.Abrir_Arquivos())
# h.DataFrame()                                       # Data frame com a curva de engenharia e a real
# #bili    = h.Bilinear()                              # Modelo Bilinear
# multi   = h.Multilinear(pontos_multi)               # Modelo Multilinear
# model   = h.Modelos(Nome_imagem,formato)            # Prepara a imagem
# img     = h.Imagem()                                # Mostra a imagem


# Exemplo 2 - 316L
M2 = '316L'
E2 = 200000
Sy2 = 290
Sut2 = 560
emax2 = 40
h2       = hd.Hardening(M2,E2,Sy2,Sut2,emax2)
exp2     = h2.Experimental('ensaio_longitudinal_316L.txt') # puxa os dados do experimental Stress vs Strain, pode usar o método Abrir_Arquivos
h2.DataFrame()
#bili2    = h2.Bilinear()
pontos_multi2 = [5,10,13,20,40]
multi2 = h2.Multilinear(pontos_multi2)
Nome_imagem2, formato2 = ['Modelos2','.png']
model2 = h2.Modelos(Nome_imagem2,formato2)
img2     = h2.Imagem()