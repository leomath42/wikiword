#!/usr/bin/env python3

"""
Developed by: https://github.com/leomath42
contact: 


"""
class manager:
	data;
	request;
	formata;
"""

import pickle 
import sys 
import os
import urllib

import bs4
from bs4 import BeautifulSoup as bs

from urllib import request

def _search(word, site):
	#word
	#request = urllib.request
	word = word.replace(" ", "_").lower()
	r = request.urlopen(site+"/"+word)
	t = r.read()
	r.close()
	return t


def _extract(html, word, ex_num=5):
	"""
		Essa função extrai do html a definição da palavra 'word' e
		deixa no 'melhor' formato o possível;
		ex_num => número máximo de exemplos, defaut 5;
		html => html do dicionário(site) a extrair informações;
		word => palavra procurada no dicionário;
	"""
	
	# istancia soup
	soup = bs(html)
	
	#busca a Tag meta e retorna uma lista,
	#em <em>, <em/> tags html
	tags = soup.find_all('em')
		
	#variaveis para fazer "slice"
	start = len("<em>")
	end = len("</em>")
	cont = int()
	
	#lista com as ocorrencias da palavra "word"
	word_list = list()
	
	#arq = open("teste.txt","w")
	for tag in tags:
		
		# decodifica para string as tags
		text = tag.decode()
		
		if word in text:
			if text.startswith("<em>") and text.endswith("</em>"):
				#slice
				text = text[start:]
				text = text[:-end]
				
				#adiciona ao final da fila o texto
				word_list.append(text)
				cont+=1
		
		if cont > ex_num:
			break
		
	return word_list

class WordMean():

	def __init__(self, sites=None):
		self.sites = list()
		#self.sites.append("https://en.oxforddictionaries.com/definition/")
		#self.default_site = "https://en.oxforddictionaries.com/definition/"
		#self.sites.append(self.default_site)
		if sites:
			self.sites = sites
		else:
			self.sites = "sites"

		try:
			arq = open(self.sites)
			self.sites = arq.readlines()
			#print(self.sites)
			if self.sites != '':
				for i in self.sites:
					if i.endswith("\n"):
						i = i[:-1]
						self.sites.append(i)
		except FileNotFoundError:
			raise Exception("arquivo 'sites' contendo os dicionários não encontrado.")
		except:
			pass

	def search(self, word, exemples=1):
		#word_list = list()
		resulte = None
		word_dict= dict()
		#word_list.append(word)
		
		c = len(self.sites)
		i = 0
		while(i < c):
			try:
				html = _search(word, self.sites[i])
				resulte = _extract(html, word, exemples)
				break
			except:
				pass
			i+=1

		if resulte == None:
			return None
		else:
			word_dict["word"] = word
			word_dict["resulte"]=resulte
			return word_dict #retorna a palavra pesquisada e "a lista resultado"

if __name__ == "__main__":
	"""
	word = "loose"
	s = search(word, "https://en.oxforddictionaries.com/definition/")
	#arq = open("html","r")
	#s = arq.read()
	#arq.close()
	
	s =	extract(s, word)
	for i in s:
		print(i)
	"""
	w = WordMean()
	aux = w.search("loose")
	try:
		print(aux['word'])
		for i in aux["resulte"]:
			print(i)

	except:
		raise Exception("lista vazia, verifique o arquivo 'sites'")


