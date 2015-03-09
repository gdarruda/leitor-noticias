import mysql.connector
import time
from datetime import date


class BancoDados:

    'Classe abstrata para manipulacao de banco de dados'


class BancoMySQL(BancoDados):

    'Classe para manipulacao de banco de dados em MySQL'

    def __init__(self, usuario, senha, host, banco):
        self.conexao = mysql.connector.connect(user=usuario, password=senha, host=host, database=banco, buffered=True)

    def conta_noticias(self, link):

        contador_noticia = self.conexao.cursor()

        query_noticia = ('select count(*) from noticias where link =  %s')
        contador_noticia.execute(query_noticia, (link,))

        return contador_noticia

    def adiciona_noticia(self, link, titulo, texto_limpo, tweet, id_feed, id_perfil):

        cursor_noticia = self.conexao.cursor()

        insert_noticia = ('insert into noticias (link, titulo, corpo, tweet, data_importacao, id_feed, id_perfil) values (%s, %s, %s, %s, %s, %s, %s)')
        dados_noticia = (link, titulo, texto_limpo, tweet, date(int(time.strftime('%y')), int(time.strftime('%m')), int(time.strftime('%d'))), id_feed, id_perfil)

        cursor_noticia.execute(insert_noticia, dados_noticia)

        self.conexao.commit()

        return cursor_noticia.lastrowid

    def procura_entidade(self, entidade):

        cursor_entidade = self.conexao.cursor()

        query_entidade = ('select id_entidade from entidades where nome = %s')
        cursor_entidade.execute(query_entidade, (entidade,))

        return cursor_entidade

    def adiciona_entidade(self, nome, tipo):

        cursor_entidade = self.conexao.cursor()

        insert_entidade = (
            'insert into entidades (nome, tipo) values (%s, %s)')
        dados_entidade = (nome, tipo)

        cursor_entidade.execute(insert_entidade, dados_entidade)

        self.conexao.commit()

        return cursor_entidade.lastrowid

    def adiciona_entidade_noticia(self, id_noticia, id_entidade):

        cursor_entidade_noticia = self.conexao.cursor()

        insert_entidade_noticia = ('insert ignore into entidades_x_noticias (id_noticia, id_entidade) values (%s, %s)')
        dados_entidade_noticia = (id_noticia, id_entidade)

        cursor_entidade_noticia.execute(
            insert_entidade_noticia, dados_entidade_noticia)

        self.conexao.commit()

    def procura_feeds(self):

        cursor_feeds = self.conexao.cursor()

        query_feeds = (
            'select id_feed, link from feeds where ind_ativo = \'S\'')
        cursor_feeds.execute(query_feeds)

        return cursor_feeds

    def procura_perfis(self):

        cursor_tweets = self.conexao.cursor()

        query_tweets = ('select id_perfil, nome from perfis_twitter where ind_ativo = \'S\'')
        cursor_tweets.execute(query_tweets)

        return cursor_tweets

    def adiciona_execucao(self):

        cursor_execucao = self.conexao.cursor()

        data_execucao = date(int(time.strftime('%y')), int(time.strftime('%m')), int(time.strftime('%d')),)

        cursor_execucao.execute('insert into log_execucoes (data_execucao) values (%s)', (data_execucao,))

        self.conexao.commit()

        return cursor_execucao.lastrowid

    def adiciona_erro_execucao(self, id_execucao, descricao):

        cursor_erro = self.conexao.cursor()

        insert_erro = ('insert into log_execucoes_deta (id_execucao, descricao) values (%s,%s)')
        dados_erro = (id_execucao, descricao)

        cursor_erro.execute(insert_erro, dados_erro)

        self.conexao.commit()

    def seleciona_noticias(self):

        cursor_noticias = self.conexao.cursor()

        query_noticias = ('select corpo, id_noticia from noticias where corpo != \'\' order by id_noticia desc')
        cursor_noticias.execute(query_noticias)

        return cursor_noticias

    def fecha_conexao(self):

        self.conexao.close()
