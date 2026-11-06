# Modelo de dados

## Tabelas

| Tabela | Tipo | Origem | Linhas |
|---|---|---|---|
| `Vendas` | Fatos (uma linha por venda) | `consultas_m/Vendas_csv.pq` (ou `Vendas_xlsx.pq`) | 730 |
| `Calendário` | Dimensão de datas | Tabela calculada em DAX (`medidas_dax.md`) | 730 dias (2021–2022) |

## Relacionamento

```
 Calendário                       Vendas
 ┌────────────────┐               ┌────────────────┐
 │ Data        (1)│───────────────│(*) Data        │
 │ Ano            │  1 : N        │ SKU            │
 │ Número do Mês  │  filtro em    │ Tipo           │
 │ Nome do Mês    │  sentido único│ Marca          │
 └────────────────┘  Calendário   │ Faturamento    │
                     → Vendas     │ Lucro          │
                                  │ (Ano, Número do│
                                  │  Mês, Nome do  │
                                  │  Mês: ocultar) │
                                  └────────────────┘
```

| De | Para | Cardinalidade | Direção do filtro | Ativo |
|---|---|---|---|---|
| `Calendário[Data]` | `Vendas[Data]` | Um para muitos (1:N) | Única (Calendário filtra Vendas) | Sim |

Como criar: Exibição de modelo > arraste `Calendário[Data]` até `Vendas[Data]` e confira a cardinalidade e a direção acima.

## Decisões

- **O SKU não é chave.** Na Fase 1 vimos que 191 dos 460 SKUs aparecem com mais de um Tipo/Marca (ex.: SKU 353 é Camisa/Reserva e também Sandália/CalopStore). Ele não identifica um produto, então não é usado em nenhum relacionamento. A lista está em `dados/tratados/sku_inconsistentes.csv`.
- **A Data é a única chave.** `Calendário[Data]` tem valores únicos (um por dia), e `Vendas[Data]` se repete (várias vendas no mesmo dia).
- **Tipo e Marca ficam na própria tabela Vendas.** São só 9 tipos e 3 marcas, sem atributos extras, então criar dimensões separadas não traria ganho para este protótipo.
- **Colunas de data em Vendas:** `Vendas[Ano]`, `Vendas[Número do Mês]` e `Vendas[Nome do Mês]` continuam na base tratada, que também serve fora do Power BI. No modelo, recomenda-se **ocultá-las** (botão direito > Ocultar na exibição de relatório) e usar sempre as colunas da `Calendário` nos visuais, para que todos os filtros de data passem pelo mesmo relacionamento.
- **Data/hora automática:** recomenda-se desativar em Arquivo > Opções > Arquivo atual > Carregamento de dados > "Data/hora automática". Assim o Power BI não cria tabelas de data ocultas que concorrem com a `Calendário`.
