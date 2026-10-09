# Publicação no Render

Estado em 09/10/2026: conta criada, banco Free solicitado e Web Service Docker criado em Virginia. Os PRs #1 a #3 foram integrados na main pelo proprietário. As primeiras tentativas de publicação falharam na inicialização (status 127); publicação e CD ainda não foram validados. A correção do comando segue em PR separado, sem autorização de merge automático.

## Configuração escolhida

Usar o painel Render: um Web Service Docker e um PostgreSQL gerenciado, na mesma região (Virginia). Não é necessário outro serviço nem Compose em produção. O Dockerfile existente constrói a aplicação, coleta estáticos e inicia Gunicorn na porta fornecida pelo Render.

Na criação, conferir os preços atuais e aprovar o custo antes de provisionar. Selecionar serviço web pago que suporte pre-deploy e PostgreSQL pago com backup; registrar plano, retenção e custo efetivamente escolhidos. Não tratar banco gratuito temporário como armazenamento de produção.

## Ativação, quando a conta estiver disponível

1. Conectar GitHub ao Render e autorizar o repositório `vitaa1/foveli-app`.
2. Após revisão, CI e autorização do proprietário para integrar o código, criar PostgreSQL 17, banco `foveli`, na região escolhida. Restringir acesso externo e usar a URL interna no serviço web.
3. Criar Web Service do repositório, branch `main`, linguagem Docker, Dockerfile `./Dockerfile`, contexto raiz. Manter o comando padrão da imagem; não usar runserver.
4. Preencher as variáveis abaixo no painel. O hostname deve ser o endereço exato atribuído ao serviço, sem curinga. Se necessário, corrigir esse valor antes de repetir a primeira publicação.
5. Configurar Pre-Deploy Command: `python manage.py migrate --noinput`; Health Check Path: `/health/`; Auto-Deploy: **After CI Checks Pass**. Sem filtros de caminhos e sem publicação de PRs.
6. Conferir o primeiro deploy e seus logs. Criar o administrador pelo Shell do serviço com `python manage.py createsuperuser`, informando a senha interativamente.

| Variável | Valor |
| --- | --- |
| `DJANGO_DEBUG` | `false` |
| `DJANGO_SECRET_KEY` | Segredo aleatório exclusivo, com pelo menos 50 caracteres, gerado e guardado fora do Git |
| `DATABASE_URL` | URL interna do PostgreSQL, tratada como segredo |
| `DJANGO_ALLOWED_HOSTS` | Hostname exato do serviço, por exemplo `nome-atribuido.onrender.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Origem HTTPS correspondente, por exemplo `https://nome-atribuido.onrender.com` |
| `DJANGO_TRUST_PROXY` | `true`, apenas no serviço atrás do proxy Render |

Não copiar credenciais locais de `.env.example` nem colocar segredos em PRs ou neste documento. Domínios adicionais exigem atualização explícita dos hosts e origens.

## Critérios para declarar CD ativo

- `/health/` responde 200 via HTTPS; `/admin/login/` carrega com CSS e login funcional. A raiz `/` ainda responde 404 porque a interface comercial não foi implementada.
- Validar no ambiente Render que o health check alcança a consulta ao banco: o Render aceita redirecionamentos como sucesso, portanto um 301 de HTTPS sozinho não comprova banco saudável. Se o proxy não encaminhar o protocolo esperado no health interno, corrigir esse comportamento com teste antes de declarar o ambiente validado.
- Conferir `check --deploy --fail-level WARNING`, migrações aplicadas e ausência de DEBUG.
- Configurar proteção da main exigindo PR e o check **Backend e infraestrutura**. Verificar a regra no GitHub; o workflow sozinho não impede merge.
- Após um merge autorizado, comparar SHA da main, execução CI e versão publicada. Render deve esperar a aprovação do CI do commit integrado. Não testar uma falha artificial na main de produção.
- Conferir retenção de backup e realizar restauração em banco separado antes de dados reais. Não presumir que voltar uma imagem reverte migrações: alterações devem ser compatíveis com a versão anterior; restauração exige decisão explícita.

## Ambiente temporário Free

O proprietário escolheu Free para os testes iniciais. O banco gratuito expira após 30 dias; acompanhar a data no painel e migrar o plano antes de manter dados reais. O roteiro pago acima continua sendo a referência de produção.

No Web Service Free, deixar Pre-Deploy vazio e configurar Docker Command como `python scripts/start_render.py`. O script executa migrações e só inicia Gunicorn se elas passarem, respeitando PORT e substituindo o processo para receber sinais de parada. Usar uma única instância neste ambiente; ao evoluir para serviço pago, voltar ao Pre-Deploy e remover esse override. Não executar migrações no build.

As tentativas de 09/10/2026 com comandos compostos entre aspas falharam com status 127: a sequência inteira foi interpretada como um executável. O script evita depender dessa interpretação do painel. Ele precisa estar integrado na main antes de configurar o novo comando. Manter Auto-Deploy em After CI Checks Pass e /health/ como health check. Preencher os hosts exatos assim que o endereço do serviço estiver disponível.

## Limite da migração UUID

O primeiro banco de produção deve ser novo. `users.0002_user_uuid` interrompe se encontrar usuários ou sessões anteriores. Não apagar contas ou volumes para forçar a migração; um ambiente populado exige plano próprio de migração de dados. Criar o administrador somente depois das migrações.

## Referências oficiais consultadas em 09/10/2026

- https://render.com/docs/deploys
- https://render.com/docs/docker
- https://render.com/docs/deploy-django
- https://render.com/docs/health-checks
- https://render.com/docs/postgresql-creating-connecting

Este roteiro não comprova publicação, configuração de backup ou funcionamento remoto; essas verificações permanecem pendentes da ativação.
