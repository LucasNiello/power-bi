# Medidas DAX e tabela Calendário

Tabela de fatos: `Vendas` (carregada por `consultas_m/Vendas_csv.pq` ou `Vendas_xlsx.pq`).
Sugestão: crie as medidas na própria tabela `Vendas` (Ferramentas de tabela > Nova medida).

## Medidas

| Medida | Formato | Valor esperado (base inteira) |
|---|---|---|
| Soma de Faturamento | Moeda R$, 2 casas | R$ 65.827,61 |
| Soma de Lucro | Moeda R$, 2 casas | R$ 28.083,66 |
| Média de Faturamento | Moeda R$, 2 casas | R$ 90,17 |
| Média de Lucro | Moeda R$, 2 casas | R$ 38,47 |
| Margem de Lucro (%) | Porcentagem, 2 casas | 42,66% |

Os quatro primeiros valores são os mesmos dos cartões da imagem de referência (R$ 65,83 Mil, R$ 28,08 Mil, R$ 90,17 e R$ 38,47).

```dax
Soma de Faturamento = SUM ( Vendas[Faturamento] )
```
Soma do faturamento de todas as vendas no contexto do filtro.

```dax
Soma de Lucro = SUM ( Vendas[Lucro] )
```
Soma do lucro de todas as vendas no contexto do filtro.

```dax
Média de Faturamento = AVERAGE ( Vendas[Faturamento] )
```
Faturamento médio por venda (cada linha da base é uma venda).

```dax
Média de Lucro = AVERAGE ( Vendas[Lucro] )
```
Lucro médio por venda.

```dax
Margem de Lucro (%) = DIVIDE ( [Soma de Lucro], [Soma de Faturamento] )
```
Quanto do faturamento virou lucro. `DIVIDE` retorna vazio em vez de erro quando o faturamento é zero.

## Tabela Calendário

Modelagem > Nova tabela > colar:

```dax
Calendário =
VAR DataInicial = DATE ( YEAR ( MIN ( Vendas[Data] ) ), 1, 1 )
VAR DataFinal   = DATE ( YEAR ( MAX ( Vendas[Data] ) ), 12, 31 )
RETURN
    ADDCOLUMNS (
        SELECTCOLUMNS ( CALENDAR ( DataInicial, DataFinal ), "Data", [Date] ),
        "Ano", YEAR ( [Data] ),
        "Número do Mês", MONTH ( [Data] ),
        "Nome do Mês",
            SWITCH (
                MONTH ( [Data] ),
                1, "Janeiro",  2, "Fevereiro", 3, "Março",     4, "Abril",
                5, "Maio",     6, "Junho",     7, "Julho",     8, "Agosto",
                9, "Setembro", 10, "Outubro",  11, "Novembro", 12, "Dezembro"
            )
    )
```

- Gera um dia por linha de 01/01/2021 a 31/12/2022, ou seja, os anos completos da base. Isso dá 730 dias, número que coincide por acaso com as 730 vendas.
- Os nomes dos meses vêm de um `SWITCH`, em vez de `FORMAT(..., "mmmm")`, para ficarem iguais em qualquer idioma do Power BI e com inicial maiúscula.

Depois de criar a tabela:
1. **Classificar Nome do Mês:** selecione `Calendário[Nome do Mês]` > Ferramentas de coluna > Classificar por coluna > `Número do Mês`. Sem isso o eixo fica em ordem alfabética (Abril, Agosto, Dezembro…).
2. **Marcar como tabela de datas:** selecione a tabela `Calendário` > Ferramentas de tabela > Marcar como tabela de datas > coluna `Data`.
3. Configure os formatos das medidas conforme a tabela acima.
