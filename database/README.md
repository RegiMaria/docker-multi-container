# Database Service

## O que é

Serviço responsável por armazenar e persistir as mensagens do quadro de mensagens da aplicação.
Usa PostgreSQL rodando em container, com dados criados automaticamente na primeira inicialização.

## Tecnologia

- PostgreSQL 14 (Alpine)

## Decisões que tomei

### Por que Postgres 14?

Optei por fixar uma versão específica (14) em vez de usar `latest`, para garantir builds
reproduzíveis - com `latest`, a versão do Postgres poderia mudar sem eu perceber,
quebrando o comportamento esperado.

### Por que a variante Alpine?

Alpine é uma distribuição Linux minimalista (cerca de 5MB), construída com musl libc e BusyBox.
Usá-la como base reduz bastante o tamanho final da imagem comparado a distribuições como 
Debian/Ubuntu - na prática, o mesmo pacote instalado pode ocupar até 4x menos espaço.
O trade-off é que, por ser mais enxuta, às vezes faltam ferramentas presentes em distribuições maiores
(por exemplo, vi um warning de "locale not found" nos logs, que não afeta o funcionamento,
mas é consequência direta dessa escolha).

### Por que não usei multi-stage build aqui?

Multi-stage build existe pra separar uma etapa de "construção"
(com ferramentas pesadas, dependências de desenvolvimento)
de uma etapa final enxuta. Nesse serviço não há nenhum código 
sendo compilado ou buildado - a imagem oficial do Postgres já
vem pronta e otimizada, e eu só adiciono um script de inicialização.
Como não existe fase de build, multi-stage não traria nenhum ganho aqui.

## Como funciona a inicialização

O `init.sql` é copiado para `/docker-entrypoint-initdb.d/` dentro da imagem.
A imagem oficial do Postgres tem um mecanismo interno que executa
automaticamente qualquer arquivo `.sql` encontrado nessa pasta, mas 
**apenas na primeira vez** que o container sobe com um volume de dados vazio. 
É assim que a tabela `messages` é criada e populada com dados de exemplo sem intervenção manual.

## Segurança

Esse serviço não expõe nenhuma porta para fora da máquina host (sem `ports:` no compose). 
Apenas containers na mesma rede Docker interna (o `backend`) conseguem se conectar a ele. 
Isso reduz a superfície de ataque, já que o banco de dados nunca fica acessível diretamente
pela internet ou pela máquina local.

## Como testar isolado

\`\`\`bash
docker build -t meu-database ./database
docker run -d --name teste-db -p 5433:5432 meu-database
docker logs teste-db
\`\`\`

Se tudo estiver correto, os logs devem mostrar `CREATE TABLE` e `INSERT 0 2`,
confirmando que o script de inicialização rodou com sucesso.