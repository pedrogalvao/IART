Para testar o programa cria-se um objeto da classe Test:
test = Test()
Em seguida invoca-se uma das seguintes funções para testar e treinar o agente em jogos contra-si mesmo, contra o Minimax ou apenas observando as jogadas efetuadas pelo Minimax:
test.testDQN()
test.testMinimaxDQN()
test.testMinimax()


Para mudar o número de episodios em cada teste:
test.episodes = n
Para testar o output da rede para um input específico (no formato (6,6,5)):
test.dqnagent.model.predict(input)
Para testar a ação do agente em um tabuleiro específico:
test.dqnagent.act(board)