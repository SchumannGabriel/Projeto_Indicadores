# Projeto Indicadores

> Framework para extração, tratamento de dados e visualização de indicadores estratégicos consumindo dados diretamente da API da **Smartsheet**.

---

## Sumário

* [Sobre o Projeto](#-sobre-o-projeto)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Estrutura de Pastas](#-estrutura-de-pastas)
* [Configuração e Instalação](#-configuração-e-instalação)
* [Como Usar](#-como-usar)
* [Contribuição](#-contribuição)
* [Licença](#-licença)

---

## Sobre o Projeto

Este projeto foi desenvolvido para automatizar a ponte entre o armazenamento de dados na Smartsheet e a visualização analítica.

* **Propósito:** Ter uma base pronta para uso (boilerplate) a fim de otimizar o tempo de desenvolvimento de novos dashboards.
* **Público:** Destinado a analistas e desenvolvedores que precisam de agilidade no ETL (Extração, Transformação e Carga) de dados de planilhas online.
* **Diferenciais:** * Conexão nativa via SDK oficial.
    * Normalização automática de caracteres especiais (acentuação e símbolos).
    * Estrutura modular que separa a lógica de busca de dados da visualização.

---

## Tecnologias Utilizadas

As principais ferramentas e bibliotecas que dão vida a este projeto:

| Categoria | Tecnologia | Finalidade |
| :--- | :--- | :--- |
| **Linguagem** | [Python 3.10+](https://python.org) | Core do projeto |
| **Interface** | [Streamlit](https://docs.streamlit.io/) | Criação do Dashboard interativo |
| **API** | [Smartsheet SDK](https://smartsheet-platform.github.io/smartsheet-python-sdk/) | Integração e consumo de dados |
| **Tratamento** | [Pandas](https://pandas.pydata.org/) | Manipulação e limpeza de DataFrames |
| **Gráficos** | [Plotly](https://plotly.com/python/) | Visualizações dinâmicas e interativas |
| **Normalização** | [Unicodedata](https://docs.python.org/3/library/unicodedata.html) | Tratamento de strings e remoção de acentos |

---

## 📁 Estrutura de Pastas

Organização do diretório principal focada em segurança e modularidade:

```bash
.
├── 📁 .streamlit/         # Configurações do Streamlit
│   └── 📄 secrets.toml    # Armazenamento SEGURO de tokens e IDs (Não commitar!)
├── 📁 src/                # Código-fonte da aplicação
│   ├── 📄 app.py          # Arquivo principal (Interface)
│   ├── 📄 connection.py   # Lógica de conexão com Smartsheet
│   └── 📄 utils.py        # Funções de tratamento (unicodedata, etc)
├── 📄 .gitignore          # Arquivos e pastas ignorados pelo Git
├── 📄 requirements.txt    # Lista de dependências para instalação
└── 📄 README.md           # Documentação do projeto
