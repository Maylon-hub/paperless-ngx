---
trigger: manual
---

O projeto prático consiste em selecionar um sistema real, configurar seu ambiente de execução,
executar sua suíte de testes automatizados, medir cobertura, configurar integração contínua e análise
estática, implementar melhorias acompanhadas por testes e produzir evidências claras de todas as
atividades realizadas.

Escolher um sistema ativo, open-source e hospedado no GitHub.

Requisitos mínimos:

1. O sistema deve possuir armazenamento persistente;
2. O sistema deve ter uma boa suíte de testes automatizados;
3. O sistema não pode ter sido implementado por nenhum membro do grupo;
4. O sistema deve ter instruções minimamente claras de instalação, execução e teste;
5. O projeto deve estar ativo, com sinais de manutenção recente.
O ideal é escolher um projeto realista para o período da disciplina: suficientemente relevante
para permitir análise e melhorias, mas não tão complexo a ponto de inviabilizar a configuração do
ambiente.
Além dos requisitos gerais, o sistema-alvo precisa permitir a realização das atividades de teste,
cobertura, integração contínua e análise estática previstas no projeto.
O sistema escolhido deve permitir:
6. execução local do sistema;
7. execução local dos testes automatizados;
8. medição de cobertura de código;
9. implementação e execução de testes de unidade com pytest;
10. análise estática com SonarQube ou SonarCloud;
11. configuração de uma pipeline no GitHub Actions.
A interface gráfica é opcional. O ponto central é que o grupo consiga baixar, construir, executar,
testar, medir cobertura e analisar o projeto. Se o sistema não tiver GUI, o grupo deve apenas demonstrar
que o sistema foi configurado corretamente e está funcionando.
