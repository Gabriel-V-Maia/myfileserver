# myfileserver
Repositório para um sistema que criei para um servidor dedicado a armazenamento!!
Ele não é feito pra servidores de produção ou algo do tipo, ele é mais uma ferramenta pessoal mesmo.

# !! BRANCH DEV !!
Você está vendo arquivos da branch dev, onde eu uso para fazer testes antes de tacar na branch principal.
Logo tudo é experimental, e não é garantido que rode, pois eu faço os commits como eu acho que deve ser feito.



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

# Licença

MIT


