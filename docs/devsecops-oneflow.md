# DevSecOps e Oneflow Datasus

Este documento registra o baseline de trabalho DevSecOps que o Stack Base deve apoiar ao gerar, validar e evoluir projetos. O objetivo é manter um fluxo simples, rastreável e compatível com automações de análise, validação e implantação.

## Estratégia de branches

A implementação do Oneflow assume três conjuntos de branches:

| Branch | Papel | Regra principal |
| --- | --- | --- |
| `main` | Versão de produção da aplicação. | Deve representar somente código aprovado para produção. |
| `develop` | Base de desenvolvimento e branch padrão para análise estática. | Recebe features por rebase e fast-forward merge. |
| `feat/<funcionalidade>` | Desenvolvimento de funcionalidades. | Deve partir de `develop` e voltar para `develop` após os gates. |

## Nomenclatura de branches de feature

Branches de feature devem usar o prefixo `feat/` seguido de uma string curta e descritiva da funcionalidade.

Exemplos:

```text
feat/tela-de-login
feat/cadastro-paciente
feat/devsecops-oneflow
```

## Nomenclatura de tags

As tags delimitam versões implantáveis, rastreiam artefatos e disparam pipelines para cada ambiente.

| Tipo | Padrão | Exemplo | Ambiente esperado |
| --- | --- | --- | --- |
| Feature | `dev-feat-<funcionalidade>-<N>` | `dev-feat-tela-de-login-1` | Validação de feature/local |
| Desenvolvimento | `dev-v<MAJOR>.<MINOR>.<PATCH>` | `dev-v1.2.0` | Desenvolvimento |
| Candidata a release | `hmg-v<MAJOR>.<MINOR>.<PATCH>-rc<N>` | `hmg-v1.2.0-rc1` | Homologação |
| Produção | `v<MAJOR>.<MINOR>.<PATCH>` | `v1.2.0` | Produção |

> Observação: a candidata a release deve usar o prefixo `hmg-v`, pois ela representa o pacote validado em homologação antes da promoção para produção.

## Estratégia de merge

A integração de features deve preservar uma árvore linear:

1. Criar a feature a partir de `develop`.
2. Implementar commits pequenos e rastreáveis.
3. Atualizar a feature com `git rebase develop` antes da integração.
4. Abrir Merge Request para `develop`.
5. Aprovar somente após todos os quality/security gates.
6. Integrar por fast-forward merge.

Comandos de referência:

```bash
git switch develop
git pull --ff-only
git switch -c feat/nome-da-funcionalidade
# implementar e commitar
git fetch origin
git rebase origin/develop
git switch develop
git merge --ff-only feat/nome-da-funcionalidade
```

## Quality e Security Gates

Os gates mínimos de integração contínua devem rodar em tempo de Merge Request:

| Gate | Objetivo | Exemplos de ferramentas |
| --- | --- | --- |
| Build e testes unitários | Garantir que a aplicação monta e que os testes passam. | Maven, Gradle, pytest, npm test |
| Análise estática e cobertura | Encontrar code smells, bugs e cobertura insuficiente. | SonarQube, coverage.py, JaCoCo |
| SAST e dependency scan | Identificar vulnerabilidades no código e nas dependências. | SonarQube, Trivy, scanners nativos do GitLab |
| IaC/container scan | Avaliar Dockerfiles, manifests e imagens. | Trivy |
| Code review | Validar arquitetura, legibilidade e aderência ao padrão do time. | Merge Request approval |
| DAST | Avaliar a aplicação implantada em ambiente controlado. | OWASP ZAP |

Merge Requests só devem ser aprovados quando os gates obrigatórios estiverem com parecer favorável ou quando uma exceção estiver formalmente registrada.

## Rastreabilidade de artefatos e deploy

A regra geral para artefatos é:

```text
A tag Git aplicada ao repositório deve ser idêntica à tag da imagem de container implantada.
```

Mapeamento esperado:

| Tag Git | Ação esperada |
| --- | --- |
| `dev-feat-*` | Gerar artefato para validação de feature. |
| `dev-v*` | Gerar e implantar artefato em desenvolvimento. |
| `hmg-v*-rc*` | Gerar e implantar candidata a release em homologação. |
| `v*` | Promover para produção o mesmo commit aprovado em homologação. |

## Como o Stack Base deve apoiar esse fluxo

O Stack Base passa a tratar DevSecOps como uma capacidade transversal:

- documentar o fluxo Oneflow no projeto gerado;
- gerar um baseline de pipeline com estágios de validação, testes, segurança e empacotamento;
- manter branch/tag naming explícitos na TUI;
- orientar que novas features sejam criadas em branches `feat/<funcionalidade>`;
- preparar o projeto para ferramentas como GitLab, SonarQube, Trivy e OWASP ZAP sem acoplar a TUI a um único provedor.
