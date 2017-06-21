import bitcoin
import blockcypher
import hashlib
#generate a random private key
#valid_private_key = False
#while not valid_private_key:
#	private_key = bitcoin.random_key()
#	decoded_private_key = bitcoin.decode_privkey(private_key,'hex')
#	valid_private_key = 0 < decoded_private_key < bitcoin.N
#testnetAddress = bitcoin.privkey_to_address(private_key,111)
#print "My private key is: ", private_key
#print "My decoded private key is: ", decoded_private_key
#print "My testnetAddress is: ", testnetAddress
#pubkey1 = bitcoin.privkey_to_pubkey('139cb0d1038dccc8b5e7e224216670b76647c9f8df8a8ec29069cbb3d59aed2b')
#pubkey2 = bitcoin.privkey_to_pubkey('36b4fbdf43365191d3aea9361467b234f58a7244ae8d05f696e634726a162d01')
#pubkey = bitcoin.privkey_to_pubkey('15e9a5e2097c9a40eb4bd0aea4e334dd2f799c7e1f6173cb59505d470816fe9e')
#print "pubkey 1: ", pubkey1
#print "pubkey 2: ", pubkey2
#print "intial pubkey: ", pubkey
#num = bitcoin.is_privkey('15e9a5e2097c9a40eb4bd0aea4e334dd2f799c7e1f6173cb59505d470816fe9e')
pub = bitcoin.privkey_to_pubkey('15e9a5e2097c9a40eb4bd0aea4e334dd2f799c7e1f6173cb59505d470816fe9e')
compPub = bitcoin.compress(pub)
add = bitcoin.pubkey_to_address(compPub,111)
print compPub
print add
#if num:
#	print "OK"
#else:
#	print "damn"
#print add
transaction_info = '01000000018fd99010bf216c4aeece38bebcc94a740b853d64a4ee5d7d8217bf61b77abb1a010000006b483045022100f2353403f2f6aeb981b0870f35c0441e58a15786dd4c76307b8129d786031fcc022039c1861433a28d71026ba5860078cd8aa61951faee73af916fcb7d3301ac6ffc0121035ec6f5e117a67b3164f388105bf23b3d2af9fb39f939e24df53cf303b27e1bf7ffffffff01e01fec22000000001976a91464e6df2dbc78c34a8fffe908c223bd05683c479688ac00000000'
txinfo_hex = transaction_info.decode("hex")
transaction_i = hashlib.sha256(txinfo_hex).digest()
transaction_id = hashlib.sha256(transaction_i).digest()
transaction_id = transaction_id[::-1].encode('hex_codec')
print transaction_id



#Starting
api = '2422c50d3321416d97d2184cb76a2fed'
tx = '0100000001aa4e7c55ad414ef9d1d3724043190436fb551930d455d8fa0b84f51375e46182000000006b483045022100c51a09fb137084f7f2149c14ccac7209fdb3e772a3a7e49b5247ac14b9eaa71802203321b6998d812aaa91b3578187918d6f65e72624fd2c4be45bc417f5d453b522012102a10be900dfd57ac00eeb0259b7f4c61566b111599fd762ae4befb7a16ed8d78fffffffff0240420f00000000001976a91464e6df2dbc78c34a8fffe908c223bd05683c479688ac6416fb06000000001976a91447a022a80d1cbf4f7ebf84870caf4b3596728bd788ac00000000'
print blockcypher.pushtx(tx,coin_symbol='btc-testnet',api_key=api)