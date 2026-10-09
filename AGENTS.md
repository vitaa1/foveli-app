# Regras de desenvolvimento da Foveli

- Consultar `docs/MVP.md` para regras aprovadas e `CONTEXT.md` para vocabulário. Não implementar todo o escopo de uma vez; entregar incrementos pequenos.
- Modelos proprios da Foveli usam UUID v4 como chave primaria: `UUIDField(primary_key=True, default=uuid.uuid4, editable=False)`. Manter IDs nativos das tabelas internas do Django. UUID nao substitui autorizacao nem isolamento de dados.
- Nunca desenvolver nem fazer commits diretamente na `main`. Usar branch própria por funcionalidade, correção, infraestrutura ou documentação. Não integrar na `main` sem solicitação do proprietário.
- Sempre acompanhar novas funcionalidades e mudanças de comportamento com testes automatizados. Correções exigem teste de regressão que reproduza o defeito.
- Usar Django test runner no Docker com PostgreSQL de testes. Cobrir regras, permissões, dados de outros usuários, validações, dinheiro e estoque; validar transações/concorrência no banco real quando pertinente.
- Antes de concluir um incremento, executar `docker compose run --rm web python manage.py test`, `docker compose run --rm web python manage.py check` e `docker compose run --rm web python manage.py makemigrations --check --dry-run`. Corrigir falhas e relatar honestamente o que foi executado ou ficou bloqueado.
- Mudanças apenas documentais exigem revisão de consistência e `git diff --check`, sem testes artificiais do texto. Testes existentes não comprovam funcionalidades futuras apenas descritas no plano.
- Manter segredos, `.env`, banco, backups e arquivos gerados fora do Git. Priorizar Django nativo, poucos apps e Docker Compose; não adicionar tecnologias sem necessidade atual.
- Manter `.github/workflows/ci.yml` executando toda a suíte em PRs e pushes. Não pular testes, enfraquecer checks ou usar `continue-on-error` para fazer o CI passar. Conferir o resultado remoto do commit antes de propor merge; CI não substitui os revisores. Ver `docs/CI-CD.md`.

## Revisores obrigatórios antes do merge

- Por solicitação do proprietário, após implementar cada feature e passar nos testes, executar dois subagentes independentes em paralelo: `code-reviewer` e `security-guard`. Aplicar também a correções e mudanças de infraestrutura/código antes de integrar na `main`.
- Usar as instruções em `docs/reviews/code-reviewer.md` e `docs/reviews/security-guard.md`, respectivamente. Fornecer aos dois a mesma base e o mesmo commit final, requisitos, escopo e resultados dos testes. Identificar a base real da integração; se a branch acumula incrementos não integrados, revisar todo o diff destinado à `main`.
- Os revisores inspecionam e reportam; não alteram arquivos nem fazem commits, pushes ou merge. Coordenar testes que compartilhem banco para evitar colisões; inspeções podem ocorrer em paralelo.
- O agente implementador trata os achados, adiciona testes de regressão quando aplicável e repete testes e revisão após mudanças. Achado descartado exige justificativa verificável; não ocultar divergências.
- Não solicitar ou realizar merge com revisão faltante, testes falhando ou defeito/vulnerabilidade confirmado em aberto. Sugestões opcionais não bloqueiam. Se um revisor estiver indisponível, informar que a revisão está pendente; não substituí-la por alegação de aprovação.
- Registrar base/commit revisados, resultados dos dois revisores, achados e resolução no PR ou em `docs/reviews/results/`. Nenhum resultado deve afirmar ausência garantida de vulnerabilidades. Mudança posterior de código/configuração/testes invalida a revisão da versão anterior.
- Esta é uma regra de execução pelos agentes no projeto; não configura GitHub Actions nem proteção de branch. Merge continua dependendo de solicitação do proprietário. Alterações somente documentais seguem revisão de consistência; documentos que afetam implementação não dispensam revisar o código quando ele for implementado.
