# Stack Base

Ferramenta interativa de terminal para criação, detecção, validação e padronização de projetos de software.

O Stack Base é executado como uma CLI, mas abre uma TUI — Terminal User Interface — construída com Python e Textual.

```bash
stackbase
```

Durante o desenvolvimento, também pode ser executado diretamente:

```bash
python -m app.main
```

---

## Sumário

* [Visão geral](#visão-geral)
* [Objetivos](#objetivos)
* [Status atual](#status-atual)
* [Visão geral da arquitetura](#visão-geral-da-arquitetura)
* [Fluxos principais](#fluxos-principais)
* [Stack tecnológica](#stack-tecnológica)
* [Variáveis de ambiente](#variáveis-de-ambiente)
* [Estrutura de diretórios](#estrutura-de-diretórios)
* [Diretório de conteúdo](#diretório-de-conteúdo)
* [Módulos da aplicação](#módulos-da-aplicação)
* [Serviços, workflows e models](#serviços-workflows-e-models)
* [Detecção de projetos](#detecção-de-projetos)
* [Templates e presets](#templates-e-presets)
* [Execução local](#execução-local)
* [Testes](#testes)
* [Common hurdles](#common-hurdles)
* [Design patterns](#design-patterns)
* [Checklist pós-implementação](#checklist-pós-implementação)
* [Roadmap](#roadmap)
* [Licença](#licença)

---

# Visão geral

Criar um novo projeto geralmente exige repetir várias decisões e tarefas:

* definir uma estrutura de diretórios;
* escolher uma arquitetura;
* configurar build;
* adicionar testes;
* preparar Docker;
* criar documentação;
* adicionar persistência;
* definir configurações;
* validar padrões arquiteturais;
* identificar tecnologias em projetos existentes.

O Stack Base busca centralizar esse processo.

A ferramenta poderá trabalhar em dois modos principais:

## Criar novo projeto

O desenvolvedor seleciona características genéricas:

```text
Tipo de aplicação
Linguagem
Framework
Arquitetura
Capacidades
Diretório de saída
```

Exemplos de capacidades:

```text
API REST
SQL
NoSQL
Mensageria
Cache
Autenticação
Container
Testes
CI/CD
```

O Stack Base utiliza templates e presets versionados para gerar o projeto.

## Abrir projeto existente

O desenvolvedor informa um diretório e o Stack Base tenta detectar automaticamente:

```text
Linguagem
Framework
Build tool
Persistência
Provider de banco
Container
Testes
Arquitetura provável
```

Exemplo:

```text
Projeto: customer-api
Linguagem: Java 21
Framework: Spring Boot
Build tool: Maven
Persistência: SQL
Provider detectado: Oracle
Container: Docker
Testes: JUnit
```

---

# Objetivos

## Objetivo principal

Reduzir o trabalho repetitivo necessário para iniciar, analisar e padronizar projetos de software.

## Objetivos específicos

* fornecer uma TUI simples para desenvolvedores;
* criar projetos a partir de templates versionados;
* detectar tecnologias presentes em projetos existentes;
* separar capacidades genéricas de implementações específicas;
* validar convenções arquiteturais;
* gerar documentação inicial;
* reduzir inconsistências entre projetos;
* permitir presets por equipe ou organização;
* evoluir sem acoplar a ferramenta a uma única linguagem.

---

# Status atual

O projeto está em desenvolvimento.

## Implementado

* estrutura inicial do repositório;
* ambiente Python;
* aplicação Textual;
* tela inicial da TUI;
* tema visual carmesim;
* navegação por opções fixas;
* estrutura para telas;
* estrutura para generator;
* estrutura para validation;
* estrutura para workflows;
* estrutura para models;
* documentação inicial;
* diretório de templates;
* diretório de presets.

## Em desenvolvimento

* abertura de projeto existente;
* detecção de Java;
* detecção de Spring Boot;
* detecção de Maven e Gradle;
* detecção de SQL e NoSQL;
* detecção de providers de banco;
* diagnóstico visual na TUI;
* criação de projetos Java Spring;
* validação arquitetural.

## Ainda não implementado

* geração completa de projetos;
* gerenciamento de templates externos;
* plugins;
* marketplace de templates;
* IA conversacional;
* atualização automática;
* criação de múltiplos microservices;
* publicação automática em GitHub ou GitLab.

---

# Visão geral da arquitetura

O Stack Base segue uma arquitetura modular orientada por responsabilidades.

```text
TUI / CLI
   ↓
Workflow
   ↓
Validation / Generator
   ↓
Infrastructure
   ↓
File system, Git, templates e comandos externos
```

A interface não deve conter regras de negócio.

A camada de workflow coordena os casos de uso.

Os módulos de validation e generator executam as regras principais.

Infrastructure acessa sistema de arquivos, Git e comandos externos.

Models transportam dados entre os módulos.

---

## Arquitetura lógica

```text
┌──────────────────────────────────────────┐
│ UI / CLI                                 │
│ Textual screens, widgets e comandos      │
└───────────────────┬──────────────────────┘
                    │
┌───────────────────▼──────────────────────┐
│ Workflow                                 │
│ Coordenação dos casos de uso             │
└───────────────────┬──────────────────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
┌────────▼─────────┐  ┌────────▼─────────┐
│ Validation       │  │ Generator        │
│ Detectar/validar │  │ Gerar projetos   │
└────────┬─────────┘  └────────┬─────────┘
         │                     │
         └──────────┬──────────┘
                    │
┌───────────────────▼──────────────────────┐
│ Infrastructure                           │
│ Arquivos, Git, templates e processos     │
└──────────────────────────────────────────┘
```

---

## Princípios arquiteturais

* UI não acessa arquivos diretamente.
* Workflow não conhece detalhes visuais.
* Generator não detecta tecnologias.
* Validation não gera projetos.
* Infrastructure não decide regras de negócio.
* Models não dependem da interface.
* Templates permanecem fora do código da TUI.
* Capacidades genéricas são separadas de providers específicos.

Exemplo:

```text
Capacidade: SQL
Provider: Oracle
```

Outro exemplo:

```text
Capacidade: Container
Provider: Docker
```

---

# Fluxos principais

## Fluxo de abertura de projeto

```text
Usuário escolhe uma pasta
        ↓
ValidateScreen
        ↓
OpenProjectWorkflow
        ↓
ProjectDetector
        ↓
ProjectReader
        ↓
DetectedProject
        ↓
Resultado exibido na TUI
```

## Fluxo de validação

```text
DetectedProject
        ↓
ValidateProjectWorkflow
        ↓
ProjectValidator
        ↓
ValidationResult
        ↓
Avisos, erros e conformidades
```

## Fluxo de criação

```text
Usuário configura projeto
        ↓
CreateScreen
        ↓
ProjectConfig
        ↓
CreateProjectWorkflow
        ↓
TemplateLoader
        ↓
ProjectGenerator
        ↓
FileSystem
        ↓
Projeto criado
```

---

# Stack tecnológica

## Linguagem

```text
Python 3.13
```

## Interface de terminal

```text
Textual
```

Responsável por:

* TUI;
* navegação;
* screens;
* widgets;
* atalhos;
* layout;
* estilização com TCSS.

## Empacotamento

```text
setuptools
pyproject.toml
```

## Testes

Atualmente podem ser utilizados:

```text
unittest
Textual run_test
```

Dependências futuras opcionais:

```text
pytest
pytest-cov
```

## Templates

Implementação inicial prevista:

```text
pathlib
shutil
string.Template
```

Evolução possível:

```text
Jinja2
```

## Configuração

Inicialmente:

```text
JSON
```

Possíveis formatos futuros:

```text
YAML
TOML
```

## Sistema de arquivos

```text
pathlib
shutil
tempfile
```

## Execução de processos

```text
subprocess
```

## Git

Inicialmente por comandos controlados:

```text
git init
git status
git add
git commit
```

## Distribuição futura

Possíveis estratégias:

```text
PyInstaller
pipx
executável standalone
```

---

# Variáveis de ambiente

O Stack Base deve funcionar com configurações padrão mesmo sem variáveis de ambiente.

As variáveis abaixo fazem parte do contrato planejado do projeto.

## Aplicação

### `STACKBASE_ENV`

Define o ambiente de execução.

```env
STACKBASE_ENV=development
```

Valores:

```text
development
test
production
```

Padrão:

```text
development
```

---

### `STACKBASE_DEBUG`

Ativa informações adicionais de diagnóstico.

```env
STACKBASE_DEBUG=false
```

Valores:

```text
true
false
```

Padrão:

```text
false
```

---

### `STACKBASE_LOG_LEVEL`

Define o nível mínimo dos logs.

```env
STACKBASE_LOG_LEVEL=INFO
```

Valores esperados:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Padrão:

```text
INFO
```

---

## Diretórios

### `STACKBASE_HOME`

Diretório principal utilizado pela ferramenta.

```env
STACKBASE_HOME=C:\Users\usuario\.stackbase
```

Padrão:

```text
~/.stackbase
```

---

### `STACKBASE_TEMPLATE_DIR`

Diretório adicional de templates.

```env
STACKBASE_TEMPLATE_DIR=C:\stackbase\templates
```

Padrão:

```text
<repository>/templates
```

---

### `STACKBASE_PRESET_DIR`

Diretório adicional de presets.

```env
STACKBASE_PRESET_DIR=C:\stackbase\presets
```

Padrão:

```text
<repository>/presets
```

---

### `STACKBASE_OUTPUT_DIR`

Diretório padrão para projetos gerados.

```env
STACKBASE_OUTPUT_DIR=C:\Projects
```

Padrão:

```text
diretório atual
```

---

### `STACKBASE_CACHE_DIR`

Diretório de cache.

```env
STACKBASE_CACHE_DIR=C:\Users\usuario\.stackbase\cache
```

Padrão:

```text
~/.stackbase/cache
```

---

### `STACKBASE_LOG_DIR`

Diretório de logs.

```env
STACKBASE_LOG_DIR=C:\Users\usuario\.stackbase\logs
```

Padrão:

```text
~/.stackbase/logs
```

---

## Comportamento

### `STACKBASE_ALLOW_OVERWRITE`

Permite sobrescrever diretórios existentes.

```env
STACKBASE_ALLOW_OVERWRITE=false
```

Padrão:

```text
false
```

Recomendação:

Nunca habilitar automaticamente em produção.

---

### `STACKBASE_AUTO_GIT_INIT`

Inicializa Git após a geração.

```env
STACKBASE_AUTO_GIT_INIT=true
```

Padrão:

```text
false
```

---

### `STACKBASE_VALIDATE_AFTER_GENERATE`

Executa validações após gerar um projeto.

```env
STACKBASE_VALIDATE_AFTER_GENERATE=true
```

Padrão:

```text
true
```

---

### `STACKBASE_DEFAULT_LANGUAGE`

Define a linguagem padrão da tela de criação.

```env
STACKBASE_DEFAULT_LANGUAGE=java
```

Padrão:

```text
java
```

---

### `STACKBASE_DEFAULT_FRAMEWORK`

Define o framework padrão.

```env
STACKBASE_DEFAULT_FRAMEWORK=spring-boot
```

Padrão:

```text
spring-boot
```

---

### `STACKBASE_DEFAULT_ARCHITECTURE`

Define a arquitetura padrão.

```env
STACKBASE_DEFAULT_ARCHITECTURE=layered
```

Padrão:

```text
layered
```

---

## Integrações futuras

### `STACKBASE_GITHUB_TOKEN`

Token para criação ou publicação de repositórios.

```env
STACKBASE_GITHUB_TOKEN=
```

Não deve ser versionado.

---

### `STACKBASE_GITLAB_TOKEN`

Token para integração futura com GitLab.

```env
STACKBASE_GITLAB_TOKEN=
```

Não deve ser versionado.

---

## Exemplo de `.env.example`

```env
STACKBASE_ENV=development
STACKBASE_DEBUG=false
STACKBASE_LOG_LEVEL=INFO

STACKBASE_HOME=
STACKBASE_TEMPLATE_DIR=
STACKBASE_PRESET_DIR=
STACKBASE_OUTPUT_DIR=
STACKBASE_CACHE_DIR=
STACKBASE_LOG_DIR=

STACKBASE_ALLOW_OVERWRITE=false
STACKBASE_AUTO_GIT_INIT=false
STACKBASE_VALIDATE_AFTER_GENERATE=true

STACKBASE_DEFAULT_LANGUAGE=java
STACKBASE_DEFAULT_FRAMEWORK=spring-boot
STACKBASE_DEFAULT_ARCHITECTURE=layered

STACKBASE_GITHUB_TOKEN=
STACKBASE_GITLAB_TOKEN=
```

O arquivo `.env` não deve ser enviado ao repositório.

---

# Estrutura de diretórios

```text
stack-base/
├── app/
│   ├── cli/
│   │   ├── app.py
│   │   └── __init__.py
│   │
│   ├── configuration/
│   │   └── __init__.py
│   │
│   ├── generator/
│   │   └── __init__.py
│   │
│   ├── infrastructure/
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── project_config.py
│   │   └── __init__.py
│   │
│   ├── ui/
│   │   ├── screens/
│   │   │   ├── widgets/
│   │   │   │   ├── command_input.py
│   │   │   │   ├── project_preview.py
│   │   │   │   ├── sidebar.py
│   │   │   │   └── __init__.py
│   │   │   │
│   │   │   ├── about_screen.py
│   │   │   ├── create_screen.py
│   │   │   ├── home_screen.py
│   │   │   ├── templates_screen.py
│   │   │   ├── validate_screen.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── application.py
│   │   ├── console.py
│   │   ├── stack_base.tcss
│   │   └── __init__.py
│   │
│   ├── validation/
│   │   └── __init__.py
│   │
│   ├── workflow/
│   │   └── __init__.py
│   │
│   ├── main.py
│   └── __init__.py
│
├── docs/
│   ├── architecture.md
│   ├── commands.md
│   └── templates.md
│
├── presets/
│
├── templates/
│   └── java-spring/
│
├── tests/
│   ├── integration/
│   │   ├── test_cli.py
│   │   └── test_create_project.py
│   │
│   ├── unit/
│   │   ├── test_project_generator.py
│   │   ├── test_project_validator.py
│   │   └── test_template_loader.py
│   │
│   └── __init__.py
│
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

---

# Diretório de conteúdo

O Stack Base utiliza dois diretórios principais de conteúdo:

```text
templates/
presets/
```

## Templates

Um template contém a estrutura física que será gerada.

```text
templates/
└── java-spring/
    ├── template.json
    ├── skeleton/
    │   ├── src/
    │   ├── README.md.template
    │   ├── pom.xml.template
    │   └── .gitignore.template
    └── assets/
```

### `template.json`

Exemplo planejado:

```json
{
  "id": "java-spring-layered",
  "name": "Java Spring Layered",
  "language": "java",
  "framework": "spring-boot",
  "architecture": "layered",
  "version": "1.0.0",
  "capabilities": [
    "rest-api",
    "sql",
    "testing"
  ]
}
```

### `skeleton`

Contém pastas e arquivos do projeto gerado.

### `assets`

Contém arquivos auxiliares que não precisam de renderização.

---

## Presets

Um preset reúne decisões pré-configuradas.

```text
presets/
├── spring-api.json
├── spring-service.json
└── spring-sql-service.json
```

Exemplo:

```json
{
  "id": "spring-sql-service",
  "language": "java",
  "framework": "spring-boot",
  "architecture": "layered",
  "capabilities": [
    "rest-api",
    "sql",
    "testing",
    "container"
  ]
}
```

O preset não deve conter credenciais ou informações sensíveis.

---

# Módulos da aplicação

## `app/cli`

Responsável por comandos diretos.

Exemplos futuros:

```bash
stackbase
stackbase create
stackbase validate .
stackbase templates
```

O comando sem argumentos abre a TUI.

---

## `app/configuration`

Responsável por:

* variáveis de ambiente;
* configurações padrão;
* caminhos;
* nomes de arquivos;
* flags;
* limites;
* comportamento global.

Arquivos previstos:

```text
settings.py
constants.py
environment.py
```

---

## `app/generator`

Responsável por:

* carregar templates;
* renderizar arquivos;
* criar diretórios;
* gerar configurações;
* copiar assets;
* impedir sobrescritas acidentais.

Serviços previstos:

```text
ProjectGenerator
TemplateLoader
TemplateRenderer
```

---

## `app/infrastructure`

Responsável por acesso técnico externo:

* leitura de arquivos;
* escrita de arquivos;
* execução de processos;
* Git;
* cache;
* logs;
* sistema operacional.

Serviços previstos:

```text
FileSystem
ProjectReader
CommandRunner
GitService
```

---

## `app/models`

Responsável pelos modelos de transporte e domínio.

Models previstos:

```text
ProjectConfig
DetectedProject
Technology
DetectionResult
ValidationResult
GenerationResult
TemplateDefinition
PresetDefinition
```

---

## `app/ui`

Responsável exclusivamente pela interface Textual.

Não deve conter regras de geração, detecção ou validação.

---

## `app/validation`

Responsável por:

* identificar tecnologias;
* validar estrutura;
* validar arquivos;
* verificar convenções;
* identificar riscos;
* gerar avisos.

Serviços previstos:

```text
ProjectDetector
ProjectValidator
DetectionRules
ValidationRules
```

---

## `app/workflow`

Responsável por coordenar casos de uso.

Workflows previstos:

```text
OpenProjectWorkflow
CreateProjectWorkflow
ValidateProjectWorkflow
ListTemplatesWorkflow
```

---

# Serviços, workflows e models

## Serviços

### `ProjectGenerator`

Recebe um `ProjectConfig` validado e gera o projeto.

Entradas:

```text
ProjectConfig
TemplateDefinition
Output path
```

Saída:

```text
GenerationResult
```

---

### `TemplateLoader`

Localiza e carrega templates.

Responsabilidades:

* encontrar template;
* validar manifesto;
* ler arquivos;
* carregar metadata.

---

### `TemplateRenderer`

Substitui variáveis em arquivos de template.

Exemplo:

```text
{{ project_name }}
{{ package_name }}
{{ java_version }}
```

---

### `ProjectReader`

Lê arquivos e diretórios de um projeto existente.

Não interpreta o conteúdo como regra de negócio.

---

### `ProjectDetector`

Analisa evidências e identifica tecnologias.

Exemplos:

```text
pom.xml → Maven
build.gradle → Gradle
@SpringBootApplication → Spring Boot
spring-data-jpa → SQL
ojdbc → Oracle
```

---

### `ProjectValidator`

Aplica regras após a detecção.

Exemplos:

```text
src/main/java existe
src/test/java existe
README existe
configuração sensível foi versionada
controller acessa repository diretamente
```

---

### `FileSystem`

Abstrai operações de arquivos.

Responsabilidades:

* criar diretório;
* escrever arquivo;
* copiar arquivo;
* verificar existência;
* remover conteúdo temporário.

---

### `CommandRunner`

Executa comandos externos de maneira controlada.

Exemplos futuros:

```text
git
mvn
gradle
docker
```

---

### `GitService`

Responsável por operações Git.

Exemplos:

```text
git init
git status
git add
```

---

## Workflows

### `OpenProjectWorkflow`

```text
Receber caminho
Validar caminho
Executar detector
Retornar DetectedProject
```

---

### `CreateProjectWorkflow`

```text
Receber ProjectConfig
Validar configuração
Carregar template
Gerar projeto
Executar validação pós-geração
Retornar GenerationResult
```

---

### `ValidateProjectWorkflow`

```text
Receber projeto detectado
Executar regras
Classificar problemas
Retornar ValidationResult
```

---

### `ListTemplatesWorkflow`

```text
Localizar templates
Validar manifestos
Retornar catálogo
```

---

## Models

### `ProjectConfig`

Representa as escolhas para um projeto novo.

Campos previstos:

```text
name
project_type
language
framework
architecture
capabilities
output_path
initialize_git
```

---

### `DetectedProject`

Representa um projeto existente analisado.

Campos previstos:

```text
root_path
name
languages
frameworks
build_tools
capabilities
providers
detected_files
warnings
```

---

### `Technology`

Representa uma tecnologia encontrada.

Campos:

```text
category
name
version
confidence
```

---

### `ValidationResult`

Campos previstos:

```text
is_valid
errors
warnings
successes
score
```

---

### `GenerationResult`

Campos previstos:

```text
success
project_path
generated_files
warnings
errors
```

---

### `TemplateDefinition`

Campos previstos:

```text
id
name
version
language
framework
architecture
capabilities
template_path
```

---

# Detecção de projetos

O detector deve trabalhar por evidências.

## Java

Indicadores:

```text
src/main/java
arquivos .java
pom.xml
build.gradle
build.gradle.kts
```

## Spring Boot

Indicadores:

```text
spring-boot-starter
spring-boot-maven-plugin
spring-boot-starter-parent
@SpringBootApplication
application.yml
application.properties
```

## SQL

Indicadores:

```text
spring-data-jpa
spring-jdbc
hibernate
jooq
spring.datasource
jdbc:
```

## Providers SQL

### PostgreSQL

```text
org.postgresql
postgresql
jdbc:postgresql
```

### Oracle

```text
com.oracle.database
ojdbc
jdbc:oracle
```

### MySQL

```text
com.mysql
mysql-connector
jdbc:mysql
```

### SQL Server

```text
com.microsoft.sqlserver
mssql-jdbc
jdbc:sqlserver
```

O provider é informação secundária.

O modelo principal deve continuar genérico:

```text
Persistência: SQL
Provider: Oracle
```

---

# Templates e presets

## Regras para templates

Todo template deve:

* possuir identificador único;
* possuir versão;
* declarar linguagem;
* declarar framework;
* declarar arquitetura;
* declarar capacidades;
* evitar credenciais;
* possuir README;
* possuir testes mínimos;
* possuir manifesto válido.

## Regras para presets

Todo preset deve:

* referenciar um template existente;
* utilizar apenas capacidades suportadas;
* possuir identificador único;
* não conter caminhos absolutos;
* não conter informações pessoais;
* não conter segredos.

---

# Execução local

## Criar ambiente virtual

Windows:

```powershell
py -m venv .venv
```

Ativação:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Executar aplicação

```powershell
python -m app.main
```

## Instalar Textual

Em ambiente autorizado:

```powershell
python -m pip install textual
```

## Executar testes

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

---

# Common hurdles

## 1. `src does not exist`

### Problema

```text
error in 'egg_base' option: 'src' does not exist
```

### Causa

O `pyproject.toml` foi configurado para layout `src`, mas o projeto usa o pacote `app` na raiz.

### Solução

Configurar:

```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]
```

---

## 2. `Unresolved reference 'app'`

### Causa

O PyCharm não reconheceu a raiz do projeto ou está usando um interpretador incorreto.

### Solução

* abrir o projeto pela pasta que contém `app`;
* marcar a raiz como `Sources Root`;
* conferir o interpretador `.venv`;
* executar comandos na raiz.

Import correto:

```python
from app.ui.application import StackBaseApp
```

---

## 3. Textual não encontrado

### Erro

```text
ModuleNotFoundError: No module named 'textual'
```

### Solução

Instalar o pacote em ambiente autorizado:

```powershell
python -m pip install textual
```

Confirmar o interpretador utilizado pelo PyCharm.

---

## 4. TCSS não aceita `@media`

### Erro

```text
Expected selector or end of file
```

### Causa

TCSS não é CSS de navegador e não suporta todas as regras CSS.

### Solução

Não utilizar:

```css
@media
```

Preferir layout fluido e medidas simples.

---

## 5. TUI desenhada várias vezes

### Causa

Atualizações manuais em eventos de resize ou reconstrução incorreta de widgets.

### Solução

* montar a tela apenas no `compose`;
* evitar reconstrução durante resize;
* usar widgets reativos;
* manter layout inicial simples.

---

## 6. Logo ASCII quebra o layout

### Causa

Logo maior que o terminal ou fonte incompatível.

### Solução

* usar logo compacta;
* evitar largura fixa excessiva;
* não depender de Nerd Fonts;
* utilizar somente caracteres ASCII compatíveis.

---

## 7. Ícones aparecem como quadrados

### Causa

Fonte do terminal não possui os glifos.

### Solução

Trocar símbolos especiais por caracteres comuns:

```text
+
-
>
*
#
```

---

## 8. `CliRunner` não funciona com Textual

### Causa

`CliRunner` pertence ao Typer e não testa aplicações Textual.

### Solução

Utilizar:

```python
async with app.run_test() as pilot:
    await pilot.press("q")
```

---

## 9. Testes não encontram módulos

### Causa

Os testes foram executados fora da raiz ou o projeto não está no path.

### Solução

Executar na raiz:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

---

## 10. `.venv` versionada por engano

### Problema

Arquivos do ambiente virtual aparecem no Git.

### Solução

Adicionar ao `.gitignore`:

```gitignore
.venv/
venv/
```

Caso já tenha sido adicionada:

```bash
git rm -r --cached .venv
```

---

## 11. `__pycache__` aparece no repositório

### Solução

Adicionar:

```gitignore
__pycache__/
*.py[cod]
```

Caso já esteja versionado:

```bash
git rm -r --cached app/**/__pycache__
```

---

## 12. Detector reconhece tecnologia incorreta

### Causa

Uma única evidência foi usada para concluir a stack.

### Solução

Utilizar múltiplas evidências e confidence score.

Exemplo:

```text
pom.xml encontrado
spring-boot-starter encontrado
@SpringBootApplication encontrada
```

Quanto mais evidências, maior a confiança.

---

# Design patterns

## 1. Layered Architecture

O projeto está dividido por responsabilidades:

```text
UI
Workflow
Validation / Generator
Infrastructure
Models
```

---

## 2. Model-View-Presenter adaptado

A TUI funciona como View.

Workflow e services preparam os dados exibidos.

A tela não executa regras diretamente.

---

## 3. Command Pattern

Ações da TUI e comandos CLI podem ser representados como comandos.

Exemplos:

```text
CreateProjectCommand
ValidateProjectCommand
OpenProjectCommand
```

---

## 4. Strategy Pattern

Diferentes estratégias podem detectar stacks distintas.

Exemplos futuros:

```text
JavaDetectionStrategy
PythonDetectionStrategy
NodeDetectionStrategy
```

---

## 5. Factory Pattern

Uma factory poderá selecionar o detector correto.

```text
ProjectDetectorFactory
```

Entrada:

```text
arquivos encontrados
```

Saída:

```text
detector adequado
```

---

## 6. Template Method

O fluxo de geração pode seguir etapas fixas:

```text
validar
preparar
renderizar
escrever
validar saída
```

Cada stack personaliza partes específicas.

---

## 7. Builder Pattern

Projetos complexos podem ser configurados progressivamente.

```text
ProjectConfigBuilder
```

Exemplo:

```python
builder.with_language("java")
builder.with_framework("spring-boot")
builder.with_capability("sql")
```

---

## 8. Repository Pattern

Templates e presets podem ser acessados por repositories.

```text
TemplateRepository
PresetRepository
```

A UI não precisa saber onde os arquivos estão armazenados.

---

## 9. Adapter Pattern

Integrações externas são encapsuladas.

Exemplos:

```text
GitAdapter
FileSystemAdapter
CommandRunnerAdapter
```

---

## 10. Facade Pattern

Workflows oferecem uma interface simplificada para operações complexas.

Exemplo:

```python
OpenProjectWorkflow.execute(path)
```

Internamente ele pode executar vários serviços.

---

## 11. Chain of Responsibility

A detecção pode executar vários detectores em sequência.

```text
Java detector
Spring detector
Persistence detector
Docker detector
Testing detector
```

Cada detector adiciona informações ao resultado.

---

## 12. Specification Pattern

Regras de validação podem ser encapsuladas.

Exemplos:

```text
HasReadmeSpecification
HasTestsSpecification
HasBuildFileSpecification
NoExposedSecretsSpecification
```

---

## 13. Result Object Pattern

Operações não devem retornar apenas `True` ou `False`.

Devem retornar objetos ricos:

```text
GenerationResult
ValidationResult
DetectionResult
```

Esses objetos carregam erros, avisos e dados.

---

## 14. Dependency Injection

Services devem receber suas dependências pelo construtor.

Exemplo:

```python
class OpenProjectWorkflow:
    def __init__(self, detector: ProjectDetector):
        self.detector = detector
```

Isso facilita testes e substituição de implementações.

---

# Checklist pós-implementação

## Arquitetura

* [ ] UI não contém regras de negócio.
* [ ] Workflows coordenam os casos de uso.
* [ ] Infrastructure está isolada.
* [ ] Generator não realiza detecção.
* [ ] Validation não gera arquivos.
* [ ] Models não dependem da UI.
* [ ] Não há dependências circulares.
* [ ] Serviços possuem responsabilidades claras.

## TUI

* [ ] Tela inicial abre sem erros.
* [ ] A interface não entra em loop.
* [ ] Navegação por setas funciona.
* [ ] Enter seleciona opções.
* [ ] Q encerra a aplicação.
* [ ] Esc retorna ou encerra corretamente.
* [ ] Layout funciona no terminal padrão.
* [ ] Não depende de Nerd Font.
* [ ] Tema carmesim está consistente.
* [ ] Mensagens de erro são legíveis.

## Detecção

* [ ] Pasta inexistente é tratada.
* [ ] Arquivo no lugar de pasta é tratado.
* [ ] Projeto vazio não é reconhecido.
* [ ] Java é detectado.
* [ ] Maven é detectado.
* [ ] Gradle é detectado.
* [ ] Spring Boot é detectado.
* [ ] SQL é detectado.
* [ ] NoSQL é detectado.
* [ ] Provider de banco é detectado separadamente.
* [ ] Docker é detectado.
* [ ] Testes são detectados.
* [ ] Confidence score é utilizado.
* [ ] Avisos são retornados ao usuário.

## Geração

* [ ] Nome do projeto é validado.
* [ ] Diretório de saída é validado.
* [ ] Diretório existente não é sobrescrito automaticamente.
* [ ] Template é encontrado.
* [ ] Manifesto é validado.
* [ ] Arquivos são renderizados.
* [ ] Diretórios são criados.
* [ ] README é gerado.
* [ ] `.gitignore` é gerado.
* [ ] Testes mínimos são gerados.
* [ ] Resultado da geração é retornado.
* [ ] Falhas deixam mensagens claras.
* [ ] Arquivos temporários são removidos.

## Segurança

* [ ] Nenhum token está no repositório.
* [ ] `.env` está ignorado.
* [ ] `.env.example` não possui segredos.
* [ ] Caminhos recebidos são validados.
* [ ] Comandos externos não concatenam entrada insegura.
* [ ] Sobrescrita exige confirmação.
* [ ] Logs não expõem credenciais.
* [ ] Templates não contêm informações privadas.

## Testes

* [ ] Models possuem testes.
* [ ] Detector possui testes.
* [ ] Validator possui testes.
* [ ] Generator possui testes.
* [ ] Template loader possui testes.
* [ ] Workflows possuem testes.
* [ ] TUI possui testes de navegação.
* [ ] Diretórios temporários são utilizados.
* [ ] Testes não dependem de projetos reais externos.
* [ ] Testes funcionam no Windows.
* [ ] Testes funcionam sem acesso à internet.

## Documentação

* [ ] README está atualizado.
* [ ] Arquitetura está documentada.
* [ ] Comandos estão documentados.
* [ ] Templates estão documentados.
* [ ] Variáveis de ambiente estão documentadas.
* [ ] Novos design patterns estão justificados.
* [ ] Limitações atuais estão descritas.
* [ ] Roadmap está atualizado.

## Git

* [ ] `.venv` não está versionada.
* [ ] `__pycache__` não está versionado.
* [ ] `.pyc` não está versionado.
* [ ] Logs não estão versionados.
* [ ] Arquivos temporários não estão versionados.
* [ ] Commits seguem um padrão consistente.
* [ ] Branch principal está atualizada.
* [ ] Alterações importantes possuem testes.

---

# Roadmap

## v0.1.0

* TUI inicial;
* tema visual;
* navegação;
* abertura de projeto existente;
* detecção de Java;
* detecção de Spring Boot;
* detecção de Maven e Gradle;
* detecção de SQL;
* diagnóstico básico.

## v0.2.0

* validação arquitetural;
* detecção de Docker;
* detecção de testes;
* detecção de providers;
* score do projeto;
* relatório visual.

## v0.3.0

* criação de projeto Java Spring;
* template em camadas;
* API REST;
* SQL opcional;
* testes;
* README;
* Docker opcional.

## v0.4.0

* presets;
* templates versionados;
* catálogo de templates;
* configuração do diretório de saída;
* validação pós-geração.

## v1.0.0

* CLI direta;
* TUI completa;
* criação e validação;
* templates extensíveis;
* documentação estável;
* distribuição em executável.

---

# Contribuição

Contribuições deverão seguir as regras abaixo:

* manter a arquitetura existente;
* não mover diretórios sem discussão;
* evitar dependências sem necessidade;
* adicionar testes;
* documentar novas variáveis;
* documentar novos templates;
* manter compatibilidade com Windows;
* não adicionar segredos;
* explicar novos padrões arquiteturais.

---

# Licença

Este projeto utiliza a licença MIT.

Consulte o arquivo:

```text
LICENSE
```

---

# Stack Base

```text
Detecte.
Crie.
Valide.
Padronize.
```
