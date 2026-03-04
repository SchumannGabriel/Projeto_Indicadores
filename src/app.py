import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Importações dos arquivos locais
from connection import carregar_dados_smartsheet
from utils import normalizar

st.set_page_config(page_title="Dashboard 5S", layout="wide")

# --- SISTEMA DE LOGIN ---
def check_password():
    if "password_correct" not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.write("# Acesso Restrito")
            with st.form("login_form"):
                user_input = st.text_input("Usuário ou E-mail")
                password_input = st.text_input("Senha", type="password")
                submit_button = st.form_submit_button("Entrar")
                
                if submit_button:
                    try:
                        usuarios_validos = st.secrets["usuarios"]
                        if user_input in usuarios_validos and str(usuarios_validos[user_input]) == password_input:
                            st.session_state["password_correct"] = True
                            st.rerun()
                        else:
                            st.error("Usuário ou senha incorretos.")
                    except KeyError:
                        st.error("Configuração de 'usuarios' não encontrada nos Secrets.")
        return False
    return True

if check_password():
    if st.sidebar.button("Sair / Logout"):
        del st.session_state["password_correct"]
        st.rerun()

    # --- CARREGAMENTO DE DADOS (COM CACHE) ---
    @st.cache_data(ttl=600)
    def get_data():
        try:
            TOKEN = st.secrets["SMARTSHEET_TOKEN"]
            ID_PLANILHA = st.secrets["ID_PLANILHA"]
            return carregar_dados_smartsheet(TOKEN, ID_PLANILHA)
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            st.stop()

    df, sensos, col_ncs_lista = get_data()

    # --- SIDEBAR E FILTROS ---
    st.sidebar.header("Filtros de Auditoria")
    setor_sel = st.sidebar.selectbox("Selecione o Setor", ['Todos'] + sorted(df['Setor'].unique()))
    mes_sel = st.sidebar.selectbox("Selecione o Mês/Ano", ['Todos'] + sorted(df['Mes_Ano_Ref'].unique(), reverse=True))

    df_plot = df.copy()
    if setor_sel != 'Todos':
        df_plot = df_plot[df_plot['Setor'] == setor_sel]
    if mes_sel != 'Todos':
        df_plot = df_plot[df_plot['Mes_Ano_Ref'] == mes_sel]

    if df_plot.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    # --- INTERFACE PRINCIPAL ---
    st.title("Dashboard de Auditoria 5S")
    
    # Métricas
    m1, m2, m3 = st.columns(3)
    m1.metric("Nota Média (Geral)", f"{df_plot['Nota'].mean():.1f}%")
    m2.metric("Total de NCs", int(df_plot[col_ncs_lista].sum().sum()))
    m3.metric("Qtd Auditorias", len(df_plot))
    st.divider()

    # Cards por Senso
    cols_sensos = st.columns(5)
    for i, s in enumerate(sensos):
        media_s = df_plot[s].mean() if s in df_plot.columns else 0
        s_norm = normalizar(s)
        col_nc_esp = [c for c in col_ncs_lista if s_norm in normalizar(c)]
        total_nc_s = df_plot[col_nc_esp].sum().sum() if col_nc_esp else 0

        cols_sensos[i].metric(
            label=s,
            value=f"{media_s:.1f}%",
            delta=f"{int(total_nc_s)} NCs",
            delta_color="inverse"
        )

    # --- GRÁFICOS ---
    st.subheader("Evolução Mensal e Variação")
    df_hist = df if setor_sel == 'Todos' else df[df['Setor'] == setor_sel]
    df_mensal = df_hist.set_index('Data').resample('ME').agg({'Nota': 'mean'}).reset_index()

    if not df_mensal.empty:
        df_mensal['Mes_Ano'] = df_mensal['Data'].dt.strftime('%m/%Y')
        df_mensal['Variacao'] = df_mensal['Nota'].diff().fillna(0)
        fig_evol = go.Figure()
        fig_evol.add_bar(x=df_mensal['Mes_Ano'], y=df_mensal['Nota'], name='Nota (%)', text=df_mensal['Nota'].round(1), textposition='auto')
        fig_evol.add_scatter(x=df_mensal['Mes_Ano'], y=df_mensal['Variacao'], name='Dif (p.p.)', mode='lines+markers+text', text=df_mensal['Variacao'].round(1), textposition='top center', yaxis='y2')
        fig_evol.update_layout(yaxis=dict(title="Nota %", range=[0, 115]), yaxis2=dict(title="Variação", overlaying='y', side='right', showgrid=False), height=400)
        st.plotly_chart(fig_evol, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        valores_radar = [df_plot[s].mean() if s in df_plot.columns else 0 for s in sensos]
        fig_rad = go.Figure(go.Scatterpolar(r=valores_radar + [valores_radar[0]], theta=sensos + [sensos[0]], fill='toself'))
        fig_rad.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="Radar de Performance (%)")
        st.plotly_chart(fig_rad, use_container_width=True)

    with c2:
        df_nc_bar = df_plot[col_ncs_lista].sum().reset_index()
        df_nc_bar.columns = ['Categoria', 'Total']
        df_nc_bar['Categoria'] = df_nc_bar['Categoria'].str.replace('QTD NC ', '', case=False)
        fig_nc = px.bar(df_nc_bar, x='Categoria', y='Total', text_auto=True, title="Total de NCs por Categoria")
        st.plotly_chart(fig_nc, use_container_width=True)

    # Detalhamento
    with st.expander("Visualizar dados brutos"):
        df_display = df_plot.copy()
        df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y')
        st.dataframe(df_display, use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.caption("Dashboard v3.1 | Schumann")
