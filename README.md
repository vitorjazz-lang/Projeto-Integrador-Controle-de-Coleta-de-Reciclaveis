# ♻️ Sistema de Gestão e Controle de Coleta de Recicláveis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/Storage-JSON-lightgrey?logo=json&logoColor=white)

**Aplicação em Python para controle operacional de resíduos recicláveis em condomínios, com algoritmos clássicos de ordenação, busca, recursão e gestão de filas.**

O **Sistema de Gestão de Coleta de Recicláveis** foi desenvolvido para organizar o fluxo de coleta seletiva em ambientes residenciais ou corporativos. Além de registrar pesagens por tipo de material (plástico, papel, vidro e metal) e alertar quando o estoque atinge a meta para retirada externa (`100 kg`), o projeto destaca-se pela implementação manual de estruturas de dados e algoritmos fundamentais de Ciência da Computação sem depender de funções prontas de ordenação.

---

## 🎯 Objetivos do Projeto

* Registrar e persistir históricos de coletas seletivas em arquivo estruturado (`coletas.json`) com gravação atômica segura.
* Implementar algoritmos clássicos manualmente: **Bubble Sort** (ordenação por peso), **Selection Sort** (ordenação por código) e **Pesquisa Binária**.
* Gerenciar solicitações de coleta de moradores/blocos através de uma estrutura de **Fila (FIFO - First-In, First-Out)**.
* Gerar relatórios matriciais ($12 \times 4$ — Mês $\times$ Material) e estatísticas consolidadas com cálculo recursivo.

---

## 📸 Demonstração

> *(Dica: Tire um print do menu e dos relatórios no terminal, salve como `preview.png` dentro da pasta `assets/` e a imagem aparecerá aqui!)*

![Execução no Terminal](assets/preview.png)

---

## 🛠️ Tecnologias e Conceitos Aplicados

* **Python 3.x** (Biblioteca Padrão: `json`, `os`, `datetime`, `pathlib`)
* **Estruturas de Dados:** Listas de registros (dicionários), Fila FIFO e Matriz bidimensional ($12 \times 4$)
* **Algoritmos Clássicos:** Bubble Sort, Selection Sort, Busca Sequencial, Busca Binária e Recursão
* **Persistência de Dados:** Leitura e escrita segura em JSON com validação rigorosa de entradas

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* **Python 3.8+** instalado (não requer instalação de bibliotecas externas).

### Passo a passo

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/SEU-USUARIO/sistema-gestao-reciclaveis.git
   cd sistema-gestao-reciclaveis
   ```

2. **Execute a aplicação:**
   ```bash
   python gestao_reciclaveis.py
   ```
   *(O arquivo `coletas.json` será criado automaticamente na pasta após o primeiro cadastro).*

---

## 🤝 Contribuição

Sugestões de melhorias (como exportação de relatórios para CSV ou interface gráfica) são sempre bem-vindas! Abra uma *Issue* ou envie um *Pull Request*.
