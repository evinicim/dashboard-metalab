# 📊 Dashboard Metalab Marketing Digital

Dashboard interativo para análise de dados da Metalab, incluindo inscrições, avaliações e status dos alunos.

## 🚀 Início Rápido

### Instalação

```bash
pip install -r requirements.txt
```

### Executar Dashboard

```bash
streamlit run dashboard_metalab.py
```

O dashboard abrirá automaticamente em: http://localhost:8501

## 📁 Estrutura do Projeto

```
.
├── dashboard_metalab.py      # Código principal do dashboard
├── requirements.txt           # Dependências Python
├── README.md                 # Este arquivo
├── .gitignore               # Arquivos ignorados pelo Git
│
├── assets/                   # Recursos visuais
│   └── Logo3.png            # Logo do projeto
│
├── .streamlit/              # Configurações do Streamlit
│   └── secrets.toml.example # Arquivo de exemplo para configuração
│
└── dados/                    # Dados locais (opcional, para fallback)
    ├── Metalab_inscricoes_.csv
    ├── Avaliacao_metalab.csv
    └── Metalab_Mcom_DadosAlunos.csv
```

## 📊 Funcionalidades

- **Métricas Principais**: Total de inscrições, alunos formados, taxa de desistência, alunos cursando
- **Perfil dos Alunos**: Análise por sexo, idade, raça/cor, renda familiar
- **Canais de Divulgação**: Análise dos principais canais de comunicação
- **Status dos Alunos**: Distribuição por status (Formado, Desistente, Em Curso)
- **Avaliações Detalhadas**: Análise completa das avaliações dos alunos
- **Análise Temporal**: Evolução das inscrições ao longo do tempo
- **Filtros Interativos**: Filtros por ciclo, local, status e gênero
- **Design Responsivo**: Otimizado para desktop, tablet e mobile

## 🌐 Publicar Online

### Streamlit Cloud (Recomendado)

1. Acesse: https://streamlit.io/cloud
2. Conecte seu repositório GitHub
3. Configure os Secrets no Streamlit Cloud:
   - Vá em Settings → Secrets
   - Adicione a configuração do Google Sheets:
   ```toml
   [google_sheets]
   SHEET_ID = "seu_sheet_id"
   GID_INSCRICOES = "0"
   GID_AVALIACOES = "0"
   GID_ALUNOS = "0"
   ```
4. Deploy automático!

**Nota**: O deploy usa dados do Google Sheets diretamente, não requer arquivos CSV no repositório.

## 📝 Requisitos

- Python 3.8+
- Streamlit >= 1.28.0
- Pandas >= 2.0.0
- Plotly >= 5.17.0

## 🔧 Configuração Local

Para usar o dashboard localmente:

1. Copie o arquivo de exemplo:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Edite `.streamlit/secrets.toml` com seus valores do Google Sheets

3. Configure o Google Sheets como público (apenas leitura)

4. Execute: `streamlit run dashboard_metalab.py`

---

**Desenvolvido por Vinicius Mendes** | GitHub: [@evinicim](https://github.com/evinicim) 📈
