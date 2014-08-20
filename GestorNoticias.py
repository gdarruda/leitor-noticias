class GestorNoticias(object):
  'Responsavel por gerir as noticias'

  def __init__(self, bd, api):
    self.bd = bd
    self.api = api

  def adiciona_noticia(self, link, titulo, corpo_noticia, tweet, id_feed, id_perfil):

    #Adiciona noticia no Banco de Dados
    id_noticia = self.bd.adiciona_noticia(link, titulo, corpo_noticia, tweet, id_feed, id_perfil)

    #Recupera as entidades a partir do texto processado da noticia
    entidades = self.api.obtem_entidades(corpo_noticia)

    #Para cada entidade recuperada pela API...
    for entidade in entidades['entities']:

      #Procura se a entidade jah esta presente no banco de dados
      entidade_banco = self.bd.procura_entidade(entidade['text']).fetchone()

      #Se nao estiver, adiciona e recupera o novo ID
      if entidade_banco != None:
        id_entidade = entidade_banco[0] #Pega a primeira coluna da consulta contendo o id da entidade
      else:
        id_entidade = self.bd.adiciona_entidade(entidade['text'], entidade['type']) #Adiciona a nova entidade e pega o seu ID

      #Adiciona entidade por noticias
      self.bd.adiciona_entidade_noticia(id_noticia, id_entidade)
