# Revisão da infraestrutura e backend — 07/10/2026

## Versão e conclusão

- Branch: `fix/revisao-infraestrutura`.
- Base de integração: `00563b5d21540965c0334eb2160995bfc8e22495` (`main`).
- Primeira revisão: `21bf2351ef149986fa2e69e5ebacabec076606d3`.
- Código final revisado pelos dois agentes: `c6ad89e2e62809666bf8d491ec7248d7e4718758`.
- Resultado final do `code-reviewer`: **sem achados bloqueantes**.
- Resultado final do `security-guard`: **sem achados bloqueantes no escopo revisado**.

O diff acumulado destinado à main foi inspecionado; não houve merge. Este relatório é um acréscimo documental posterior ao commit de código revisado. Nenhuma funcionalidade comercial foi adicionada nesta revisão.

## Escopo

Dockerfile, Compose, exclusões de arquivos, dependências, configuração Django, conexão PostgreSQL, migração inicial, usuário personalizado, Django Admin, endpoint health e testes existentes. O ambiente local foi atualizado para a imagem corrigida. Não houve contratação ou publicação no Render.

## Achados e resolução

### P2 — Chaves e backups locais podiam entrar na imagem

Confirmado independentemente pelos dois agentes. O Git ignorava `.pem`, `.key` e `.dump`, mas o contexto Docker não; `COPY . .` poderia incluí-los na imagem. Não foi encontrada evidência de um vazamento ocorrido.

Correção: exclusões recursivas no `.dockerignore` para chaves, backups, arquivos de ambiente, caches e diretórios de configuração. Também excluídos `.aws/` e `.codex/` do Git.

Regressão automatizada: `scripts/Test-DockerContext.ps1` cria contexto temporário com 14 arquivos fictícios na raiz/subpastas, aplica o filtro real e verifica os arquivos copiados pelo Docker. Um arquivo de código serve como controle positivo. Nenhum segredo local é lido; a limpeza verifica o caminho absoluto temporário.

Evidência: com o `.dockerignore` do commit inicial, o teste falhou indicando `private.pem` incluído; com o filtro corrigido, os 14 arquivos ficaram excluídos e o código foi preservado.

### P2 — Gunicorn anterior à correção de limites HTTP/1

Identificado pelo security-guard. Gunicorn 26.2.0 não limitava corretamente linhas de tamanho de chunk e trailers sem término. A exploração externa depende do encaminhamento de requisições pelo proxy; não foi executado ataque ou teste de carga.

Correção: Gunicorn 26.2.2, instalado do repositório oficial no commit `8d98faa9a13d3399a7bea81b5169e5cd72225395`, com SHA-256 `b42561d72978f30c97b65ea1ba54b0171dfe7f1ef8603b13085647cacec2077d` fixado em ambos os arquivos de dependências. As tags oficiais existiam, mas o PyPI consultado ainda oferecia apenas 26.2.0; uma instalação por número 26.2.2 falhou antes da escolha da referência oficial verificável. Não foi utilizada branch móvel.

Regressão automatizada: dois testes em `core/test_gunicorn.py`, com entradas finitas menores que 100 bytes, sem socket. Em 26.2.0 falharam com `NoMoreData` e `ChunkMissingTerminator`; em 26.2.2 passaram, verificando a aplicação dos limites por `InvalidChunkSize` e `LimitRequestHeaders`.

Fontes primárias: [Gunicorn 26.2.1](https://github.com/benoitc/gunicorn/releases/tag/26.2.1) e [26.2.2](https://github.com/benoitc/gunicorn/releases/tag/26.2.2).

## Verificações realizadas pelo implementador

| Verificação | Resultado |
| --- | --- |
| Suíte antes das correções | 5 testes aprovados em PostgreSQL. |
| Suíte final | 16 testes aprovados em PostgreSQL. |
| Configuração de ambiente | Testes de defaults de produção, segredo inválido, URL PostgreSQL, credenciais codificadas, SSL e proxy/hosts. |
| Admin | Acesso permitido ao superusuário; usuário comum bloqueado; inativo não autentica; desativação invalida acesso de sessão existente; login sem CSRF é rejeitado. |
| Health | Conexão real ao banco e falha sem exposição de detalhes. |
| Regressões | Contexto Docker e parser HTTP/1 reproduzidos antes e aprovados depois. |
| Django | `check` sem problemas; `makemigrations --check --dry-run` sem alterações. |
| Dependências | `pip check` sem incompatibilidades; metadados confirmam Gunicorn 26.2.2. |
| Construção | Docker build com imagem Python atualizada por `--pull`; build final bem-sucedido. |
| Banco vazio | Migrações completas em projeto Compose temporário com banco e volume próprios. |
| Persistência | Reinício do banco temporário seguido de `migrate --check` aprovado; migrações permaneceram aplicadas. |
| Imagem de produção | Sem montagem do código local; executada sem root; `.env` e `.git` ausentes; health com banco, login Admin e CSS respondem 200; HTTP redireciona para HTTPS. |
| Configuração de produção | `check --deploy --fail-level WARNING` sem avisos. |
| Limpeza | Removidos somente o projeto/volume temporários e o container de smoke criados pela revisão; banco local preservado. |

Versões observadas: Python 3.13.16; Django 5.2.18; Gunicorn 26.2.2; PostgreSQL 17.11 (Debian 17.11-1.pgdg12+2); psycopg/psycopg-binary 3.3.6; libpq 18.6; sqlparse 0.6.0; asgiref 3.12.1; WhiteNoise 6.12.0.

## Evidência independente dos agentes

Ambos revisaram em paralelo a mesma base e o mesmo commit final. Não editaram arquivos nem executaram testes que compartilhassem o banco. O code-reviewer verificou o diff acumulado, a correção, os testes e `git diff --check`; não encontrou defeitos adicionais confirmados. O security-guard confirmou a resolução dos dois achados e examinou configurações, permissões, isolamento dos testes e fontes oficiais das dependências.

As execuções operacionais da tabela são do implementador e foram fornecidas aos revisores; não são apresentadas como execução independente deles.

Consultas de segurança adicionais: [Django 5.2.18](https://docs.djangoproject.com/en/dev/releases/5.2.18/), [PostgreSQL 17](https://www.postgresql.org/support/security/17/), [Python 3.13.16](https://www.python.org/downloads/release/python-31316/), [sqlparse](https://github.com/andialbrecht/sqlparse/security/advisories/GHSA-cfqr-cjx5-5jcm), [psycopg](https://github.com/psycopg/psycopg/security), [asgiref](https://github.com/django/asgiref/security) e [WhiteNoise](https://github.com/evansd/whitenoise/security). Não foram identificados outros avisos aplicáveis nas páginas examinadas.

## Limitações e próximos passos

- Revisão manual e testes não garantem ausência de falhas ou vulnerabilidades.
- Não houve scanner completo de imagem nem auditoria de todos os pacotes Debian/OpenSSL; `pip check` verifica compatibilidade, não CVEs.
- Configuração real do Render, backup/restauração de produção e proteção da main no GitHub ainda não foram validados/configurados.
- Estoque, financeiro, permissões comerciais e isolamento de dados dos vendedores ainda não existem; precisarão de testes e revisões nos próximos incrementos.
- Antes de integrar futuras alterações de código, configuração ou testes, repetir a revisão na nova versão. O proprietário não autorizou merge nesta tarefa.
