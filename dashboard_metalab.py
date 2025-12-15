import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import gc  # Garbage collector para liberar memória
import warnings
import re  # Para expressões regulares na normalização
warnings.filterwarnings('ignore')  # Suprimir avisos desnecessários

# Google Sheets disponível via URLs públicas (não precisa de bibliotecas extras)

# Tema customizado para os gráficos - fundo transparente igual à tela
px.defaults.template = "plotly"

# Função para aplicar tema escuro consistente nos gráficos
def aplicar_tema_escuro(fig):
    """Aplica tema escuro consistente nos gráficos com fundo igual à tela"""
    fig.update_layout(
        plot_bgcolor='rgba(30, 30, 46, 0)',  # Transparente - igual ao fundo da tela
        paper_bgcolor='rgba(30, 30, 46, 0)',  # Transparente - igual ao fundo da tela
        font=dict(color='#e0e0e0', size=12),
        xaxis=dict(
            gridcolor='rgba(92, 107, 192, 0.2)', 
            linecolor='rgba(92, 107, 192, 0.5)',
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='rgba(92, 107, 192, 0.2)', 
            linecolor='rgba(92, 107, 192, 0.5)',
            showgrid=True
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)', 
            font=dict(color='#e0e0e0'),
            bordercolor='rgba(92, 107, 192, 0.3)',
            borderwidth=1
        ),
        title=dict(font=dict(color='#90caf9'))
    )
    return fig

# Cores do projeto Metalab Marketing Digital - Tema Escuro
CORES_METALAB = {
    'primary': '#1a237e',      # Azul escuro
    'secondary': '#3949ab',     # Azul médio
    'accent': '#5c6bc0',        # Azul claro
    'light': '#90caf9',         # Azul claro brilhante
    'success': '#66bb6a',       # Verde claro
    'warning': '#ffa726',       # Laranja claro
    'error': '#ef5350',         # Vermelho claro
    'bg-dark': '#1e1e2e',       # Fundo escuro
    'card-dark': '#2d2d44',     # Card escuro
}

# Paleta de cores para gráficos - Tema Escuro
PALETA_METALAB = ['#5c6bc0', '#90caf9', '#7986cb', '#9fa8da', '#b39ddb']

# Configuração da página - Responsivo
st.set_page_config(
    page_title="Dashboard Metalab - Análise de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",  # No mobile, pode ser colapsada pelo usuário
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Dashboard Metalab - Criado por Vinicius Mendes | GitHub: @evinicim"
    }
)

# CSS personalizado - Tema Escuro Metalab + Responsividade Mobile
st.markdown("""
    <style>
    /* Retângulos de créditos full width */
    .creditos-topo, .creditos-rodape {
        position: relative;
        width: 100vw;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        background: #000000;
        padding: 0.8rem 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    .creditos-topo {
        margin-top: -1rem;
        margin-bottom: 1rem;
    }
    .creditos-rodape {
        margin-top: 2rem;
        margin-bottom: -1rem;
    }
    
    /* Container da logo com fundo branco */
    .logo-container {
        background: #ffffff !important;
        padding: 1.5rem !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
        display: block !important;
        width: 100% !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        position: relative !important;
        z-index: 1 !important;
    }
    .logo-container img,
    .logo-container [data-testid="stImage"] {
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 0 auto !important;
        position: relative !important;
        z-index: 2 !important;
    }
    
    /* Fundo escuro principal */
    .stApp {
        background-color: #1e1e2e;
        color: #e0e0e0;
    }
    
    /* Sidebar escura */
    .css-1d391kg {
        background-color: #252538;
    }
    
    /* Cards de métricas com fundo escuro */
    .stMetric {
        background: linear-gradient(135deg, #2d2d44 0%, #1e1e2e 100%);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #3949ab;
    }
    .stMetric label {
        color: #b0b0b0 !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #5c6bc0 !important;
        font-weight: bold;
        font-size: 2rem;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: #90caf9 !important;
    }
    
    /* Títulos e textos */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #5c6bc0;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(92, 107, 192, 0.3);
    }
    
    /* Seções */
    h2, h3 {
        color: #90caf9 !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Cores do projeto Metalab - Tema Escuro */
    :root {
        --metalab-primary: #1a237e;
        --metalab-secondary: #3949ab;
        --metalab-accent: #5c6bc0;
        --metalab-light: #90caf9;
        --metalab-bg-dark: #1e1e2e;
        --metalab-card-dark: #2d2d44;
    }
    
    /* Cards de métricas customizados */
    .metric-card-custom {
        min-height: 140px;
        margin-bottom: 1rem;
    }
    
    .metric-card-custom:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.5) !important;
    }
    
    /* Responsividade Mobile */
    @media screen and (max-width: 768px) {
        /* Header responsivo */
        .main-header {
            font-size: 1.5rem !important;
            padding: 0.5rem;
        }
        
        /* Métricas em coluna única no mobile */
        [data-testid="stMetric"] {
            margin-bottom: 1rem;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        /* Cards de métricas customizados no mobile */
        .metric-card-custom {
            min-height: 120px !important;
            padding: 1.2rem !important;
            margin-bottom: 1rem !important;
        }
        
        .metric-card-custom p[style*="font-size: 2.2rem"] {
            font-size: 1.6rem !important;
        }
        
        .metric-card-custom p[style*="font-size: 0.95rem"] {
            font-size: 0.85rem !important;
        }
        
        .metric-card-custom p[style*="font-size: 0.85rem"] {
            font-size: 0.75rem !important;
        }
        
        /* Colunas empilhadas no mobile - força uma por linha */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Sidebar mais compacta */
        .css-1d391kg {
            width: 100% !important;
        }
        
        /* Gráficos responsivos */
        .js-plotly-plot {
            width: 100% !important;
            height: auto !important;
        }
        
        /* Textos menores */
        h2 {
            font-size: 1.3rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
        
        /* Logo menor no mobile */
        img {
            max-width: 150px !important;
        }
    }
    
    /* Tablet - layout intermediário */
    @media screen and (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 2rem !important;
        }
        
        .metric-card-custom {
            min-height: 130px !important;
            padding: 1.3rem !important;
        }
        
        .metric-card-custom p[style*="font-size: 2.2rem"] {
            font-size: 1.9rem !important;
        }
        
        /* Layout 2-3 no tablet */
        [data-testid="column"]:nth-child(1),
        [data-testid="column"]:nth-child(2) {
            width: 50% !important;
            flex: 1 1 50% !important;
        }
        
        [data-testid="column"]:nth-child(3),
        [data-testid="column"]:nth-child(4),
        [data-testid="column"]:nth-child(5) {
            width: 33.33% !important;
            flex: 1 1 33.33% !important;
        }
    }
    
    /* Sidebar mais acessível no mobile */
    @media screen and (max-width: 768px) {
        [data-testid="stSidebar"] {
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            z-index: 999;
            overflow-y: auto;
        }
        
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }
        
        /* Botão de toggle da sidebar mais visível */
        [data-testid="stSidebar"] button {
            padding: 0.75rem;
            font-size: 1rem;
        }
        
        /* Selectboxes mais fáceis de usar no mobile */
        .stSelectbox label {
            font-size: 0.9rem !important;
        }
        
        /* Info boxes mais compactos */
        .stInfo {
            padding: 0.75rem !important;
            font-size: 0.85rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Créditos no início - Retângulo preto full width no topo (antes da logo)
st.markdown("""
<style>
    .creditos-topo {
        position: relative;
        width: 100vw;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        background: #000000;
        padding: 0.8rem 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: -1rem;
        margin-bottom: 1rem;
    }
</style>
<div class="creditos-topo">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="white" style="vertical-align: middle;">
        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
    </svg>
    <p style='color: #ffffff; margin: 0; font-size: 1rem; font-weight: 500;'>
        Criado por Vinicius Mendes | <a href="https://github.com/evinicim" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 600;">@evinicim</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Logo e Título - Responsivo (com fundo branco)
import os
import base64
logo_paths = ['assets/Logo2.png', 'assets/Logo3.png', 'Logo2.png', 'Logo3.png']
logo_found = False
for logo_path in logo_paths:
    if os.path.exists(logo_path):
        try:
            # Usar coluna única no mobile, centralizada
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # Converter imagem para base64 e incorporar diretamente no HTML
                with open(logo_path, "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
                
                # Container com fundo branco e imagem dentro
                st.markdown(f"""
                <div class="logo-container">
                    <img src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;" />
                </div>
                """, unsafe_allow_html=True)
            logo_found = True
            break
        except Exception as e:
            # Fallback: usar método Streamlit padrão sem fundo branco
            try:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(logo_path, use_container_width=True)
                logo_found = True
                break
            except:
                continue

st.markdown('<h1 class="main-header">📊 Dashboard Metalab Marketing Digital</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #90caf9; font-size: 1.1rem; margin-bottom: 2rem;">Análise de Dados e Resultados</p>', unsafe_allow_html=True)

# Função para carregar do Google Sheets via URL pública (muito mais rápido)
@st.cache_data(ttl=3600, max_entries=1, show_spinner=False)  # Cache por 1 hora
def load_from_google_sheets():
    """Carrega dados do Google Sheets se configurado (método simples sem autenticação)"""
    try:
        # Verificar se há configuração de Google Sheets nos secrets
        secrets = st.secrets.get("google_sheets", {})
        
        # Suporta planilha única com múltiplas abas OU planilhas separadas
        sheet_id = secrets.get("SHEET_ID")  # Planilha única
        sheet_id_inscricoes = secrets.get("SHEET_ID_INSCRICOES")  # Planilha separada
        sheet_id_avaliacoes = secrets.get("SHEET_ID_AVALIACOES")
        sheet_id_alunos = secrets.get("SHEET_ID_ALUNOS")
        
        # Se usar planilha única (recomendado)
        if sheet_id:
            gid_inscricoes = secrets.get("GID_INSCRICOES", "0")
            gid_avaliacoes = secrets.get("GID_AVALIACOES", "0")
            gid_alunos = secrets.get("GID_ALUNOS", "0")
            
            # Carregar inscrições
            url_inscricoes = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_inscricoes}"
            inscricoes = pd.read_csv(url_inscricoes, encoding='utf-8', low_memory=False)
            
            # Carregar avaliações
            url_avaliacoes = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_avaliacoes}"
            avaliacoes = pd.read_csv(url_avaliacoes, encoding='utf-8', low_memory=False)
            
            # Carregar alunos
            url_alunos = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_alunos}"
            alunos = pd.read_csv(url_alunos, encoding='utf-8', low_memory=False, sep=',')
            
            return inscricoes, avaliacoes, alunos
        
        # Se usar planilhas separadas (fallback)
        elif all([sheet_id_inscricoes, sheet_id_avaliacoes, sheet_id_alunos]):
            aba_inscricoes = secrets.get("ABA_INSCRICOES", "0")
            url_inscricoes = f"https://docs.google.com/spreadsheets/d/{sheet_id_inscricoes}/export?format=csv&gid={aba_inscricoes}"
            inscricoes = pd.read_csv(url_inscricoes, encoding='utf-8', low_memory=False)
            
            aba_avaliacoes = secrets.get("ABA_AVALIACOES", "0")
            url_avaliacoes = f"https://docs.google.com/spreadsheets/d/{sheet_id_avaliacoes}/export?format=csv&gid={aba_avaliacoes}"
            avaliacoes = pd.read_csv(url_avaliacoes, encoding='utf-8', low_memory=False)
            
            aba_alunos = secrets.get("ABA_ALUNOS", "0")
            url_alunos = f"https://docs.google.com/spreadsheets/d/{sheet_id_alunos}/export?format=csv&gid={aba_alunos}"
            alunos = pd.read_csv(url_alunos, encoding='utf-8', low_memory=False, sep=',')
            
            return inscricoes, avaliacoes, alunos
        else:
            return None, None, None
    except Exception as e:
        # Se falhar, retornar None para usar CSV como fallback
        return None, None, None

# Carregar dados com tratamento de erros robusto e cache agressivo
@st.cache_data(ttl=86400, max_entries=1, show_spinner=False)  # Cache por 24 horas
def load_data():
    """
    Carrega dados do Google Sheets (se configurado) ou CSV como fallback.
    Google Sheets é muito mais rápido que CSV.
    """
    import os
    
    # Tentar carregar do Google Sheets primeiro (muito mais rápido)
    inscricoes_gs, avaliacoes_gs, alunos_gs = load_from_google_sheets()
    if inscricoes_gs is not None and avaliacoes_gs is not None and alunos_gs is not None:
        return inscricoes_gs, avaliacoes_gs, alunos_gs
    
    # Se Google Sheets não disponível, usar CSV como fallback
    data_dir = os.getenv('DATA_DIR', 'dados')
    
    try:
        # Carregar inscrições - procurar primeiro em dados/, depois na raiz
        inscricoes_path = os.path.join('dados', 'Metalab_inscricoes_.csv')
        if not os.path.exists(inscricoes_path):
            inscricoes_path = 'Metalab_inscricoes_.csv'
        
        # Tentar diferentes encodings
        inscricoes = None
        encodings_tentados = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings_tentados:
            try:
                inscricoes = pd.read_csv(
                    inscricoes_path, 
                    encoding=encoding, 
                    low_memory=False
                )
                break
            except Exception:
                continue
        
        if inscricoes is None:
            # Última tentativa com tratamento de erros
            try:
                inscricoes = pd.read_csv(inscricoes_path, encoding='utf-8', low_memory=False, on_bad_lines='skip', errors='ignore')
            except TypeError:
                # Versão antiga do pandas não tem on_bad_lines
                inscricoes = pd.read_csv(inscricoes_path, encoding='utf-8', low_memory=False, error_bad_lines=False, warn_bad_lines=False)
        
        # Limitar tamanho se muito grande (proteção contra crashes)
        if len(inscricoes) > 20000:  # Reduzido de 50000 para melhor performance
            inscricoes = inscricoes.head(20000)
        gc.collect()  # Liberar memória
        
        # Carregar avaliações - procurar primeiro em dados/, depois na raiz
        # Tentar diferentes nomes possíveis
        avaliacoes_path = os.path.join('dados', 'Avaliacao_metalab.csv')
        formato_long = False
        if not os.path.exists(avaliacoes_path):
            avaliacoes_path = os.path.join('dados', 'Avaliacao_programando_google_planilha.csv')
        if not os.path.exists(avaliacoes_path):
            avaliacoes_path = 'Avaliacao_metalab.csv'
        if not os.path.exists(avaliacoes_path):
            avaliacoes_path = 'Avaliacao_programando_google_planilha.csv'
        
        # Tentar diferentes encodings e separadores
        avaliacoes = None
        encodings_tentados = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        separadores_tentados = [';', ',', None]  # Ponto e vírgula primeiro (mais comum no Brasil)
        
        for encoding in encodings_tentados:
            for sep in separadores_tentados:
                try:
                    if sep is None:
                        avaliacoes = pd.read_csv(avaliacoes_path, encoding=encoding, sep=None, engine='python', low_memory=False)
                    else:
                        avaliacoes = pd.read_csv(avaliacoes_path, encoding=encoding, sep=sep, low_memory=False)
                    
                    # Verificar se é formato longo (tem coluna 'Pergunta')
                    colunas_lower = [str(col).lower() for col in avaliacoes.columns]
                    if 'pergunta' in colunas_lower and ('nome exibido' in colunas_lower or 'resposta de texto livre' in colunas_lower or 'resposta' in ' '.join(colunas_lower)):
                        formato_long = True
                        break
                except Exception:
                    continue
            if avaliacoes is not None and formato_long:
                break
        
        # Se ainda não conseguiu carregar, tentar última opção
        if avaliacoes is None:
            try:
                try:
                    avaliacoes = pd.read_csv(avaliacoes_path, encoding='utf-8', sep=';', low_memory=False, on_bad_lines='skip')
                except TypeError:
                    # Versão antiga do pandas não tem on_bad_lines
                    avaliacoes = pd.read_csv(avaliacoes_path, encoding='utf-8', sep=';', low_memory=False, error_bad_lines=False, warn_bad_lines=False)
                colunas_lower = [col.lower() for col in avaliacoes.columns]
                if 'pergunta' in colunas_lower:
                    formato_long = True
            except Exception:
                avaliacoes = pd.DataFrame()  # DataFrame vazio como fallback
        
        # Se for formato longo, transformar para formato largo (wide) - OTIMIZADO
        # Verificar novamente se é formato longo (pode ter sido carregado com encoding diferente)
        if not formato_long and avaliacoes is not None and len(avaliacoes) > 0:
            colunas_lower = [str(col).lower() for col in avaliacoes.columns]
            if 'pergunta' in colunas_lower:
                formato_long = True
        
        if formato_long and len(avaliacoes) > 0:
            # Limitar dados antes do pivot para melhor performance
            if len(avaliacoes) > 10000:
                # Se muito grande, usar apenas amostra para pivot
                avaliacoes = avaliacoes.head(10000)
            
            # Identificar coluna de identificador (pode ter caracteres especiais)
            id_col = None
            for col in avaliacoes.columns:
                col_lower = str(col).lower()
                if any(palavra in col_lower for palavra in ['usuário', 'usuario', 'opinião', 'opiniao', 'pesquisa']):
                    id_col = col
                    break
            
            # Encontrar coluna de Pergunta (pode ter variações)
            coluna_pergunta = None
            for col in avaliacoes.columns:
                if 'pergunta' in str(col).lower():
                    coluna_pergunta = col
                    break
            
            # Se não encontrou coluna_pergunta, tentar buscar de forma mais ampla
            if coluna_pergunta is None:
                for col in avaliacoes.columns:
                    col_str = str(col).lower()
                    if 'pergunta' in col_str or 'question' in col_str:
                        coluna_pergunta = col
                        break
            
            if coluna_pergunta:
                # Criar índice único de forma mais eficiente
                primeira_pergunta = avaliacoes[coluna_pergunta].iloc[0]
                if id_col:
                    avaliacoes['avaliacao_id'] = (avaliacoes[coluna_pergunta] == primeira_pergunta).groupby(avaliacoes[id_col], sort=False).cumsum()
                else:
                    avaliacoes['avaliacao_id'] = (avaliacoes[coluna_pergunta] == primeira_pergunta).cumsum()
                
                # Escolher coluna de valor (buscar variações)
                valor_col = None
                for col in avaliacoes.columns:
                    col_lower = col.lower()
                    if 'resposta de texto livre' in col_lower or 'resposta' in col_lower:
                        if avaliacoes[col].notna().sum() > len(avaliacoes) * 0.1:
                            valor_col = col
                            break
                
                # Se não encontrou resposta de texto livre, usar Nome exibido
                if valor_col is None:
                    for col in avaliacoes.columns:
                        if 'nome exibido' in col.lower():
                            valor_col = col
                            break
                
                if valor_col:
                    # Pivot otimizado: usar apenas colunas necessárias e limitar
                    try:
                        # Garantir que avaliacao_id existe e é único
                        if 'avaliacao_id' not in avaliacoes.columns:
                            primeira_pergunta = avaliacoes[coluna_pergunta].iloc[0]
                            if id_col:
                                avaliacoes['avaliacao_id'] = (avaliacoes[coluna_pergunta] == primeira_pergunta).groupby(avaliacoes[id_col], sort=False).cumsum()
                            else:
                                avaliacoes['avaliacao_id'] = (avaliacoes[coluna_pergunta] == primeira_pergunta).cumsum()
                        
                        # Remover duplicatas antes do pivot
                        colunas_pivot = ['avaliacao_id', coluna_pergunta, valor_col]
                        avaliacoes_para_pivot = avaliacoes[colunas_pivot].copy()
                        
                        # Remover linhas com valores nulos críticos
                        avaliacoes_para_pivot = avaliacoes_para_pivot.dropna(subset=[coluna_pergunta, valor_col])
                        
                        # Tentar pivot simples primeiro
                        try:
                            avaliacoes_pivot = avaliacoes_para_pivot.pivot(
                                index='avaliacao_id',
                                columns=coluna_pergunta,
                                values=valor_col
                            )
                            avaliacoes = avaliacoes_pivot.reset_index(drop=True)
                            avaliacoes.columns.name = None
                            gc.collect()
                        except Exception as e_pivot:
                            # Se pivot falhar, usar pivot_table como fallback (mais robusto)
                            try:
                                avaliacoes_pivot = avaliacoes_para_pivot.pivot_table(
                                    index='avaliacao_id',
                                    columns=coluna_pergunta,
                                    values=valor_col,
                                    aggfunc='first',  # Pegar primeiro valor se houver duplicatas
                                    fill_value=None
                                )
                                avaliacoes = avaliacoes_pivot.reset_index(drop=True)
                                avaliacoes.columns.name = None
                                gc.collect()
                            except Exception as e_pivot_table:
                                # Se ainda falhar, tentar método alternativo usando groupby
                                try:
                                    avaliacoes_grouped = avaliacoes_para_pivot.groupby(['avaliacao_id', coluna_pergunta])[valor_col].first().unstack(fill_value=None)
                                    avaliacoes = avaliacoes_grouped.reset_index(drop=True)
                                    avaliacoes.columns.name = None
                                    gc.collect()
                                except Exception as e_groupby:
                                    # Se ainda falhar, manter formato longo e mostrar aviso
                                    pass
                    except Exception as e:
                        # Se ainda falhar, manter formato longo
                        pass
        
        # Carregar dados dos alunos - procurar primeiro em dados/, depois na raiz
        alunos_path = os.path.join('dados', 'Metalab_Mcom_DadosAlunos.csv')
        if not os.path.exists(alunos_path):
            alunos_path = 'Metalab_Mcom_DadosAlunos.csv'
        
        # Tentar diferentes encodings
        alunos = None
        encodings_tentados = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings_tentados:
            try:
                alunos = pd.read_csv(
                    alunos_path, 
                    encoding=encoding, 
                    low_memory=False, 
                    sep=','
                )
                break
            except Exception:
                continue
        
        if alunos is None:
            # Última tentativa com tratamento de erros
            try:
                alunos = pd.read_csv(alunos_path, encoding='utf-8', low_memory=False, sep=',', on_bad_lines='skip', errors='ignore')
            except TypeError:
                # Versão antiga do pandas não tem on_bad_lines
                alunos = pd.read_csv(alunos_path, encoding='utf-8', low_memory=False, sep=',', error_bad_lines=False, warn_bad_lines=False)
        
        # Limitar tamanho se muito grande (proteção contra crashes)
        if len(alunos) > 20000:  # Reduzido de 50000 para melhor performance
            alunos = alunos.head(20000)
        
        # Liberar memória após carregar
        gc.collect()
        
        return inscricoes, avaliacoes, alunos
    except FileNotFoundError as e:
        st.error(f"⚠️ Arquivo de dados não encontrado: {e}")
        st.info("""
        **Instruções:**
        1. Coloque os arquivos CSV na pasta dados/:
           - Metalab_inscricoes_.csv
           - Avaliacao_metalab.csv (ou Avaliacao_programando_google_planilha.csv)
           - Metalab_Mcom_DadosAlunos.csv
        2. Ou configure a variável de ambiente DATA_DIR com o caminho dos arquivos
        """)
        return None, None, None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None, None, None

# Carregar dados (sem spinner para melhor performance)
try:
    inscricoes, avaliacoes, alunos = load_data()
    
    if inscricoes is None or avaliacoes is None or alunos is None:
        st.error("⚠️ Erro ao carregar dados. Verifique se os arquivos CSV estão na pasta dados/")
        st.stop()
        
    # Verificar se os dados não estão vazios
    if len(inscricoes) == 0 or len(alunos) == 0:
        st.error("⚠️ Arquivos de dados estão vazios. Verifique os arquivos CSV.")
        st.stop()
        
except Exception as e:
    st.error(f"⚠️ Erro crítico ao carregar dados: {str(e)}")
    st.info("""
    **Solução:**
    1. Verifique se os arquivos CSV estão na pasta dados/
    2. Verifique se os arquivos não estão corrompidos
    3. Tente limpar o cache: Menu → Settings → Clear cache
    4. Recarregue a página
    """)
    st.stop()

# Função para pré-processar dados (com cache agressivo)
@st.cache_data(ttl=86400, max_entries=1, show_spinner=False)  # Cache por 24 horas
def preprocessar_dados(_inscricoes, _avaliacoes, _alunos):
    """Pré-processa dados para melhor performance"""
    inscricoes_proc = _inscricoes.copy()
    alunos_proc = _alunos.copy()
    
    # Limpar colunas de inscrições
    if 'Carimbo de data/hora' in inscricoes_proc.columns:
        inscricoes_proc['Data_Inscricao'] = pd.to_datetime(inscricoes_proc['Carimbo de data/hora'], errors='coerce')
        inscricoes_proc['Ano'] = inscricoes_proc['Data_Inscricao'].dt.year
        inscricoes_proc['Mes'] = inscricoes_proc['Data_Inscricao'].dt.month
    
    # Preparar dados de alunos (otimizado com vectorização)
    if 'STATUS' in alunos_proc.columns:
        alunos_proc['STATUS'] = alunos_proc['STATUS'].astype(str).str.upper().str.strip()
        
        # Otimizar: usar vectorização ao invés de apply (muito mais rápido)
        mask_concluido = alunos_proc['STATUS'].str.contains('CONCLUIDO|CONCLUÍDO', case=False, na=False, regex=True)
        mask_cursando = alunos_proc['STATUS'].str.contains('CURSANDO|EM CURSO|EM ANDAMENTO', case=False, na=False, regex=True)
        mask_desistente = alunos_proc['STATUS'].str.contains('DESISTENTE', case=False, na=False, regex=True)
        
        alunos_proc['STATUS_NORMALIZADO'] = 'OUTROS'
        alunos_proc.loc[mask_concluido, 'STATUS_NORMALIZADO'] = 'CONCLUÍDO'
        alunos_proc.loc[mask_cursando, 'STATUS_NORMALIZADO'] = 'CURSANDO'
        alunos_proc.loc[mask_desistente, 'STATUS_NORMALIZADO'] = 'DESISTENTE'
    else:
        alunos_proc['STATUS_NORMALIZADO'] = 'OUTROS'
    
    return inscricoes_proc, alunos_proc

# Função para fazer pivot das avaliações (converter de longo para largo)
def fazer_pivot_avaliacoes(_avaliacoes):
    """Converte avaliações de formato longo para formato largo (wide)"""
    if _avaliacoes is None or len(_avaliacoes) == 0:
        return _avaliacoes
    
    # Verificar se já está em formato largo (não tem coluna 'Pergunta')
    colunas_lower = [str(col).lower() for col in _avaliacoes.columns]
    if 'pergunta' not in colunas_lower:
        return _avaliacoes  # Já está em formato largo
    
    # Está em formato longo, fazer pivot
    try:
        # Encontrar colunas necessárias
        coluna_pergunta = None
        for col in _avaliacoes.columns:
            if 'pergunta' in str(col).lower():
                coluna_pergunta = col
                break
        
        id_col = None
        for col in _avaliacoes.columns:
            col_lower = str(col).lower()
            if any(palavra in col_lower for palavra in ['usuário', 'usuario', 'opinião', 'opiniao', 'pesquisa']):
                id_col = col
                break
        
        valor_col = None
        for col in _avaliacoes.columns:
            col_lower = str(col).lower()
            if 'resposta de texto livre' in col_lower:
                if _avaliacoes[col].notna().sum() > len(_avaliacoes) * 0.1:
                    valor_col = col
                    break
        
        if valor_col is None:
            for col in _avaliacoes.columns:
                if 'nome exibido' in str(col).lower():
                    valor_col = col
                    break
        
        if coluna_pergunta and valor_col:
            # Criar ID único baseado na primeira pergunta
            primeira_pergunta = _avaliacoes[coluna_pergunta].iloc[0]
            if id_col:
                _avaliacoes['avaliacao_id'] = (_avaliacoes[coluna_pergunta] == primeira_pergunta).groupby(_avaliacoes[id_col], sort=False).cumsum()
            else:
                _avaliacoes['avaliacao_id'] = (_avaliacoes[coluna_pergunta] == primeira_pergunta).cumsum()
            
            # Extrair CICLO antes do pivot (se a pergunta CICLO existir)
            ciclo_values = {}
            perguntas_unicas = _avaliacoes[coluna_pergunta].unique()
            for pergunta in perguntas_unicas:
                pergunta_str = str(pergunta).upper().strip()
                # Verificar se a pergunta é exatamente "CICLO" ou contém "CICLO"
                if pergunta_str == 'CICLO' or 'CICLO' in pergunta_str:
                    # Encontrar avaliações com pergunta CICLO
                    mask_ciclo = _avaliacoes[coluna_pergunta].astype(str).str.upper().str.strip() == pergunta_str
                    if mask_ciclo.any():
                        ciclo_data = _avaliacoes[mask_ciclo][['avaliacao_id', valor_col]].copy()
                        ciclo_data = ciclo_data.rename(columns={valor_col: 'CICLO'})
                        ciclo_data = ciclo_data.dropna(subset=['CICLO'])
                        # Filtrar valores inválidos (como "Ignorados", "nan", etc)
                        ciclo_data = ciclo_data[~ciclo_data['CICLO'].astype(str).str.upper().str.strip().isin(['IGNORADOS', 'NAN', 'NONE', '', 'NULL'])]
                        # Mapear avaliacao_id para ciclo (normalizar removendo .0)
                        for idx, row in ciclo_data.iterrows():
                            ciclo_val = str(row['CICLO']).strip()
                            # Remover .0 do final se houver
                            if ciclo_val.endswith('.0'):
                                ciclo_val = ciclo_val[:-2]
                            if ciclo_val and ciclo_val.upper() not in ['IGNORADOS', 'NAN', 'NONE', 'NULL']:
                                ciclo_values[row['avaliacao_id']] = ciclo_val.strip()
                    break
            
            # Preservar coluna Pesquisa antes do pivot (se existir)
            pesquisa_values = {}
            if 'Pesquisa' in _avaliacoes.columns:
                # Mapear avaliacao_id para Pesquisa (usar o primeiro valor de cada avaliacao_id)
                pesquisa_data = _avaliacoes[['avaliacao_id', 'Pesquisa']].copy()
                # Remover duplicatas mantendo o primeiro valor de cada avaliacao_id
                pesquisa_data = pesquisa_data.drop_duplicates(subset=['avaliacao_id'], keep='first')
                for idx, row in pesquisa_data.iterrows():
                    if pd.notna(row['Pesquisa']):
                        pesquisa_values[row['avaliacao_id']] = row['Pesquisa']
            
            # Fazer pivot usando pivot_table
            avaliacoes_para_pivot = _avaliacoes[['avaliacao_id', coluna_pergunta, valor_col]].copy()
            avaliacoes_para_pivot = avaliacoes_para_pivot.dropna(subset=[coluna_pergunta, valor_col])
            
            avaliacoes_pivot = avaliacoes_para_pivot.pivot_table(
                index='avaliacao_id',
                columns=coluna_pergunta,
                values=valor_col,
                aggfunc='first',
                fill_value=None
            )
            
            # Adicionar coluna CICLO se foi extraída (antes de reset_index)
            if ciclo_values:
                ciclos_list = [ciclo_values.get(idx, None) for idx in avaliacoes_pivot.index]
                avaliacoes_pivot['CICLO'] = ciclos_list
                # Preencher valores faltantes
                avaliacoes_pivot['CICLO'] = avaliacoes_pivot['CICLO'].fillna(method='ffill').fillna(method='bfill')
            
            # Adicionar coluna Pesquisa se foi preservada
            if pesquisa_values:
                pesquisas_list = [pesquisa_values.get(idx, None) for idx in avaliacoes_pivot.index]
                avaliacoes_pivot['Pesquisa'] = pesquisas_list
                # Preencher valores faltantes
                avaliacoes_pivot['Pesquisa'] = avaliacoes_pivot['Pesquisa'].fillna(method='ffill').fillna(method='bfill')
            
            avaliacoes_pivot = avaliacoes_pivot.reset_index(drop=True)
            avaliacoes_pivot.columns.name = None
            
            return avaliacoes_pivot
    except Exception as e:
        pass
    
    return _avaliacoes  # Se falhar, retornar original

# Pré-processar dados uma vez (com cache, sem spinner)
inscricoes_originais, alunos_originais = preprocessar_dados(inscricoes, avaliacoes, alunos)

# Fazer pivot das avaliações ANTES dos filtros
avaliacoes_pivotadas = fazer_pivot_avaliacoes(avaliacoes)

# Manter cópia original das avaliações (já pivotadas) para filtros
avaliacoes_originais = avaliacoes_pivotadas.copy() if avaliacoes_pivotadas is not None else avaliacoes_pivotadas

# Criar cópias para filtros (sem cache - serão modificadas pelos filtros)
inscricoes = inscricoes_originais.copy()
alunos = alunos_originais.copy()

# ==========================================
# SIDEBAR - FILTROS
# ==========================================
st.sidebar.title("🔍 Filtros")

# Inicializar session state para filtros interativos
if 'filtro_status_clicado' not in st.session_state:
    st.session_state.filtro_status_clicado = None
if 'filtro_genero_clicado' not in st.session_state:
    st.session_state.filtro_genero_clicado = None
if 'filtro_ciclo' not in st.session_state:
    st.session_state.filtro_ciclo = 'Todos'
if 'filtro_local' not in st.session_state:
    st.session_state.filtro_local = 'Todos'
if 'filtro_status' not in st.session_state:
    st.session_state.filtro_status = 'Todos'
if 'filtro_genero' not in st.session_state:
    st.session_state.filtro_genero = 'Todos'

# Função auxiliar para relacionar locais de forma inteligente
def relacionar_locais(local_aluno, colunas_inscricoes):
    """Relaciona local de aluno com colunas de inscrições usando nomes de regiões"""
    if pd.isna(local_aluno) or local_aluno == '':
        return False
    
    local_aluno_str = str(local_aluno).upper().strip()
    
    # Lista de palavras-chave comuns de regiões do DF
    regioes_df = ['PLANALTINA', 'GAMA', 'CEILANDIA', 'CEILÂNDIA', 'TAGUATINGA', 'SAMAMBAIA', 
                   'BRAZLANDIA', 'BRAZLÂNDIA', 'SOBRADINHO', 'SOBRADINHO II', 'SOBRADINHO 2',
                   'GUARA', 'GUARÁ', 'CRUZEIRO', 'SUDOESTE', 'NORTE', 'SUL', 'LESTE', 'OESTE',
                   'ASA NORTE', 'ASA SUL', 'LAGO NORTE', 'LAGO SUL', 'AGUAS CLARAS', 'ÁGUAS CLARAS',
                   'RIACHO FUNDO', 'SANTA MARIA', 'RECANTO DAS EMAS', 'CANDANGOLANDIA', 'CANDANGOLÂNDIA']
    
    # Extrair palavras-chave do local do aluno
    palavras_chave = []
    for regiao in regioes_df:
        if regiao in local_aluno_str:
            palavras_chave.append(regiao)
    
    # Se não encontrou palavras-chave conhecidas, usar o próprio nome
    if not palavras_chave:
        palavras_chave = [local_aluno_str]
    
    # Procurar em todas as colunas de inscrições que podem conter local
    for col in colunas_inscricoes:
        col_lower = col.lower()
        if any(palavra in col_lower for palavra in ['local', 'região', 'regiao', 'cidade', 'endereco', 'endereço', 'bairro']):
            return True
    
    return False

# Função para aplicar filtros (sem cache - filtros mudam dinamicamente)
def aplicar_filtros(_alunos, _inscricoes, ciclo_selecionado, local_selecionado, status_selecionado, genero_selecionado):
    """Aplica filtros aos dados de alunos e inscrições com proteção contra erros - FILTROS RELACIONADOS"""
    try:
        alunos_filtrados = _alunos.copy()
        inscricoes_filtradas = _inscricoes.copy()
    except Exception as e:
        st.error(f"Erro ao copiar dados: {e}")
        return _alunos, _inscricoes  # Retornar dados originais em caso de erro
    
    # Filtro por ciclo (afeta alunos e pode afetar inscrições relacionadas)
    if ciclo_selecionado != 'Todos' and 'CICLO' in alunos_filtrados.columns:
        alunos_filtrados = alunos_filtrados[alunos_filtrados['CICLO'].astype(str) == ciclo_selecionado]
        
        # Se houver coluna de ciclo nas inscrições, filtrar também
        if 'CICLO' in inscricoes_filtradas.columns:
            inscricoes_filtradas = inscricoes_filtradas[inscricoes_filtradas['CICLO'].astype(str) == ciclo_selecionado]
        else:
            # Tentar relacionar por outras colunas que possam conter ciclo
            for col in inscricoes_filtradas.columns:
                if 'ciclo' in col.lower():
                    inscricoes_filtradas = inscricoes_filtradas[inscricoes_filtradas[col].astype(str) == str(ciclo_selecionado)]
                    break
        
        # RELACIONAR CICLO COM INSCRIÇÕES: Tentar relacionar alunos filtrados com inscrições
        colunas_relacao = []
        palavras_chave_relacao = ['email', 'e-mail', 'nome', 'cpf', 'telefone', 'celular', 'whatsapp']
        
        for col_aluno in alunos_filtrados.columns:
            col_aluno_lower = col_aluno.lower()
            for col_inscricao in inscricoes_filtradas.columns:
                col_inscricao_lower = col_inscricao.lower()
                if (col_aluno_lower == col_inscricao_lower or 
                    any(palavra in col_aluno_lower and palavra in col_inscricao_lower for palavra in palavras_chave_relacao)):
                    colunas_relacao.append((col_aluno, col_inscricao))
                    break
        
        # Se encontrou colunas de relação, filtrar inscrições relacionadas
        if colunas_relacao:
            valores_relacao = set()
            for col_aluno, col_inscricao in colunas_relacao:
                valores = alunos_filtrados[col_aluno].dropna().astype(str).str.strip().str.upper()
                valores_relacao.update(valores.unique())
            
            if valores_relacao:
                mask_inscricoes = pd.Series([False] * len(inscricoes_filtradas))
                for col_aluno, col_inscricao in colunas_relacao:
                    valores_inscricao = inscricoes_filtradas[col_inscricao].astype(str).str.strip().str.upper()
                    mask_inscricoes |= valores_inscricao.isin(valores_relacao)
                inscricoes_filtradas = inscricoes_filtradas[mask_inscricoes]
    
    # Filtro por local - RELAÇÃO INTELIGENTE com inscrições usando nomes de regiões
    if local_selecionado != 'Todos' and 'LOCAL' in alunos_filtrados.columns:
        alunos_filtrados = alunos_filtrados[alunos_filtrados['LOCAL'] == local_selecionado]
        
        # Normalizar local selecionado para busca
        local_selecionado_upper = str(local_selecionado).upper().strip()
        
        # Extrair palavras-chave do local (ex: "Planaltina", "Gama", etc)
        palavras_chave_local = []
        regioes_df = ['PLANALTINA', 'GAMA', 'CEILANDIA', 'CEILÂNDIA', 'TAGUATINGA', 'SAMAMBAIA', 
                      'BRAZLANDIA', 'BRAZLÂNDIA', 'SOBRADINHO', 'GUARA', 'GUARÁ', 'CRUZEIRO',
                      'AGUAS CLARAS', 'ÁGUAS CLARAS', 'RIACHO FUNDO', 'SANTA MARIA', 
                      'RECANTO DAS EMAS', 'CANDANGOLANDIA', 'CANDANGOLÂNDIA']
        
        for regiao in regioes_df:
            if regiao in local_selecionado_upper:
                palavras_chave_local.append(regiao)
        
        # Se não encontrou palavras-chave conhecidas, usar o próprio nome
        if not palavras_chave_local:
            palavras_chave_local = [local_selecionado_upper]
        
        # Filtrar inscrições por local usando busca inteligente
        # 1. Se houver coluna LOCAL exata nas inscrições
        if 'LOCAL' in inscricoes_filtradas.columns:
            mask_local = pd.Series([False] * len(inscricoes_filtradas))
            for palavra in palavras_chave_local:
                mask_local |= inscricoes_filtradas['LOCAL'].astype(str).str.upper().str.contains(
                    palavra, case=False, na=False, regex=False
                )
            inscricoes_filtradas = inscricoes_filtradas[mask_local]
        
        # 2. Buscar em outras colunas que possam conter local/região
        colunas_local = []
        for col in inscricoes_filtradas.columns:
            col_lower = col.lower()
            if any(palavra in col_lower for palavra in ['local', 'região', 'regiao', 'cidade', 'endereco', 'endereço', 'bairro', 'endereco completo', 'endereço completo']):
                colunas_local.append(col)
        
        # Aplicar busca em todas as colunas de local encontradas
        if colunas_local:
            mask_inscricoes_local = pd.Series([False] * len(inscricoes_filtradas))
            for col in colunas_local:
                for palavra in palavras_chave_local:
                    mask_inscricoes_local |= inscricoes_filtradas[col].astype(str).str.upper().str.contains(
                        palavra, case=False, na=False, regex=False
                    )
            if mask_inscricoes_local.sum() > 0:
                inscricoes_filtradas = inscricoes_filtradas[mask_inscricoes_local]
    
    # Filtro por status (incluindo filtro interativo de gráfico)
    status_final = status_selecionado
    if st.session_state.filtro_status_clicado:
        status_final = st.session_state.filtro_status_clicado
    
    # Aplicar filtro de status apenas se não for 'Todos'
    if status_final != 'Todos':
        if 'STATUS_NORMALIZADO' in alunos_filtrados.columns:
            if status_final == 'CURSANDO':
                alunos_filtrados = alunos_filtrados[alunos_filtrados['STATUS_NORMALIZADO'] == 'CURSANDO']
            elif status_final == 'CONCLUÍDO':
                alunos_filtrados = alunos_filtrados[alunos_filtrados['STATUS_NORMALIZADO'] == 'CONCLUÍDO']
            elif status_final == 'CURSANDO + CONCLUÍDO':
                alunos_filtrados = alunos_filtrados[alunos_filtrados['STATUS_NORMALIZADO'].isin(['CURSANDO', 'CONCLUÍDO'])]
        elif 'STATUS' in alunos_filtrados.columns:
            # Normalizar STATUS para comparação (case-insensitive e com regex)
            status_upper = alunos_filtrados['STATUS'].astype(str).str.upper().str.strip()
            if status_final == 'CONCLUÍDO' or status_final == 'CONCLUIDO':
                alunos_filtrados = alunos_filtrados[status_upper.str.contains('CONCLUIDO|CONCLUÍDO', case=False, na=False, regex=True)]
            elif status_final == 'CURSANDO':
                alunos_filtrados = alunos_filtrados[status_upper.str.contains('CURSANDO|EM CURSO|EM ANDAMENTO', case=False, na=False, regex=True)]
            elif status_final == 'CONCLUIDO + CURSANDO' or status_final == 'CURSANDO + CONCLUÍDO':
                alunos_filtrados = alunos_filtrados[status_upper.str.contains('CONCLUIDO|CONCLUÍDO|CURSANDO|EM CURSO', case=False, na=False, regex=True)]
            elif status_final == 'DESISTENTE':
                alunos_filtrados = alunos_filtrados[status_upper.str.contains('DESISTENTE', case=False, na=False, regex=True)]
            else:
                # Tentar match exato
                alunos_filtrados = alunos_filtrados[status_upper == status_final.upper()]
        
        # RELACIONAR STATUS COM INSCRIÇÕES: Se filtrar por status, tentar relacionar com inscrições
        # Buscar colunas que possam relacionar alunos com inscrições (email, nome, CPF, etc)
        colunas_relacao = []
        palavras_chave_relacao = ['email', 'e-mail', 'nome', 'cpf', 'telefone', 'celular', 'whatsapp']
        
        for col_aluno in alunos_filtrados.columns:
            col_aluno_lower = col_aluno.lower()
            for col_inscricao in inscricoes_filtradas.columns:
                col_inscricao_lower = col_inscricao.lower()
                # Match exato ou match por palavra-chave
                if (col_aluno_lower == col_inscricao_lower or 
                    any(palavra in col_aluno_lower and palavra in col_inscricao_lower for palavra in palavras_chave_relacao)):
                    colunas_relacao.append((col_aluno, col_inscricao))
                    break
        
        # Se encontrou colunas de relação, filtrar inscrições relacionadas
        if colunas_relacao:
            # Pegar valores únicos dos alunos filtrados para relacionar
            valores_relacao = set()
            for col_aluno, col_inscricao in colunas_relacao:
                valores = alunos_filtrados[col_aluno].dropna().astype(str).str.strip().str.upper()
                valores_relacao.update(valores.unique())
            
            # Filtrar inscrições que têm esses valores
            if valores_relacao:
                mask_inscricoes = pd.Series([False] * len(inscricoes_filtradas))
                for col_aluno, col_inscricao in colunas_relacao:
                    valores_inscricao = inscricoes_filtradas[col_inscricao].astype(str).str.strip().str.upper()
                    mask_inscricoes |= valores_inscricao.isin(valores_relacao)
                inscricoes_filtradas = inscricoes_filtradas[mask_inscricoes]
    
    # Filtro por gênero - RELACIONADO: afeta inscrições E pode afetar alunos relacionados
    genero_final = genero_selecionado
    if st.session_state.filtro_genero_clicado:
        genero_final = st.session_state.filtro_genero_clicado
    
    # Aplicar filtro de gênero nas inscrições
    if genero_final != 'Todos':
        # Filtrar inscrições por gênero
        if 'Sexo:' in inscricoes_filtradas.columns:
            inscricoes_filtradas = inscricoes_filtradas[inscricoes_filtradas['Sexo:'].astype(str).str.upper().str.strip() == genero_final.upper().strip()]
        
        # Se houver coluna de gênero/sexo nos alunos, filtrar também
        for col in alunos_filtrados.columns:
            if 'sexo' in col.lower() or 'genero' in col.lower() or 'gênero' in col.lower():
                alunos_filtrados = alunos_filtrados[alunos_filtrados[col].astype(str).str.upper().str.strip() == genero_final.upper().strip()]
                break
    
    return alunos_filtrados, inscricoes_filtradas

# Filtro por ciclo (se disponível) - usar dados originais para opções
if 'CICLO' in alunos_originais.columns:
    ciclos_disponiveis = ['Todos'] + sorted(alunos_originais['CICLO'].dropna().unique().astype(str).tolist())
    # Usar session_state para controlar o valor
    if st.session_state.filtro_ciclo not in ciclos_disponiveis:
        st.session_state.filtro_ciclo = 'Todos'
    
    ciclo_selecionado = st.sidebar.selectbox(
        "Ciclo", 
        ciclos_disponiveis,
        index=ciclos_disponiveis.index(st.session_state.filtro_ciclo) if st.session_state.filtro_ciclo in ciclos_disponiveis else 0,
        key='selectbox_ciclo'
    )
    st.session_state.filtro_ciclo = ciclo_selecionado
else:
    ciclo_selecionado = 'Todos'
    st.session_state.filtro_ciclo = 'Todos'

# Filtro por local - usar dados originais para opções
if 'LOCAL' in alunos_originais.columns:
    locais_disponiveis = ['Todos'] + sorted(alunos_originais['LOCAL'].dropna().unique().tolist())
    # Usar session_state para controlar o valor
    if st.session_state.filtro_local not in locais_disponiveis:
        st.session_state.filtro_local = 'Todos'
    
    local_selecionado = st.sidebar.selectbox(
        "Local", 
        locais_disponiveis,
        index=locais_disponiveis.index(st.session_state.filtro_local) if st.session_state.filtro_local in locais_disponiveis else 0,
        key='selectbox_local'
    )
    st.session_state.filtro_local = local_selecionado
else:
    local_selecionado = 'Todos'
    st.session_state.filtro_local = 'Todos'

# Filtro por status - Foco em Cursando e Concluído - usar dados originais para opções
if 'STATUS_NORMALIZADO' in alunos_originais.columns:
    status_opcoes = ['Todos', 'CURSANDO', 'CONCLUÍDO', 'CURSANDO + CONCLUÍDO']
    # Usar session_state para controlar o valor
    if st.session_state.filtro_status not in status_opcoes:
        st.session_state.filtro_status = 'Todos'
    # Se houver filtro clicado, usar ele
    if st.session_state.filtro_status_clicado and st.session_state.filtro_status_clicado in status_opcoes:
        st.session_state.filtro_status = st.session_state.filtro_status_clicado
    status_selecionado = st.sidebar.selectbox(
        "Status", 
        status_opcoes,
        index=status_opcoes.index(st.session_state.filtro_status) if st.session_state.filtro_status in status_opcoes else 0,
        key='selectbox_status'
    )
    st.session_state.filtro_status = status_selecionado
elif 'STATUS' in alunos_originais.columns:
    status_disponiveis = ['Todos', 'CONCLUIDO', 'CURSANDO', 'CONCLUIDO + CURSANDO'] + \
                         [s for s in sorted(alunos_originais['STATUS'].dropna().unique().tolist()) 
                          if s not in ['CONCLUIDO', 'CURSANDO']]
    # Usar session_state para controlar o valor
    if st.session_state.filtro_status not in status_disponiveis:
        st.session_state.filtro_status = 'Todos'
    
    status_selecionado = st.sidebar.selectbox(
        "Status", 
        status_disponiveis,
        index=status_disponiveis.index(st.session_state.filtro_status) if st.session_state.filtro_status in status_disponiveis else 0,
        key='selectbox_status'
    )
    st.session_state.filtro_status = status_selecionado
else:
    status_selecionado = 'Todos'
    st.session_state.filtro_status = 'Todos'

# Filtro por gênero - usar dados originais para opções
if 'Sexo:' in inscricoes_originais.columns:
    generos_disponiveis = ['Todos'] + sorted(inscricoes_originais['Sexo:'].dropna().unique().tolist())
    # Usar session_state para controlar o valor
    if st.session_state.filtro_genero not in generos_disponiveis:
        st.session_state.filtro_genero = 'Todos'
    # Se houver filtro clicado, usar ele
    if st.session_state.filtro_genero_clicado and st.session_state.filtro_genero_clicado in generos_disponiveis:
        st.session_state.filtro_genero = st.session_state.filtro_genero_clicado
    genero_selecionado = st.sidebar.selectbox(
        "Gênero", 
        generos_disponiveis,
        index=generos_disponiveis.index(st.session_state.filtro_genero) if st.session_state.filtro_genero in generos_disponiveis else 0,
        key='selectbox_genero'
    )
    st.session_state.filtro_genero = genero_selecionado
else:
    genero_selecionado = 'Todos'
    st.session_state.filtro_genero = 'Todos'


# Função para filtrar avaliações baseado nos filtros aplicados
def filtrar_avaliacoes(_avaliacoes, _alunos_filtrados, _inscricoes_filtradas, _alunos_originais, _inscricoes_originais, ciclo_selecionado):
    """Filtra avaliações baseado nos filtros aplicados em alunos e inscrições"""
    if _avaliacoes is None or len(_avaliacoes) == 0:
        return _avaliacoes
    
    avaliacoes_filtradas = _avaliacoes.copy()
    
    # Função auxiliar para normalizar valores de ciclo (remover .0, espaços, etc)
    def normalizar_ciclo(valor):
        if pd.isna(valor):
            return None
        valor_str = str(valor).strip()
        # Remover .0 do final se houver
        if valor_str.endswith('.0'):
            valor_str = valor_str[:-2]
        # Remover espaços e converter para string limpa
        return valor_str.strip()
    
    # Função para extrair ciclo da coluna Pesquisa
    def extrair_ciclo_da_pesquisa(valor):
        """Extrai o número do ciclo do nome da pesquisa"""
        if pd.isna(valor):
            return None
        valor_str = str(valor).upper().strip()
        # Se contém "X CICLO" (ex: "2 CICLO", "3 CICLO")
        match = re.search(r'(\d+)\s*CICLO', valor_str)
        if match:
            return match.group(1)
        # Se não tem número de ciclo explícito, é ciclo 1
        if 'AVALIAÇÃO' in valor_str and ('MCOM' in valor_str or 'MKT DIGITAL' in valor_str):
            # Verificar se não tem número de ciclo
            if not re.search(r'\d+\s*CICLO', valor_str):
                return '1'
        return None
    
    # Aplicar filtro de ciclo primeiro (se houver coluna CICLO nas avaliações)
    if ciclo_selecionado != 'Todos':
        ciclo_selecionado_normalizado = normalizar_ciclo(ciclo_selecionado)
        mask_ciclo = pd.Series([False] * len(avaliacoes_filtradas))
        
        # 1. Tentar filtrar pela coluna CICLO se existir
        if 'CICLO' in avaliacoes_filtradas.columns:
            ciclos_normalizados = avaliacoes_filtradas['CICLO'].apply(normalizar_ciclo)
            mask_ciclo |= (ciclos_normalizados == ciclo_selecionado_normalizado)
        
        # 2. Tentar filtrar pela coluna Pesquisa (prioridade alta)
        if 'Pesquisa' in avaliacoes_filtradas.columns:
            ciclos_pesquisa = avaliacoes_filtradas['Pesquisa'].apply(extrair_ciclo_da_pesquisa)
            # Normalizar valores None para evitar problemas na comparação
            ciclos_pesquisa_normalizados = ciclos_pesquisa.apply(lambda x: normalizar_ciclo(x) if x is not None else None)
            mask_pesquisa = (ciclos_pesquisa_normalizados == ciclo_selecionado_normalizado)
            mask_ciclo |= mask_pesquisa
        
        # 3. Tentar encontrar ciclo em outras colunas
        for col in avaliacoes_filtradas.columns:
            col_lower = str(col).lower()
            if 'ciclo' in col_lower and col != 'CICLO' and col != 'Pesquisa':
                valores_normalizados = avaliacoes_filtradas[col].apply(normalizar_ciclo)
                mask_ciclo |= (valores_normalizados == ciclo_selecionado_normalizado)
        
        # Aplicar o filtro se encontrou algum match
        if mask_ciclo.any():
            avaliacoes_filtradas = avaliacoes_filtradas[mask_ciclo].copy()
        elif 'Pesquisa' in avaliacoes_filtradas.columns:
            # Se não encontrou nenhum match, tentar busca mais detalhada na coluna Pesquisa
            mask_ciclo_detalhado = pd.Series([False] * len(avaliacoes_filtradas))
            for idx in range(len(avaliacoes_filtradas)):
                pesquisa_val = avaliacoes_filtradas['Pesquisa'].iloc[idx]
                ciclo_extraido = extrair_ciclo_da_pesquisa(pesquisa_val)
                if ciclo_extraido is not None:
                    ciclo_extraido_norm = normalizar_ciclo(ciclo_extraido)
                    if ciclo_extraido_norm == ciclo_selecionado_normalizado:
                        mask_ciclo_detalhado.iloc[idx] = True
            if mask_ciclo_detalhado.any():
                avaliacoes_filtradas = avaliacoes_filtradas[mask_ciclo_detalhado].copy()
    
    # Se não há outros filtros aplicados além do ciclo, retornar avaliações filtradas por ciclo
    if len(_alunos_filtrados) == len(_alunos_originais) and len(_inscricoes_filtradas) == len(_inscricoes_originais):
        return avaliacoes_filtradas
    
    # Função auxiliar para normalizar valores de ciclo (remover .0, espaços, etc)
    def normalizar_ciclo_fallback(valor):
        if pd.isna(valor):
            return None
        valor_str = str(valor).strip()
        # Remover .0 do final se houver
        if valor_str.endswith('.0'):
            valor_str = valor_str[:-2]
        return valor_str.strip()
    
    # Função para extrair ciclo da coluna Pesquisa (fallback)
    def extrair_ciclo_da_pesquisa_fallback(valor):
        """Extrai o número do ciclo do nome da pesquisa"""
        if pd.isna(valor):
            return None
        valor_str = str(valor).upper().strip()
        # Se contém "X CICLO" (ex: "2 CICLO", "3 CICLO")
        match = re.search(r'(\d+)\s*CICLO', valor_str)
        if match:
            return match.group(1)
        # Se não tem número de ciclo explícito, é ciclo 1
        if 'AVALIAÇÃO' in valor_str and ('MCOM' in valor_str or 'MKT DIGITAL' in valor_str):
            # Verificar se não tem número de ciclo
            if not re.search(r'\d+\s*CICLO', valor_str):
                return '1'
        return None
    
    # Se após filtrar por ciclo não há dados, tentar buscar ciclo em colunas do pivot
    if len(avaliacoes_filtradas) == 0 and ciclo_selecionado != 'Todos':
        ciclo_selecionado_normalizado = normalizar_ciclo_fallback(ciclo_selecionado)
        mask_ciclo_fallback = pd.Series([False] * len(_avaliacoes))
        
        # Tentar encontrar ciclo na coluna Pesquisa primeiro
        if 'Pesquisa' in _avaliacoes.columns:
            ciclos_pesquisa = _avaliacoes['Pesquisa'].apply(extrair_ciclo_da_pesquisa_fallback)
            mask_ciclo_fallback |= (ciclos_pesquisa == ciclo_selecionado_normalizado)
        
        # Tentar encontrar coluna que contém ciclo (pode ser uma das perguntas pivotadas)
        for col in _avaliacoes.columns:
            col_lower = str(col).lower()
            if 'ciclo' in col_lower and col != 'Pesquisa':
                valores_normalizados = _avaliacoes[col].apply(normalizar_ciclo_fallback)
                mask_ciclo_fallback |= (valores_normalizados == ciclo_selecionado_normalizado)
        
        if mask_ciclo_fallback.any():
            avaliacoes_filtradas = _avaliacoes[mask_ciclo_fallback]
        
        # Se ainda não encontrou, retornar todas (melhor que nada quando filtramos apenas por ciclo)
        if len(avaliacoes_filtradas) == 0:
            # Se só filtramos por ciclo e não há outros filtros, retornar todas
            if len(_alunos_filtrados) == len(_alunos_originais) and len(_inscricoes_filtradas) == len(_inscricoes_originais):
                return _avaliacoes
            return avaliacoes_filtradas
    
    # Tentar relacionar avaliações com alunos/inscrições filtrados através de colunas comuns
    # Buscar colunas que possam relacionar (email, nome, CPF, etc)
    valores_relacao = set()
    palavras_chave_relacao = ['email', 'e-mail', 'nome', 'cpf', 'telefone', 'celular', 'whatsapp']
    
    # Buscar valores de identificação em alunos filtrados
    for col_aluno in _alunos_filtrados.columns:
        col_aluno_lower = str(col_aluno).lower()
        if any(palavra in col_aluno_lower for palavra in palavras_chave_relacao):
            valores = _alunos_filtrados[col_aluno].dropna().astype(str).str.strip().str.upper()
            valores_relacao.update(valores.unique())
    
    # Buscar valores de identificação em inscrições filtradas
    for col_inscricao in _inscricoes_filtradas.columns:
        col_inscricao_lower = str(col_inscricao).lower()
        if any(palavra in col_inscricao_lower for palavra in palavras_chave_relacao):
            valores = _inscricoes_filtradas[col_inscricao].dropna().astype(str).str.strip().str.upper()
            valores_relacao.update(valores.unique())
    
    # Tentar encontrar coluna de identificação nas avaliações para relacionar
    id_col_avaliacoes = None
    palavras_chave_id = ['usuário', 'usuario', 'opinião', 'opiniao', 'pesquisa', 'email', 'e-mail', 'nome']
    
    for col in avaliacoes_filtradas.columns:
        col_lower = str(col).lower()
        if any(palavra in col_lower for palavra in palavras_chave_id):
            id_col_avaliacoes = col
            break
    
    # Se encontrou coluna de identificação e valores para relacionar, filtrar
    if id_col_avaliacoes and valores_relacao:
        valores_avaliacoes = avaliacoes_filtradas[id_col_avaliacoes].astype(str).str.strip().str.upper()
        mask = valores_avaliacoes.isin(valores_relacao)
        avaliacoes_filtradas = avaliacoes_filtradas[mask]
    
    # Se não conseguiu relacionar com alunos/inscrições, mas filtrou por ciclo, manter filtro de ciclo
    # Se não há outros filtros além do ciclo, já retornamos acima
    # Se há outros filtros mas não conseguiu relacionar, retornar avaliações filtradas apenas por ciclo
    if len(avaliacoes_filtradas) == 0 and ciclo_selecionado != 'Todos':
        # Tentar filtrar novamente apenas por ciclo usando a coluna Pesquisa
        if 'Pesquisa' in _avaliacoes.columns:
            ciclos_pesquisa = _avaliacoes['Pesquisa'].apply(extrair_ciclo_da_pesquisa)
            # Normalizar valores None
            ciclos_pesquisa_normalizados = ciclos_pesquisa.apply(lambda x: normalizar_ciclo(x) if x is not None else None)
            mask_ciclo_pesquisa = (ciclos_pesquisa_normalizados == ciclo_selecionado_normalizado)
            if mask_ciclo_pesquisa.any():
                avaliacoes_filtradas = _avaliacoes[mask_ciclo_pesquisa].copy()
                return avaliacoes_filtradas
        
        # Se ainda não encontrou, tentar pela coluna CICLO diretamente
        if 'CICLO' in _avaliacoes.columns:
            ciclos_normalizados = _avaliacoes['CICLO'].apply(normalizar_ciclo)
            mask_ciclo_direto = (ciclos_normalizados == ciclo_selecionado_normalizado)
            if mask_ciclo_direto.any():
                avaliacoes_filtradas = _avaliacoes[mask_ciclo_direto].copy()
                return avaliacoes_filtradas
    
    return avaliacoes_filtradas

# Aplicar filtros nos dados ORIGINAIS (sem cache - filtros mudam dinamicamente)
alunos_filtrados, inscricoes_filtradas = aplicar_filtros(alunos_originais, inscricoes_originais, ciclo_selecionado, local_selecionado, status_selecionado, genero_selecionado)

# Filtrar avaliações baseado nos filtros aplicados
avaliacoes_filtradas = filtrar_avaliacoes(avaliacoes_originais, alunos_filtrados, inscricoes_filtradas, alunos_originais, inscricoes_originais, ciclo_selecionado)

# Usar dados filtrados para o restante do dashboard
alunos = alunos_filtrados
inscricoes = inscricoes_filtradas

# Garantir que avaliações filtradas sejam usadas
if avaliacoes_filtradas is not None and len(avaliacoes_filtradas) > 0:
    avaliacoes = avaliacoes_filtradas
elif ciclo_selecionado != 'Todos' and avaliacoes_originais is not None and len(avaliacoes_originais) > 0:
    # Se não encontrou dados filtrados mas há filtro de ciclo, tentar filtrar diretamente
    def extrair_ciclo_pesquisa_simples(valor):
        if pd.isna(valor):
            return None
        valor_str = str(valor).upper().strip()
        match = re.search(r'(\d+)\s*CICLO', valor_str)
        if match:
            return match.group(1)
        if 'AVALIAÇÃO' in valor_str and ('MCOM' in valor_str or 'MKT DIGITAL' in valor_str):
            if not re.search(r'\d+\s*CICLO', valor_str):
                return '1'
        return None
    
    ciclo_selecionado_norm = str(ciclo_selecionado).strip()
    if ciclo_selecionado_norm.endswith('.0'):
        ciclo_selecionado_norm = ciclo_selecionado_norm[:-2]
    
    # Tentar filtrar pela coluna Pesquisa
    if 'Pesquisa' in avaliacoes_originais.columns:
        ciclos_pesquisa = avaliacoes_originais['Pesquisa'].apply(extrair_ciclo_pesquisa_simples)
        mask = ciclos_pesquisa == ciclo_selecionado_norm
        if mask.any():
            avaliacoes = avaliacoes_originais[mask]
        else:
            avaliacoes = avaliacoes_originais
    # Tentar filtrar pela coluna CICLO se existir
    elif 'CICLO' in avaliacoes_originais.columns:
        ciclos_normalizados = avaliacoes_originais['CICLO'].astype(str).str.strip()
        ciclos_normalizados = ciclos_normalizados.str.replace('.0', '', regex=False)
        mask = ciclos_normalizados == ciclo_selecionado_norm
        if mask.any():
            avaliacoes = avaliacoes_originais[mask]
        else:
            avaliacoes = avaliacoes_originais
    else:
        avaliacoes = avaliacoes_originais
else:
    avaliacoes = avaliacoes_originais

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Informações")
# Mostrar indicador se filtros estão ativos
filtros_ativos = []
if ciclo_selecionado != 'Todos':
    filtros_ativos.append(f"Ciclo: {ciclo_selecionado}")
if local_selecionado != 'Todos':
    filtros_ativos.append(f"Local: {local_selecionado}")
if status_selecionado != 'Todos':
    filtros_ativos.append(f"Status: {status_selecionado}")
if genero_selecionado != 'Todos':
    filtros_ativos.append(f"Gênero: {genero_selecionado}")

if filtros_ativos:
    st.sidebar.success(f"**Filtros Ativos:**\n" + "\n".join(filtros_ativos))

st.sidebar.info(f"""
**Total de Registros:** {len(alunos):,}

**Última Atualização:** {datetime.now().strftime("%d/%m/%Y")}
""")


# Função helper para criar cards de métricas
def criar_card_metrica(titulo, valor, cor_borda, cor_texto, subtitulo=None):
    """Cria um card de métrica estilizado e responsivo"""
    if subtitulo:
        subtitulo_html = f'<p style="color: #b0b0b0; font-size: 0.85rem; margin: 0.3rem 0 0 0;">{subtitulo}</p>'
    else:
        subtitulo_html = ''
    
    html = f'<div class="metric-card-custom" style="background: linear-gradient(135deg, #2d2d44 0%, #1e1e2e 100%); padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.4); border: 2px solid {cor_borda}; height: 100%; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s ease, box-shadow 0.2s ease;"><p style="color: #b0b0b0; font-weight: 600; font-size: 0.95rem; margin: 0 0 0.8rem 0; line-height: 1.3;">{titulo}</p><div><p style="color: {cor_texto}; font-weight: bold; font-size: 2.2rem; margin: 0; line-height: 1.2;">{valor}</p>{subtitulo_html}</div></div>'
    return html

# ==========================================
# SEÇÃO 1: MÉTRICAS PRINCIPAIS
# ==========================================
st.markdown("---")
st.markdown("## 📈 Métricas Principais")

# Calcular métricas ANTES de exibir (usando dados FILTRADOS)
total_inscricoes = len(inscricoes)
total_alunos = len(alunos)

# Calcular status dos alunos (usando dados FILTRADOS)
if 'STATUS_NORMALIZADO' in alunos.columns:
    # Usar STATUS_NORMALIZADO se disponível (mais confiável)
    formados = len(alunos[alunos['STATUS_NORMALIZADO'] == 'CONCLUÍDO'])
    desistentes = len(alunos[alunos['STATUS_NORMALIZADO'] == 'DESISTENTE'])
    cursando = len(alunos[alunos['STATUS_NORMALIZADO'] == 'CURSANDO'])
    taxa_desistencia = (desistentes / total_alunos * 100) if total_alunos > 0 else 0
elif 'STATUS' in alunos.columns:
    # Usar STATUS original com múltiplas variações
    formados = len(alunos[alunos['STATUS'].astype(str).str.upper().str.contains('CONCLUIDO|CONCLUÍDO', case=False, na=False, regex=True)])
    desistentes = len(alunos[alunos['STATUS'].astype(str).str.upper().str.contains('DESISTENTE', case=False, na=False, regex=True)])
    cursando = len(alunos[alunos['STATUS'].astype(str).str.upper().str.contains('CURSANDO|EM CURSO|EM ANDAMENTO', case=False, na=False, regex=True)])
    taxa_desistencia = (desistentes / total_alunos * 100) if total_alunos > 0 else 0
else:
    formados = 0
    desistentes = 0
    cursando = 0
    taxa_desistencia = 0

# Layout responsivo: 5 colunas no desktop, empilhado no mobile
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(criar_card_metrica(
        "Total de Inscrições", 
        f"{total_inscricoes:,}", 
        "#90caf9", 
        "#90caf9"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(criar_card_metrica(
        "Total de Alunos", 
        f"{total_alunos:,}", 
        "#5c6bc0", 
        "#5c6bc0"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(criar_card_metrica(
        "Alunos Formados", 
        f"{formados:,}", 
        "#66bb6a", 
        "#66bb6a"
    ), unsafe_allow_html=True)

with col4:
    st.markdown(criar_card_metrica(
        "Taxa de Desistência", 
        f"{taxa_desistencia:.1f}%", 
        "#ef5350", 
        "#ef5350",
        f"Total: {desistentes:,} desistentes"
    ), unsafe_allow_html=True)

with col5:
    st.markdown(criar_card_metrica(
        "Alunos Cursando", 
        f"{cursando:,}", 
        "#ffa726", 
        "#ffa726"
    ), unsafe_allow_html=True)

# ==========================================
# SEÇÃO 2: PERFIL DOS ALUNOS
# ==========================================
st.markdown("---")
st.markdown("## 👥 Perfil dos Alunos")

col1, col2 = st.columns(2)

# Função para criar gráficos SEM cache (para permitir filtros dinâmicos)
def criar_grafico_sexo(_alunos):
    """Cria gráfico de distribuição por sexo usando dados de ALUNOS (DadosMetalab) - SEM CACHE para permitir filtros"""
    if _alunos is None or len(_alunos) == 0:
        return None
    
    # Procurar coluna de sexo/gênero nos dados de alunos
    coluna_sexo = None
    for col in _alunos.columns:
        if 'sexo' in col.lower() or 'genero' in col.lower() or 'gênero' in col.lower():
            coluna_sexo = col
            break
    
    if coluna_sexo is None:
        return None
    
    sexo_counts = _alunos[coluna_sexo].value_counts()
    if len(sexo_counts) == 0:
        return None
    fig = px.pie(
        values=sexo_counts.values,
        names=sexo_counts.index,
        title="Distribuição por Sexo",
        color_discrete_sequence=PALETA_METALAB
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
    fig.update_traces(hovertemplate="Sexo: %{label}<br>Quantidade: %{value}<extra></extra>")
    return aplicar_tema_escuro(fig)

def criar_grafico_idade(_alunos):
    """Cria gráfico de distribuição por idade agrupada em faixas etárias usando dados de ALUNOS (DadosMetalab)"""
    if _alunos is None or len(_alunos) == 0:
        return None
    
    idades_numericas = None
    
    # PRIORIDADE 1: Procurar coluna de idade direta (se existir)
    coluna_idade = None
    for col in _alunos.columns:
        col_lower = col.lower().strip()
        if any(palavra in col_lower for palavra in ['idade', 'age']):
            # Verificar se a coluna parece conter idades (números)
            amostra = _alunos[col].dropna().head(10)
            if len(amostra) > 0:
                valores_numericos = pd.to_numeric(amostra, errors='coerce').dropna()
                if len(valores_numericos) > 0:
                    valores_validos = valores_numericos[(valores_numericos >= 10) & (valores_numericos <= 100)]
                    if len(valores_validos) > 0:
                        coluna_idade = col
                        break
    
    # Se encontrou coluna de idade direta, usar ela
    if coluna_idade:
        idades = _alunos[coluna_idade].dropna()
        if len(idades) > 0:
            idades_numericas = pd.to_numeric(idades, errors='coerce').dropna()
            # Se não conseguiu converter, tentar extrair números do texto
            if len(idades_numericas) == 0:
                idades_numericas = idades.astype(str).str.extract(r'(\d+)')[0]
                idades_numericas = pd.to_numeric(idades_numericas, errors='coerce').dropna()
    
    # PRIORIDADE 2: Se não encontrou idade direta, calcular a partir de DATA DE NASCIMENTO
    if idades_numericas is None or len(idades_numericas) == 0:
        # Procurar coluna de data de nascimento (busca mais ampla)
        coluna_nascimento = None
        palavras_chave_nasc = ['data de nascimento', 'data nascimento', 'nascimento', 'nasc', 'birth', 'birthday', 'data nasc', 'dt nascimento', 'dt nasc', 'datanascimento']
        
        # Priorizar busca exata por "DATA DE NASCIMENTO"
        for col in _alunos.columns:
            col_lower = col.lower().strip()
            if 'data de nascimento' in col_lower or col_lower == 'data de nascimento':
                coluna_nascimento = col
                break
        
        # Se não encontrou exato, buscar por outras variações
        if coluna_nascimento is None:
            for col in _alunos.columns:
                col_lower = col.lower().strip()
                # Buscar por qualquer palavra-chave relacionada a nascimento
                if any(palavra in col_lower for palavra in palavras_chave_nasc):
                    coluna_nascimento = col
                    break
        
        # Se encontrou coluna de nascimento, calcular idade
        if coluna_nascimento:
            # Tentar múltiplos formatos de data
            datas_nasc = None
            
            # Método 1: Tentar com inferência automática (dayfirst=True para formato brasileiro)
            try:
                datas_nasc = pd.to_datetime(_alunos[coluna_nascimento], errors='coerce', dayfirst=True, infer_datetime_format=True)
            except:
                pass
            
            # Método 2: Se falhou, tentar formato brasileiro comum (DD/MM/YYYY)
            if datas_nasc is None or datas_nasc.isna().all():
                try:
                    datas_nasc = pd.to_datetime(_alunos[coluna_nascimento], errors='coerce', format='%d/%m/%Y')
                except:
                    pass
            
            # Método 3: Tentar formato ISO (YYYY-MM-DD)
            if datas_nasc is None or datas_nasc.isna().all():
                try:
                    datas_nasc = pd.to_datetime(_alunos[coluna_nascimento], errors='coerce', format='%Y-%m-%d')
                except:
                    pass
            
            # Método 4: Tentar sem especificar formato (pandas tenta inferir)
            if datas_nasc is None or datas_nasc.isna().all():
                try:
                    datas_nasc = pd.to_datetime(_alunos[coluna_nascimento], errors='coerce')
                except:
                    pass
            
            # Se conseguiu converter pelo menos algumas datas
            if datas_nasc is not None:
                # Filtrar apenas datas válidas
                datas_validas = datas_nasc.dropna()
                
                if len(datas_validas) > 0:
                    # Calcular idade atual
                    hoje = pd.Timestamp.now()
                    
                    # Calcular diferença em anos, ajustando para aniversário
                    # Se ainda não fez aniversário este ano, subtrair 1
                    idades_calculadas = hoje.year - datas_validas.dt.year
                    # Ajustar se ainda não fez aniversário
                    mask_nao_aniversario = (hoje.month < datas_validas.dt.month) | (
                        (hoje.month == datas_validas.dt.month) & (hoje.day < datas_validas.dt.day)
                    )
                    idades_calculadas = idades_calculadas - mask_nao_aniversario.astype(int)
                    
                    # Filtrar idades válidas (entre 10 e 100 anos)
                    idades_numericas = idades_calculadas[(idades_calculadas >= 10) & (idades_calculadas <= 100)]
                    
                    if len(idades_numericas) == 0:
                        idades_numericas = None
                else:
                    idades_numericas = None
            else:
                idades_numericas = None
    
    # Se ainda não conseguiu calcular idades, retornar None
    if idades_numericas is None or len(idades_numericas) == 0:
        return None
    
    # Filtrar idades razoáveis (entre 10 e 100 anos) - garantir novamente
    idades_numericas = idades_numericas[(idades_numericas >= 10) & (idades_numericas <= 100)]
    
    if len(idades_numericas) == 0:
        return None
    
    # Criar faixas etárias
    bins = [0, 18, 25, 30, 35, 40, 45, 50, 60, 100]
    labels = ['Até 18', '19-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-60', 'Acima de 60']
    
    # Agrupar idades em faixas
    idades_faixas = pd.cut(idades_numericas, bins=bins, labels=labels, include_lowest=True)
    idade_counts = idades_faixas.value_counts().sort_index()
    
    # Remover faixas vazias
    idade_counts = idade_counts[idade_counts > 0]
    
    if len(idade_counts) == 0:
        return None
    
    fig = px.bar(
        x=idade_counts.index.astype(str),
        y=idade_counts.values,
        title="Distribuição por Idade",
        labels={'x': 'Faixa Etária', 'y': 'Quantidade'},
        color=idade_counts.values,
        color_continuous_scale=['#1a237e', '#3949ab', '#5c6bc0', '#7986cb', '#90caf9']
    )
    fig.update_traces(
        hovertemplate="Faixa Etária: %{x} anos<br>Quantidade: %{y}<extra></extra>",
        marker_line_color='rgba(92, 107, 192, 0.5)',
        marker_line_width=1
    )
    fig.update_layout(
        xaxis=dict(title="Faixa Etária (anos)", tickangle=-45),
        yaxis=dict(title="Quantidade de Alunos")
    )
    return aplicar_tema_escuro(fig)

def criar_grafico_raca(_alunos):
    """Cria gráfico de distribuição por raça/cor usando dados de ALUNOS (DadosMetalab) - SEM CACHE para permitir filtros"""
    if _alunos is None or len(_alunos) == 0:
        return None
    
    # Procurar coluna de raça/cor nos dados de alunos
    coluna_raca = None
    for col in _alunos.columns:
        if 'ibge' in col.lower() or 'raça' in col.lower() or 'raca' in col.lower() or 'cor' in col.lower() or 'autodeclara' in col.lower():
            coluna_raca = col
            break
    
    if coluna_raca is None:
        return None
    
    raca_counts = _alunos[coluna_raca].value_counts()
    if len(raca_counts) == 0:
        return None
    fig = px.bar(
        x=raca_counts.values,
        y=raca_counts.index,
        orientation='h',
        title="Distribuição por Raça/Cor (IBGE)",
        labels={'x': 'Quantidade', 'y': 'Raça/Cor'},
        color=raca_counts.values,
        color_continuous_scale=['#1a237e', '#3949ab', '#5c6bc0', '#7986cb', '#90caf9']
    )
    fig.update_traces(hovertemplate="Raça/Cor: %{y}<br>Quantidade: %{x}<extra></extra>")
    return aplicar_tema_escuro(fig)

def remover_acentos(texto):
    """Remove acentos de um texto de forma robusta"""
    if pd.isna(texto):
        return texto
    
    texto_str = str(texto).lower()
    # Mapeamento completo de acentos
    acentos = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ć': 'c', 'č': 'c',
        'ñ': 'n', 'ń': 'n',
        'ý': 'y', 'ÿ': 'y'
    }
    resultado = texto_str
    for acento, sem_acento in acentos.items():
        resultado = resultado.replace(acento, sem_acento)
    return resultado

def normalizar_categoria_renda(valor):
    """Normaliza e padroniza categorias de renda para agrupar duplicatas de forma robusta"""
    if pd.isna(valor) or valor == '':
        return None
    
    # Converter para string e normalizar
    valor_str = str(valor).strip()
    
    # Remover acentos e converter para minúsculas
    valor_normalizado = remover_acentos(valor_str)
    
    # Normalizar espaços múltiplos
    valor_normalizado = re.sub(r'\s+', ' ', valor_normalizado).strip()
    
    # Remover palavras comuns que podem variar
    valor_normalizado = valor_normalizado.replace('recebe', '').replace('de', '').strip()
    valor_normalizado = re.sub(r'\s+', ' ', valor_normalizado).strip()
    
    # Padrões de correspondência (em ordem de especificidade)
    
    # 1. Não possui renda mensal (mais específico primeiro)
    padroes_sem_renda = [
        'nao possui renda mensal', 'nao possui renda', 'sem renda mensal', 
        'sem renda', 'sem renda familiar', 'nao tem renda'
    ]
    if any(padrao in valor_normalizado for padrao in padroes_sem_renda):
        return 'Não possui renda mensal'
    
    # 2. Até meio salário mínimo
    padroes_meio = ['meio salario', '0.5 salario', 'ate meio', 'até meio']
    if any(padrao in valor_normalizado for padrao in padroes_meio) and 'salario' in valor_normalizado:
        return 'Até meio salário mínimo'
    
    # 3. Até um salário mínimo
    padroes_um = ['ate um', 'até um', 'ate 1', 'até 1', 'um salario', '1 salario']
    if any(padrao in valor_normalizado for padrao in padroes_um) and 'salario' in valor_normalizado and 'meio' not in valor_normalizado:
        return 'Até um salário mínimo'
    
    # 4. De 1 a 2 salários mínimos
    padroes_1_2 = ['1 a 2', '1-2', '1 ate 2', '1 até 2', 'um a dois']
    if any(padrao in valor_normalizado for padrao in padroes_1_2) and 'salario' in valor_normalizado:
        return 'De 1 a 2 salários mínimos'
    
    # 5. De 2 a 3 salários mínimos (NOVO - estava faltando!)
    padroes_2_3 = ['2 a 3', '2-3', '2 ate 3', '2 até 3', 'dois a tres', 'dois a três']
    if any(padrao in valor_normalizado for padrao in padroes_2_3) and 'salario' in valor_normalizado:
        return 'De 2 a 3 salários mínimos'
    
    # 6. De 3 a 4 salários mínimos
    padroes_3_4 = ['3 a 4', '3-4', '3 ate 4', '3 até 4', 'tres a quatro', 'três a quatro']
    if any(padrao in valor_normalizado for padrao in padroes_3_4) and 'salario' in valor_normalizado:
        return 'De 3 a 4 salários mínimos'
    
    # 7. Acima de 5 salários mínimos
    padroes_5_mais = ['acima de 5', 'mais de 5', 'acima 5', 'mais 5', '5 ou mais', '5+']
    if any(padrao in valor_normalizado for padrao in padroes_5_mais) and 'salario' in valor_normalizado:
        return 'Acima de 5 salários mínimos'
    
    # 8. Correspondência por números e palavras-chave (fallback mais inteligente)
    # Extrair números do texto
    numeros = re.findall(r'\d+', valor_normalizado)
    
    if 'salario' in valor_normalizado or 'salários' in valor_normalizado:
        if 'meio' in valor_normalizado or '0.5' in valor_normalizado:
            return 'Até meio salário mínimo'
        elif 'um' in valor_normalizado or '1' in valor_normalizado:
            if '2' not in valor_normalizado and '3' not in valor_normalizado:
                return 'Até um salário mínimo'
        elif len(numeros) >= 2:
            num1, num2 = int(numeros[0]), int(numeros[1])
            if num1 == 1 and num2 == 2:
                return 'De 1 a 2 salários mínimos'
            elif num1 == 2 and num2 == 3:
                return 'De 2 a 3 salários mínimos'
            elif num1 == 3 and num2 == 4:
                return 'De 3 a 4 salários mínimos'
        elif len(numeros) == 1:
            num = int(numeros[0])
            if num >= 5:
                return 'Acima de 5 salários mínimos'
    
    # Se não encontrou padrão conhecido, retornar o valor original capitalizado
    return valor_str.title()

def criar_grafico_renda(_alunos):
    """Cria gráfico de distribuição por renda usando dados de ALUNOS (DadosMetalab) - SEM CACHE para permitir filtros"""
    if _alunos is None or len(_alunos) == 0:
        return None
    
    # Procurar coluna de renda nos dados de alunos
    coluna_renda = None
    for col in _alunos.columns:
        if 'renda' in col.lower() or 'salario' in col.lower() or 'salário' in col.lower() or 'familiar' in col.lower():
            coluna_renda = col
            break
    
    if coluna_renda is None:
        return None
    
    # Normalizar e padronizar categorias de renda
    renda_normalizada = _alunos[coluna_renda].apply(normalizar_categoria_renda)
    renda_normalizada = renda_normalizada.dropna()
    
    if len(renda_normalizada) == 0:
        return None
    
    # Contar valores normalizados
    renda_counts = renda_normalizada.value_counts()
    
    # Ordenar por ordem lógica de renda (do menor para o maior)
    ordem_categorias = [
        'Não possui renda mensal',
        'Até meio salário mínimo',
        'Até um salário mínimo',
        'De 1 a 2 salários mínimos',
        'De 2 a 3 salários mínimos',
        'De 3 a 4 salários mínimos',
        'Acima de 5 salários mínimos'
    ]
    
    # Reordenar mantendo apenas as categorias que existem
    renda_counts_ordenado = renda_counts.reindex([cat for cat in ordem_categorias if cat in renda_counts.index])
    # Adicionar categorias que não estão na lista de ordem (caso apareçam outras)
    outras_categorias = renda_counts.index[~renda_counts.index.isin(ordem_categorias)]
    if len(outras_categorias) > 0:
        renda_counts_ordenado = pd.concat([renda_counts_ordenado, renda_counts[outras_categorias]])
    
    if len(renda_counts_ordenado) == 0:
        return None
    
    fig = px.bar(
        x=renda_counts_ordenado.values,
        y=renda_counts_ordenado.index,
        orientation='h',
        title="Distribuição por Renda Familiar",
        labels={'x': 'Quantidade', 'y': 'Renda'},
        color=renda_counts_ordenado.values,
        color_continuous_scale=['#2e7d32', '#43a047', '#66bb6a', '#81c784', '#a5d6a7']
    )
    fig.update_traces(hovertemplate="Renda: %{y}<br>Quantidade: %{x}<extra></extra>")
    return aplicar_tema_escuro(fig)

with col1:
    # Distribuição por Sexo (usa dados de ALUNOS - DadosMetalab FILTRADOS)
    fig_sexo = criar_grafico_sexo(alunos)
    if fig_sexo:
        st.plotly_chart(fig_sexo, use_container_width=True, key="sexo_chart")
    else:
        st.info("Não há dados de sexo disponíveis nos dados de alunos.")
    
    # Distribuição por Idade (usa dados de ALUNOS - DadosMetalab FILTRADOS)
    st.markdown("### Distribuição por Idade")
    fig_idade = criar_grafico_idade(alunos)
    if fig_idade:
        st.plotly_chart(fig_idade, use_container_width=True)
    else:
        # Debug: mostrar colunas disponíveis para ajudar a identificar o problema
        colunas_possiveis = [col for col in alunos.columns if any(palavra in col.lower() for palavra in ['idade', 'age', 'anos', 'nascimento', 'nasc', 'year'])]
        if colunas_possiveis:
            st.warning(f"Não foi possível processar dados de idade. Colunas encontradas relacionadas: {', '.join(colunas_possiveis[:5])}")
        else:
            st.warning("Não há dados de idade disponíveis para exibição. Verifique se há colunas de idade nos dados de alunos.")

with col2:
    # Distribuição por Raça/Cor (usa dados de ALUNOS - DadosMetalab FILTRADOS)
    fig_raca = criar_grafico_raca(alunos)
    if fig_raca:
        st.plotly_chart(fig_raca, use_container_width=True)
    else:
        st.info("Não há dados de raça/cor disponíveis nos dados de alunos.")
    
    # Distribuição por Renda Familiar (usa dados de ALUNOS - DadosMetalab FILTRADOS)
    fig_renda = criar_grafico_renda(alunos)
    if fig_renda:
        st.plotly_chart(fig_renda, use_container_width=True)
    else:
        st.info("Não há dados de renda disponíveis nos dados de alunos.")

# ==========================================
# SEÇÃO 3: CANAIS DE DIVULGAÇÃO
# ==========================================
st.markdown("---")
st.markdown("## 📢 Canais de Divulgação e Acesso")

col1, col2 = st.columns(2)

with col1:
    # Canais de inscrição (usa dados FILTRADOS)
    if len(inscricoes) > 0 and 'Quais foram os canais de comunicação pelos quais você tomou conhecimento do curso MetaLab?' in inscricoes.columns:
        canais_inscricao = inscricoes['Quais foram os canais de comunicação pelos quais você tomou conhecimento do curso MetaLab?'].value_counts()
        if len(canais_inscricao) > 0:
            fig_canais = px.bar(
                x=canais_inscricao.values,
                y=canais_inscricao.index,
                orientation='h',
                title="Canais de Comunicação - Inscrições",
                labels={'x': 'Quantidade', 'y': 'Canal'},
                color=canais_inscricao.values,
                color_continuous_scale=['#e65100', '#f57c00', '#ff9800', '#ffb74d', '#ffcc80']
            )
            fig_canais.update_traces(hovertemplate="Canal: %{y}<br>Quantidade: %{x}<extra></extra>")
            fig_canais = aplicar_tema_escuro(fig_canais)
            st.plotly_chart(fig_canais, use_container_width=True)
        else:
            st.info("Não há dados de canais para os filtros selecionados.")
    else:
        st.info("Não há dados de canais disponíveis.")

with col2:
    # Canais de avaliação - procurar por diferentes variações do nome
    coluna_canal = None
    for col in avaliacoes.columns:
        if 'sabendo' in col.lower() and 'curso' in col.lower():
            coluna_canal = col
            break
    
    if coluna_canal:
        canais_avaliacao = avaliacoes[coluna_canal].value_counts()
        fig_canais_av = px.pie(
            values=canais_avaliacao.values,
            names=canais_avaliacao.index,
            title="Canais de Divulgação - Avaliações",
            color_discrete_sequence=PALETA_METALAB
        )
        fig_canais_av.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
        fig_canais_av = aplicar_tema_escuro(fig_canais_av)
        st.plotly_chart(fig_canais_av, use_container_width=True)

# ==========================================
# SEÇÃO 4: STATUS DOS ALUNOS
# ==========================================
st.markdown("---")
st.markdown("## 📊 Status dos Alunos")

if 'STATUS' in alunos.columns:
    col1, col2 = st.columns(2)
    
    with col1:
        status_counts = alunos['STATUS'].value_counts()
        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Distribuição de Status",
            color_discrete_map={
                'CONCLUIDO': CORES_METALAB['success'],
                'DESISTENTE': CORES_METALAB['error'],
                'EM CURSO': CORES_METALAB['light'],
                'CURSANDO': CORES_METALAB['light'],
                'OUTROS': '#90caf9'
            }
        )
        fig_status.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
        fig_status = aplicar_tema_escuro(fig_status)
        st.caption("💡 Use o filtro de Status na sidebar para filtrar os dados")
        st.plotly_chart(fig_status, use_container_width=True, key="status_chart")
    
    with col2:
        # Status por Curso
        if 'CURSO' in alunos.columns:
            status_curso = pd.crosstab(alunos['CURSO'], alunos['STATUS'])
            fig_status_curso = px.bar(
                status_curso,
                title="Status por Curso",
                labels={'value': 'Quantidade', 'index': 'Curso'},
                barmode='group',
                color_discrete_map={
                    'CONCLUIDO': CORES_METALAB['success'],
                    'DESISTENTE': CORES_METALAB['error'],
                    'EM CURSO': CORES_METALAB['light'],
                    'CURSANDO': CORES_METALAB['light']
                }
            )
            fig_status_curso = aplicar_tema_escuro(fig_status_curso)
            st.plotly_chart(fig_status_curso, use_container_width=True)
    
    # Tabela detalhada de status
    st.markdown("### Detalhamento por Status")
    
    # Função para normalizar e padronizar status
    def normalizar_status(status):
        """Normaliza e padroniza status para agrupar variações"""
        if pd.isna(status) or status == '' or str(status).upper().strip() in ['NAN', 'NONE', 'NULL', 'N/A', 'NA']:
            return 'SEM STATUS'
        
        status_str = str(status).upper().strip()
        
        # Padronizar CONCLUÍDO/CONCLUIDO
        if 'CONCLUIDO' in status_str or 'CONCLUÍDO' in status_str or 'CONCLU' in status_str:
            return 'CONCLUÍDO'
        
        # Padronizar CURSANDO/EM CURSO
        if 'CURSANDO' in status_str or 'EM CURSO' in status_str or 'EM ANDAMENTO' in status_str or 'ANDAMENTO' in status_str:
            return 'CURSANDO'
        
        # Padronizar DESISTENTE
        if 'DESISTENTE' in status_str or 'DESISTIU' in status_str or 'DESISTENCIA' in status_str:
            return 'DESISTENTE'
        
        # Padronizar NÃO COMPARECEU
        if 'NÃO COMPARECEU' in status_str or 'NAO COMPARECEU' in status_str or 'NÃO COMPARECEU' in status_str or 'FALTOU' in status_str:
            return 'NÃO COMPARECEU'
        
        # Retornar status original se não encontrou padrão conhecido
        return status_str
    
    # Criar coluna de status normalizado para análise
    # IMPORTANTE: Usar alunos_originais para garantir que todos os alunos sejam contados
    alunos_com_status_normalizado = alunos_originais.copy()
    
    # Garantir que a coluna STATUS existe
    if 'STATUS' not in alunos_com_status_normalizado.columns:
        # Tentar encontrar coluna de status com variações
        for col in alunos_com_status_normalizado.columns:
            if 'status' in str(col).lower():
                alunos_com_status_normalizado['STATUS'] = alunos_com_status_normalizado[col]
                break
    
    # Aplicar normalização de status
    if 'STATUS' in alunos_com_status_normalizado.columns:
        alunos_com_status_normalizado['STATUS_NORMALIZADO'] = alunos_com_status_normalizado['STATUS'].apply(normalizar_status)
    else:
        # Se não houver coluna STATUS, criar uma coluna padrão
        alunos_com_status_normalizado['STATUS'] = 'SEM STATUS'
        alunos_com_status_normalizado['STATUS_NORMALIZADO'] = 'SEM STATUS'
    
    # Criar resumo usando status normalizado
    # Usar size() para contar TODOS os registros, não apenas uma coluna específica
    status_summary = alunos_com_status_normalizado.groupby('STATUS_NORMALIZADO').size().reset_index(name='Quantidade')
    status_summary = status_summary.set_index('STATUS_NORMALIZADO')
    
    # Adicionar coluna de principais cursos se existir
    if 'CURSO' in alunos_com_status_normalizado.columns:
        cursos_por_status = alunos_com_status_normalizado.groupby('STATUS_NORMALIZADO')['CURSO'].apply(
            lambda x: ', '.join(x.value_counts().head(3).index.astype(str))
        )
        status_summary['Principais Cursos'] = status_summary.index.map(cursos_por_status)
    else:
        status_summary['Principais Cursos'] = 'N/A'
    
    # Ordenar por quantidade (decrescente)
    status_summary = status_summary.sort_values('Quantidade', ascending=False)
    
    # Calcular totais
    total_alunos = len(alunos_originais)
    total_summary = status_summary['Quantidade'].sum()
    
    # Se houver diferença, adicionar linha "OUTROS" ou "SEM STATUS" para garantir que todos sejam contados
    if total_alunos != total_summary:
        diferenca = total_alunos - total_summary
        # Adicionar linha para alunos não contados
        if diferenca > 0:
            outros_data = {'Quantidade': diferenca}
            if 'Principais Cursos' in status_summary.columns:
                outros_data['Principais Cursos'] = 'N/A'
            outros_df = pd.DataFrame([outros_data], index=['OUTROS/NÃO CLASSIFICADOS'])
            status_summary = pd.concat([status_summary, outros_df])
            total_summary = status_summary['Quantidade'].sum()
    
    # Mostrar resumo
    st.dataframe(status_summary, use_container_width=True)
    
    # Mostrar informações adicionais
    st.caption(f"📊 **Total de alunos na base:** {total_alunos:,} | **Total no resumo:** {total_summary:,}")
    if total_alunos != total_summary:
        st.warning(f"⚠️ Ainda há diferença de {total_alunos - total_summary} aluno(s). Verifique duplicatas ou dados inconsistentes.")

# ==========================================
# SEÇÃO 5: AVALIAÇÕES DETALHADAS
# ==========================================
st.markdown("---")
st.markdown("## ⭐ Avaliações dos Alunos")

# Garantir que a filtragem por ciclo funcione mesmo se a função filtrar_avaliacoes não funcionou
if ciclo_selecionado != 'Todos' and avaliacoes is not None and len(avaliacoes) > 0:
    # Verificar se realmente filtrou (comparar tamanho com originais)
    if len(avaliacoes) == len(avaliacoes_originais) and 'Pesquisa' in avaliacoes.columns:
        # Se não filtrou, aplicar filtro diretamente aqui
        def extrair_ciclo_final(valor):
            if pd.isna(valor):
                return None
            valor_str = str(valor).upper().strip()
            match = re.search(r'(\d+)\s*CICLO', valor_str)
            if match:
                return match.group(1)
            if 'AVALIAÇÃO' in valor_str and ('MCOM' in valor_str or 'MKT DIGITAL' in valor_str):
                if not re.search(r'\d+\s*CICLO', valor_str):
                    return '1'
            return None
        
        ciclo_selecionado_final = str(ciclo_selecionado).strip()
        if ciclo_selecionado_final.endswith('.0'):
            ciclo_selecionado_final = ciclo_selecionado_final[:-2]
        
        ciclos_finais = avaliacoes['Pesquisa'].apply(extrair_ciclo_final)
        mask_final = (ciclos_finais == ciclo_selecionado_final)
        if mask_final.any():
            avaliacoes = avaliacoes[mask_final].copy()

# Verificar se há dados de avaliações disponíveis
debug_avaliacoes = False
if len(avaliacoes.columns) > 0:
    colunas_lower = [str(col).lower() for col in avaliacoes.columns]
    # Verificar se há colunas relacionadas às perguntas esperadas
    tem_avaliacao_curso = any('considerei' in c or 'curso' in c for c in colunas_lower)
    tem_avaliacao_prof = any('educador' in c or 'professor' in c for c in colunas_lower)
    tem_curso_realizado = any('curso realizou' in c or 'qual curso' in c for c in colunas_lower)
    tem_intencao = any('pretende' in c or 'intencao' in c for c in colunas_lower)
    tem_suporte = any('suporte' in c for c in colunas_lower)
    
    if not (tem_avaliacao_curso or tem_avaliacao_prof or tem_curso_realizado or tem_intencao or tem_suporte):
        debug_avaliacoes = True

col1, col2 = st.columns(2)

with col1:
    # Avaliação Geral do Curso
    # Procurar coluna de avaliação do curso (busca mais ampla nas perguntas que viraram colunas)
    coluna_avaliacao_curso = None
    palavras_chave_avaliacao_curso = ['considerei', 'considerou', 'avaliacao', 'avaliação', 'avaliar', 'avaliou', 'curso', 'meta', 'metalab']
    
    # Buscar em todas as colunas (que são as perguntas após o pivot)
    for col in avaliacoes.columns:
        col_lower = str(col).lower()
        # Verificar se contém palavras-chave relacionadas a avaliação E curso
        tem_avaliacao = any(palavra in col_lower for palavra in ['considerei', 'considerou', 'avaliacao', 'avaliação', 'avaliar', 'avaliou'])
        tem_curso = any(palavra in col_lower for palavra in ['curso', 'meta', 'metalab'])
        
        if tem_avaliacao and tem_curso:
            coluna_avaliacao_curso = col
            break
        # Também aceitar se tiver várias palavras-chave mesmo sem ambas
        elif sum(1 for palavra in palavras_chave_avaliacao_curso if palavra in col_lower) >= 2:
            coluna_avaliacao_curso = col
            break
    
    if coluna_avaliacao_curso:
        try:
            avaliacao_curso = avaliacoes[coluna_avaliacao_curso].dropna().value_counts()
            if len(avaliacao_curso) > 0:
                fig_av_curso = px.bar(
                    x=avaliacao_curso.index,
                    y=avaliacao_curso.values,
                    title="Avaliação Geral do Curso",
                    labels={'x': 'Avaliação', 'y': 'Quantidade'},
                    color=avaliacao_curso.values,
                    color_continuous_scale=['#c62828', '#ef5350', '#ffa726', '#66bb6a', '#2e7d32']
                )
                fig_av_curso = aplicar_tema_escuro(fig_av_curso)
                st.plotly_chart(fig_av_curso, use_container_width=True)
            else:
                st.info("Não há dados de avaliação do curso disponíveis.")
        except Exception as e:
            st.warning(f"Não foi possível criar gráfico de avaliação do curso: {str(e)}")
    else:
        # Debug: mostrar colunas disponíveis
        colunas_relacionadas = [col for col in avaliacoes.columns if any(palavra in str(col).lower() for palavra in palavras_chave_avaliacao_curso)]
        if colunas_relacionadas:
            st.info(f"Coluna de avaliação do curso não encontrada. Colunas relacionadas encontradas: {', '.join(colunas_relacionadas[:3])}")
        else:
# Removido debug - não mostrar mensagens desnecessárias
            st.info("Coluna de avaliação do curso não encontrada nos dados de avaliações.")
    
    # Avaliação do Professor
    # Procurar coluna de avaliação do professor/educador (busca mais ampla)
    coluna_avaliacao_prof = None
    palavras_chave_avaliacao_prof = ['avalie', 'avaliar', 'avaliou', 'avaliação', 'avaliacao']
    palavras_chave_prof = ['professor', 'educador', 'educadora', 'instrutor', 'instrutora', 'docente', 'educador social']
    
    for col in avaliacoes.columns:
        col_lower = str(col).lower()
        tem_avaliacao = any(palavra in col_lower for palavra in palavras_chave_avaliacao_prof)
        tem_prof = any(palavra in col_lower for palavra in palavras_chave_prof)
        
        if tem_avaliacao and tem_prof:
            coluna_avaliacao_prof = col
            break
    
    if coluna_avaliacao_prof:
        try:
            avaliacao_prof = avaliacoes[coluna_avaliacao_prof].dropna().value_counts()
            if len(avaliacao_prof) > 0:
                fig_av_prof = px.bar(
                    x=avaliacao_prof.index,
                    y=avaliacao_prof.values,
                    title="Avaliação do Professor",
                    labels={'x': 'Avaliação', 'y': 'Quantidade'},
                    color=avaliacao_prof.values,
                    color_continuous_scale=['#1a237e', '#3949ab', '#5c6bc0', '#7986cb', '#90caf9']
                )
                fig_av_prof = aplicar_tema_escuro(fig_av_prof)
                st.plotly_chart(fig_av_prof, use_container_width=True)
            else:
                st.info("Não há dados de avaliação do professor disponíveis.")
        except Exception as e:
            st.warning(f"Não foi possível criar gráfico de avaliação do professor: {str(e)}")
    else:
        # Debug: mostrar colunas relacionadas
        colunas_relacionadas = [col for col in avaliacoes.columns if any(palavra in str(col).lower() for palavra in palavras_chave_prof)]
        if colunas_relacionadas:
            st.info(f"Coluna de avaliação do professor não encontrada. Colunas relacionadas: {', '.join(colunas_relacionadas[:3])}")
        else:
            st.info("Coluna de avaliação do professor não encontrada nos dados de avaliações.")

with col2:
    # Satisfação com Espaço Físico
    if 'No que se refere ao espaço físico (Laboratório de Informática), qual seu nível de satisfação?' in avaliacoes.columns:
        satisfacao_espaco = avaliacoes['No que se refere ao espaço físico (Laboratório de Informática), qual seu nível de satisfação?'].value_counts()
        fig_sat_espaco = px.pie(
            values=satisfacao_espaco.values,
            names=satisfacao_espaco.index,
            title="Satisfação com Espaço Físico",
            color_discrete_sequence=PALETA_METALAB
        )
        fig_sat_espaco.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
        fig_sat_espaco = aplicar_tema_escuro(fig_sat_espaco)
        st.plotly_chart(fig_sat_espaco, use_container_width=True)
    
    # Satisfação com Instalações
    if 'Avalie seu nível de satisfação em relação as demais instalações da ONG (hall de entrada, banheiro, recepção, auditório):' in avaliacoes.columns:
        satisfacao_inst = avaliacoes['Avalie seu nível de satisfação em relação as demais instalações da ONG (hall de entrada, banheiro, recepção, auditório):'].value_counts()
        fig_sat_inst = px.pie(
            values=satisfacao_inst.values,
            names=satisfacao_inst.index,
            title="Satisfação com Instalações",
            color_discrete_sequence=PALETA_METALAB
        )
        fig_sat_inst.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
        fig_sat_inst = aplicar_tema_escuro(fig_sat_inst)
        st.plotly_chart(fig_sat_inst, use_container_width=True)

# Análise de Canais de Divulgação (das avaliações)
st.markdown("### Como Ficou Sabendo do Curso?")
coluna_sabendo_curso = None
for col in avaliacoes.columns:
    if 'sabendo' in str(col).lower() and 'curso' in str(col).lower():
        coluna_sabendo_curso = col
        break

if coluna_sabendo_curso:
    try:
        sabendo_curso = avaliacoes[coluna_sabendo_curso].dropna().value_counts()
        if len(sabendo_curso) > 0:
            fig_sabendo = px.pie(
                values=sabendo_curso.values,
                names=sabendo_curso.index,
                title="Como Ficou Sabendo do Curso?",
                color_discrete_sequence=PALETA_METALAB
            )
            fig_sabendo.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
            fig_sabendo = aplicar_tema_escuro(fig_sabendo)
            st.plotly_chart(fig_sabendo, use_container_width=True)
    except Exception as e:
        pass

# Análise de Expectativas e Outras Métricas
st.markdown("### Outras Avaliações")
col1, col2 = st.columns(2)

with col1:
    # O Conteúdo Atendeu Minhas Expectativas?
    coluna_expectativas = None
    for col in avaliacoes.columns:
        col_lower = str(col).lower()
        if 'expectativas' in col_lower or ('conteudo' in col_lower and 'atendeu' in col_lower):
            coluna_expectativas = col
            break
    
    if coluna_expectativas:
        try:
            expectativas = avaliacoes[coluna_expectativas].dropna().value_counts()
            if len(expectativas) > 0:
                fig_expectativas = px.bar(
                    x=expectativas.index,
                    y=expectativas.values,
                    title="O Conteúdo Atendeu Minhas Expectativas?",
                    labels={'x': 'Resposta', 'y': 'Quantidade'},
                    color=expectativas.values,
                    color_continuous_scale=['#c62828', '#ef5350', '#ffa726', '#66bb6a', '#2e7d32']
                )
                fig_expectativas = aplicar_tema_escuro(fig_expectativas)
                st.plotly_chart(fig_expectativas, use_container_width=True)
        except Exception as e:
            pass
    
with col2:
    # Você Indicaria o Curso?
    coluna_indicacao = None
    for col in avaliacoes.columns:
        col_lower = str(col).lower()
        if 'indicaria' in col_lower or ('indicaria' in col_lower and 'curso' in col_lower):
            coluna_indicacao = col
            break
    
    if coluna_indicacao:
        try:
            indicacao = avaliacoes[coluna_indicacao].dropna().value_counts()
            if len(indicacao) > 0:
                fig_indicacao = px.pie(
                    values=indicacao.values,
                    names=indicacao.index,
                    title="Você Indicaria o Curso para Familiares e Amigos?",
                    color_discrete_sequence=[CORES_METALAB['success'], CORES_METALAB['warning'], CORES_METALAB['error']]
                )
                fig_indicacao.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
                fig_indicacao = aplicar_tema_escuro(fig_indicacao)
                st.plotly_chart(fig_indicacao, use_container_width=True)
        except Exception as e:
            pass
    
    # Suporte Pedagógico
    coluna_suporte = None
    palavras_chave_suporte = ['suporte', 'coordenacao', 'coordenação', 'pedagogica', 'pedagógica', 'recebi suporte']
    
    for col in avaliacoes.columns:
        col_lower = str(col).lower()
        if any(palavra in col_lower for palavra in ['recebi suporte', 'suporte coordenacao', 'suporte coordenação', 'suporte pedagogica', 'suporte pedagógica']):
            coluna_suporte = col
            break
        elif any(palavra in col_lower for palavra in ['suporte']) and any(palavra in col_lower for palavra in ['coordenacao', 'coordenação', 'pedagogica', 'pedagógica']):
            coluna_suporte = col
            break
    
    if coluna_suporte:
        try:
            suporte_ped = avaliacoes[coluna_suporte].dropna().value_counts()
            if len(suporte_ped) > 0:
                fig_suporte = px.bar(
                    x=suporte_ped.index,
                    y=suporte_ped.values,
                    title="Suporte da Coordenação Pedagógica",
                    labels={'x': 'Resposta', 'y': 'Quantidade'},
                    color=suporte_ped.values,
                    color_continuous_scale=['#1a237e', '#3949ab', '#5c6bc0', '#7986cb', '#90caf9']
                )
                fig_suporte = aplicar_tema_escuro(fig_suporte)
                st.plotly_chart(fig_suporte, use_container_width=True)
        except Exception as e:
            pass


# ==========================================
# SEÇÃO 6: ANÁLISE POR REGIÃO/LOCAL
# ==========================================
st.markdown("---")
st.markdown("## 📍 Análise por Região/Local")

col1, col2 = st.columns(2)

with col1:
    # Inscrições por Região
    if 'SELECIONE A SUA REGIÃO MAIS PRÓXIMA PARA REALIZAR O CURSO:' in inscricoes.columns:
        regiao_counts = inscricoes['SELECIONE A SUA REGIÃO MAIS PRÓXIMA PARA REALIZAR O CURSO:'].value_counts()
        fig_regiao = px.bar(
            x=regiao_counts.values,
            y=regiao_counts.index,
            orientation='h',
            title="Inscrições por Região",
            labels={'x': 'Quantidade', 'y': 'Região'},
            color=regiao_counts.values,
            color_continuous_scale=['#c62828', '#e53935', '#ef5350', '#e57373', '#ef9a9a']
        )
        fig_regiao = aplicar_tema_escuro(fig_regiao)
        st.plotly_chart(fig_regiao, use_container_width=True)

with col2:
    # Alunos por Local
    if 'LOCAL' in alunos.columns:
        local_counts = alunos['LOCAL'].value_counts()
        fig_local = px.bar(
            x=local_counts.values,
            y=local_counts.index,
            orientation='h',
            title="Alunos por Local",
            labels={'x': 'Quantidade', 'y': 'Local'},
            color=local_counts.values,
            color_continuous_scale=['#2e7d32', '#43a047', '#66bb6a', '#81c784', '#a5d6a7']
        )
        fig_local = aplicar_tema_escuro(fig_local)
        st.plotly_chart(fig_local, use_container_width=True)

# ==========================================
# SEÇÃO 7: ANÁLISE TEMPORAL
# ==========================================
st.markdown("---")
st.markdown("## 📅 Análise Temporal")

col1, col2 = st.columns(2)

with col1:
    # Evolução de Inscrições
    if 'Data_Inscricao' in inscricoes.columns and 'Ano' in inscricoes.columns and 'Mes' in inscricoes.columns:
        # Filtrar apenas linhas com Ano e Mes válidos
        inscricoes_validas = inscricoes.dropna(subset=['Ano', 'Mes'])
        if len(inscricoes_validas) > 0:
            inscricoes_por_mes = inscricoes_validas.groupby(['Ano', 'Mes']).size().reset_index(name='Quantidade')
            # Criar data de forma mais segura
            inscricoes_por_mes['Data'] = pd.to_datetime(
                inscricoes_por_mes['Ano'].astype(str) + '-' + 
                inscricoes_por_mes['Mes'].astype(str).str.zfill(2) + '-01',
                errors='coerce'
            )
            inscricoes_por_mes = inscricoes_por_mes.dropna(subset=['Data']).sort_values('Data')
        
            if len(inscricoes_por_mes) > 0:
                fig_temporal_insc = px.line(
                    inscricoes_por_mes,
                    x='Data',
                    y='Quantidade',
                    title="Evolução de Inscrições ao Longo do Tempo",
                    markers=True,
                    labels={'Quantidade': 'Número de Inscrições', 'Data': 'Data'}
                )
                fig_temporal_insc.update_traces(line_color='#90caf9', line_width=3)
                fig_temporal_insc = aplicar_tema_escuro(fig_temporal_insc)
                st.plotly_chart(fig_temporal_insc, use_container_width=True)
            else:
                st.warning("Não há dados temporais suficientes para exibir o gráfico.")
        else:
            st.warning("Não há dados de inscrição com data válida.")

with col2:
    # Distribuição por Horário
    if 'Qual horário do curso?' in avaliacoes.columns:
        horario_counts = avaliacoes['Qual horário do curso?'].value_counts()
        fig_horario = px.bar(
            x=horario_counts.index,
            y=horario_counts.values,
            title="Distribuição por Horário do Curso",
            labels={'x': 'Horário', 'y': 'Quantidade'},
            color=horario_counts.values,
            color_continuous_scale=['#c62828', '#e53935', '#ef5350', '#e57373', '#ef9a9a']
        )
        fig_horario = aplicar_tema_escuro(fig_horario)
        st.plotly_chart(fig_horario, use_container_width=True)


# ==========================================
# RODAPÉ
# ==========================================
# Créditos no final - Retângulo preto full width
st.markdown("""
<div class="creditos-rodape">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="white" style="vertical-align: middle;">
        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
    </svg>
    <p style='color: #ffffff; margin: 0; font-size: 1rem; font-weight: 500;'>
        Criado por Vinicius Mendes | <a href="https://github.com/evinicim" target="_blank" style="color: #ffffff; text-decoration: none; font-weight: 600;">@evinicim</a>
    </p>
</div>
""", unsafe_allow_html=True)

