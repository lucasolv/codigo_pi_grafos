#https://colab.research.google.com/gist/chrisgod336/ee53106aa8c9a22cc2403f6e4b5196b6/grafospi.ipynb#scrollTo=R9SpFXEiLHGq

#rodar "pip install requests" no terminal

class Vertice:

  def __init__(self, value):
    self.value = value
    self.checked = 0
    self.edges = []
    self.fathers = None

  def addEdge(self, value):
    if value not in self.edges:
      self.edges.append(value)

  def returnEdges(self):
    return self.edges

class Queue:

  def __init__(self):
    self.struct = []

  def enqueue(self, value):
    self.struct.append(value)

  def dequeue(self):
    return self.struct.pop(0)

  def getSize(self):
      return  len(self.struct)

class Graph:

  def __init__(self):
    self.vertices = {}

  def addVertice(self, value):
    if value not in list(self.vertices.keys()):
      self.vertices[value] = Vertice(value)

  def addEdge(self, value1, value2):
    self.addVertice(value1)
    self.addVertice(value2)

    self.vertices[value1].addEdge(value2)
    self.vertices[value2].addEdge(value1)

  def returnAdjasenceList(self):
    adjasenceList = {}

    for vertice in self.vertices:
      adjasenceList[vertice] = self.vertices[vertice].returnEdges()

    return adjasenceList

  def bfs(self, entry, exit):
    queue = Queue()
    queue.enqueue(entry)
    self.vertices[entry].checked = 1

    while queue.getSize():
      vertice = self.vertices[queue.dequeue()]
      print(vertice.value)
      if vertice.value == exit:
        answer = []
        while vertice.value != entry:
          answer.append(vertice.value)
          vertice = self.vertices[self.vertices[vertice.value].fathers]
          #print('vertice: ',vertice.value)
          #print('resposta: ', answer)
        answer.append(entry)
        response = []
        while len(answer) != 0:
          response.append(answer.pop())
        return response
      for edge in vertice.returnEdges():
        if self.vertices[edge].checked == 0:
          queue.enqueue(edge)
          self.vertices[edge].checked = 1
          self.vertices[edge].fathers = vertice.value


#conexao com a API:

#visualizando os labirintos disponiveis

import urllib3

urllib3.disable_warnings()

import requests

response = requests.get('https://gtm.delary.dev/labirintos', verify=False)

if response.status_code == 200:
    labirintos = response.json()
    print(labirintos)
else:
    print(f"A solicitação falhou com o código de status {response.status_code}")


#iniciando o labirinto

dados = {
    "id": "Mickey",
    "labirinto" : labirintos[2]
}

response = requests.post('https://gtm.delary.dev/iniciar', json=dados, verify=False)

if response.status_code == 200:
    inicio = response.json()
    print(inicio)
    print(dados)
else:
    print(f"A solicitação falhou com o código de status {response.status_code}")

#percorrendo o labirinto dfs/bfs

def move(dados, posicao):
  new_dados = {
  "id": dados["id"],
  "labirinto": dados["labirinto"],
  "nova_posicao": posicao
  }

  return requests.post('https://gtm.delary.dev/movimentar', json=new_dados, verify=False)


start = inicio['pos_atual']
end = None

atual = inicio

percorridos = [start]
pilha = [inicio]

grafo = Graph()

print('atual: '+str(atual))

while True:
  x = 0
  for m in atual['movimentos']:
    grafo.addEdge(atual['pos_atual'], m)
    if not m in percorridos:
      atual = move(dados, m).json()
      print('atual: '+str(atual))
      if atual['final']:
        end = atual['pos_atual']
      pilha.append(atual)
      percorridos.append(atual['pos_atual'])
      x = 1
      break
  if x == 0 and len(pilha) > 1:
    pilha.pop()
    atual = pilha[len(pilha) - 1]
    move(dados, atual['pos_atual'])
    print('novo atual: '+str(atual))
  else:
    if len(pilha) > 1:
      continue
    else:
      break

print(grafo.returnAdjasenceList())
print('inicio: '+str(start))
print('final: '+str(end))

path = grafo.bfs(start,end)

print("Caminho: ", path)

dados["todos_movimentos"] = path

print('Dados: ', dados)

response = requests.post('https://gtm.delary.dev/validar_caminho', json=dados, verify=False)

print("Resposta: ", response.json())
