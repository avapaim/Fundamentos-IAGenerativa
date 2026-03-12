# Projeto 04 - Assistente com Memória

Disciplina: IA Generativa
Professora: Sabrina Bet

## Descrição

Este projeto implementa um assistente conversacional em Python utilizando modelos de linguagem (LLMs), com controle de memória, persona definida, execução de funções Python e persistência de histórico em arquivo JSON.

O objetivo da atividade foi evoluir o chatbot desenvolvido nas aulas anteriores, adicionando mecanismos para gerenciar contexto da conversa, integrar funções externas e manter o histórico salvo entre execuções do programa.

---

## Como executar o projeto

1. Acesse a pasta do projeto:

cd projeto04

2. Execute o programa:

python main.py

O chatbot iniciará no terminal aguardando perguntas do usuário.

---

## Funcionalidades implementadas

### 1. Controle de memória

Foi implementado um comando especial:

/limpar

Ao utilizar esse comando, todo o histórico da conversa armazenado é apagado.

Após executar o comando, o assistente retorna a mensagem:

Memória da conversa apagada.

---

### 2. Persona do assistente

Foi definida uma mensagem de sistema para controlar o comportamento do assistente durante a conversa.

Persona utilizada:

"Você é um assistente corporativo educado, objetivo e útil. Sempre responda de forma clara e profissional."

Essa definição garante que o assistente mantenha respostas consistentes e apropriadas ao longo da interação.

---

### 3. Limite de memória

Para evitar crescimento excessivo do histórico e consumo desnecessário de tokens na API, foi implementado um limite de memória.

O sistema mantém apenas:

as últimas 10 mensagens da conversa

Quando esse limite é ultrapassado, as mensagens mais antigas são removidas automaticamente.

Isso melhora a eficiência do sistema e evita contextos muito longos.

---

### 4. Integração de funções Python

Foram implementadas funções Python que podem ser executadas automaticamente durante a conversa quando o usuário faz perguntas específicas.

#### Função: data atual

Arquivo:

tools.py

Função implementada:

data_atual()

Essa função retorna a data atual do sistema.

Exemplo de uso:

Usuário: qual a data hoje
Assistente: Hoje é 2026-03-12

---

#### Função: cálculo de IMC

Função implementada:

calcular_imc(peso, altura)

Essa função calcula o Índice de Massa Corporal com base nos dados informados pelo usuário.

Exemplo de uso:

Usuário: calcular imc

O sistema solicitará o peso e a altura e retornará o valor do IMC calculado.

---

### 5. Persistência de dados

O histórico da conversa é salvo automaticamente em um arquivo JSON chamado:

memoria_chat.json

Esse arquivo armazena todas as mensagens da conversa.

Quando o programa é iniciado novamente, o histórico é carregado automaticamente, permitindo continuar a conversa do ponto anterior.

---

## Estrutura do projeto

projeto04

main.py
tools.py
requirements.txt
tarefa.md
README.md
memoria_chat.json

---

## Reflexões

### Se o histórico crescer muito, quais problemas podem ocorrer no uso de LLMs?

Se o histórico crescer muito, o modelo precisa processar uma quantidade maior de tokens a cada requisição. Isso pode causar aumento de custo na utilização da API, maior tempo de resposta e também possível perda de relevância nas respostas, pois informações antigas podem interferir no contexto atual da conversa.

---

### Por que algumas tarefas são melhores resolvidas por funções Python do que pelo próprio LLM?

Funções Python são mais adequadas para tarefas determinísticas, como cálculos matemáticos, obtenção de dados do sistema ou processamento específico. Modelos de linguagem são excelentes para interpretação e geração de texto, porém podem cometer erros em cálculos ou gerar respostas imprecisas. Utilizar funções Python garante maior precisão nesses casos.

---

### Quais riscos existem ao deixar que o LLM tome decisões sobre quando usar uma função?

Se o modelo tiver autonomia total para decidir quando executar funções, ele pode chamar funções inadequadas ou deixar de utilizar funções quando necessário. Isso pode gerar respostas incorretas, comportamento inesperado ou até problemas de segurança dependendo da função disponível.

---

## Dificuldades encontradas

Durante o desenvolvimento do projeto, as principais dificuldades foram organizar o controle do histórico da conversa, garantir que a mensagem de sistema fosse preservada, implementar o limite de memória corretamente e integrar funções Python ao fluxo do chatbot.

---

## Conclusão

O projeto atingiu os objetivos propostos na atividade, evoluindo o chatbot com controle de memória, definição de persona, execução de funções Python e persistência de histórico em arquivo JSON. Essas melhorias tornam o assistente mais robusto e preparado para aplicações mais complexas.
