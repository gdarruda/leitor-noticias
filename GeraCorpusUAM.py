from lxml import etree
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import csv

class GeraCorpus(object):
  'Gera o diretorio de corpus para ser utilizado junto ao MetaAnn'

  def __init__(self, bd):
    self.bd = bd

  def carrega_lista_noticias(self):

    #Cria conjunto de noticias
    noticias_incluidas = set()

    #Monta dicionario para verificar se determinada noticia eh elegivel
    with open(os.path.join('noticias_incluidas','corpus.csv')) as arquivocsv:

      #Transforma em um objeto iteravel
      linhas = csv.reader(arquivocsv, delimiter=';')

      for linha in linhas:

        #Se a linha for 'Incluida', adiciona a colecao
        if linha[1] == 'Incluida':
          noticias_incluidas.add(int(linha[0]))

    return noticias_incluidas

  def gera_noticias(self):

    #Recuperar as noticias a serem incluidas no corpus
    noticias_incluidas = self.carrega_lista_noticias()

    #Procura todas as noticias extraidas pelo sistema
    cursor_noticias = self.bd.seleciona_noticias()

    caminho = 'UAM'

    # Se nao houver o diretorio C1, cria o diretorio
    if not os.path.exists(caminho):
      os.makedirs(caminho)

    #Percorre todas elas e gera os arquivos textos
    for (corpo_noticia, id_noticia) in cursor_noticias:

      #Processa se a noticia for selecionada para geracao do corpus
      if not id_noticia in noticias_incluidas:
        continue

      #Gera o arquivo com o ID da noticia
      arquivo_noticia = open(os.path.join(caminho, str(id_noticia) + '.txt'),'w')
      arquivo_noticia.write(corpo_noticia.encode('utf-8'))
      arquivo_noticia.close()
