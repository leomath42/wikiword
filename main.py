import sys
from ankipack import AnkiPack
from wordmean import WordMean


#usage: python [option] ... [-c cmd | -m mod | file | -] [arg] ...
h = """
wikiword v0.1
usos: wikiword [op] ... [--wordlist | --insertion | ] [arg] ... 
      wikiword [op1][arg1]...[op n-1][arg n-1] ...
parametros:
-wl ou --wordlist: um arquivo do tipo .txt com uma lista de palavras. 
                   É necessário que cada palavra pesquisada esteja em 
                   linhas diferentes.	
-i ou --insertion: pesquisa cada palavra dada, para interromper use Ctrl+C.

opções:
-d ou -deck:       nome do deck, por padrão o nome de saída é "deck".
	
-m ou --model:     nome do arquivo com o modelo dos cards,
                   caso não seja utilizado, será usado o modelo default.

-s ou --sites:     arquivo com dicionários online a ser utilizado,
                   caso não seja utilizado, será usado o arquivo padrão.

-e ou example:     número de exemplos que será extraído do dicionário, o padrão é 1.
-p ou --pack:      nome do .apkg de saída, por padrão é default.apkg.

outros:
-h ou --help:      imprime essa mensagem de ajuda.
"""

def formata(dic):
	s = str()
	for i in dic:
		#print(i)
		s = s+i+"\n"

	return s
def arguments():
	len_argv = len(sys.argv)
	#for i in sys.argv:
	if len_argv > 1:
		if sys.argv[1] == "--help" or sys.argv[1] == "-h":
			print(h)
		elif sys.argv[1] == "--wordlist" or sys.argv[1] == "-wl": #BUG_IN "-wl"
			try:
				cond = True
				arq = open(sys.argv[2], "r")
				wordlist = arq.read().split("\n")
				arq.close()
			except:
				cond = False
				print("Arquivo não encontrado, tente outra entrada.")

			#Argumentos opcionais::
			deck = model = sites = pack = None
			exemple = 1
			if cond:
				for i, j in enumerate(sys.argv):
					if j == "--deck" or j == "-d":
						deck = sys.argv[i+1]
					if j == "--model" or j == "-m":
						model = sys.argv[i+1]
					if j == "--sites" or j == "-s":
						sites = sys.argv[i+1]
					if j == "--example" or j == "-e":
						exemple = sys.argv[i+1]
					if j == "--pack" or j == "-p":
						pack = sys.argv[i+1]

				wm = WordMean(sites)
				ap = AnkiPack(deck, model)
				#ap.create_package("output")
				#wl = list()
				#print(wordlist)
				#print("\n")
				for i in wordlist:
					d = wm.search(i, exemple) # retorna "word" e "resulte"
					
					#print(d)
					
					s = formata(d["resulte"])
					
					#print(s)
					
					ap.create_card(d["word"], s)
					#print(d["word"], d["resulte"])
				
				if pack:
					ap.create_package(pack)
				else:
					ap.create_package()
				
				#ap.create_package("output")
		elif (sys.argv[1] == "--insertion") or (sys.argv[1] == "-i"):
			deck = model = sites = pack = None
			exemple = 1
			for i, j in enumerate(sys.argv):
				if j == "--deck" or j == "-d":
					deck = sys.argv[i+1]
				if j == "--model" or j == "-m":
					model = sys.argv[i+1]
				if j == "--sites" or j == "-s":
					sites = sys.argv[i+1]
				if j == "--example" or j == "-e":
					exemple = sys.argv[i+1]
				if j == "--pack" or j == "-p":
					pack = sys.argv[i+1]

			wm = WordMean(sites)
			ap = AnkiPack(deck, model)

			print("Para sair use CTRL+C:")
			while(1):
				try:
					info = input("Word:")
					d = wm.search(info, exemple)
					s = formata(d["resulte"])
					ap.create_card(d["word"], s)

				except KeyboardInterrupt:
					break

			if pack:
				ap.create_package(pack)
			else:
				ap.create_package()
				
	else:		
		print("passe algum argumento, ou use --help:")

def main():
	pass

if __name__ == "__main__":
	#print(sys.argv)
	arguments()