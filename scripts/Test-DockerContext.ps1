# Testa o filtro real do Docker com arquivos ficticios, sem ler segredos locais.
param([string]$IgnoreFile = (Join-Path (Split-Path -Parent $PSScriptRoot) '.dockerignore'))
$ErrorActionPreference = 'Stop'
$temporaryRoot = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
$auditRoot = Join-Path $temporaryRoot ('foveli-context-' + [guid]::NewGuid().ToString('N'))
$contextRoot = Join-Path $auditRoot 'context'
$outputRoot = Join-Path $auditRoot 'output'
$canaries = @(
    'private.pem', 'private.key', 'backup.dump', '.env', '.env.production',
    'nested/private.pem', 'nested/private.key', 'nested/backup.dump',
    'nested/.env', 'nested/.env.production', '.aws/credentials',
    '.codex/session.json', 'nested/.aws/credentials', 'data.sqlite3-journal'
)
try {
    New-Item -ItemType Directory -Path $contextRoot -Force | Out-Null
    Copy-Item -LiteralPath $IgnoreFile -Destination (Join-Path $contextRoot '.dockerignore')
    [IO.File]::WriteAllText((Join-Path $contextRoot 'Dockerfile'), "FROM scratch`nCOPY . /context/`n")
    [IO.File]::WriteAllText((Join-Path $contextRoot 'application.py'), '# source must be included')
    foreach ($relativePath in $canaries) {
        $canaryPath = Join-Path $contextRoot $relativePath
        New-Item -ItemType Directory -Path (Split-Path -Parent $canaryPath) -Force | Out-Null
        [IO.File]::WriteAllText($canaryPath, 'NOT A SECRET - regression fixture')
    }
    docker build --quiet --output "type=local,dest=$outputRoot" $contextRoot
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao construir contexto de teste.' }
    $copiedRoot = Join-Path $outputRoot 'context'
    if (-not (Test-Path -LiteralPath (Join-Path $copiedRoot 'application.py'))) {
        throw 'Controle positivo falhou: codigo da aplicacao nao foi copiado.'
    }
    foreach ($relativePath in $canaries) {
        if (Test-Path -LiteralPath (Join-Path $copiedRoot $relativePath)) {
            throw "Arquivo excluido entrou no contexto: $relativePath"
        }
    }
    Write-Output "OK: $($canaries.Count) arquivos ficticios excluidos; codigo preservado."
} finally {
    # Nunca remover um caminho calculado sem verificar sua localizacao absoluta.
    $resolvedAuditRoot = [IO.Path]::GetFullPath($auditRoot)
    $allowedPrefix = $temporaryRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if (-not $resolvedAuditRoot.StartsWith($allowedPrefix, [StringComparison]::OrdinalIgnoreCase) -or
        -not ([IO.Path]::GetFileName($resolvedAuditRoot)).StartsWith('foveli-context-')) {
        throw 'Caminho temporario fora do limite permitido; limpeza interrompida.'
    }
    if (Test-Path -LiteralPath $resolvedAuditRoot) {
        Remove-Item -LiteralPath $resolvedAuditRoot -Recurse -Force
    }
}
