# 🤖 FullTrack Report Automation

Automação RPA desenvolvida em Python utilizando Playwright para automatizar a geração, exportação, download e organização de relatórios operacionais em uma plataforma web.

## 📌 Sobre o projeto

Este projeto automatiza uma rotina operacional que anteriormente era realizada manualmente, realizando login no sistema, navegação pelos módulos de relatórios, aplicação de filtros, exportação dos arquivos e organização automática dos documentos gerados.

## 🚀 Funcionalidades

- Login automatizado na plataforma;
- Navegação automática no sistema;
- Geração de relatórios de permanência em ponto;
- Exportação de relatórios em CSV;
- Download automático dos arquivos;
- Organização dos relatórios por:
  - Ano;
  - Cliente/Posto;
  - Mês;
  - Tipo de relatório.

## 🛠️ Tecnologias utilizadas

- Python
- Playwright
- PyAutoGUI
- pathlib
- datetime
- shutil

## 📂 Estrutura do projeto

fulltrack-report-automation

-src
  -fulltrack_bot.py
-README.md
-requirements.txt
-.gitignore
-.env.example