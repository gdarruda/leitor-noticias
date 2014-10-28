from lxml import etree
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import csv


class GeraCorpus(object):

    'Gera o diretorio de corpus para ser utilizado junto ao MetaAnn'

    def __init__(self, bd):
        self.bd = bd
        self.contador_segmento = 1
        self.desconto_segmento = 0

    def carrega_lista_noticias(self):

        # Cria conjunto de noticias
        noticias_incluidas = set()

        # Monta dicionario para verificar se determinada noticia eh elegivel
        with open(os.path.join('noticias_incluidas', 'corpus.csv')) as arquivocsv:

            # Transforma em um objeto iteravel
            linhas = csv.reader(arquivocsv, delimiter=';')

            # Para cada linha, cria um dicionario
            for linha in linhas:

                if linha[1] == 'Incluida':
                    noticias_incluidas.add(int(linha[0]))

            return noticias_incluidas

    def gera_id_documento(self, contador_noticia, prefixo):

        # Transforma o numero contador em uma string
        contador_string = str(contador_noticia)

        # Se a noticia for maior que 99, apenas concatenam, senao preenche com
        # zeros
        if contador_noticia > 99:
            return prefixo + contador_string
        else:
            return prefixo + contador_string.zfill(3)

    def gera_xml_documento(self, corpo_noticia, contador_noticia, id_noticia):

        # Cria a raiz do documento
        documento = etree.Element('plainDocument')

        # Cria os campos fixos do xml
        documento.append(etree.Element(
            'info', type='id', value=self.gera_id_documento(contador_noticia, 'R')))
        documento.append(
            etree.Element('info', type='banco_id', value=str(id_noticia)))

        # Adiciona o texto da noticia
        texto = etree.Element('text')
        texto.text = corpo_noticia
        documento.append(texto)

        # Retorna o documento formatado
        return etree.tostring(documento, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    def gera_nome_source(self, contador_noticia):

        return 'src_' + self.gera_id_documento(contador_noticia, 'R') + '_C1_' + self.gera_id_documento(contador_noticia, 'a') + '.xml'

    def eh_repeticao(self, id_segmento, matriz_similaridade):

        # Verifica se passa do limiar de similaridade
        for i, similaridade in enumerate(matriz_similaridade[id_segmento]):

            # Se a similaridade for maior que limiar
            if similaridade > 0.8:

                # Gera apenas uma vez segmentos similare
                return i < id_segmento

    def gera_xml_segmentacao(self, dicionario_segmentos, contador_noticia, matriz_similaridade):

        # Cria a raiz da segmentacao
        segmentacao = etree.Element('document')

        # Cria os campos fixos do xml
        segmentacao.append(
            etree.Element('info', type='id', value='{0:0{1}d}'.format(contador_noticia, 4)))
        segmentacao.append(
            etree.Element('info', type='scheme', value='clause01'))
        segmentacao.append(etree.Element(
            'info', type='source', value=self.gera_id_documento(contador_noticia, 'R')))
        segmentacao.append(
            etree.Element('info', type='source-corpus', value='C1'))

        # Gera o xml para cada noticia
        for id_segmento in dicionario_segmentos:

            if id_segmento == -1:
                continue

            if self.eh_repeticao(id_segmento - 1, matriz_similaridade):
                self.desconto_segmento += 1
                continue

            # Cria o XML do segmento
            xml_segmento = etree.Element(
                'unit', id='{0:0{1}d}'.format(id_segmento - self.desconto_segmento, 4))
            xml_segmento.text = dicionario_segmentos[id_segmento]

            # Adiciona o segmento ao xml criado
            segmentacao.append(xml_segmento)

            self.contador_segmento += 1

        # Retorna a segmentacao formatada
        return etree.tostring(segmentacao, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    def gera_nome_segmentacao(self, contador_noticia):

        return 'seg_' + '{0:0{1}d}'.format(contador_noticia, 4) + '_clause01_C1_' + self.gera_id_documento(contador_noticia, 'R') + '_res.xml'

    def gera_noticias(self):

        # Recuperar as noticias a serem incluidas no corpus
        noticias_incluidas = self.carrega_lista_noticias()

        # Procura todas as noticias extraidas pelo sistema
        cursor_noticias = self.bd.seleciona_noticias()

        # Contador de noticicas
        i = 1

        # Diretorio de textos fonte
        caminho_source = 'C1'
        caminho_segmentacao = 'clause01'

        # Lista de segmentos e dicionario de noticias
        lista_segmentos = list()
        dicionario_noticias = dict()

        # Percorre todas elas e gera o XML
        for (corpo_noticia, id_noticia) in cursor_noticias:

            # Processa se a noticia for selecionada para geracao do corpus
            if not id_noticia in noticias_incluidas:
                continue

            # Separa a noticia em paragrafos
            noticia_segmentada = corpo_noticia.split('\n')

            # Dicionario segmentos
            dicionario_segmentos = dict()
            dicionario_segmentos[-1] = corpo_noticia

            # Para cada segmento, adiciona na lista para calculo de tf-idf e
            # adiciona nos segmentos da noticia
            for segmento in noticia_segmentada:
                lista_segmentos.append(segmento)
                dicionario_segmentos[self.contador_segmento] = segmento
                self.contador_segmento += 1

            # Cria um dicionario de noticias
            dicionario_noticias[id_noticia] = dicionario_segmentos

        # Cria a matriz de tf-idf
        tfidf_vectorizer = TfidfVectorizer()
        matriz_tfidf = tfidf_vectorizer.fit_transform(lista_segmentos)
        matriz_similaridade = cosine_similarity(matriz_tfidf, matriz_tfidf)

        # Seleciona os IDs das noticias de forma ordenada
        id_noticias = dicionario_noticias.keys()
        id_noticias.sort(reverse=True)

        # Para cada noticia, gera o arquivo texto
        for id_noticia in id_noticias:

            # Se nao houver o diretorio C1, cria o diretorio
            if not os.path.exists(caminho_source):
                os.makedirs(caminho_source)

            # Novo arquivo para cada nova noticia
            arquivo_noticia = open(
                os.path.join(caminho_source, self.gera_nome_source(i)), 'w')
            arquivo_noticia.write(
                self.gera_xml_documento(dicionario_noticias[id_noticia][-1], i, id_noticia))
            arquivo_noticia.close()

            if not os.path.exists(caminho_segmentacao):
                os.makedirs(caminho_segmentacao)

            arquivo_segmentacao = open(
                os.path.join(caminho_segmentacao, self.gera_nome_segmentacao(i)), 'w')
            arquivo_segmentacao.write(self.gera_xml_segmentacao(
                dicionario_noticias[id_noticia], i, matriz_similaridade))
            arquivo_segmentacao.close()

            i += 1
