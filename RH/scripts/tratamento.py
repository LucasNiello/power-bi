"""
Tratamento da base "Vendas - Site" para o Power BI.

Entrada : dados/brutos/Vendas_-_Site.xlsx - Vendas.csv   (nunca é alterada)
Saídas  : dados/tratados/vendas_tratado.csv    (UTF-8 com BOM, ";" e decimal ",")
          dados/tratados/vendas_tratado.xlsx
          dados/tratados/sku_inconsistentes.csv (apenas documentação, nada é corrigido)
          dados/tratados/log_tratamento.txt     (log antes/depois)

Uso: python scripts/tratamento.py
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "dados" / "brutos" / "Vendas_-_Site.xlsx - Vendas.csv"
SAIDA = RAIZ / "dados" / "tratados"

# Totais conferidos na exploração (Fase 1) e no relatório de referência
TOTAL_FATURAMENTO_ESPERADO = 65827.61
TOTAL_LUCRO_ESPERADO = 28083.66

TIPOS_ESPERADOS = {"Camisa", "Casaco", "Camiseta", "Sandália", "Boné",
                   "Meia", "Bota", "Chinelo", "Sapato"}
MARCAS_ESPERADAS = {"Reserva", "CalopStore", "MarcoGPT"}

NOMES_MESES = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

log = []


def registrar(texto=""):
    """Mostra no terminal e guarda a linha para o arquivo de log."""
    print(texto)
    log.append(texto)


def resumo(df, titulo, col_fat, col_luc):
    """Registra linhas, tipos e totais de um DataFrame (usado no antes e no depois)."""
    registrar(f"=== {titulo} ===")
    registrar(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")
    registrar("Tipos:")
    for coluna, tipo in df.dtypes.items():
        registrar(f"  {coluna:<15} {tipo}")
    registrar(f"Nulos: {int(df.isna().sum().sum())}")
    registrar(f"Faturamento total: {df[col_fat].sum() if col_fat else '(texto, não somável)'}")
    registrar(f"Lucro total:       {df[col_luc].sum() if col_luc else '(texto, não somável)'}")
    registrar()


def moeda_para_decimal(serie):
    """Converte texto no formato 'R$ 1.234,56' para número decimal (1234.56)."""
    return (serie.str.replace("R$", "", regex=False)
                 .str.strip()
                 .str.replace(".", "", regex=False)    # separador de milhar
                 .str.replace(",", ".", regex=False)   # vírgula decimal -> ponto
                 .astype(float))


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)

    # 1. Leitura: tudo como texto, em UTF-8, para não perder acentos nem deixar o pandas adivinhar tipos
    bruto = pd.read_csv(ENTRADA, dtype=str, encoding="utf-8")
    resumo(bruto, "ANTES (base bruta)", None, None)

    df = bruto.copy()

    # 2. Padronização de texto: remove espaços nas pontas
    for coluna in ["SKU", "Tipo", "Marca"]:
        df[coluna] = df[coluna].str.strip()

    tipos_fora = set(df["Tipo"]) - TIPOS_ESPERADOS
    marcas_fora = set(df["Marca"]) - MARCAS_ESPERADAS
    registrar(f"Tipos fora da lista esperada: {tipos_fora or 'nenhum'}")
    registrar(f"Marcas fora da lista esperada: {marcas_fora or 'nenhuma'}")

    # 3. Moeda: texto 'R$ 208,96' -> decimal 208.96
    df["Faturamento"] = moeda_para_decimal(df["Faturamento"])
    df["Lucro"] = moeda_para_decimal(df["Lucro"])

    # 4. Data: texto 'dd/mm/aa' -> data com ano de 4 dígitos
    df["Data"] = pd.to_datetime(df["Dia"], format="%d/%m/%y", errors="raise")

    # 5. Mês e Ano: valida que as colunas originais batem com a data e depois deriva da própria data
    mes_diverge = int((df["Mês"].astype(int) != df["Data"].dt.month).sum())
    ano_diverge = int((df["Ano"].astype(int) != df["Data"].dt.year).sum())
    registrar(f"Linhas com Mês diferente da data: {mes_diverge}")
    registrar(f"Linhas com Ano diferente da data: {ano_diverge}")
    if mes_diverge or ano_diverge:
        raise SystemExit("Mês/Ano divergem da data: revisar antes de continuar.")

    df["Ano"] = df["Data"].dt.year
    df["Número do Mês"] = df["Data"].dt.month                # usado para ordenar "Nome do Mês" no Power BI
    df["Nome do Mês"] = df["Número do Mês"].map(lambda m: NOMES_MESES[m - 1])

    # 6. SKU inconsistente: só documenta, não corrige (o SKU não será chave de relacionamento)
    combinacoes = df.groupby("SKU")[["Tipo", "Marca"]].apply(
        lambda g: sorted(set(g["Tipo"] + " | " + g["Marca"])))
    inconsistentes = combinacoes[combinacoes.map(len) > 1]
    registrar(f"SKUs distintos: {df['SKU'].nunique()}")
    registrar(f"SKUs associados a mais de um Tipo/Marca: {len(inconsistentes)}")
    registrar(f"Exemplo SKU 353: {combinacoes.get('SKU 353')}")
    (inconsistentes.map(lambda c: "; ".join(c))
                   .rename("Combinações Tipo | Marca")
                   .to_frame()
                   .assign(Quantidade=inconsistentes.map(len))
                   .to_csv(SAIDA / "sku_inconsistentes.csv", sep=";", encoding="utf-8-sig"))

    # 7. Mesma data + mesmo SKU: são vendas diferentes (Tipo/Marca/valores distintos), então ficam
    mesma_data_sku = df[df.duplicated(["Data", "SKU"], keep=False)]
    registrar(f"Linhas com mesma Data + SKU (mantidas): {len(mesma_data_sku)}")
    registrar(f"Linhas 100% duplicadas: {int(bruto.duplicated().sum())}")

    # 8. Ordena por data (estável: mantém a ordem original dentro do mesmo dia) e organiza colunas
    df = df.sort_values("Data", kind="stable").reset_index(drop=True)
    df = df[["SKU", "Data", "Ano", "Número do Mês", "Nome do Mês",
             "Tipo", "Marca", "Faturamento", "Lucro"]]
    registrar()

    resumo(df, "DEPOIS (base tratada)", "Faturamento", "Lucro")

    # 9. Conferência: nenhuma linha perdida e totais iguais aos esperados
    assert len(df) == len(bruto), "Quantidade de linhas mudou!"
    assert round(df["Faturamento"].sum(), 2) == TOTAL_FATURAMENTO_ESPERADO, "Total de Faturamento divergente!"
    assert round(df["Lucro"].sum(), 2) == TOTAL_LUCRO_ESPERADO, "Total de Lucro divergente!"
    registrar(f"Conferência OK: {len(df)} linhas | Faturamento {df['Faturamento'].sum():.2f} "
              f"| Lucro {df['Lucro'].sum():.2f}")

    # 10. Exporta CSV (padrão pt-BR) e Excel
    df.to_csv(SAIDA / "vendas_tratado.csv", sep=";", decimal=",", float_format="%.2f",
              date_format="%d/%m/%Y", index=False, encoding="utf-8-sig")

    with pd.ExcelWriter(SAIDA / "vendas_tratado.xlsx", engine="openpyxl") as excel:
        df.to_excel(excel, sheet_name="Vendas", index=False)
        planilha = excel.sheets["Vendas"]
        for linha in planilha.iter_rows(min_row=2):
            linha[1].number_format = "DD/MM/YYYY"                 # Data
            linha[7].number_format = '"R$" #,##0.00'              # Faturamento
            linha[8].number_format = '"R$" #,##0.00'              # Lucro
        for coluna, largura in zip("ABCDEFGHI", [10, 12, 7, 15, 13, 11, 12, 13, 11]):
            planilha.column_dimensions[coluna].width = largura

    registrar("Arquivos gerados em dados/tratados/: vendas_tratado.csv, vendas_tratado.xlsx, "
              "sku_inconsistentes.csv, log_tratamento.txt")
    (SAIDA / "log_tratamento.txt").write_text("\n".join(log), encoding="utf-8")


if __name__ == "__main__":
    main()
