# Foveli — plano de desenvolvimento do MVP

Atualizado em 06/10/2026. Infraestrutura inicial implementada; regras abaixo aprovadas para os próximos incrementos. Este documento distingue o escopo planejado das funcionalidades já entregues no README.

## 1. Entendimento e limites

Sistema web para um administrador e vendedores, usado principalmente no celular. Revendas são operadas pelo administrador. Produtos entregues continuam em estoque até venda, devolução ou perda. Comissões serão registradas manualmente como despesas, sem cálculo automático enquanto a regra não estiver definida. Não haverá ingredientes, lotes, validade, integração bancária ou emissão fiscal.

### Pontos que precisam ficar claros

- Venda e recebimento são medidas diferentes. Vender R$ 150 e receber R$ 100 gera R$ 150 vendidos, R$ 100 recebidos e R$ 50 pendentes; nunca R$ 250 de entradas.
- Regra corrigida pelo proprietário: sua irmã e seu pai recebem Pix ou dinheiro e depois repassam à conta da Foveli. Ambos os meios compõem a obrigação de prestação de quem recebeu.
- Cartão registrado como venda não prova recebimento pela Foveli. Sem integração, a confirmação de recebimento será manual.
- Preços praticados devem ser preservados na operação. Alterar o cadastro não pode recalcular o passado.
- A revenda é tratada como consignação no MVP descrito: só a quantidade informada como vendida gera valor devido.
- O estoque atual da revenda representa o último saldo conhecido pelo sistema, pois suas vendas podem ser informadas semanalmente.
- Saldo pendente é acumulado; filtros de período não podem esconder dívidas anteriores.
- Saldo do mês significa entradas menos saídas registradas. Não é lucro, pois não haverá custeio de produção, nem saldo bancário conciliado.
- “Receitas” será entendido como entradas financeiras; receitas culinárias e fichas técnicas estão fora do MVP.

### Regras confirmadas pelo proprietário

1. Os vendedores atuais são principalmente a irmã e o pai do proprietário. Pix e dinheiro ficam com eles até o repasse à Foveli.
2. Vendas no cartão geralmente são realizadas pelo próprio proprietário, pelo celular, sem maquininha. O sistema apenas registra a operação; não processa cobranças nem exige equipamento.
3. A revenda ainda não começou. O preço inicial será fixo em R$ 6,00 por unidade para qualquer brownie do catálogo, separado do preço sugerido ao consumidor.
4. A revenda mantém o preço até acertar o saldo. Não será necessário distribuir uma venda entre entregas com preços diferentes.
5. O proprietário define o preço ao consumidor. O vendedor não pode editar o preço ou aplicar desconto; o servidor usa o preço vigente na data efetiva da venda, inclusive no lançamento posterior, e preserva esse valor no histórico.
6. O vendedor repassa integralmente os valores recebidos. A Foveli paga sua comissão separadamente, depois do repasse, sem descontá-la da prestação. Valor fixo ou percentual ainda não definido; não presumir comissão zero nem criar uma fórmula por enquanto.

Proposta operacional: considerar o preço liberado para mudança quando não houver unidades remanescentes daquele produto na revenda nem dívida da revenda. Usar a dívida total evita criar um rateio de pagamentos por produto no MVP; explicitar essa condição na tela.

O meio de pagamento não determina quem está com o dinheiro. Nas vendas dos familiares, o padrão será recebido pelo vendedor, inclusive Pix. Nas vendas realizadas pelo proprietário, o recebimento ficará a conferir até o dinheiro estar disponível à Foveli. Não presumir que um cartão aprovado já creditou a conta da empresa. Uma exceção em que o proprietário recebe por uma venda de um familiar pode ser indicada na própria venda, mantendo separados quem vendeu e quem recebeu, sem novos perfis de acesso.

### Revisão de negócio aprovada — Q1 a Q17

1. **Q1 — Autoria:** vendedor registra suas vendas; administrador também pode registrar por ele. Separar vendedor responsável de usuário que fez o lançamento.
2. **Q2 — Momento do registro:** priorizar registro imediato e permitir posterior. Preservar data efetiva da venda e data do lançamento. Agrupamento somente para mesmo produto, preço e forma de pagamento.
3. **Q3 — Mudança de preço:** produtos já entregues passam a usar o preço vigente quando vendidos, sem alterar vendas anteriores.
4. **Q4 — Erro de lançamento:** somente administrador cancela venda confirmada, com motivo, desfazendo seus efeitos e preservando o histórico; registrar a venda correta separadamente.
5. **Q5 — Perda:** reduzir estoque e registrar motivo, sem gerar dívida automática do vendedor.
6. **Q6 — Comissão:** administrador pode pagar manualmente após repasse parcial, mesmo existindo outras pendências. Mostrar a pendência antes da confirmação; não descontar comissão da prestação.
7. **Q7 — Preço histórico:** guardar vigência dos preços definidos pelo proprietário. Venda lançada hoje com data de ontem usa o preço vigente ontem; o vendedor não escolhe livremente o preço.
8. **Q8 — Repasse excedente:** após correção/cancelamento, apresentar eventual crédito do vendedor separado da comissão; administrador pode devolver ou compensar no próximo acerto. Cancelar não movimenta dinheiro automaticamente.
9. **Q9 — Devolução real:** distinguir devolução de cliente de erro de lançamento. Produto devolvido só volta ao estoque disponível se estiver em condição de venda; caso contrário, registrar a perda sem baixar novamente a unidade que já saiu na venda.
10. **Q10 — Responsabilidade pelo estoque:** somente administrador registra perdas e confirma devoluções, inclusive o retorno de produtos do vendedor à Foveli.
11. **Q11 — Conferência posterior:** bloquear para vendedor o lançamento cuja data anteceda a última conferência que ajustou aquele produto naquele local. Explicar o bloqueio e encaminhar a correção ao administrador.
12. **Q12 — Origem do crédito:** crédito somente pelo valor que o vendedor efetivamente repassou a mais. Pagamento recebido diretamente pela Foveli não gera crédito para ele. Considerar também dinheiro ainda retido pelo vendedor em devoluções reembolsadas pela Foveli.
13. **Q13 — Reembolso:** centralizado no administrador, vinculado à venda, com valor e data. Não é comissão; não presumir pagamento a partir de cancelamento. Registrar somente o reembolso efetivamente realizado como saída de caixa.
14. **Q14 — Data da revenda:** usar a data do acerto como reconhecimento das vendas informadas, sem inventar distribuição diária. Relatórios separam essas vendas das realizadas no dia pelos vendedores.
15. **Q15 — Devolução parcial:** informar quantidade por item, limitada ao vendido ainda não devolvido, e calcular pelo preço original. Informar a condição do produto devolvido.
16. **Q16 — Dinheiro retido:** se o vendedor recebeu R$ 40 e a Foveli reembolsa R$ 40 ao cliente, os R$ 40 ainda retidos pelo vendedor continuam devidos. Reduzir vendas não elimina essa obrigação nem gera crédito indevido.
17. **Q17 — Correção da conferência:** administrador registra a venda atrasada com motivo obrigatório e indica se a saída já foi considerada na conferência. Quando já considerada, não baixar novamente; vincular a decisão à conferência e preservar a trilha de auditoria.

Essas decisões ampliam o escopo inicial com preço histórico, devoluções parciais, créditos e reembolsos. Implementar em incrementos, sem automatizar comissão ou adicionar integrações. Confirmadas pelo proprietário ao autorizar esta atualização.

## 2. Modelagem proposta

Decisão de identificadores: modelos próprios da Foveli terão `id` UUID v4 gerado pelo servidor e não editável, começando por User. Produtos, vendas, movimentações e demais modelos adotarão a mesma regra quando forem implementados; relações usam ForeignKey para preservar integridade. Tabelas internas do Django (permissões, grupos, sessões e log administrativo) mantêm seus IDs nativos, com referências ao usuário em UUID. Não criar uma classe base apenas para um campo neste momento. UUID não concede acesso nem substitui validação de permissões.

A migração inicial já aplicada será preservada. A migração `users.0002_user_uuid` converte o esquema vazio e suas referências, com bloqueio se houver usuários ou sessões. Sessões antigas devem ser invalidadas de forma explícita antes da conversão; a migração não apaga dados. O banco local foi conferido sem usuários/logs/sessões antes da alteração. Um ambiente que já contenha usuários precisa de migração de dados específica; não apagar banco, volume ou contas para contornar o bloqueio.

Usar os usuários e senhas do Django, sem tabela Seller separada: cada vendedor é um User com telefone e perfil vendedor. O administrador possui perfil administrador. Ativo/inativo usa o estado do usuário.

| Entidade | Dados essenciais e relações |
| --- | --- |
| User | Nome, login, senha gerenciada pelo Django, telefone, perfil, ativo. |
| Product | Nome, sabor, preço ao consumidor, ativo. Cada sabor é um cadastro. Preço de revenda dos brownies fixado em R$ 6,00 no MVP, sem edição por sabor. |
| ProductPrice | Produto, preço ao consumidor, início de vigência e autor; histórico para resolver o preço na data efetiva da venda. Não reescrever preços já aplicados em vendas. |
| Reseller | Estabelecimento, responsável, telefone, observação, ativo. Sem login. |
| StockLocation | Um local Foveli ou um local vinculado a um vendedor ou uma revenda. Criado automaticamente, sem tela própria. |
| StockBalance | Produto, local, quantidade. Uma linha única por produto e local; quantidade não negativa. Para revenda, mantém o preço vigente durante o saldo aberto. |
| StockMovement | Produto, quantidade positiva, tipo, origem, destino, data da operação, data de registro, autor e observação. Para envio à revenda, guarda os dois preços combinados. |
| Sale | Canal, vendedor responsável, local de saída, data efetiva, data de lançamento, forma de pagamento, destino do recebimento, autor e identificador único. Cancelamento preserva autor, motivo e data; correção após conferência preserva sua referência e se a saída já foi considerada. |
| SaleItem | Venda, produto, quantidade, preço unitário aplicado à Foveli. |
| Settlement | Vendedor ou revenda, valor informado, data, autor, situação informado/confirmado e confirmação pelo administrador. |
| CashReceipt | Valor efetivamente recebido, data e autor; vínculo com venda ou prestação confirmada, ou descrição para outra entrada manual. |
| Expense | Descrição, categoria simples, valor positivo, data e autor. Para a categoria Comissão, também identificar o vendedor beneficiário. |

Nos incrementos de devoluções e acertos, detalhar os registros vinculados de devolução por item (quantidade, condição e motivo), reembolso ao cliente e utilização/devolução de crédito do vendedor. Não representar essas operações apenas apagando uma venda ou mudando um saldo. Devolução de crédito ao vendedor e reembolso ao cliente têm destinatários e efeitos diferentes. A conferência precisa identificar produto, local, data efetiva, saldo contado e ajuste resultante, para sustentar Q11/Q17. Criar somente os registros necessários quando cada incremento for implementado.

StockLocation e StockBalance evitam colunas de estoque diferentes para cada participante. Não são módulos adicionais. A quantidade exibida no cadastro de produto é o saldo no local Foveli, sem duplicar esse número em Product.

Relações: produto e local possuem um saldo; movimentos registram entradas e saídas desses locais; uma venda possui itens; cada participante possui várias vendas e prestações. Recebimentos vinculados a prestações confirmadas devem ter vínculo único para impedir duplicidade.

O saldo é atualizado junto com o histórico, em uma única transação. Não haverá edição direta de StockBalance nem mudança de estoque pelo cadastro de produto.

### Preço da revenda

O envio já é registrado em StockMovement: essa linha guarda R$ 6,00 por brownie como preço para revenda e, separadamente, o preço final sugerido, sem criar um módulo de entregas. Aplicar um único preço de revenda para todos os sabores no MVP. O saldo do produto na revenda guarda o preço vigente; novos envios devem respeitá-lo enquanto houver saldo aberto. Cada venda preserva o preço aplicado em seu item. Uma eventual mudança futura de preço não recalcula operações anteriores.

Exemplo: 20 unidades entregues a R$ 6, com preço final sugerido de R$ 8. Informar 15 vendidas gera R$ 90 devidos à Foveli e deixa 5 unidades na revenda. Pagar R$ 60 deixa R$ 30 pendentes. O preço não pode mudar durante esse acerto aberto.

### Integridade e segurança

- Quantidades inteiras e positivas nas operações; valores monetários decimais, sem ponto flutuante.
- Movimentações, vendas e saldos gravados juntos; bloquear o saldo durante a operação para impedir duas vendas concorrentes da última unidade.
- Validar origem, destino e tipo: produção entra na Foveli; entrega sai da Foveli; venda baixa o local responsável; devolução retorna à Foveli; perda sai do local; ajuste exige motivo e administrador.
- Venda pertence a um único canal: vendedor, venda própria Foveli ou revenda. Para o acesso vendedor, o responsável vem da sessão autenticada, nunca de um campo livre enviado pelo navegador. Vendas próprias registradas pelo administrador baixam o estoque Foveli; receber o pagamento de uma venda de um familiar não muda o local de onde o produto saiu.
- Vendedor consulta apenas seus produtos, vendas, prestações e recebimentos associados. Proteção no servidor, inclusive no acesso por endereço direto.
- Somente administrador confirma dinheiro recebido. Informação de prestação enviada pelo vendedor não reduz a dívida nem aumenta o caixa antes dessa confirmação.
- Recebimentos não podem quitar a mesma venda duas vezes. Sem adiantamentos no MVP, limitar o valor confirmado ao saldo devido, com validação transacional.
- Inativar cadastros preserva histórico. Valores e estoque já lançados não devem ser alterados por edição livre; correções preservam autor e motivo, respeitando conferências posteriores para não recompor ou baixar estoque duas vezes.
- Reenvio do mesmo formulário não pode duplicar venda, transferência ou recebimento. Usar identificador único por operação.
- Autenticação, sessão, proteção CSRF e permissões nativas do Django; HTTPS em produção, segredos fora do repositório e backup com restauração verificada antes de uso real.

## 3. Fluxos

### Produção

Administrador seleciona produtos e quantidades → confirma → aumenta saldo Foveli e registra uma entrada por produto. Sem receitas culinárias ou módulo de produção.

### Vendedor

Administrador escolhe vendedor e produtos → entrega transfere saldos → vendedor vê produtos disponíveis → escolhe produto, quantidade e Pix/dinheiro/cartão → confirma venda → baixa seu estoque e preserva o preço vendido.

Na prestação, vendedor informa valor repassado → administrador confirma recebimento → reduz pendência e registra entrada uma única vez. O administrador também pode registrar diretamente um recebimento confirmado.

Pix e dinheiro recebidos pelo vendedor aumentam seu saldo a repassar. Exemplo: a irmã vende R$ 80 no Pix e R$ 40 em dinheiro; deve repassar R$ 120. Ao repassar R$ 100, a Foveli confirma R$ 100 de entrada e restam R$ 20 pendentes. Não é necessário vincular cada repasse a uma venda individual.

### Comissão do vendedor

Após o repasse, o proprietário informa manualmente a comissão efetivamente paga em Despesas, categoria Comissão, identificando vendedor, valor, data e descrição do acerto. Reutilizar o financeiro existente, sem tabela ou módulo de comissões.

O repasse pode ser parcial: outras pendências não bloqueiam o pagamento manual da comissão. Exibir o saldo pendente antes da confirmação.

O pagamento da comissão é uma saída independente: não reduz o total vendido, não abate o saldo a repassar e não altera o preço dos produtos. Enquanto valor fixo ou percentual não forem definidos, o sistema não calcula comissão devida ou pendente. O histórico registra apenas os pagamentos informados pelo administrador. A definição da regra de cálculo fica para uma decisão posterior, sem bloquear o restante do MVP.

### Vendas do proprietário

Administrador registra sua venda na mesma funcionalidade de vendas, com saída do estoque Foveli. Pode informar Pix, dinheiro ou cartão; cartão é apenas uma forma de pagamento registrada, sem integração ou exigência de maquininha. Confirmar data e valor quando o dinheiro estiver disponível à Foveli. Não gerar prestação para a irmã ou o pai nessas vendas.

Se o proprietário recebe por uma venda realizada por um familiar, registrar destino Foveli na venda desse familiar: manter sua autoria e baixa de estoque, mas não cobrar dele esse valor. O padrão dos familiares continua sendo recebimento pelo próprio vendedor, evitando um passo extra no fluxo habitual.

Se houver taxa de cartão, registrar a taxa como despesa e o recebimento bruto correspondente, deixando o saldo líquido correto. Não criar cálculo automático de taxas.

### Revenda

Administrador registra entrega com os dois preços → transfere estoque, sem receita → no acerto, informa quantidades vendidas → sistema exibe o total devido → administrador informa valor efetivamente recebido, inclusive parcial ou zero → confirma.

Venda e recebimento são registros separados, embora feitos na mesma tela. Um pagamento posterior pode quitar dívida sem registrar novamente unidades vendidas. Produtos não vendidos permanecem na revenda até devolução, perda ou próxima venda informada.

### Financeiro

Vendas alimentam indicadores de vendas e obrigações. CashReceipt alimenta entradas financeiras; despesas, reembolsos efetivamente pagos e devoluções efetivas de crédito alimentam saídas, uma única vez cada. Uma prestação não é somada novamente como receita além de seu recebimento. Compensação de crédito reduz o valor a repassar no próximo acerto, mas não é nova entrada nem saída de dinheiro.

Não calcular obrigação do vendedor apenas por vendas líquidas menos repasses: Q16 exige preservar dinheiro recebido e ainda retido quando a Foveli reembolsa o cliente. Separar vendas, custódia do dinheiro, repasses, créditos e pagamentos; validar sua reconciliação nos testes.

## 4. Telas

| Acesso | Tela | Conteúdo e ações |
| --- | --- | --- |
| Ambos | Login | Usuário e senha; destino conforme perfil. |
| Administrador | Início | Vendido hoje, unidades, despesas, estoque Foveli, pendências por participante e entradas/saídas do mês. |
| Administrador | Produtos e estoque | Cadastro, estoque por local, entrada, entrega, devolução, perda, ajuste e histórico com filtros. |
| Administrador | Registrar venda | Mesmo formulário simples de venda, acessível pelo início; vendas próprias baixam estoque Foveli. |
| Administrador | Vendedores | Lista/cadastro e detalhe com estoque, vendas por pagamento e prestação de contas. |
| Administrador | Revendas | Lista/cadastro e detalhe com entregas, estoque conhecido, quantidades vendidas e pagamentos. |
| Administrador | Financeiro | Recebimentos, despesas e outras entradas manuais. |
| Administrador | Relatórios | Uma tela com tipo de relatório e filtros compartilhados. |
| Vendedor | Meu dia | Estoque, vendido hoje, formas de pagamento, pendente e botão destacado “Registrar venda”. |
| Vendedor | Registrar venda | Produto, quantidade, forma de pagamento e confirmação. |
| Vendedor | Minhas contas | Histórico e informação de repasse; distinguir informado de confirmado. |

Formulários curtos dentro desses fluxos; evitar uma página de navegação para cada operação. Listas legíveis em telas pequenas, campos numéricos adequados ao celular, botões grandes e confirmação com mensagem clara.

Relatórios: vendas por período, vendedor, produto e revenda; estoque atual; despesas por período; pendências de vendedores e revendas. Filtros hoje, semana iniciando segunda-feira, mês e intervalo personalizado inclusivo, no fuso America/Sao_Paulo.

Resumo diário mostra estoque inicial, recebido, vendido, devolvido/perdido/ajustado e estoque final do dia. Assim, “recebeu menos vendeu” não é confundido com estoque restante quando há produtos de dias anteriores.

Estoque atual e pendências são posições acumuladas, explicitamente identificadas como tal. Estoque baixo pode usar um limite simples informado no filtro, sem criar regras automáticas de reposição.

## 5. Tecnologia e hospedagem

Django com Templates, Bootstrap e PostgreSQL. Um projeto, cinco apps: core (início e relatórios), users (acessos e revendas), products (produtos e estoque), sales (vendas e prestações) e finance (recebimentos e despesas): cinco apps ao todo. Usar a organização sugerida pelo proprietário, sem criar novos apps por operação.

Hospedagem escolhida para o MVP: Render, com um serviço Python e PostgreSQL gerenciado. Não contratar nem publicar nesta etapa.

Comparação consultada em 06/10/2026: Railway cobra recursos por uso e apresenta mínimo de US$ 5 no Hobby, sem isso garantir o custo total de aplicação e banco. Render oferece aplicação e banco gerenciado na mesma plataforma; a documentação comercial cita aproximadamente US$ 13/mês para Starter mais Basic-256mb como referência de julho de 2026, antes de extras. Escolha motivada pela configuração simples e previsibilidade inicial; confirmar a cotação vigente no provisionamento. Não é orçamento fechado em reais.

Fontes oficiais:
- https://railway.com/pricing
- https://render.com/articles/how-much-does-cloud-application-hosting-cost-for-small-businesses
- https://render.com/docs/web-services
- https://render.com/docs/free

O banco gratuito Render expira em 30 dias e o serviço gratuito pode suspender por inatividade; portanto, não são a base proposta para operação real. Por decisão posterior do proprietário, usar Docker e Docker Compose no desenvolvimento: Django e PostgreSQL em containers. No Render, usar o Dockerfile da aplicação e PostgreSQL gerenciado separado. Sem Redis, filas, API pública ou frontend separado.

## 6. Ordem de implementação e verificação

Decisão do proprietário: começar pela infraestrutura necessária e pelo backend, com desenvolvimento incremental e Git desde a primeira entrega. As telas finais vêm depois da validação das regras do negócio. Não construir toda a infraestrutura de produção antecipadamente.

| Incremento | Entrega | Critério para avançar |
| --- | --- | --- |
| 0 — Versionamento | Repositório Git local, exclusões de segredos e arquivos gerados, documentação inicial. | Primeiro commit revisado; nenhum segredo ou dado real versionado. |
| 1 — Base técnica | Dockerfile, Docker Compose com Django e PostgreSQL, dependências fixadas, configuração por ambiente e exemplo sem segredos. Definir User antes da primeira migração; criar apps conforme forem necessários. | Instalação reproduzível, conexão com banco, migrações e verificações do Django funcionando. |
| 2 — Acessos | Usuário administrador/vendedor, autenticação e regras de acesso no servidor. | Testes de usuário inativo, acesso indevido e isolamento entre vendedores. |
| 3 — Produtos e estoque | Cadastro, vigência de preços, saldos, entradas, entregas, devoluções, perdas e conferências com ajuste. | Testes de saldos e histórico, permissões, reversão integral em falha e concorrência em PostgreSQL, sem estoque negativo. |
| 4 — Vendas | Vendas próprias e dos vendedores; lançamento pelo administrador, registro posterior, preço histórico e correção após conferência. | Testes de preço na data efetiva, autoria, isolamento, bloqueio anterior à conferência, exceção auditada e ausência de baixa dupla. |
| 5 — Prestação e recebimentos | Repasse integral, confirmação e pagamentos parciais. | Testes do saldo pendente, limite da dívida e ausência de dupla contagem; recebimento pelo proprietário não gera dívida para os familiares. |
| 5a — Correções e devoluções | Cancelamento por erro e devolução real parcial com condição do produto. | Testes de permissões, preço original, quantidade máxima, repetição/concorrência e interação com conferências posteriores. |
| 5b — Créditos e reembolsos | Reembolso centralizado, crédito por repasse excedente, devolução/compensação e dinheiro retido. | Testes de reembolso antes/depois do repasse, dinheiro direto à Foveli e caixa sem duplicidade; Q16 mantém R$ 40 devidos. |
| 6 — Revendas | Cadastro, entrega a R$ 6 por brownie, quantidade vendida e acerto na data de reconhecimento. | Testes do preço preservado, estoque restante, pagamento posterior sem nova baixa e distinção nos relatórios diários. |
| 7 — Financeiro e consultas | Despesas, comissão manual, consultas do dashboard e relatórios. | Totais e períodos conferidos; comissão não altera vendas nem valor a repassar. |
| 8 — Interface móvel | Django Templates e Bootstrap para os fluxos já validados. | Testes dos formulários, permissões por URL, proteção CSRF e uso no celular; venda em poucos passos. |
| 9 — Publicação | Configuração Render, HTTPS, segredos, arquivos estáticos e backup. | Verificações de produção, restauração testada e revisão dos fluxos completos antes do uso real. |

Validar o backend com testes do Django e, quando útil, Django Admin. O Admin não deve permitir editar diretamente saldos ou contornar operações de estoque e financeiro. Não criar API ou frontend separado para testar o backend.

### Ciclo de cada incremento

1. Delimitar uma entrega pequena e seus critérios de aceite.
2. Implementar modelos, migrações e regras junto com testes automatizados dos comportamentos introduzidos ou alterados.
3. Executar os testes no PostgreSQL e verificações do Django; corrigir falhas antes de concluir a entrega.
4. Revisar as alterações e atualizar a documentação de execução e decisões.
5. Criar um commit descritivo e submeter essa versão estável aos agentes `code-reviewer` e `security-guard`, em paralelo, antes de propor integração na `main`.
6. Corrigir achados confirmados, adicionar testes de regressão e repetir testes/revisões da versão final. Registrar resultados e limitações com base e commit revisados.
7. Somente com testes aprovados e as duas revisões concluídas sem achados bloqueantes, apresentar a entrega para eventual autorização do proprietário de merge. Não integrar automaticamente na `main`.

### Revisão independente obrigatória

O `code-reviewer` verifica lógica, regras de negócio, regressões, migrações, manutenção e cobertura útil dos testes. O `security-guard` verifica vulnerabilidades, permissões, isolamento dos dados, segredos, configurações e abuso dos fluxos de estoque/financeiro. Ambos trabalham sobre o mesmo diff/commit; não corrigem o código durante a inspeção.

Defeitos e vulnerabilidades confirmados devem ser resolvidos antes de solicitar merge; sugestões opcionais não bloqueiam. Toda mudança posterior de código, configuração ou testes exige revalidação. Revisão indisponível/incompleta é pendência, não aprovação. Guardar a evidência no PR ou em `docs/reviews/results/`.

Instruções executáveis pelos agentes em `AGENTS.md`; roteiros em `docs/reviews/code-reviewer.md` e `docs/reviews/security-guard.md`. A regra vale para features, correções e infraestrutura. Não existe ainda execução desses agentes no GitHub nem proteção técnica da branch; esta atualização configura o fluxo de trabalho do projeto, sem prometer bloqueio automático no servidor.

### Testes automatizados obrigatórios

- Sempre desenvolver funcionalidades e mudanças de comportamento acompanhadas de testes automatizados. Correção de defeito inclui teste de regressão que reproduz o problema, preferencialmente falhando antes da correção.
- Usar inicialmente o test runner nativo do Django, dentro do Docker e com PostgreSQL de teste separado. Não substituir o banco por SQLite para validar transações, restrições ou concorrência.
- Cobrir caminho esperado, entradas inválidas, limites, permissões e acesso aos dados de outros usuários. Estoque e financeiro exigem testes de atomicidade, duplicidade, valores decimais e concorrência quando aplicável.
- Testes devem verificar resultados de negócio e falhas reais, sem apenas repetir a implementação. Usar mocks apenas quando necessários; operações de banco devem ser exercitadas no PostgreSQL real.
- Antes de concluir cada incremento, executar a suíte completa enquanto seu tamanho permitir, `check` e `makemigrations --check --dry-run`. Mudanças de infraestrutura também exigem construção/inicialização e verificações automatizadas pertinentes.
- Testes manuais e uso do Admin complementam, mas não substituem os automatizados. Não concluir uma funcionalidade com falhas conhecidas ou declarar validação que não foi executada; registrar qualquer bloqueio.
- Alterações exclusivamente documentais devem passar por revisão de consistência e verificação de diff; não criar testes artificiais de texto. Se rodar a suíte existente, informar que isso não valida regras futuras ainda não implementadas.
- Executar a suíte no GitHub Actions por `.github/workflows/ci.yml` em todo PR e push, além dos testes locais. O fluxo e a futura publicação no Render estão em `docs/CI-CD.md`. CI deve passar antes de propor merge; proteção técnica da main e CD no Render ainda dependem de configuração na etapa correspondente.

### Versionamento

- Nunca desenvolver ou fazer commits diretamente na `main`. Antes de qualquer alteração, criar ou selecionar uma branch de trabalho adequada. Cada nova funcionalidade terá sua própria branch `feat/<nome>`; usar `fix/<nome>` para correções e `docs/<nome>` para documentação. Essa regra também vale para infraestrutura (`chore/<nome>`).
- Fazer commits pequenos por entrega dentro da branch correspondente. Não integrar alterações na `main` automaticamente; a integração será tratada separadamente quando solicitada pelo proprietário. O primeiro commit de documentação foi criado antes desta regra; preservar seu histórico.
- Versionar código, testes, migrações, dependências, documentação e configuração de infraestrutura sem segredos.
- Não versionar senhas, `.env`, ambiente virtual, banco, backups ou arquivos gerados. Manter `.env.example` apenas com exemplos seguros.
- Criar o primeiro commit com a documentação e `.gitignore`. Usar a identidade Git já configurada; se estiver ausente, solicitar nome e e-mail ao proprietário, sem inventá-los.
- Git local mantém o histórico; remoto já conectado em https://github.com/vitaa1/foveli-app. Preservar a visibilidade configurada pelo proprietário.
- Registrar no README os passos reproduzíveis de instalação, migração e testes quando a base técnica existir.

Exemplo de aceite: produzir 100 → entregar 20 ao pai → saldos 80/20 → vender 15 a R$ 8 (R$ 80 via Pix recebido por ele e R$ 40 em dinheiro) → saldos 80/5 e R$ 120 vendidos e a repassar → confirmar repasse de R$ 100 → R$ 20 pendentes e R$ 100 de entrada. O total produzido precisa ser explicável por estoque, vendas e perdas. Uma venda própria do proprietário de 2 unidades no cartão a R$ 8 deixa estoque Foveli em 78 e R$ 16 a conferir, sem dívida do pai; só entra no financeiro após confirmação do recebimento.

Cada etapa deve funcionar e passar pelas verificações relevantes antes da próxima. O incremento de infraestrutura está implementado na branch `chore/docker-setup`; instruções de execução e escopo entregue estão no README. As regras de acesso do negócio e funcionalidades comerciais ficam para os próximos incrementos.
