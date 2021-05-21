# TOPAZ TEST

## 1. CONSIDERAÇÕES DO DESENVOLVEDOR

### 1.1 REQUISITOS

#### 1.1.1 DOCKER

Para ambiente de containers é necessario instalar:
- Docker

Construir a imagem:
```bash
docker-compose build
```
#### 1.1.2 LOCAL

Para o ambiente local é necessario instalar:
- Python 3.8
- Poetry

Foi necessario criar o arquivo `.env` para informar o root do projeto ao VSCODE.   
Exemplo:
```
PYTHONPATH=./topaz_test
```
As dependencias da aplicação são instaladas atraves do comando:
```bash
poetry install
```

### 1.2 INICIAR APLICACAO

#### 1.2.1 DOCKER
```bash
docker-compose up
```

#### 1.2.2. LOCAL
```bash
poetry run start
```
Para executar os testes unitarios (com cobertura):
```bash
poetry run test
```
Para validar a qualidade do código:

```bash
poetry run lint
```


## 2. DESAFIO 

Balanceamento de carga é muito importante em ambientes Cloud. Estamos sempre tentando minimizar os custos para que possamos manter o número de servidores o menor possível. Em contrapartida a capacidade e performance aumenta quando adicionamos mais servidores. Em nosso ambiente de simulação, em cada tick  (unidade básica de tempo da simulação), os usuários conectam aos servidores disponíveis e executam uma tarefa. Cada tarefa leva um número de ticks para ser ﬁnalizada (o número de ticks de uma tarefa é representado por ttask ), e após isso o usuário se desconecta automaticamente.

Os servidores são máquinas virtuais que se auto criam para acomodar novos usuários. Cada servidor custa R$ 1,00 por tick e suporta no máximo umax usuários simultaneamente. Você deve ﬁnalizar servidores que não estão sendo mais usados. O desaﬁo é fazer um programa em Python que recebe usuários e os aloca nos servidores tentando manter o menor custo possível.

### 2.1 Input 

Um arquivo onde: a primeira linha possui o valor de ttask ;
a segunda linha possui o valor de umax ;
as demais linhas contém o número de novos usuários para cada tick.

### 2.2 Output 

Um arquivo onde cada linha contém uma lista de servidores disponíveis no ﬁnal de cada tick , representado pelo número de usuários em cada servidor separados por vírgula e, ao ﬁnal, o custo total por utilização dos servidores

### 2.3 Limites 

- 1 ≤ ttask ≤ 10
- 1 ≤ umax ≤ 10

### 2.4 Exemplo 

input.txt
```txt
4
2
1
3
0
1
0
1
```

output.txt
```txt
1
2,2
2,2
2,2,1
1,2,1
2
2
1
1
0
15
```

### 2.5 Detalhamento do exemplo 

ttask = 4 (valor da primeira linha do input.txt)

umax = 2 (valor da segundo linha do input.txt)

| Tick | Input | Output | Explicação |
| ----- | ----- | ------ | ---------- |
| 1 | 1 | 1 | 1 servidor para 1 usuário. (1 servidor criado)
| 2 | 3 | 2,2 | 2 servidor para 14usuário. (1 servidor criado)
| 3 | 0 | 2,2 | 2 servidor para 4 usuário. (nenhum servidor criado ou removido)
| 4 | 1 | 2,2,1 | 3 servidor para 5 usuário. (1 servidor criado)
| 5 | 0 | 1,2,1 | 3 servidor para 4 usuário. (nenhum servidor criado ou removido)
| 6 | 1 | 2 | 1 servidor para 2 usuário. (2 servidores removidos)
| 7 | | 1 | 1 servidor para 2 usuário. (nenhum servidor criado ou removido)
| 8 | | 1 | 1 servidor para 1 usuário. (nenhum servidor criado ou removido)
| 9 | | 1 | 1 servidor para 1 usuário. (nenhum servidor criado ou removido)
| 10 | | 0 | nunhum servidor para nenhum usuário. (nenhum servidor criado ou removido)
| | | 15 | Custo Total: R$ 1 x 5 ticks (primeira VM) + R$ 1 x 4 ticks (segunda VM) + R$1 x 6 ticks (terceira VM) = R$15

### 2.6 Critérios de avaliação 

- Funcionamento
- Testes de unidade
- Cobertura de testes
- Complexidade de código
- Padronização de código (PEP-8, PEP-257)
