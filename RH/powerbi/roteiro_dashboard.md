# Roteiro do dashboard: "Relatório de Vendas"

Objetivo: reproduzir o dashboard de `enunciado/referencia_dashboard.png` no Power BI Desktop.
São 1 página, 1 título, 4 cartões e 3 gráficos. A Margem de Lucro (%) existe no modelo, mas **não entra no dashboard**, porque não aparece na referência.

> O `.pbix` é montado manualmente seguindo este roteiro. Sugestão de onde salvar: `powerbi/relatorio_vendas.pbix`.

---

## 1. Nomes das medidas

Um cartão exibe o **nome da medida** como rótulo. Por isso, as medidas têm os mesmos nomes da referência:
**Soma de Faturamento**, **Soma de Lucro**, **Média de Faturamento** e **Média de Lucro**, além de **Margem de Lucro (%)**, que fica só no modelo.
As fórmulas estão em `medidas_dax.md`.

---

## 2. Ordem de montagem no Power BI Desktop

1. **Opções:** Arquivo > Opções e configurações > Opções
   - Arquivo atual > Carregamento de dados > desmarque **Data/hora automática**.
   - Arquivo atual > Configurações regionais > **Português (Brasil)**, para "Mil" e vírgula decimal.
2. **Parâmetro:** Transformar dados > Gerenciar parâmetros > Novo, conforme `consultas_m/PastaProjeto.pq`.
3. **Consulta Vendas:** Nova fonte > Consulta em branco > Editor Avançado > colar `consultas_m/Vendas_csv.pq` > renomear a consulta para `Vendas` > **Fechar e aplicar**.
4. **Calendário:** Modelagem > Nova tabela > colar o DAX de `medidas_dax.md`.
   - `Nome do Mês` > Classificar por coluna > `Número do Mês`.
   - Marcar como tabela de datas > coluna `Data`.
5. **Relacionamento:** Exibição de modelo > `Calendário[Data]` → `Vendas[Data]`, 1:N, filtro único (`modelo_dados.md`).
6. **Medidas:** crie as 5 medidas na tabela `Vendas` com os nomes da seção 1 e os formatos da seção 4.
7. **Ocultar:** `Vendas[Ano]`, `Vendas[Número do Mês]` e `Vendas[Nome do Mês]` (Ocultar na exibição de relatório).
8. **Página:** seção 3 (tamanho e fundo).
9. **Visuais,** nesta ordem: Título > 4 Cartões > Área > Funil > Pizza (seção 5).
10. **Conferência:** checklist da seção 7.
11. **Salvar** o `.pbix` e tirar os prints para `documentacao/`.

---

## 3. Página e paleta

**Página:** Formatar página > Configurações da tela
- Tamanho: **16:9 (1280 × 720)**.
- Plano de fundo: cor `#F2F2F2`, transparência 0%.

**Paleta** (aproximada da referência):

| Uso | Cor |
|---|---|
| Título da página, valores dos cartões, títulos dos visuais | `#D9534F` (coral/vermelho) |
| Área do gráfico mensal, barras do funil | `#E3675F` (coral) |
| Rótulos secundários (nome do cartão, eixos) | `#8C8C8C` (cinza) |
| Fundo dos blocos | `#FFFFFF` |
| Borda dos blocos | `#E0E0E0` |
| Pizza: Reserva / CalopStore / MarcoGPT | `#6F80E0` (azul) / `#5B4A8B` (roxo) / `#E3675F` (coral) |

**Bloco padrão,** aplicado em todos os cartões e gráficos (Formatar > Geral > Efeitos):
- Plano de fundo **ativado**, branco `#FFFFFF`.
- Borda visual **ativada**, `#E0E0E0`, cantos arredondados 4 px.
- Sombra desativada.

---

## 4. Formato das medidas

Selecione a medida > Ferramentas de medida:

| Medida | Formato | Casas decimais |
|---|---|---|
| Soma de Faturamento | Moeda, R$ Português (Brasil) | 2 |
| Soma de Lucro | Moeda, R$ Português (Brasil) | 2 |
| Média de Faturamento | Moeda, R$ Português (Brasil) | 2 |
| Média de Lucro | Moeda, R$ Português (Brasil) | 2 |
| Margem de Lucro (%) | Porcentagem | 2 |

A **unidade de exibição** (Milhares ou Nenhum) é configurada em cada visual, não na medida.

---

## 5. Visuais

Posições em pixels na tela de 1280 × 720 (Formatar > Geral > Propriedades > Tamanho e Posição). São valores aproximados.

```
┌──────────────────────────── Relatório de Vendas ────────────────────────────┐ y 10
│ [Soma Fatur.]   [Soma Lucro]   [Média Fatur.]   [Média Lucro]                │ y 75
│ ┌─────────────── Soma de Faturamento por Mês (área) ──────────────────────┐ │ y 190
│ └──────────────────────────────────────────────────────────────────────────┘ │
│ ┌── Soma de Faturamento por Tipo ──┐ ┌── Soma de Faturamento por Marca ──┐ │ y 455
│ │            (funil)               │ │             (pizza)               │ │
│ └──────────────────────────────────┘ └───────────────────────────────────┘ │ y 710
└──────────────────────────────────────────────────────────────────────────────┘
```

### 5.1 Título da página
- **Tipo:** Caixa de texto (Inserir > Caixa de texto)
- **Texto:** `Relatório de Vendas`
- **Formatação:** Segoe UI Bold, 28 pt, cor `#D9534F`, centralizado. Plano de fundo da caixa desativado.
- **Posição:** X 20 · Y 10 · L 1240 · A 55

### 5.2 a 5.5 Cartões
- **Tipo:** Cartão (o clássico: valor grande com o nome da medida embaixo)
- **Campos:** um campo por cartão, no poço **Campos**
- **Valor do balão:** fonte Segoe UI Bold, 28 pt, cor `#D9534F`
- **Rótulo de categoria:** ativado, 11 pt, cor `#8C8C8C` (mostra o nome da medida)
- **Título do visual:** desativado
- **Bloco:** padrão da seção 3

| # | Campo | Unidade de exibição | Casas decimais | Mostra | Posição (X · Y · L · A) |
|---|---|---|---|---|---|
| 5.2 | Soma de Faturamento | **Milhares** | 2 | R$ 65,83 Mil | 20 · 75 · 297 · 100 |
| 5.3 | Soma de Lucro | **Milhares** | 2 | R$ 28,08 Mil | 334 · 75 · 297 · 100 |
| 5.4 | Média de Faturamento | **Nenhum** | 2 | R$ 90,17 | 648 · 75 · 297 · 100 |
| 5.5 | Média de Lucro | **Nenhum** | 2 | R$ 38,47 | 963 · 75 · 297 · 100 |

### 5.6 Gráfico de área: Soma de Faturamento por Mês
- **Tipo:** Gráfico de área
- **Campos:**
  - Eixo X: `Calendário[Nome do Mês]`
  - Eixo Y: `Soma de Faturamento`
  - Legenda: vazio
- **Classificação:** Mais opções (…) > Classificar eixo > `Nome do Mês` > **Crescente**. Como a coluna é classificada por `Número do Mês`, a ordem vai de Janeiro a Dezembro.
- **Filtros:** nenhum. Cada mês soma 2021 e 2022, como na referência.
- **Formatação:**
  - **Título:** ativado, texto `Soma de Faturamento por Mês`, Segoe UI Bold 16 pt, cor `#D9534F`, centralizado.
  - **Eixo X:** tipo Categórico, rótulos 9 pt `#8C8C8C`, título do eixo desativado.
  - **Eixo Y:** rótulos 9 pt `#8C8C8C`, unidade de exibição **Milhares**, título do eixo desativado.
  - **Linhas de grade:** desativadas.
  - **Linhas/série:** cor `#E3675F`. Área sombreada ativada, transparência ~40%.
  - **Rótulos de dados:** desativados (como na referência).
  - **Bloco:** padrão da seção 3.
- **Posição:** X 20 · Y 190 · L 1240 · A 250

### 5.7 Funil: Soma de Faturamento por Tipo
- **Tipo:** Funil
- **Campos:**
  - Categoria: `Vendas[Tipo]`
  - Valores: `Soma de Faturamento`
- **Classificação:** Mais opções (…) > Classificar eixo > `Soma de Faturamento` > **Decrescente**.
- **Filtros:** nenhum.
- **Formatação:**
  - **Título:** `Soma de Faturamento por Tipo`, Segoe UI Bold 16 pt, `#D9534F`, centralizado.
  - **Cores:** todas as barras `#E3675F`.
  - **Rótulos de dados:** ativados, posição Dentro do centro, cor branca, unidade **Milhares**, 2 casas.
  - **Rótulo da taxa de conversão:** ativado (mostra o "100%" no topo, como na referência).
  - **Eixo de categoria:** rótulos 10 pt `#8C8C8C`.
  - **Bloco:** padrão da seção 3.
- **Posição:** X 20 · Y 455 · L 612 · A 255

### 5.8 Pizza: Soma de Faturamento por Marca
- **Tipo:** Gráfico de pizza
- **Campos:**
  - Legenda: `Vendas[Marca]`
  - Valores: `Soma de Faturamento`
- **Filtros:** nenhum.
- **Formatação:**
  - **Título:** `Soma de Faturamento por Marca`, Segoe UI Bold 16 pt, `#D9534F`, centralizado.
  - **Cores das fatias:** Reserva `#6F80E0`, CalopStore `#5B4A8B`, MarcoGPT `#E3675F`.
  - **Rótulos de detalhe:** ativados.
    - Posição: Fora.
    - Conteúdo do rótulo: **Valor dos dados, Percentual do total**.
    - Unidade de exibição **Milhares**, 2 casas no valor, 2 casas na porcentagem.
    - Fonte 9 pt `#8C8C8C`.
  - **Legenda:** desativada, como na referência. A marca de cada fatia aparece ao passar o mouse (dica de ferramenta).
  - **Bloco:** padrão da seção 3.
- **Posição:** X 648 · Y 455 · L 612 · A 255

---

## 6. Filtros e segmentações

A referência **não tem segmentações** nem filtros de página. Não adicione nenhum. Os gráficos mostram o período inteiro (2021 e 2022).

---

## 7. Checklist de conferência (comparar com a referência)

### Página
- [ ] Título `Relatório de Vendas` centralizado, negrito, coral
- [ ] 4 cartões numa linha, gráfico de área largo no meio, funil à esquerda e pizza à direita embaixo
- [ ] Blocos brancos separados sobre fundo cinza claro
- [ ] **Margem de Lucro (%) não aparece** em nenhum visual

### Cartões
| Cartão | Esperado | OK |
|---|---|---|
| Soma de Faturamento | R$ 65,83 Mil (exato: 65.827,61) | [ ] |
| Soma de Lucro | R$ 28,08 Mil (exato: 28.083,66) | [ ] |
| Média de Faturamento | R$ 90,17 | [ ] |
| Média de Lucro | R$ 38,47 | [ ] |

### Pizza: Soma de Faturamento por Marca
| Marca | Valor | % | Cor | OK |
|---|---|---|---|---|
| Reserva | R$ 31,89 Mil | 48,44% | azul | [ ] |
| CalopStore | R$ 18,68 Mil | 28,37% | roxo | [ ] |
| MarcoGPT | R$ 15,26 Mil | 23,19% | coral | [ ] |

### Funil: ordem de cima para baixo
| # | Tipo | Valor | OK |
|---|---|---|---|
| 1 | Camisa | R$ 17,55 Mil | [ ] |
| 2 | Casaco | R$ 13,83 Mil | [ ] |
| 3 | Camiseta | R$ 8,90 Mil | [ ] |
| 4 | Boné | R$ 7,16 Mil | [ ] |
| 5 | Bota | R$ 5,49 Mil | [ ] |
| 6 | Sandália | R$ 4,24 Mil | [ ] |
| 7 | Sapato | R$ 4,05 Mil | [ ] |
| 8 | Meia | R$ 2,89 Mil | [ ] |
| 9 | Chinelo | R$ 1,72 Mil | [ ] |

### Área: Soma de Faturamento por Mês
| Mês | Valor | Mês | Valor |
|---|---|---|---|
| Janeiro | R$ 6,68 Mil | Julho | R$ 4,08 Mil |
| Fevereiro | R$ 3,43 Mil | Agosto | R$ 5,44 Mil |
| Março | R$ 7,26 Mil | Setembro | R$ 5,32 Mil |
| Abril | R$ 5,41 Mil | Outubro | R$ 5,84 Mil |
| Maio | R$ 5,59 Mil | Novembro | R$ 5,32 Mil |
| Junho | R$ 6,79 Mil | Dezembro | R$ 4,66 Mil |

- [ ] Eixo de Janeiro a Dezembro, sem ordem alfabética
- [ ] Formato igual ao da referência: vale em Fevereiro (menor), pico em Março (maior), segundo pico em Junho, queda em Julho
- [ ] A soma dos 12 meses dá R$ 65,83 Mil, igual ao cartão
