#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import cgi, cgitb
import sqlite3 as lite
import sys
import bitcoin
import time
import datetime
import requests
import hashlib, uuid
import blockcypher
import re
import os
import Cookie
import random
#include javascript

#initialization of variables
blockCypherApiToken = "2422c50d3321416d97d2184cb76a2fed"
bitcoinAddress = ""
form = cgi.FieldStorage()
showAdminMenu = "false"
admin = form.getvalue('login')
transactionText = form.getvalue('transactiondata')

#Initialize cookie
#expiration = datetime.datetime.now() + datetime.timedelta(days=30)

#when cookie is not set set cookie
cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
if "HTTP_COOKIE" in os.environ and os.environ["HTTP_COOKIE"]:
	cookie_string=os.environ.get('HTTP_COOKIE')
	cookie = Cookie.SimpleCookie()
	cookie.load(cookie_string)
else:
	cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
	cookie["session"] = random.randint(0,1000000000)
	cookie["loginstatus"] = "false"
#cookie["session"] = random.randint(0,1000000000)
#cookie["session"]["domain"] = ".jayconrod.com"
#cookie["session"]["path"] = "/"

#connect to database
con = lite.connect('../sqlite/server.db')

with con:
	cur = con.cursor()
	cur.execute("SELECT * FROM Bitcoin_Adresses")
	firstElement = cur.fetchone()
	if firstElement == None:
		#ainda n foi criada uma chave publica, criar aqui chave publica
		valid_private_key = False
		while not valid_private_key:
			private_key = bitcoin.random_key()
			decoded_private_key = bitcoin.decode_privkey(private_key,'hex')
			valid_private_key = 0 < decoded_private_key < bitcoin.N
		pubKey = bitcoin.privkey_to_pubkey(private_key)
		compPub = bitcoin.compress(pubKey)
		testnetAddress = bitcoin.pubkey_to_address(compPub,111)
		#get current time
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%d-%m %H:%M:%S')
		bitcoinAddress = testnetAddress
		#add to data
		cur.execute("INSERT INTO Bitcoin_Adresses(private_address,display_address,time_added) values (?,?,?)",(private_key,testnetAddress,st))
	else:
		bitcoinAddress = firstElement[2]


def checkPassword(password):
	passwd_file = open('../password/password.txt','r')
	line = passwd_file.readline()
	passwd_file.close()
	#get salt and hashed_password
	salt = line[:32]
	hashed_password = line[32:]
	test_password = hashlib.sha512(password + salt).hexdigest()
	if(hashed_password == test_password):
		return "passed"
	else:
		return "failed"

def getCurrentTime():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%d-%m %H:%M:%S')
	return st

#verified 0 as no verified, 1 as verified locally by site, 2 as verified by bitcoin network
def includeJavascript():
	#include jquery in order to use javascript
	print '<script src="/js/jquery-3.1.1.min.js"></script>'
	print '<script src="/js/server.js"></script>'
	print '<script src="/js/qrcode.js"></script>'
	print '<script src="/js/qrcode.min.js"></script>'

def printHead():
	print '<head>'
	print '<meta charset="utf-8">'
	print '<title>Terminal de Bitcoin</title>'
	includeJavascript()
	print "        <link rel='stylesheet' type='text/css' href='/css/style.css' />" 
	print "        <link href='/css/bootstrap.min.css' rel='stylesheet'>           "
	print '</head>'
	#cookie
	#print cookie.output()
	#print "Cookie set with: " + cookie.output()
	#print "session = " + cookie["session"].value
	#print os.environ
	#print os.environ["HTTP_COOKIE"]


def printNavBar():
	print '<nav class="navbar navbar-default">'
	print '<div class="container-fluid">'
	print '<div class="navbar-header">'
	print '<div class="navbar-brand"><span class="glyphicon glyphicon-bitcoin"></span><a style="color:black;" href="index.py">New-dog</a>'
	print '</div></div>'
	#if(showAdminMenu == "true"):
	#print '<button type="button" class="btn btn-default navbar-btn">Item 1</button>'
	#print '<button type="button" class="btn btn-default navbar-btn">Item 2</button>'
	print '<ul class="nav navbar-nav navbar-right">'
	print '<form action="" method="post"><input type="hidden" name="admLoginTry" value="admLogin"><button type="submit" class="btn btn-default navbar-btn" value="Submit">Modo administrativo</button></form>'
	#print '<button type="button" class="btn btn-default navbar-btn">Modo administrativo</button>'
	print '</ul>'
	print '</div></nav>'


def printContent():
	print '<div class="row">'
	print '<h1 class="productTitle"><b>Bem-vindo à barraca New Dog!</b></h1>'
	print '<p><small><h1><center>Aceitamos bitcoins</center></h1></small></p>'
	print '</div>'
	print '<p><small><h1><center>Escolha os produtos e a quantidade de cada:</center></h1></small></p>'
	print '<div class="col-md-4 col-xs-4">'
	print '<div class="thumbnail">'
	print '<img class="img-fluid productImage" src="/images/hotdog.jpg" alt="carregando" height="300">'
	print '<div class="caption">'
	print '<h2><center>Cachorro Quente</center></h2>'
	print '<p><h3><center>Preco unitario: 0.001 BTC</center></h3></p>'
	#can modularize this part####
	print '<center><form class="form-inline">'
	print '<label for="hotdog">Quantidade:</label>'
	print '<select class="form-control" id="hotdog" ><option>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select>'
	print '</form></center>'
	############################
	print '</div>'
	print '</div>'
	print '</div>'
	#inserir segundo produto
	print '<div class="col-md-4 col-xs-4">'
	print '<div class="thumbnail">'
	print '<img class="img-fluid productImage" src="/images/pipoca.jpg" alt="carregando" height="300">'
	print '<div class="caption">'
	print '<h2><center>Pipoca doce</center></h2>'
	print '<p><h3><center>Preco unitario: 0.002 BTC</center></h3></p>'
	###########################
	print '<center><form class="form-inline">'
	print '<label for="pipoca">Quantidade:</label>'
	print '<select class="form-control" id="pipoca" ><option>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select>'
	print '</form></center>'
	###########################
	print '</div>'
	print '</div>'
	print '</div>'
	#inserir terceiro produto
	print '<div class="col-md-4 col-xs-4">'
	print '<div class="thumbnail">'
	print '<img class="img-fluid productImage" src="/images/pamonha.jpg" alt="carregando" height="300">'
	print '<div class="caption">'
	print '<h2><center>Pamonha recheada</center></h2>'
	print '<p><h3><center>Preco unitario: 0.001 BTC</center></h3></p>'
	############################
	print '<center><form class="form-inline">'
	print '<label for="pamonha">Quantidade:</label>'
	print '<select class="form-control" id="pamonha" ><option>0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select>'
	print '</form></center>'
	############################
	print '</div>'
	print '</div>'
	print '</div>'

def printAdvertisement():
	#Adicionar o valor de transacao aqui
	print '<div><h3 class="productAdvertise">Total de sua compra: <p class="label label-info" id="totalCost"></p></h3></div>'
	print '<h3 class="productAdvertise"><b>Clique na foto de algum produto ou copie o endereco Bitcoin a seguir:</b></h3>'
	#print <p class="alert alert-info">Aviso: copie este endereço Bitcoin e o valor da compra para sua wallet e faça a transação.</p></div>'

def	printBitcoinAddress(publicKey):
	print '<div class="well">'
	print "<p><h3><b id=\"pubKeyValue\">%s</b></h3></p>" % (publicKey)
	#aqui deve mostrar o QR code!
	#print "<input type=\"hidden\" value=\"%s\" id=\"pubkey\">" % (publicKey)
	#print '<div id="qrcode"></div>'
	print '</div>'

def responseForm():
	print '<div class="alert alert-danger"><h2><b>Copie a transação efetuada na sua wallet e cole aqui: </b></h2>'
	print '<form action="" method="post">'
	print '<div class="form-group">'
	print '<textarea class="form-control" rows="5" name="transactiondata"></textarea><br></div>'
	print '<button type="submit" class="btn btn-default" value="Submit">Enviar a transação!</button></form></div>'

def checkTransaction(transactiontext):
	try:
		transactiontext.strip()
		deserialized = bitcoin.deserialize(transactiontext)
		for item in deserialized['outs']:
			out = item['script']
			subString = out[6:len(out)-4]
			add = bitcoin.hex_to_b58check(subString,111)
			if add == bitcoinAddress:
				return True
		return False
	except:
		return False

def admLoginPart():
	print '<form class="form-inline" method="post">'
	print '<h2><div class="form-group">'
	print '<label for="loginstatement">Entre com a senha de administrador:</label>'
	print '<input type="password" class="form-control" name="adminPass" placeholder="Senha">'
	print '</div>'
	print '<input type="hidden" name="login" value="tryLogin">'
	print '<button type="submit" class="btn btn-default" value="Submit" >Enter</button>'
	print '</h2></form>'

def admSetNewPassForm():
	print '<div class="alert alert-info"><h3><b>Trocar senha: </b></h3>'
	print '<form action="" method="post" class="form-horizontal">'
	print '<div class="form-group">'
	print '<label class="col-xs-4 col-md-4 control-label">Digite a nova senha:</label>'
	print '<div class="col-xs-8 col-md-8"><input type="password" class="form-control" name="newPass"></div>'
	print '</div>'
	print '<div class="form-group">'
	print '<label class="col-xs-4 col-md-4 control-label">Repita a nova senha:</label>'
	print '<div class="col-xs-8 col-md-8"><input type="password" class="form-control" name="newPassConfirm"></div>'
	print '</div>'
	print '<div class="form-group">'
	print '<div class="col-xs-offset-4 col-md-offset-4 col-xs-8 col-md-8">'
	print '<button type="submit" class="btn btn-default">Trocar senha</button></div>'
	print '</div>'
	print '<input type="hidden" name="changePassword" value="changingpassword">'
	print '</form></div>'

def admSetParaphrase():
	print '<div class="alert alert-info"><h3><b>Configurar a frase do dia</b></h3>'
	phrase_file = open('../password/daily_phrase.txt','r')
	line = phrase_file.readline()
	phrase_file.close()
	print '<p>Frase do dia atual: <b>'
	print line
	print '</b></p>'
	print '<form class="form-inline" action="" method="post">'
  	print '<div class="form-group">'
   	print '<label for="daily">Frase do dia:</label>'
   	print '<input type="text" class="form-control" name="dailyPhrase" placeholder="Configurar a frase">'
  	print '</div>'
  	print '<button type="submit" class="btn btn-default">Configurar</button>'
  	print '<input type="hidden" name="changeDailyPhrase" value="changing">'
  	print '</form>'
	print '</div>'

def admSeeTransaction():
	print '<div class="alert alert-danger"><h3><b>Fazer upload das transações não carregadas:</b></h3>'
	print '<form action="" method="post">'
	#table with selectble entries
	print '<table class="table">'
	#header
	print '<tr>'
	print '<th></th>'
	print '<th>Horário</th>'
	print '<th>Valor</th>'
	print '<th>ID da transação</th>'
	print '</tr>'
	#content
	with con:
		cur = con.cursor()
		not_uploaded = ('FALSE',)
		cur.execute("SELECT * FROM Transaction_Info WHERE verified =?", not_uploaded)
		rows = cur.fetchall()
		for row in rows:
			value = ""
			transaction_info = row[1]
			transaction_date = row[3]


			#strange thing happens: there is always a char 0x80 here, I need remove it to correctly decode the transaction
			deserialized = transaction_info.decode('utf8').encode('ascii',errors='ignore')
			deserialized = bitcoin.deserialize(deserialized)
			#deserialized = bitcoin.deserialize(row[1])

			txinfo_hex = transaction_info.decode("hex")
			transaction_i = hashlib.sha256(txinfo_hex).digest()
			transaction_id = hashlib.sha256(transaction_i).digest()
			transaction_id = transaction_id[::-1].encode('hex_codec')

			for item in deserialized['outs']:
				out = item['script']
				subString = out[6:len(out)-4]
				endereco = bitcoin.hex_to_b58check(subString,111)
				if endereco == bitcoinAddress:
					value = item['value']/float(100000000)
					#value_btc = value/float(100000000)
			print '<tr>'
			print '<td>'
			#checkbox here
			print "<input type=\"checkbox\" name=\"%s\" value=\"on\" checked>" % (transaction_info)
			print '</td>'
			print '<td>'
			#time here
			print transaction_date
			print '</td>'
			print '<td>'
			#value
			print value
			print ' BTC'
			print '</td>'
			print '<td>'
			#transaction here
			print transaction_id
			print '</td>'
			print '</tr>'
	print '</table>'
	print '<input type="hidden" name="upload_tx" value="upload_tx">'
	print '<button type="submit" class="btn btn-default">Fazer upload das transações selecionadas</button>'
	print '</form>'
	#botao para submeter todas as transacoes
	print '<form action="" method="post"><input type="hidden" name="uploadAll" value="uploadAll"><button type="submit" class="btn btn-default" value="Submit">Fazer upload de todas as transações</button></form>'
	print '</div>'
	#botao para expandir transacoes carregadas
	print '<button class="btn btn-default" id="seetrans">Mostrar as transações carregadas</button>'
	print '<p></p>'
	#info das transacoes carregadas
	print '<div id="uploaded" style="display: none;" >'
	#search uploaded transactions
	print '<div class="alert alert-danger"><h3><b>Deletar as transações carregadas:</b></h3>'
	print '''<form onsubmit="return confirm('Voce tem certeza que quer deletar as transações?')" action="" method="post">'''
	#table with selectble entries
	print '<table class="table">'
	#header
	print '<tr>'
	print '<th></th>'
	print '<th>Horário</th>'
	print '<th>Valor</th>'
	print '<th>ID da transação</th>'
	print '</tr>'
	#content
	with con:
		cur = con.cursor()
		uploaded = ('TRUE',)
		cur.execute("SELECT * FROM Transaction_Info WHERE verified =?", uploaded)
		rows = cur.fetchall()
		for row in rows:
			value = ""
			transaction_info = row[1]
			transaction_date = row[3]


			#strange thing happens: there is always a char 0x80 here, I need remove it to correctly decode the transaction
			deserialized = transaction_info.decode('utf8').encode('ascii',errors='ignore')
			deserialized = bitcoin.deserialize(deserialized)
			#deserialized = bitcoin.deserialize(row[1])

			txinfo_hex = transaction_info.decode("hex")
			transaction_i = hashlib.sha256(txinfo_hex).digest()
			transaction_id = hashlib.sha256(transaction_i).digest()
			transaction_id = transaction_id[::-1].encode('hex_codec')

			for item in deserialized['outs']:
				out = item['script']
				subString = out[6:len(out)-4]
				endereco = bitcoin.hex_to_b58check(subString,111)
				if endereco == bitcoinAddress:
					value = item['value']/float(100000000)
					#value_btc = value/float(100000000)
			print '<tr>'
			print '<td>'
			#checkbox here
			print "<input type=\"checkbox\" name=\"%s\" value=\"on\">" % (transaction_info)
			print '</td>'
			print '<td>'
			#time here
			print transaction_date
			print '</td>'
			print '<td>'
			#value
			print value
			print ' BTC'
			print '</td>'
			print '<td>'
			#transaction here
			print transaction_id
			print '</td>'
			print '</tr>'
	print '</table>'
	print '<input type="hidden" name="delete_tx" value="delete_tx">'
	print '<button type="submit" class="btn btn-default">Deletar as transações selecionadas</button>'
	print '</form>'
	print '</div>'
	print '</div>'




print 'Content-Type: text/html'
print
print '<html>'
printHead()
print '<body>'
print '<div class="container-fluid">'
printNavBar()

if(admin != None):
	#check passwd
	passa = form.getvalue('adminPass')
	if (checkPassword(passa) == "passed"):
		#admin page
		admSetNewPassForm()
		admSetParaphrase()
		#see transactions here!	
		admSeeTransaction()
	else:
		#alert
		print '<div class="alert-info">'
		print '<h1>Senha errada!!</h1>'
		print '</div>'
		printContent()
		printAdvertisement()
		printBitcoinAddress(bitcoinAddress)
		print '<form action="" method="post"><input type="hidden" name="sendPage" value="sendPage"><button type="submit" class="btn btn-default" value="Submit">Próximo passo</button></form>'
		#responseForm()
		#admLoginPart()
elif form.getvalue('admLoginTry') != None:
	admLoginPart()
elif form.getvalue('delete_tx') != None:
	#delete selected transactions
	print '<div class="jumbotron">'
	print '<h1>Informações das transações</h1>'
	with con:
		cur = con.cursor()
		uploaded = ('TRUE',)
		cur.execute("SELECT * FROM Transaction_Info WHERE verified =?", uploaded)
		request_fetch_if_exist_prefix = 'https://api.blockcypher.com/v1/btc/test3/txs/'
		rows = cur.fetchall()
		for row in rows:
			transaction_info = row[1]
			transaction_info_hex = transaction_info.decode('hex')
			sha_tx = hashlib.sha256(transaction_info_hex).digest()
			sha_f = hashlib.sha256(sha_tx).digest()
			sha_f = sha_f[::-1].encode('hex_codec')
			#print sha_f
			#if form.getvalue(transaction_info):
			if form.getvalue(transaction_info):
				try:
					cur.execute("DELETE FROM Transaction_Info WHERE transaction_text = ?", (transaction_info,))	
					print "<p>A transação %s foi deletada com sucesso.</p>" % (sha_f)
						###################################################
						########Add code for change transactions status####
						###################################################

				except:
						#internet connection error
					print '<div class="alert alert-warning"><h3>Ocorreu um erro e não foi possível deletar transação.</h3></div>'
					break
	print '</div>'
	print '<form action="" method="get"><button type="submit" class="btn btn-default" value="Submit">Voltar</button></form>'
elif form.getvalue('uploadAll') != None:
	#upload all transaction
	print '<div class="jumbotron">'
	print '<h1>Informações das transações</h1>'
	with con:
		cur = con.cursor()
		not_uploaded = ('FALSE',)
		cur.execute("SELECT * FROM Transaction_Info WHERE verified =?", not_uploaded)
		request_fetch_if_exist_prefix = 'https://api.blockcypher.com/v1/btc/test3/txs/'
		rows = cur.fetchall()
		for row in rows:
			transaction_info = row[1]
			transaction_info_hex = transaction_info.decode('hex')
			sha_tx = hashlib.sha256(transaction_info_hex).digest()
			sha_f = hashlib.sha256(sha_tx).digest()
			sha_f = sha_f[::-1].encode('hex_codec')
			#print sha_f
			#if form.getvalue(transaction_info):
			try:
					#try to get raw trans
					#request_url = request_fetch_if_exist_prefix + sha_f
					#now we veryfy if that is already in network
					#r = requests.get(request_url)
				result = blockcypher.pushtx(transaction_info,coin_symbol='btc-testnet',api_key=blockCypherApiToken)
					#print r
				cur.execute("UPDATE Transaction_Info SET verified = ? WHERE transaction_text = ?",('TRUE',transaction_info,))	
				print "<p>A transação %s foi submetida com sucesso.</p>" % (sha_f)
					###################################################
					########Add code for change transactions status####
					###################################################

			except:
					#internet connection error
				print '<div class="alert alert-warning"><h3>Erro de conexão: por favor, verifique sua conexão com a Internet.</h3></div>'
				break
	print '</div>'
	print '<form action="" method="get"><button type="submit" class="btn btn-default" value="Submit">Voltar</button></form>'
elif form.getvalue('upload_tx') != None:
	#check for every entry the correspond value

	print '<div class="jumbotron">'
	print '<h1>Informação das transações</h1>'
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM Transaction_Info")
		request_fetch_if_exist_prefix = 'https://api.blockcypher.com/v1/btc/test3/txs/'
		rows = cur.fetchall()
		for row in rows:
			transaction_info = row[1]
			transaction_info_hex = transaction_info.decode('hex')
			sha_tx = hashlib.sha256(transaction_info_hex).digest()
			sha_f = hashlib.sha256(sha_tx).digest()
			sha_f = sha_f[::-1].encode('hex_codec')
			#print sha_f
			if form.getvalue(transaction_info):
				
				try:
					#try to get raw trans
					#request_url = request_fetch_if_exist_prefix + sha_f
					#now we veryfy if that is already in network
					#r = requests.get(request_url)
					result = blockcypher.pushtx(transaction_info,coin_symbol='btc-testnet',api_key=blockCypherApiToken)
					#print r
					cur.execute("UPDATE Transaction_Info SET verified = ? WHERE transaction_text = ?",('TRUE',transaction_info,))
					print "<p>A transação %s foi submetida com sucesso.</p>" % (sha_f)
					############################################
					########Add code for update transactions####
					############################################	
					#cur.execute("UPDATE Transaction_Info SET verified = ? WHERE transaction_text = ?",'TRUE',transaction_info)
				except:
					#internet connection error
					print '<div class="alert alert-warning"><h3>Erro de conexão: por favor, verifique sua conexão com a Internet.</h3></div>'
					break
	print '</div>'
	print '<form action="" method="get"><button type="submit" class="btn btn-default" value="Submit">Voltar</button></form>'

elif form.getvalue('changePassword') != None:
	#changePasswordStatusPage
	newPassword = form.getvalue('newPass')
	confirmNewPassword = form.getvalue('newPassConfirm')
	if newPassword != confirmNewPassword:
		print '<div class="jumbotron">'
		print '<h1>Por favor, entre com senhas iguais novamente.</h1>'
		print '</div>'
		print '<form action="" method="get"><button type="submit" class="btn btn-default" value="Submit">Voltar</button></form>'
	else:
		passwd_file = open('../password/password.txt','w')
		salt = uuid.uuid4().hex
		hashed_password = hashlib.sha512(newPassword + salt).hexdigest()
		passInfo = salt + hashed_password
		passwd_file.write(passInfo)
		passwd_file.close()
		print '<div class="jumbotron">'
		print '<h1>A senha foi trocada com sucesso.</h1>'
		print '</div>'
		print '<form action="" method="get"><button type="submit" class="btn btn-default" value="Submit">Voltar</button></form>'
elif form.getvalue('changeDailyPhrase') != None:
	#change daily phrase
	newPhrase = form.getvalue('dailyPhrase')
	newFile = open('../password/daily_phrase.txt','w')
	newFile.write(newPhrase)
	newFile.close()
	print '<div class="jumbotron">'
	print '<h1>A frase do dia foi modificada com sucesso.</h>'
	print '</div>'
	print '<form action="" method="get"><button type="submit" class="btn btn-default" value="Submit">Voltar</button></form>'
elif form.getvalue('hiddenCost') != None:
	hiddenValor = form.getvalue('hiddenCost')
	#to represent data in a right way
	bit_address = bitcoinAddress.decode('utf8').encode('ascii',errors='ignore')
	print "<div><h3 class=\"productAdvertise\">Abra sua wallet, cole o endereço: <br><br><mark>%s </mark> <br><br> e digite o valor a ser pago: <br><br><mark>%s BTC</mark> <br><br> Copie a transação de sua wallet e cole-a no campo abaixo:</h3></div> " % (bit_address,hiddenValor)
	print '<div class="alert alert-danger"><h2><b>Copie a transação realizada em sua wallet e cole aqui: </b></h2>'
	print '<form action="" method="post">'
	print '<div class="form-group">'
	print '<textarea class="form-control" rows="5" name="transactiondata"></textarea><br></div>'
	print '<button type="submit" class="btn btn-default" value="Submit">Enviar a transação</button></form></div>'
	print '<form action="" method="get"><button type="submit" class="btn btn-default" value="Submit">Voltar</button></form>'
elif transactionText == None:
	printContent()
	printAdvertisement()
	printBitcoinAddress(bitcoinAddress)
	print '<div class="col-md-4 text-center">'
	print '<form action="" method="post"><input type="hidden" name="hiddenCost" id="hiddenCost" value=""><button type="submit" class="btn btn-lg" value="Submit">Avançar</button></form>'
	print '</div>'
	#responseForm()
	#admLoginPart()
else:
	if checkTransaction(transactionText):
		value = ""
		value_btc = ""
		endereco = ""
		deserialized = transactionText.strip()
		data = ""
		deserialized = bitcoin.deserialize(deserialized)
		for item in deserialized['outs']:
			out = item['script']
			subString = out[6:len(out)-4]
			endereco = bitcoin.hex_to_b58check(subString,111)
			if endereco == bitcoinAddress:
				value = item['value']
				value_btc = value/float(100000000)

		with con:
			cur = con.cursor()
			#to prevent duplication of records in data base
			#get current time
			ts = time.time()
			st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
			cur.execute("SELECT * FROM Transaction_Info WHERE transaction_text = ?",(transactionText,))
			data = cur.fetchall()
			cur.execute("INSERT OR IGNORE INTO Transaction_Info(transaction_text,verified,time_added) values (?,?,?)",(transactionText,'FALSE',st))
		#print transaction valid, value
		#then add transaction to sqlite data base

		#print html related to value of transaction
		if len(data)==0:
			print '<div class="jumbotron">'
			print '<h1>Transação aceita</h1>'
			print '<p>Foi feita uma transação de: '
			print value_btc
			print 'BTC</p>'
			print '<p>para o endereco do vendedor: <br>'
			print bitcoinAddress
			print 'em '
			#Time
			print getCurrentTime()
			print '</p>'
			print '</div>'
			print '<div class="alert alert-info">'
			#Frase do dia
			phrase_file = open('../password/daily_phrase.txt','r')
			line = phrase_file.readline()
			phrase_file.close()
			print line
			print '<br>'
			print '</div>'
		else:
			print '<div class="jumbotron">'
			print '<h1>Transação não aceita</h1>'
			print '<p>Por favor, não entre a mesma transação duas ou mais vezes'
			print '</p>'
			print '</div>'
	else:
		#print alert message
		print '<div class="jumbotron">'
		print '<h1>Transação não aceita</h1>'
		print '<p>Os dados da transação estão incorretos'
		print '</p>'
		print '</div>'
	#print back button
	print '<form action="" method="get"><button type="submit" class="btn btn-default" value="Submit">Voltar</button></form>'
#print "<h2 class=\"productTitle\">Página de vendas</h2>"
print '</div>'
print '</body></html>'



