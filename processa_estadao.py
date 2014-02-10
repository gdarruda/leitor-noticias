 # coding=utf-8
import re

def html_texto(html):
	
	#Remove caracteres de quebra de linha especificios
	html = html.replace('&#13;', '')

	#Separa o texto em paragrados
	paragrafos = html.split('<p>')

	#Texto limpo
	texto_limpo = ''

	for paragrafo in paragrafos:

		#Verifica se o paragrafo eh referente aos links relacionados presentes no meio da materia
		if paragrafo.find('Veja também:') > -1:
			continue
		
		#Remove as TAGs desnecessarias
		texto_limpo =  texto_limpo + re.sub('<.*?>', '', paragrafo)

	return texto_limpo

		