# myfileserver
Repositório para um sistema que criei para um servidor dedicado a armazenamento!!
Ele não é feito pra servidores de produção ou algo do tipo, ele é mais uma ferramenta pessoal mesmo.

# Setup
Para avisar, eu APENAS testei isso no UBUNTU SERVER, nenhuma outra distro foi testada.
Você precisa baixar o pyinstaller se ainda não tiver ele

```bash
pip install pyinstaller
```

Então rode um dos scripts de instalação, ``install.bat`` se tiver no windows ou ``install.sh`` no linux.

# Uso
Existem 2 comandos por enquanto, sendo eles ``pull`` e ``send``, onde send tem um alias "``push``".

Os dois são auto-explicativos, eles conseguem mandar arquivos e puxar arquivos do servidor.

```python
push <arquivo1 arquivo2>
push teste.zip teste.txt
```

```python
pull <arquivo1 arquivo2>
pull teste.zip teste.txt
```
