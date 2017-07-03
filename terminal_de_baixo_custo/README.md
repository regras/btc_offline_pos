# Uso dos diretórios

### blockcypher-python-master
Este diretório contém a biblioteca de blockcypher que precisa ser instalado na máquina para rodar o servidor web. Para ver as detalhes de instalação e de uso entra no diretório.

### sqlite
Este diretório contém um script **insertTable.py** para inicializar tabelas de banco de dados que vão ser utilizadas pelo terminal. Para inicializar as tabelas, entra no diretório sqlite e usa o comando:

`python insertTable.py`

### password
Este diretório contém senha administrativa(hashed) e frase do dia que podem ser alterados na página de configuração do terminal.

### python-cgi
Este diretório contém a biblioteca **pybitcointools** que vai ser utilizada no terminal. Além disso, todos os recursos de website ficam neste diretório. Destacamos:

- python-cgi/cgi-bin/: diretório que contém o script que vai construir a página web do terminal
- python-cgi/images/: imagens que vão ser utilizadas no site
- python-cgi/bitcoin/ : biblioteca pybitcointools
- python-cgi/css/ : diretório que contém os arquivos que mudam estilo e visual do site
- python-cgi/js/: diretório que contém os scripts de javascripts e jquery necessários para as ações e renderizações do site. Aqui destacamos arquivo **server.js** que faz o cálculo do preço total que deve ser pago pelo cliente
- python-cgi/fonts/: diretório que contém ícones de bootstrap
