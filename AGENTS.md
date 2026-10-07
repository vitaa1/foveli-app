# Regras de desenvolvimento da Foveli

- Consultar `docs/MVP.md` para regras aprovadas e `CONTEXT.md` para vocabulário. Não implementar todo o escopo de uma vez; entregar incrementos pequenos.
- Nunca desenvolver nem fazer commits diretamente na `main`. Usar branch própria por funcionalidade, correção, infraestrutura ou documentação. Não integrar na `main` sem solicitação do proprietário.
- Sempre acompanhar novas funcionalidades e mudanças de comportamento com testes automatizados. Correções exigem teste de regressão que reproduza o defeito.
- Usar Django test runner no Docker com PostgreSQL de testes. Cobrir regras, permissões, dados de outros usuários, validações, dinheiro e estoque; validar transações/concorrência no banco real quando pertinente.
- Antes de concluir um incremento, executar `docker compose run --rm web python manage.py test`, `docker compose run --rm web python manage.py check` e `docker compose run --rm web python manage.py makemigrations --check --dry-run`. Corrigir falhas e relatar honestamente o que foi executado ou ficou bloqueado.
- Mudanças apenas documentais exigem revisão de consistência e `git diff --check`, sem testes artificiais do texto. Testes existentes não comprovam funcionalidades futuras apenas descritas no plano.
- Manter segredos, `.env`, banco, backups e arquivos gerados fora do Git. Priorizar Django nativo, poucos apps e Docker Compose; não adicionar tecnologias sem necessidade atual.
