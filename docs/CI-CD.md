# Integração e entrega contínuas

## CI — verificação automática de cada mudança

O workflow `.github/workflows/ci.yml` executa no GitHub Actions quando um PR é aberto, reaberto ou atualizado, e em pushes para branches, inclusive `main`. Não usa filtro de arquivos que possa deixar o check obrigatório sem execução. Cada execução valida toda a suíte disponível no commit, não apenas os testes novos.

O job **Backend e infraestrutura** usa runner Linux descartável, Docker Compose e PostgreSQL. Executa:

1. Configuração de teste a partir do `.env.example`, sem credenciais reais.
2. Teste de exclusão de arquivos sensíveis do contexto Docker.
3. Construção da imagem e verificação de compatibilidade das dependências.
4. `check`, detecção de migrações faltantes e migração de banco vazio.
5. Toda a suíte Django, incluindo regressões de código já implementado.
6. `check --deploy` com configurações de produção e segredo temporário de teste.
7. Inicialização da aplicação e resposta do health com banco real.
8. Limpeza do banco/volume do runner, inclusive quando uma etapa falha.

Não há `continue-on-error` nas validações. Falha em uma delas impede sucesso do job. Logs resumidos dos serviços ajudam no diagnóstico; não há acesso a dados ou segredos de produção. PRs de forks podem depender de aprovação da execução, conforme as políticas do GitHub.

O workflow usa `pull_request`, nunca `pull_request_target`, token somente de leitura, checkout sem credenciais persistidas e ação de checkout fixada por SHA. Execuções obsoletas do mesmo evento/branch são canceladas. Push e PR têm grupos separados para que um não cancele a validação do outro.

Ao abrir o PR, acompanhar a aba **Checks**; todos os testes precisam passar antes de propor merge. A passagem do CI não prova que funcionalidades ainda não implementadas funcionam nem substitui a revisão pelos agentes.

## Revisões e proteção da main

Fluxo obrigatório: branch → implementação e testes locais → CI do PR → code-reviewer + security-guard → correções e nova validação → autorização do proprietário → merge.

Os agentes são executados pelo assistente conforme `AGENTS.md`; não estão hospedados no GitHub Actions. Seus relatórios identificam o commit revisado. Uma mudança posterior de código/configuração/testes exige reavaliação.

Criar futuramente uma regra de proteção da `main` exigindo PR e sucesso do check **Backend e infraestrutura**, sem permitir bypass rotineiro. A existência do workflow sozinha não impede tecnicamente um merge pelo GitHub. Não afirmar que essa proteção foi configurada sem verificar a regra no repositório. Não fazer merge nesta entrega.

## CD — publicação após integração validada

CI valida; CD publica a versão validada. Um PR aberto não publica em produção.

Na etapa de publicação do MVP, conectar o serviço Render à branch `main`, usar o Dockerfile e PostgreSQL gerenciado. Configurar **Auto-Deploy: After CI Checks Pass**. O workflow também roda após o merge na `main`, validando o commit efetivamente integrado antes de o Render publicar.

No Render, configurar segredos próprios, domínio/hosts, proxy HTTPS, migrações antes de iniciar a nova versão, health check `/health/` e backup/restauração. Verificar a compatibilidade das migrações com a versão anterior antes de definir rollback; voltar a imagem não desfaz automaticamente alterações no banco.

O Render considera checks com conclusão `neutral` ou `skipped` aceitáveis, além de `success`. Portanto, manter o job de testes obrigatório e sem condição que o pule na `main`, e verificar o funcionamento real do gatilho na primeira publicação.

**Estado desta entrega:** workflow de CI adicionado; serviço Render e CD ainda não provisionados. A proteção de branch permanece pendente. Não adicionar deploy hooks, tokens de produção ou publicação automática de PRs nesta etapa.

## Referências oficiais

- [Sintaxe de workflows do GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Cuidados com pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)
- [Render: publicação após CI](https://render.com/docs/deploys)
