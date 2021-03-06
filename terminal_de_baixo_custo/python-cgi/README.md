# Instruções para inicializar o webserver na placa Intel Galileo Gen2

## Para a configuração da placa Intel Galileo Gen2:

As especificações da placa podem ser encontradas [aqui](https://ark.intel.com/pt-br/products/83137/Intel-Galileo-Gen-2-Board).

Primeiro precisamos bootar o sistema com cartão micro SD. Segue as [instruções](https://software.intel.com/en-us/get-started-galileo-linux-step1).

### Acessar a placa via SSH
Após ter feito isto, conecta o cabo de energia na placa. Ao mesmo tempo, conecta a porta de ethernet do roteador de casa com a porta de ethernet da placa como mostrado na figura abaixo:

![Alt text](../readme_img/img1.jpg?raw=true "Optional Title")

##### Configurando para DHCP
O sistema operacional Linux Yocto que vem no cartão micro SD tem como default funcionando com DHCP, por isso provavelmente se olharmos na página de configuração do roteador vamos encontrar um dispositivo chamado galileo com o seu respectivo endereço ip. Guarde esse endereço ip, podemos acessar remotamente a placa com o comando shell:

`ssh <usuário>@<endereço ip>`

A placa já vem com o usuário ‘root’ como default. A porta default de telnet/SSH é 22, se configuramos esta porta para outro número precisamos adicionar argumento -p <numero de porta> para especificar a porta.

##### Configuração de IP estático (recomendado)
Se o sistema não vier com DHCP configurado, podemos configurar ip estática. Para isso precisamos conectar um cabo USB para microUSB na placa e no computador pessoal. Precisamos baixar o IDE do arduino:
https://www.arduino.cc/en/Main/Software

Depois da instalação do IDE.
Abre o IDE, entra menu **tools->board->board manager**, instale o suporte para seguinte placa:

![Alt text](../readme_img/im2.png?raw=true "Optional Title")

Após ter feito isso, vamos selecionar no **menu tools->board-> Intel Galileo Gen 2**
Seleciona também a porta usb que está conectado com a placa:
**tools->ports**.
Podemos escrever um script em sketch e fazer upload para a placa configurando o endereço ip estático da placa:

![Alt text](../readme_img/img3.png?raw=true "Optional Title")

Para compilar o script clique **‘verify’**, submetendo na placa Galileo **‘upload’**. As informações do pacote ifconfig de linux pode ser encontrado [aqui](https://linux.die.net/man/8/ifconfig).

Se o endereço ip estiver configurado corretamente. Podemos usar o mesmo comando de ssh para conectar na placa remotamente.

![Alt text](../readme_img/im4.png?raw=true "Optional Title")

##### Configuração da placa Wi-fi
Podemos também conectar o nosso terminal a uma rede WiFi local desde que tenhamos disponível um módulo de placa WiFi. Basta seguir o [tutorial](https://software.intel.com/en-us/blogs/2014/04/25/wireless-galileo-on-yocto-linux-iot-devkit-image).

## Fazer upload dos arquivos do terminal na placa
Não recomendo usar o usuário root para as operações da placa, portanto vamos criar um novo usuário. Vamos utilizar SSH para entrar na placa. A criação do novo usuário pode ser consultada [aqui](https://www.tecmint.com/add-users-in-linux/). Após ter configurado isto é só usar SSH para conectar no terminal.

Agora podemos utilizar o comando

`ssh <novo usuario>@<ip>` para conectar a placa com o usuário adequado.

Podemos fazer upload dos arquivos com [filezilla](https://filezilla-project.org/) ou sftp.

## Instalação das dependências que faltam na placa

Agora precisamos instalar as dependências que faltam na placa para funcionar corretamente o terminal:
Primeira biblioteca que precisamos instalar é o **[blockcypher](https://github.com/blockcypher/blockcypher-python)**.

Utilize o comando `pip install block cypher` para instalar blockcypher.

Utilizamos também a biblioteca **[pybitcointools](https://github.com/vbuterin/pybitcointools)** no nosso terminal.

Entre no diretório **terminal_de_baixo_custo/python-cgi** e usa:

`python setup.py install` para instalar as pacotes de bitcoin do python

Utilizar **pip** para instalar **python-requests**:

`pip install requests`

## Inicialização de banco de dados sqlite3
Se o terminar não vier com **sqlite3**, instale com `opkg install sqlite3`.
Criar o banco de dados para o nosso site com comando no diretório **terminal_de_baixo_custo/sqlite**:

`sqlite3 server.db`

Após isto, vamos rodar o script que inicializa o banco de dados com as tabelas:

`python insertTable.py`

A seguir podemos inicializar o nosso servidor com o comando 

`python -m CGIHTTPServer <numero da porta>`

Podemos acessar este servidor com quaisquer dispositivos conectados na mesma rede do Intel Galileo 2 via URL:

http://\<ip do terminal\>:\<numero da porta\>/cgi-bin/index.py

A seguinte página aparecerá:

![Alt text](../readme_img/im5.png?raw=true "Optional Title")

## Colocar o servidor para funcionar na inicialização da placa
Para colocar o servidor já funciona na inicialização. Podemos criar um shell script com os comandos necessários para inicializar o servidor, conforme o [link](https://stackoverflow.com/questions/12973777/how-to-run-a-shell-script-at-startup).


