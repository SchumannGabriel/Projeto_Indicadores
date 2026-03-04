import smartsheet
import pandas as pd
import streamlit as st

def carregar_dados_smartsheet(token, id_planilha):
    """Conecta ao Smartsheet e retorna o DataFrame tratado."""
    smart = smartsheet.Smartsheet(token)
    sheet = smart.Sheets.get_sheet(id_planilha)
    
    cols = [column.title for column in sheet.columns]
    data = [[cell.value for cell in row.cells] for row in sheet.rows]
    df = pd.DataFrame(data, columns=cols)

    if df.empty:
        raise ValueError("A planilha está vazia.")

    # Definição dos Sensos
    sensos = ['Descarte', 'Organização', 'Limpeza', 'Saúde e Higiene', 'Autodisciplina']
    col_ncs_lista = [c for c in df.columns if 'NC' in c.upper()]

    # Garantir colunas essenciais
    if 'Setor' not in df.columns:
        df['Setor'] = 'Indefinido'
    if 'Data' not in df.columns:
        raise ValueError("Coluna 'Data' não encontrada na planilha.")
    if 'Nota' not in df.columns:
        df['Nota'] = 0

    # Tratamento de Dados
    df = df.dropna(how='all')
    df['Setor'] = df['Setor'].fillna('Indefinido').astype(str)
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df = df.dropna(subset=['Data'])
    df['Mes_Ano_Ref'] = df['Data'].dt.strftime('%m/%Y')

    # Limpeza de valores numéricos
    colunas_valores = sensos + ['Nota']
    for col in colunas_valores:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace('%', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            # Normaliza escala de 0-1 para 0-100
            if 0 < df[col].mean() <= 1.0:
                df[col] = df[col] * 100

    for col in col_ncs_lista:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df = df.sort_values('Data')
    return df, sensos, col_ncs_lista
