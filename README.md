# SiteOps - ECHO (Excel Control & Handling Operator)
Echo é uma aplicação desktop com design simples e moderno, focado na automação e simplificação de tarefas envolvendo planilhas. Possui sistema de cards interativos e menu lateral, dividindo as funcionalidades de acordo com área/foco.

# Índice

- Sobre o projeto
- Principais funcionalidades
- Interface
- Como utilizar
- Documentação completa
- Tecnologias Utilizadas

# Sobre o Projeto
Tem como objetivo automatizar operações longas e factiveis a erros, além de simplificar processos comuns, como remover duplicadas, dividir planilhas grandes, transformar de csv para excel entre outras funcionalidades, isso tudo de maneira rapida e simplificada, sem a necessidade do usuário ter de abrir o arquivo e alterá-lo manualmente, poupando assim tempo de trabalho e diminuindo consideravelmente os possíveis erros que tais operações poderiam gerar sendo realizadas de maneira manual.
# Principais Funcionalidades

| 💼 Recurso                  | Descrição                                                           |
| --------------------------- | ------------------------------------------------------------------- |
| 🔁 Remover Duplicatas       | Com base no modelo de planilha (MSP ou EXP) faz a verificação e remoção com base nos padrões de valor daquele modelo.                         |
| 🧩 Dividir tabela        | Segmenta uma planilha em vários arquivos com base na quantidade selecionada pelo usuário |
| 📝 Exp para MSP        | Transforma a planilha de um padrão para o outro, fazendo as alterações necessárias nas colunas. |
| 🏡 Corrigir Cidades      | Verifica com base em um dicionário se a cidade é diferente de fato ou apenas está com uma escrita diferente da usual. |
| 🧩 CSV para Excel        | Transforma uma planilha do modelo CSV para xlsx. |

# Interface
A interface é composta por:

- 📁 Menu lateral fixo com navegação categorizada

- 🧠 Cards de funcionalidades com frente (ação) e verso (informações detalhadas)

- 💬 Notificações simples informando finalização do processo e erros antes ou durante a execução do mesmo
- 💡  Feedback visual, onde ao selecionar um arquivo aparece o nome do mesmo, assim como é feito a limpeza do botão ao finalizar o processo, deixando o card pronto para executar outra ação.

## Imagens da aplicação


<p align="center">
  <img src="ASSETS\IMAGES\image (3).png" width="700"/>
</p>
<p align="center">
  <img src="ASSETS\IMAGES\image (1).png" width="340" style="margin-right: 20px;"/>
  <img src="ASSETS\IMAGES\image (2).png" width="340"/>
</p>

# Como Utilizar

Para utilizar o software basta fazer o download do arquivo .exe, encontrado em: [SiteOps-Echo](dist/SiteOps-Echo.exe)

# Documentação Completa
Para ter acesso a documentação completa do software, contendo mais detalhadamente sobre como utilizar e toda a estrutura do projeto explicado, acesse o Notion: https://www.notion.so/quero/SiteOps-Echo-1a671685286b80c4817fe9e0314f24a5

# Tecnologias Utilizadas

- pandas
- Python 3.10+
- PySide6
- xlwings



