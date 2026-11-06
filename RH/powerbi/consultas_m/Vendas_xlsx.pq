// Consulta "Vendas" — alternativa: lê a base tratada em Excel
// Use esta OU a Vendas_csv.pq (não as duas). O resultado é o mesmo.
// Como usar: Página Inicial > Obter dados > Consulta em branco > Editor Avançado > colar este código.
// Depende do parâmetro PastaProjeto (PastaProjeto.pq). Se a pasta mudar de lugar, edite só o parâmetro.
let
    Caminho = PastaProjeto & "\dados\tratados\vendas_tratado.xlsx",

    Fonte = Excel.Workbook(File.Contents(Caminho), null, true),

    // Planilha "Vendas" gerada pelo script de tratamento
    Planilha = Fonte{[Item = "Vendas", Kind = "Sheet"]}[Data],

    Cabecalhos = Table.PromoteHeaders(Planilha, [PromoteAllScalars = true]),

    // No Excel os valores já são número/data; aqui só fixamos o tipo de cada coluna
    Tipos = Table.TransformColumnTypes(
        Cabecalhos,
        {
            {"SKU", type text},
            {"Data", type date},
            {"Ano", Int64.Type},
            {"Número do Mês", Int64.Type},
            {"Nome do Mês", type text},
            {"Tipo", type text},
            {"Marca", type text},
            {"Faturamento", Currency.Type},
            {"Lucro", Currency.Type}
        },
        "pt-BR"
    )
in
    Tipos
