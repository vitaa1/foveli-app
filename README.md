# Foveli

Gestão simples de produtos, estoque, vendas e prestações de contas.

## Estado atual

Primeiro incremento: Django 5.2 LTS, Python 3.13, PostgreSQL 17 e Docker Compose. Inclui usuário personalizado, Django Admin e verificação de disponibilidade do banco. Estoque, vendas, permissões de negócio e telas móveis ainda serão desenvolvidos nos próximos incrementos.

Validação inicial: imagem construída, migrações aplicadas, cinco testes aprovados em PostgreSQL, nenhuma migração pendente e verificação de produção do Django sem avisos. Gunicorn, conexão com banco e CSS do Admin também verificados na imagem sem montagem do código local. Não houve publicação no Render.

Revisão de infraestrutura em 07/10/2026: suíte ampliada para 16 testes, incluindo configuração de produção, banco por URL/SSL, desativação de sessão, CSRF e regressões HTTP/1 do Gunicorn. Exclusões Docker verificadas com 14 arquivos fictícios em contexto isolado. Migrações em banco vazio, persistência após reinício e imagem de produção também verificadas; os relatórios dos revisores ficam em `docs/reviews/results/`.

## Iniciar no Windows

Instale e inicie o Docker Desktop com containers Linux. Não é necessário instalar Python ou PostgreSQL no computador.

Na pasta do projeto, usando PowerShell:

```powershell
Copy-Item .env.example .env
docker compose build
docker compose run --rm web python manage.py migrate
docker compose up -d
```

Copie o exemplo apenas na primeira configuração; preserve um `.env` existente. O Compose inicia o banco e aguarda sua disponibilidade. O volume `postgres_data` mantém o banco entre reinicializações. Credenciais do exemplo são exclusivas de desenvolvimento; não reutilizar em produção.

- Disponibilidade: http://localhost:8000/health/
- Administração: http://localhost:8000/admin/
- A raiz `/` ainda não tem página; isso será feito no incremento de interface.

Crie sua conta administrativa de forma interativa, sem colocar senha no código:

```powershell
docker compose exec web python manage.py createsuperuser
```

## Verificação

Testes automatizados são obrigatórios em cada incremento de desenvolvimento. Funcionalidades novas incluem testes dos comportamentos esperados e dos erros relevantes; correções incluem testes de regressão. Verificações manuais não substituem a suíte. As regras completas estão em [Testes automatizados obrigatórios](docs/MVP.md#testes-automatizados-obrigatórios).

```powershell
docker compose run --rm web python manage.py check
docker compose run --rm web python manage.py makemigrations --check --dry-run
docker compose run --rm web python manage.py test
```

Os testes usam um banco PostgreSQL separado, criado e removido pelo Django. Execute somente com a configuração local/de testes, nunca com credenciais de produção.

Ao alterar Dockerfile ou `.dockerignore`, execute também no PowerShell, com o Docker ligado:

```powershell
.\scripts\Test-DockerContext.ps1
```

O teste usa um contexto temporário com arquivos fictícios, aplica o `.dockerignore` real e verifica o resultado de `COPY`. Não lê chaves, backups ou `.env` locais. O contexto temporário é removido ao final.

## Uso diário

```powershell
docker compose up -d
docker compose logs --tail=50 web
docker compose down
```

`down` preserva o volume. Não use `down -v` para parar: essa opção apaga os dados do volume. Alterações no código são recarregadas pelo servidor local; após mudar dependências ou Dockerfile, reconstrua com `docker compose up -d --build`.

As dependências diretas ficam em `requirements.in`; todas as versões resolvidas estão fixadas em `requirements.txt`. Após atualizar versões diretas, regenere o arquivo em container Python limpo e teste antes do commit:

Exceção documentada: Gunicorn 26.2.2 é instalado do arquivo oficial do commit `8d98faa9a13d3399a7bea81b5169e5cd72225395`, com SHA-256 fixado na URL. Em 07/10/2026, as tags corrigidas existiam no GitHub, mas o índice PyPI consultado ainda oferecia apenas 26.2.0. A atualização incorpora os limites de parsing HTTP/1 da [release 26.2.1](https://github.com/benoitc/gunicorn/releases/tag/26.2.1). Não trocar essa referência por uma branch móvel nem remover o hash ao atualizar o lock. Quando a versão corrigida estiver disponível no índice, a migração para o pacote publicado deve preservar os testes de regressão.

```powershell
docker run --rm --mount "type=bind,source=$($PWD.Path),target=/app" -w /app python:3.13-slim-bookworm sh -c "pip install -r requirements.in && pip freeze > requirements.txt"
```

## Configuração

| Variável | Uso |
| --- | --- |
| `DJANGO_SECRET_KEY` | Segredo obrigatório; em produção, aleatório e com pelo menos 50 caracteres. |
| `DJANGO_DEBUG` | `true` somente localmente; padrão seguro `false`. |
| `DJANGO_ALLOWED_HOSTS` | Hosts separados por vírgula, sem protocolo. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origens HTTPS confiáveis, separadas por vírgula, quando necessário. |
| `POSTGRES_DB/USER/PASSWORD/HOST/PORT` | Conexão local com PostgreSQL. |
| `DATABASE_URL` | Alternativa para produção; tem precedência sobre a conexão local. |
| `POSTGRES_SSLMODE` | SSL do banco; sobrescreve `sslmode` da URL quando definido. |
| `DJANGO_TRUST_PROXY` | `true` apenas atrás de proxy confiável que controla `X-Forwarded-Proto`. |
| `PORT` | Porta do Gunicorn; padrão 8000. |

O Compose é de desenvolvimento: usa recarga automática, código montado e porta acessível apenas pelo próprio computador. O banco não expõe porta no host. Não inclua `.env`, dados ou backups no Git ou na imagem.

## Produção planejada

Render construirá o Dockerfile, que inicia Gunicorn e inclui arquivos estáticos via WhiteNoise. O PostgreSQL será gerenciado pelo Render, separado do container da aplicação. O Compose local não será executado no Render.

Na etapa de publicação: configurar segredos próprios, hosts, HTTPS/proxy e banco; executar migrações uma vez por publicação, `check --deploy`, verificar backup/restauração e testar os fluxos. A inicialização do servidor não executa migrações automaticamente. Ainda não houve publicação nem contratação de serviço.

## Git e desenvolvimento

Nunca desenvolver diretamente em `main`. Cada incremento começa em uma branch `feat/`, `fix/`, `chore/` ou `docs/`; testar, revisar e documentar antes do commit. Não integrar na `main` sem solicitação do proprietário.

Após implementar e testar cada feature, executar em paralelo os agentes [code-reviewer](docs/reviews/code-reviewer.md) e [security-guard](docs/reviews/security-guard.md). Corrigir os achados e revalidar antes de propor merge. As duas revisões devem identificar o commit avaliado e suas limitações. O procedimento também se aplica a correções e infraestrutura; regras completas em [AGENTS.md](AGENTS.md). Essa política ainda não é um bloqueio automático configurado no GitHub.

Remoto: https://github.com/vitaa1/foveli-app

Regras e próximos incrementos: [plano do MVP](docs/MVP.md). Vocabulário: [CONTEXT.md](CONTEXT.md).
