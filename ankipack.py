import genanki
from random import randrange

gk = genanki

class AnkiPack(super):

    def __init__(self, deck_name=None, model_name=None):
        # Variáveis do pacote a ser gerado::
        if model_name:
            self.model_name = model_name
        else:
            self.model_name = "default_model"

        if deck_name:
            self.deck_name = deck_name
        else:
            self.deck_name="deck"

        self.model = None
        self.card = None
        self.deck = None
        self.package = None

        self.deck = self.__create_deck(self.deck_name)

        try:
            self.model = self.__load_model(self.model_name) #"default_model.txt")

        except Exception:
            #try:
            self.model = self.__load_model(self.model_name)
        except:
            raise Exception(FileNotFoundError, "Error, default model don't found.")
            #print("Erro, modelo padrão não encontrado.")
        #finally:
        #    self.__create_deck


    def create_card(self, *args):
        """
            *args: lista com as informações dos campos,
            ex fields=["frente", "verso"]
        """

        #Cria um card::
        note = genanki.Note(model=self.model,fields=args)
        
        #Adiciona a nota(card) ao deck
        self.deck.add_note(note)

    def __create_deck(self, deck_name):
        random_id = randrange(1 << 30, 1 << 31) # igual a randrange(1*(2**30), 1*(2**31))
        return gk.Deck(random_id, deck_name)
    
    def __load_model(self, path):
        arq = open(path, "r")
        aux = arq.readlines()

        fields_dict = None
        templates_dict = dict()
        fields, templates = list(), list()      #list(fields_dict) errado #list(templates_dict) errado --"
        
        #model_cond = fields_cond = templates_cond = bool()

        for i in aux:
            if i.endswith("\n"):
                i = i[:-1]
            if i.startswith("[model]"):
                a = i.find(":")
                model_name = i[a+1:]
            
            elif i.startswith("[fields]"):
                aux = dict()
                a = i.find("]")
                b = i.find(":")
                nome = i[a+1:b]
                valor = i[b+1:]
                #print(nome, valor)
                aux[nome] = valor
                fields.append(aux)
            
            elif i.startswith("[templates]"):
                a = i.find("]")
                b = i.find(":")
                nome = i[a+1:b]
                valor = i[b+1:]
                #print(nome, valor)
                templates_dict[nome] = valor

        templates.append(templates_dict)
        
        """Cria o modelo::"""

        random_id = randrange(1 << 30, 1 << 31)
        
        self.model_name = model_name
        model = genanki.Model(random_id, self.model_name, fields=fields, templates=templates)
 
        return model

    def __create_model(self):
        #Cria um modelo para o cartão do Anki::
        pass

    def __gen_model(self):
        pass

    def create_package(self, name="default"):
        gk.Package(self.deck).write_to_file(name+".apkg")
        #genanki.Package(my_deck).write_to_file('output.apkg')

if __name__ == "__main__":
    c = AnkiPack(deck_name="teste", model_name="default_model")
    c.create_card('teste1', 'teste2')
    c.create_package()