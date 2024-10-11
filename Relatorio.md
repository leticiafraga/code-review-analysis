
# Análise de Code Reviews em Repositórios Populares do GitHub

Daniel Leão, Juliana Serra e Letícia Fraga

## Introdução

Este trabalho tem como objetivo analisar as variáveis que influenciam o merge de um pull request (PR) em repositórios populares do GitHub. Para isso, focamos em PRs que passaram por processos de revisão manual, excluindo revisões automáticas de bots e ferramentas de CI/CD. As questões de pesquisa analisam como o tamanho, o tempo de análise, a descrição e as interações nos PRs influenciam o status final e o número de revisões realizadas.

### Hipóteses Iniciais

- H1: PRs maiores (com mais arquivos e linhas modificadas) tendem a receber feedback mais negativo e requerem mais revisões.
- H2: PRs com tempo de análise maior (duração desde a submissão até o fechamento) tendem a ter feedbacks mais negativos e um número maior de revisões.
- H3: PRs com descrições mais detalhadas (maior número de caracteres) tendem a ter um feedback positivo e necessitam de menos revisões.
- H4: PRs com mais interações (comentários e participantes) têm uma maior chance de ser aceitos (merged) e passam por menos revisões.

## Metodologia

1. **Criação do Dataset:**
   - Foram selecionados os 200 repositórios mais populares do GitHub, considerando apenas aqueles com pelo menos 100 PRs (merged + closed).
   - Selecionamos PRs com status MERGED ou CLOSED e com pelo menos uma revisão registrada.
   - PRs que levaram menos de uma hora entre submissão e conclusão foram excluídos.

2. **Questões de Pesquisa:**
   - **RQ1:** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?
   - **RQ2:** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?
   - **RQ3:** Qual a relação entre a descrição dos PRs e o feedback final das revisões?
   - **RQ4:** Qual a relação entre as interações nos PRs e o feedback final das revisões?
   - **RQ5:** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?
   - **RQ6:** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?
   - **RQ7:** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?
   - **RQ8:** Qual a relação entre as interações nos PRs e o número de revisões realizadas?

3. **Métricas Definidas:**
   - **Tamanho:** Número de arquivos modificados e total de linhas adicionadas/removidas.
   - **Tempo de Análise:** Intervalo de tempo entre a submissão do PR e seu fechamento ou merge.
   - **Descrição:** Número de caracteres no corpo da descrição do PR.
   - **Interações:** Número de participantes e comentários em cada PR.

## Resultados

*Em desenvolvimento.*

## Discussão

*Em desenvolvimento.*

## Visuais 

*Em desenvolvimento.*

## Conclusão

*Em desenvolvimento.*
