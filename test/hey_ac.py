import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tree import Tree
from utils import *
from textblob import TextBlob

class HeyAC:
    def __init__(self, grammar_path='../grammars/grammar_combined.txt'):
        self.lemmatizer = WordNetLemmatizer()
        self.grammar = nltk.CFG.fromstring(open(grammar_path, "r"))
        self.parser = nltk.RecursiveDescentParser(self.grammar)

    def classify(self, text):
        '''
        Classifies the intent from the pruned text
        '''
        harvest = self.prune(text)

        if harvest['ACT'] is not None:
            print("[DIRECT COMMAND]")
        else:
            print("[INDIRECT COMMAND]")
            if harvest['VALUE'] is not None:
                value = harvest['VALUE']
            else:
                value = harvest['VBG']
            print("[VALUE]", value)

            if harvest['NEG'] is not None:
                neg = True
            else:
                neg = False
            print("[NEG]", neg)

            if harvest['NN_PROP']:
                prop = harvest['NN_PROP']
                print('[PROP]', prop)
            else:
                prop = None

            if harvest['NN_OBJ']:
                obj = harvest['NN_OBJ']
                print('[OBJ]', obj)
            else:
                obj = None

            RESPONSE = "[RESPONSE]"
            response = { 
                    "TEMP_UP":f"{RESPONSE} Increasing the temperature.",
                    "TEMP_DOWN":f"{RESPONSE} Decreasing the temperature.",
                    "HUMIDITY_UP":f"{RESPONSE} Condensing the room.",
                    "HUMIDITY_DOWN":f"{RESPONSE} Drying the room.",
                    'FAN_UP':f'{RESPONSE} Increasing the air volume.',
                    'FAN_DOWN':f'{RESPONSE} Decreasing the air volume.',
                    'SWING_DOWN':f'{RESPONSE} Swinging downwards.',
                    'SWING_UP':f'{RESPONSE} Swinging upwards.',
                    }

            if value in ["COLD", "HOT", "DRY" , "HUMID", "STRONG", "FAST", "WEAK", "SLOW"]:
                if (value == "COLD" and neg == False) or (value == "HOT" and neg == True):
                    print(response['TEMP_UP'])
                elif (value == "HOT" and neg == False) or (value == "COLD" and neg == True):
                    print(response['TEMP_DOWN'])
                elif (value == "DRY" and neg == False) or (value == "HUMID" and neg == True):
                    print(response['HUMIDITY_UP'])
                elif (value == "HUMID" and neg == False) or (value == "DRY" and neg == True):
                    print(response['HUMIDITY_DOWN'])
                elif (value in ["STRONG", "FAST"] and neg == False) or (value in ["WEAK", "SLOW"] and neg == True):
                    print(response['FAN_DOWN'])
                elif (value in ["STRONG", "FAST"] and neg == True) or (value in ["WEAK", "SLOW"] and neg == False):
                    print(response['FAN_UP'])

            if prop == 'VOLUME' and (value in ["HIGH"]):
                print(response['FAN_DOWN'])
            elif prop == 'VOLUME' and (value in ["LOW"]):
                print(response['FAN_UP'])
            elif prop == 'TEMPERATURE' and (value in ['HIGH']):
                print(response['TEMP_DOWN'])
            elif prop == 'TEMPERATURE' and (value in ['LOW']):
                print(response['TEMP_UP'])
            elif prop == 'HUMIDITY' and (value in ['LOW']):
                print(response['HUMIDITY_UP'])
            elif prop == 'HUMIDITY' and (value in ['HIGH']):
                print(response['HUMIDITY_DOWN'])
            elif (prop == 'BREEZE' or obj in ['FAN', 'SWING']) and value in ['HIGH']:
                print(response['SWING_DOWN'])
            elif (prop == 'BREEZE' or obj in ["FAN", 'SWING']) and value in ['LOW']:
                print(response['SWING_UP'])

    def prune(self, text):
        '''
        Prunes the important words from the raw text
        '''
        processed_text, list_var = HeyAC._preprocess(text)
        parse_trees = self._parse(processed_text)
        parse_trees = self._dummy_to_digit(parse_trees, list_var)
        harvest = self._prune(parse_trees)
        return harvest 
    
    def _prune(self, parse_trees):
        '''
        Prunes the important words from the parse tree
        '''
        harvest = {
                'NN_PROP':None,
                'NN_OBJ':None,
                'NEG':None,
                'VALUE':None,
                'ACT':None,  
                'DIR':None,
                'VBG':None,
                'CO':None,
                'UNIT':None,
                }
        
        if len(parse_trees) > 1:
            print('[WARNING] More than a single parse detected')

        parse_tree = parse_trees[0]

        for sub_tree in parse_tree.subtrees():
            label = sub_tree.label()
            if label in harvest.keys():
                try:
                    harvest[label] = list(sub_tree)[0].label()
                except:
                    harvest[label] = list(sub_tree)[0].upper()
        return harvest

    def parse(self, text):
        processed_text, list_var = HeyAC._preprocess(text)
        parse_trees = self._parse(processed_text)
        parse_trees = self._dummy_to_digit(parse_trees, list_var)
        return parse_trees

    def _parse(self, text):
        '''
        Syntactically parses text
        '''
        tokens = HeyAC._tokenize(text)
        parse_trees = list(self.parser.parse(tokens))
        return parse_trees
    
    def _dummy_to_digit(self, parse_trees, list_var):
        '''
        Converts hey_num back to the original variable
        '''
        for parse_tree in parse_trees:
            counter = 0
            for pos in parse_tree.treepositions('leaves'):
                if parse_tree[pos] == 'hey_num':
                    parse_tree[pos] = list_var[counter]
                    counter += 1

        return parse_trees

    @staticmethod
    def _preprocess(text):
        ''' 
        Preprocess the text
            1. Converting numbers and variables to a dummy word "hey_num"
            2. Converting all the letters to lowercase
            3. Correcting any spelling mistakes
        '''
        processed_text = HeyAC._word_to_digit(text)
        processed_text, list_var = HeyAC._digit_to_dummy(processed_text)
        processed_text = TextBlob(processed_text)
        processed_text = processed_text.lower()
        #processed_text = processed_text.correct()
        processed_text = str(processed_text)

        return processed_text, list_var

    @staticmethod
    def _word_to_digit(text):
        '''
        Convert text to digit
            "Set the temperature to twenty degrees" -> "Set the temperature to 20 degrees"
        '''
        is_var, processed_text = check_var(text)
        return processed_text
    
    @staticmethod
    def _digit_to_dummy(text):
        '''
        Convert digit to a dummy word "hey_num" and returns the list of variables
            "Set the temperature to 20 degrees" -> "Set the temperature to hey_num degrees"
        '''
        text_split = text.split()
        text_split_dummy = [ "hey_num" if i.isdigit() else i for i in text_split]
        list_var = [i for i in text_split if i.isdigit()]
        processed_text = ' '.join(text_split_dummy)
        return processed_text, list_var
    
    @staticmethod
    def _tokenize(text):
        '''
        Splits the text into a list of words
        '''
        tokens = text.split(' ')
        return tokens
