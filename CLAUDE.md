# Atividade Power BI — SENAI (Desenvolvimento de Sistemas)

Protótipo acadêmico: tratar a base de vendas e preparar o BI e a documentação.
Não adicionar nada além do que o enunciado pede. Entrega final: pasta zipada no Google Classroom.

- Enunciado: não há texto. A imagem `enunciado/referencia_dashboard.png` É o enunciado, e o objetivo é REPRODUZIR esse dashboard
  ("Relatório de Vendas": 4 cartões + área por mês + funil por tipo + pizza por marca). A Margem de Lucro (%) não entra no dashboard.
- Base: `dados/brutos/Vendas_-_Site.xlsx` e `dados/brutos/Vendas_-_Site.xlsx - Vendas.csv`

## Estrutura
```
power-bi/
├── CLAUDE.md              (regras e contexto da atividade)
├── enunciado/             (PDF ou texto da atividade)
├── dados/
│   ├── brutos/            (base original, nunca alterada)
│   └── tratados/          (saída do tratamento)
├── scripts/               (Python do tratamento)
├── powerbi/
│   ├── consultas_m/       (Power Query)
│   ├── medidas_dax.md     (medidas + tabela Calendário)
│   ├── modelo_dados.md    (relacionamentos)
│   └── roteiro_dashboard.md
└── documentacao/          (relatório final + prints)
```

## Ambiente
- Python 3.12.10 em `%LOCALAPPDATA%\Programs\Python\Python312\python.exe` (fora do PATH nesta máquina)
- pandas 3.1.0, openpyxl 3.1.5
- Power BI Desktop 2.159.883.0 (já instalado)

## Permissões
- Ler `enunciado/` e `dados/brutos/`: sim
- Criar/editar `scripts/`, `dados/tratados/`, `powerbi/`, `documentacao/`: sim
- Alterar ou apagar `dados/brutos/`: NÃO
- Instalar pacotes (pandas, openpyxl): sim, avisando antes
- Git: NUNCA rodar add/commit/push ou nada que altere histórico. Só sugerir mensagens de commit como texto.

## Fluxo (só avançar com aprovação do estudante nos checkpoints)
EXPLORAÇÃO → PLANO (checkpoint) → TRATAMENTO → MODELAGEM/DAX → ROTEIRO DO DASHBOARD → DOCUMENTAÇÃO → AUTO-REVISÃO

1. Explorar a base e listar problemas (nulos, duplicados, tipos, padronização). Sem código de tratamento. Apresentar plano e aguardar.
2. Script em `scripts/` gerando `dados/tratados/`, com log antes/depois.
3. Consultas M, medidas DAX e modelo de relacionamentos em `powerbi/`.
4. Roteiro página a página do dashboard (visual, campos, filtros).
5. Documentação em Word: contexto, base, problemas e tratamento, código comentado, justificativa dos visuais, conclusões, com espaços marcados para os prints.
6. Auto-revisão: conferir cada item do enunciado contra o entregue e listar o que falta.

## Não fazer
- Alterar a base original.
- Inventar dados ou preencher valores sem mostrar a regra.
- Criar APIs, bancos, automações ou extras não pedidos.
- Afirmar que gerou o .pbix — ele é montado manualmente pelo estudante.
- Prosseguir sem aprovação nos checkpoints.
