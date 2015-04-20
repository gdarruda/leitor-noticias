import semantria
import nltk

class IdentificadorEntidades(object):

    def __init__(self, bd):
        self.bd = bd
        self.semantria_key = 'ea19dcd8-eeaa-456d-9679-a7e374f0423e'
        self.semantria_secret = 'c41f1570-705a-4dba-b0f7-cbbb0fecb6b8'
        self.tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        self.serializer = semantria.JsonSerializer()
        self.session = semantria.Session(self.semantria_key, self.semantria_secret, self.serializer, use_compression=True)

    def retorna_chave(self, id_noticia):

        if '_' in id_noticia:
            return id_noticia[:id_noticia.index('_')]
        else:
            return id_noticia

    def atualiza_entidades(self):

        total_noticias = 0
        resultados = list()

        for (id_noticia, corpo) in self.bd.seleciona_noticias_corpus():

            texto_noticia = ''
            contador = 1

            for sentenca in self.tokenizer.tokenize(corpo):

                if len(texto_noticia + sentenca) < 8192:
                    texto_noticia = texto_noticia + sentenca
                else:
                    documento = {'id':str(id_noticia) + '_' + str(contador), 'text':texto_noticia}
                    status = self.session.queueDocument(documento)

                    if status == 202:
                        print(documento['id'],'Incluido na fila')
                        total_noticias+=1

                    contador+=1
                    texto_noticia = sentenca

            if contador==1:
                documento = {'id':id_noticia, 'text':texto_noticia}
            else:
                documento = {'id':str(id_noticia) + '_' + str(contador), 'text':texto_noticia}

            status = self.session.queueDocument(documento)

            if status == 202:
                print(documento['id'],'Incluido na fila')
                total_noticias+=1

        while len(resultados) < total_noticias:

            status = self.session.getProcessedDocuments()
            resultados.extend(status)

        # print (resultados)

        for resultado in resultados:

            if 'entities' in resultado:

                for entidade in resultado['entities']:

                    entidade_banco = self.bd.procura_entidade_semantria(entidade['title']).fetchone()

                    if entidade_banco != None:
                        id_entidade = entidade_banco[0]
                    else:
                        id_entidade = self.bd.adiciona_entidade_semantria(entidade['title'], entidade['entity_type'])

                    self.bd.adiciona_entidade_noticia_semantria(self.retorna_chave(resultado['id']), id_entidade)
            else:
                print('Sem entidade:', resultado['id'])
