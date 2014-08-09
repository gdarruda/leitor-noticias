# coding=utf-8
import urllib
import ProcessadorHTML

def extrai_link(tweet):

	#Encontra a URL do Tweet
	posic_url_ini = tweet.find('http://')

	#Se nao encontrou nenhuma posicao, retorna nulo
	if posic_url_ini == -1:
		return None

	#Encontra o primeiro espaco depois do inicio do link
	posic_url_fim = tweet.find(' ', posic_url_ini) + 1

	#Retorna o inicio da URL ate o primeiro espaco ou fim
	if posic_url_fim == 0:
		return tweet[posic_url_ini:]
	else:
		return tweet[posic_url_ini:posic_url_fim]


def url_importada(link, bd):

	#Verifica se a URL já está presente no Banco de Dados
	count_noticia = bd.conta_noticias(link)

	#Retorna o contador
	return count_noticia.fetchone()[0] > 0
