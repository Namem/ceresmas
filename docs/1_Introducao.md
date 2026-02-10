# 1. INTRODUÇÃO

O agronegócio brasileiro, embora reconhecido mundialmente por sua eficiência em latifúndios e commodities, apresenta uma dicotomia tecnológica severa. Enquanto grandes produtores utilizam agricultura de precisão, drones e sistemas de ERP (Enterprise Resource Planning) robustos, o pequeno e médio produtor opera, frequentemente, em um vácuo de gestão dados.

Este Trabalho de Conclusão de Curso propõe o desenvolvimento do **Ceres MAS**, um sistema baseado em Arquitetura Multiagente (MAS) e Processamento de Linguagem Natural (PLN), desenhado para mitigar a assimetria de informações financeiras e comerciais na agricultura familiar e de médio porte.

## 1.1 Contextualização e Problema
A gestão de uma propriedade rural envolve variáveis complexas: biológicas (safra, pragas), financeiras (fluxo de caixa, custos de insumos) e comerciais (volatilidade de preços). Em entrevista preliminar realizada com engenheiros agrônomos atuantes no setor, identificou-se que a principal dor do pequeno produtor não é agronômica, mas gerencial.

O problema central abordado neste trabalho é a **"Caixa Preta Financeira"**: o desconhecimento do Custo Real de Produção. Sem ferramentas adequadas, o produtor mistura finanças pessoais com as da safra, realiza compras de insumos sem planejamento de fluxo de caixa e desconhece sua margem de lucro real por talhão.

Concomitantemente, existe um problema de **Desconexão Comercial**. A oferta do pequeno produtor é fragmentada, dificultando o atendimento à demanda de qualidade e frequência exigida pelos grandes compradores (supermercados e indústrias), resultando em vendas a preços subvalorizados para intermediários.

## 1.2 Justificativa
A Engenharia da Computação pode oferecer soluções de baixo custo computacional para este cenário através de Sistemas Multiagentes. Diferente de softwares monolíticos tradicionais que exigem preenchimento manual rigoroso (formulários complexos), agentes inteligentes equipados com LLMs (Large Language Models) podem interagir via linguagem natural, reduzindo a barreira de entrada tecnológica.

A escolha por uma arquitetura MAS justifica-se pela natureza distribuída do problema:
1.  **Agente Financeiro:** Monitora custos de forma autônoma.
2.  **Agente Agronômico:** Gerencia o calendário biológico.
3.  **Agente Comercial:** Busca oportunidades de mercado.

Esta abordagem permite desacoplar as complexidades, facilitando a manutenção e a escalabilidade do sistema.

## 1.3 Objetivos

### 1.3.1 Objetivo Geral
Desenvolver e validar um protótipo funcional de um Sistema Multiagente (Ceres MAS MAS) capaz de extrair custos de produção a partir de linguagem natural e orquestrar o planejamento de safra com oportunidades comerciais.

### 1.3.2 Objetivos Específicos
* **Implementar uma arquitetura de Agentes Inteligentes** utilizando a biblioteca CrewAI e modelos Gemini, segregando responsabilidades de finanças, agronomia e vendas.
* **Desenvolver um módulo de RAG (Retrieval-Augmented Generation)** para permitir que os agentes consultem manuais técnicos e boas práticas agrícolas.
* **Criar ferramentas determinísticas (Tools)** para cálculo de custos, garantindo que a IA generativa não alucine em operações matemáticas.
* **Validar a eficácia do sistema** comparando os custos apurados pelo Agente Financeiro com o método manual tradicional (planilhas), utilizando dados reais de safras passadas.