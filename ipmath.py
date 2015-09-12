#!/usr/bin/env python
import sys,os,random,struct,socket,re


#Todo
#Add PTR and exists methods.  Also add :/ support for a, mx etc.
#Validate that a supplied IP is allowed or denied in the SPF record(s)


class ip4:
	def __init__(self,inp):
		self.cidr=-1
		self.start=-1
		self.end=-1
		self.parseip(inp)
		


	def parseip(self,inp):
		self.ipversion=4
		self.bits=32
		self.ipsize=16777216
		self.bitl=256
		if inp.isdigit():
			self.ip=inp
		elif re.match('((?:\d+\.){3}\d+)$',inp):
                        n=re.match('((?:\d+\.){3}\d+)',inp)
                        self.ip=self.ip2dec(n.group(1))
                else:
                        n=re.match('((?:\d+\.){3}\d+)/(\d+)',inp)
                        self.ip=self.ip2dec(n.group(1))
                        self.cidr=int(n.group(2))
                        self.setstartend()

		


	def dec2bin(self,inp):
		c=2**self.bits
		b=""
		while c>=1:
			if inp&c:
				b+="1"
			else:
				b+="0"
			c/=2
		return b

	def dec2ip(self,dec):
		ip=""
		s=self.ipsize
		while s>1:
			n=dec/s
			ip+="%d."%n
			dec=dec-n*s
			s/=self.bitl
		ip+="%d"%dec
		return ip


	def ip2dec(self,ip):
		ret=0
		s=self.ipsize
		for a in ip.split('.'):
			ret+=int(a)*s
			s/=self.bitl
		return ret


	def displaynet(self):
		if self.cidr!=-1:
			bas=2**(self.bits-int(self.cidr))
			netd=bas*int(int(self.ip)/bas)
			return "%s/%d"%(self.dec2ip(netd),self.cidr)

	def setstartend(self):
		if self.cidr!=-1:
			bas=2**(self.bits-self.cidr)
			self.start=bas*int(self.ip/bas)
			self.end=self.start+bas
			

	def getdec(self):
		return self.ip

        def getsize(self):
                if self.cidr==-1:
                        return 1
                else:
                        return self.end-self.start

	def getipversion(self):
		return self.ipversion

	def equals(self,a):
		if self.cidr == a.cidr and self.ipversion == self.ipversion:
			if (self.cidr == -1):
				if self.ip == a.ip:
					return True
			else:
				if self.displaynet() == a.displaynet():
					return True
		return False



	def ipinnet(self,ip):
		if self.cidr==-1:
			return self.equals(ip)
		dec=ip.getdec()
		return dec >= self.start and dec <=self.end


	def getarpa(self):
		ip=self.dec2ip(self.ip)
		ret=""
		for a in ip.split('.'):
			ret="%s.%s"%(a,ret)
		ret+="in-addr.arpa"
		return ret
		

	def __str__(self):
		return self.dec2ip(self.ip)


class ip6(ip4):
        def parseip(self,inp):
                self.ipversion=6
                self.bits=128
                self.ipsize=5192296858534827628530496329220096
                self.bitl=65536
                if inp.isdigit():
                        self.ip=inp
		elif re.match('[0-9A-Fa-f:]+$',inp):
                        n=re.match('([0-9A-Fa-f:]+)$',inp)
                        self.ip=self.ip2dec(n.group(1))
                else:
                        n=re.match('([0-9A-Fa-f:]+)/(\d+)$',inp)
                        self.ip=self.ip2dec(n.group(1))
                        self.cidr=int(n.group(2))
                        self.setstartend()

        def dec2ip(self,dec,long=0):
                ip=""
                s=self.ipsize
                while s>1:
                        n=dec/s
                        ip+="%s:"%hex(n).rstrip('L').split('x')[1].lower()
                        dec=dec-n*s
                        s/=self.bitl
                ip+="%s"%hex(dec).rstrip('L').split('x')[1].lower()
		if long==0:
			ip=re.sub('(:0)+',':',ip)
			if ip[-1]==':':
				ip+=':'
			if ip[0:3]=='0::':
				ip='::'+ip[3:]
                return ip

        def ip2dec(self,ip):
                ret=0
                s=self.ipsize
                m=re.search('(.*)::(.*)$',ip)
                if m:
                        if (m.group(1) != ''):
                                for a in m.group(1).split(':'):
                                        ret+=s*int(a,16)
                                        s/=self.bitl
                        t=self.bitl**(len(m.group(2).split(':'))-1)
                        if (m.group(2) != ''):
				for a in m.group(2).split(':'):
					ret+=t*int(a,16)
					t/=self.bitl
                else:
                        for a in ip.split(':'):
                                ret+=self*int(a,16)
                                s/=s.bitl
                return ret



        def getarpa(self):
                ip=self.dec2ip(self.ip,1)
                ret=""
                for a in ip.split(':'):
			while len(a)<4:
				a="0%s"%a
			for b in a:
				ret="%s.%s"%(b,ret)
                ret+="ip6.arpa"
                return ret



if __name__ == "__main__":
	a=ip4("192.168.12.1")
	print a
