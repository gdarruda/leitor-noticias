class LogErros:
  'Classe para log de erros das execucoes do crawler'

  def __init__(self, bd):
    self.bd = bd
    self.id_execucao = 0

  def inicia_processo(self):
    #Insere um novo registro de execucao e recupera o ID
    self.id_execucao = self.bd.adiciona_execucao()

  def registra_erro(self, texto):
   #Insere um novo erro no log
   self.bd.adiciona_erro_execucao(self.id_execucao, texto)
