# Como Traduzir Modelos de IA para o Hardware de Rede?
Este repositório contém todo o conteúdo auxiliar para facilitar as atividades práticas e material didático complementar

## Tutorial INETRM

### Passo a passo de instalação
Dependências obrigatórias:
- docker
- openvswitch
- python3
- python3-venv

Passo 1: Clonar o repositório na máquina local

```bash
git clone https://github.com/ifpb/in-netroadmap inetrm
cd inetrm
```

Passo 2: Criar uma python venv para isolar a instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Passo 3: Fazer a instalação via pip
```bash
pip install -e .
```

### Iniciando um projeto inetrm
Você pode iniciar um projeto através do inetrm usando o seguinte comando:
```bash
inetrm init
```
Desta forma, o inetrm gerará toda a estrutura do projeto no diretório de trabalho (pwd).

Alternativamente, é possível especificar o caminho em que o projeto é iniciado:
```bash
inetrm init --output-dir caminho/do/seu/projeto
```

Para verificar se o diretório de trabalho pertence a um projeto inetrm:
```bash
inetrm init --verify
```

### Módulo de treinamento
A função do módulo de treinamento é ler um dataset no formato csv, com colunas de valores relacionados a cabeçalhos de pacote de rede e obrigatóriamente uma coluna de classe não vazia. O framework então repassa o dataset para um jupyter notebook, que aparecerá no navegador do usuário, contendo todos os blocos de código que treinam o modelo de machine-learning escolhido.

Para usar o módulo de treinamento:
```bash
inetrm train seu_dataset.csv
```

Alternativamente, um diretório alvo pode ser passado como argumento:
```bash
inetrm train seu_dataset.csv --output-dir diretorio/alvo/
```

Depois de executar o bloco de códigos no jupyter, o modelo treinado é salvo em formato .pkl na raiz do projeto.

### Módulo de conversão
O módulo de conversão realiza o mapeamento do modelo de machine learning desejado para um código em P4. O P4 gerado pelo módulo de conversão possui uma implementação genérica onde o pipeline de classificação do pacote do modelo de ML não interfere no encaminhamento de pacotes, feito através de uma tabela de match ipv4, então o código foi feito para ser alterado. O módulo também gera um arquivo de texto contendo as entradas de todas as tabelas de match-action do pipeline de classificação do modelo.

Para usar o módulo de conversão:
```bash
inetrm convert seu_modelo.pkl
```

Alternativamente, um diretório alvo pode ser passado como argumento:
```bash
inetrm convert seu_modelo.pkl --output-dir diretorio/alvo/
```

O diretório recomendado para guardar tanto o código quanto as tabelas é o diretório p4, localizado na raiz do projeto.

### Módulo de provisionamento
Este módulo é responsável por gerenciar uma infraestrutura de rede virtual para testes e simulação com in-network machine learning. A topologia pode ser configurada no config.toml, através da declaração de nós e links.
Internamente, o módulo de provisionamento gerencia containers docker e o containernet, abstraindo etapas que são naturais de qualquer aplicação de in-network machine learning, como compilar o código P4 nos switches virtuais.
O módulo tem seu funcionamento dividido em 3 etapas: gerar o script da topologia consumido pelo containernet; construir os containers e levantar a infraestrutura virtual. Usa-se da seguinte forma:

```bash
inetrm provision generate
```
Gera o arquivo topology.py no diretório containernet na raiz do projeto, podendo ser modificado a partir daqui.

```bash
inetrm provision build
```
Constrói todas as imagens de containers localizadas no diretório images, na raiz do projeto, permitindo que sejam feitos containers customizados

```
inetrm provision up
```
Puxa uma imagem docker com containernet instalado e a usa para levantar a infraestrutura virtual por um tempo limitado. O tempo padrão é 60 segundos, mas pode ser modificado usando a flag time:
```bash
inetrm provision up --time 180
# ou inetrm provision up -t 180
```

Alternativamente, todas as etapas podem ser realizadas de uma vez:
```bash
inetrm provision
```
