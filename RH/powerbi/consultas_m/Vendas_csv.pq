// Consulta "Vendas" — lê a base tratada em CSV (opção principal)
// Como usar: Página Inicial > Obter dados > Consulta em branco > Editor Avançado > colar este código.
// Depende do parâmetro PastaProjeto (PastaProjeto.pq). Se a pasta mudar de lugar, edite só o parâmetro.
let
    Caminho = PastaProjeto & "\dados\tratados\vendas_tratado.csv",

    // UTF-8 (65001) preserva os acentos; ";" é o separador gerado pelo script de tratamento
    Fonte = Csv.Document(
        File.Contents(Caminho),
        [Delimiter = ";", Columns = 9, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),

    // A primeira linha do arquivo é o cabeçalho
    Cabecalhos = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),

    // Tipos com cultura pt-BR: lê "208,96" como 208,96 e "01/01/2021" como 1º de janeiro
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
