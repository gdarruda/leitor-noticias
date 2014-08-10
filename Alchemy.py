from alchemyapi import AlchemyAPI
import URL
import json

class Alchemy(object):
  'Chama API para leitura de feeds Atom RSS'

  def __init__(self):
    #Chamador do AlchemyAPI
    self.alchemy_api = AlchemyAPI()

  def processa_html(self, link):

    #Retorna o texto limpo a partir de uma URL
    return self.alchemy_api.text('url', link)['text']

  def obtem_titulo(self, link):

    #Retorna o texto limpo a partir de uma URL
    return self.alchemy_api.title('url', link)['title']

  def obtem_entidades(self, texto):

    #Retorna as entidaades encontradas no texto
    return self.alchemyapi.entities('text', demo_url, {'sentiment': 1})
