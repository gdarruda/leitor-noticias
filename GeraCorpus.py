from lxml import etree
import os
import re

class GeraCorpus(object):
  'Gera o diretorio de corpus para ser utilizado junto ao MetaAnn'

  def __init__(self, bd):
    self.bd = bd
    self.contador_segmento = 1

  def gera_id_documento(self, contador_noticia, prefixo):

    #Transforma o numero contador em uma string
    contador_string = str(contador_noticia)

    #Se a noticia for maior que 99, apenas concatenam, senao preenche com zeros
    if contador_noticia > 99:
      return prefixo + contador_string
    else:
      return prefixo + contador_string.zfill(3)

  def gera_xml_documento(self, corpo_noticia, contador_noticia):

    #Cria a raiz do documento
    documento = etree.Element('plainDocument')

    #Cria os campos fixos do xml
    documento.append(etree.Element('info', type='id', value=self.gera_id_documento(contador_noticia,'R')))

    #Adiciona o texto da noticia
    texto = etree.Element('text')
    texto.text = corpo_noticia
    documento.append(texto)

    #Retorna o documento formatado
    return etree.tostring(documento, pretty_print = True, xml_declaration=True, encoding="UTF-8")

  def gera_nome_source(self, contador_noticia):

    return 'src_' + self.gera_id_documento(contador_noticia,'R') + '_C1_' + self.gera_id_documento(contador_noticia,'a') + '.xml'

  def gera_xml_segmentacao(self, corpo_noticia, contador_noticia):

    #Cria a raiz da segmentacao
    segmentacao = etree.Element('document')

    #Cria os campos fixos do xml
    segmentacao.append(etree.Element('info', type='id', value='{0:0{1}d}'.format(contador_noticia,4)))
    segmentacao.append(etree.Element('info', type='scheme', value='clause01'))
    segmentacao.append(etree.Element('info', type='source', value=self.gera_id_documento(contador_noticia,'R')))
    segmentacao.append(etree.Element('info', type='source-corpus', value='C1'))

    #Remove as quebras de linha
    corpo_noticia = corpo_noticia.replace('\n',' ')

    #Segmenta noticia a partir de pontos de final de frase
    regexp_pontuacao = re.compile('(?<=[.!?]) +')
    noticia_segmentada = regexp_pontuacao.split(corpo_noticia)

    #Gera o xml para cada noticia
    for segmento in noticia_segmentada:
      #Cria o XML do segmento
      xml_segmento = etree.Element('unit', id='{0:0{1}d}'.format(self.contador_segmento,4))
      xml_segmento.text = segmento

      #Adiciona o segmento ao xml criado
      segmentacao.append(xml_segmento)

      self.contador_segmento+=1

    #Retorna a segmentacao formatada
    return etree.tostring(segmentacao, pretty_print = True, xml_declaration=True, encoding="UTF-8")

  def gera_nome_segmentacao(self, contador_noticia):

    return 'seg_' + '{0:0{1}d}'.format(contador_noticia,4) + '_clause01_C1_' + self.gera_id_documento(contador_noticia,'R') + '_res.xml'

  def gera_noticias(self):

    #Procura todas as noticias extraidas pelo sistema
    cursor_noticias = self.bd.seleciona_noticias()

    #Contador de noticicas
    i = 1

    #Diretorio de textos fonte
    caminho_source = 'C1'
    caminho_segmentacao = 'clause01'

    #Percorre todas elas e gera o XML
    for (corpo_noticia,) in cursor_noticias:

      #Se nao houver o diretorio C1, cria o diretorio
      if not os.path.exists(caminho_source):
        os.makedirs(caminho_source)

      #Novo arquivo para cada nova noticia
      arquivo_noticia = open(os.path.join(caminho_source, self.gera_nome_source(i)),'w')
      arquivo_noticia.write(self.gera_xml_documento(corpo_noticia,i))
      arquivo_noticia.close()

      if not os.path.exists(caminho_segmentacao):
        os.makedirs(caminho_segmentacao)

      arquivo_segmentacao = open(os.path.join(caminho_segmentacao, self.gera_nome_segmentacao(i)),'w')
      arquivo_segmentacao.write(self.gera_xml_segmentacao(corpo_noticia,i))
      arquivo_segmentacao.close()

      i+=1
