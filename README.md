# myfileserver
Repositório para um sistema que criei para um servidor dedicado a armazenamento!!
Ele não é feito pra servidores de produção ou algo do tipo, ele é mais uma ferramenta pessoal mesmo.

# Setup
Clone o repositório onde quiser, vai ter arquivos para a desinstalação e instalação, arquivos .ps1 são feitos para windows enquanto .sh para sistemas linux.

Para utilizar um dos arquivos powershell, utilize o comando:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
-- OU --
powershell -ExecutionPolicy Bypass -File .\uninstall.ps1
```

Saiba que você pode e deve modificar o código para seus casos de uso!!

# Comandos

```python
push <arquivo1 arquivo2>
push teste.zip teste.txt
```

```python
pull <arquivo1 arquivo2>
pull teste.zip teste.txt
```

```python
server
```

# Funcionamento

Eu fiz um protocolo simples para enviar os pacotes

```
+--------------------------------------------------------------+
| HEADER BLOCK                                                 |
+--------------------------------------------------------------+
| FIELD         | DESCRIPTION                                  |
+---------------+----------------------------------------------+
| CMD           | Comando: 'push' ou 'pull'                   |
| COUNT         | Número de arquivos sendo enviados/solicitados |
| DIR           | Nome da pasta de destino (push) ou origem (pull) |
| ENDHDR        | Delimitador de fim de header ('ENDHDR')     |
+--------------------------------------------------------------+
```

CMD: define a operação (push/send ou pull).

COUNT: número total de arquivos que serão enviados ou recebidos.

DIR: pasta alvo ou origem.

ENDHDR: marca o fim do bloco de header.

Exemplo de funcionamento:

```
┌───────────────────────────────┐
│         CLIENTE               │
└──────────────┬────────────────┘
               │
               ▼
      ┌──────────────────────────┐
      │ HEADER GLOBAL            │
      │ CMD=push/pull            │
      │ COUNT=2                  │
      │ DIR=Docs                 │
      │ ENDHDR                   │
      └──────────────┬───────────┘
                     │
                     ▼
         ┌─────────────────────┐
         │ HEADER ARQUIVO 1    │
         │ NAME=arquivo1.txt   │
         │ SIZE=123            │
         │ CHECK=<sha256>      │
         │ ENDHDR              │
         └─────────────┬───────┘
                       │
                       ▼
         ┌─────────────────────┐
         │ PAYLOAD ARQUIVO 1   │
         │ [conteúdo binário]  │
         └─────────────┬───────┘
                       │
                       ▼
         ┌─────────────────────┐
         │ RESPOSTA SERVIDOR   │
         │ STATUS=ok           │
         │ ENDHDR              │
         └─────────────┬───────┘
                       │
                       ▼
         ┌─────────────────────┐
         │ HEADER ARQUIVO 2    │
         │ NAME=arquivo2.pdf   │
         │ SIZE=4567           │
         │ CHECK=<sha256>      │
         │ ENDHDR              │
         └─────────────┬───────┘
                       │
                       ▼
         ┌─────────────────────┐
         │ PAYLOAD ARQUIVO 2   │
         │ [conteúdo binário]  │
         └─────────────┬───────┘
                       │
                       ▼
         ┌─────────────────────┐
         │ RESPOSTA SERVIDOR   │
         │ STATUS=ok           │
         │ ENDHDR              │
         └─────────────┬───────┘
                       │
                       ▼
               ┌─────────────┐
               │ Cliente     │
               │ Conexão     │
               │ fechada     │
               └─────────────┘
```

```

[main.py] → InputManagement.start() ──┐
                                       │
                                       ▼
                            Loop de input do terminal
                                       │
                       Commands.execute(cmd)
                      /                   \
                 fileserver()          outros comandos
                     │
                     ▼
              FileServer(host, port, storage)
                     │
                     ▼
             Thread daemon: FileServer.start()
                     │
                     ▼
           TCP socket listening (0.0.0.0:6000)
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
     handle(conn1)               handle(conn2)
        │                         │
   _push / _pull             _push / _pull
```

# Licença

MIT


