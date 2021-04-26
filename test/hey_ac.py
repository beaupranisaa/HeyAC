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
                'SWING_START':f'{RESPONSE} Started swinging.',
                'SWING_STOP':f'{RESPONSE} Stopped swinging.',
                'TURN_ON':f'{RESPONSE} Started AC.',
                'TURN_OFF':f'{RESPONSE} Stopped AC.',
                }

        if harvest['ACT'] is not None:
            print("[DIRECT COMMAND]")

            act = harvest['ACT']

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

            if harvest['DIR']:
                direction = harvest['DIR']
                print('[DIR]',direction)
            else:
                direction = None
            
            if harvest['VALUE']:
                value = harvest['VALUE']
                print('[VALUE]',value)
            else:
                value = None

            if harvest['UNIT']:
                unit = harvest['UNIT']
                print('[UNIT]',unit)
            else:
                unit = None

            if act == 'ACTIVATE' or (act == 'TURN_ACT' and direction == 'ON'):
                if obj in ['AC','FAN']:
                    if unit == 'DEGREE':
                        resp = 'turn on ac to VALUE'
                    elif unit in ['PM', 'AM', "O_CLOCK"]:
                        resp = 'turn on ac from VALUE[0] [to VALUE[1]]'
                    else:
                        resp = 'turn on ac'
                elif obj == 'SWING':
                    resp = 'turn on swing'
                elif value == 'MODES':
                    resp = 'set to MODE'
            elif act == 'STOP' or (act == 'TURN_ACT' and direction == 'OFF'):
                if obj in ['AC','FAN']:
                    resp = 'turn off ac'
                elif obj == 'SWING':
                    resp = 'turn off swing'
            elif act == 'INCREASE' or (act == 'TURN_ACT' and direction == 'UP'):
                if prop == 'TEMPERATURE':
                    if value:
                        resp = 'increase temperature to VALUE'
                    else:
                        resp = 'increase temperature'
                elif (prop in ['BREEZE', 'VOLUME']) or (obj == 'FAN'):
                    if value:
                        resp = 'increase fan to VALUE'
                    else:
                        resp = 'increase fan'
                elif prop == 'HUMIDITY':
                    if value:
                        resp = 'increase humidity to VALUE'
                    else:
                        resp = 'increase humidity'
                elif obj == 'SWING':
                    if value:
                        resp = 'swing to VALUE'
                    else:
                        resp == 'swing up'
            elif act == 'DECREASE' or (act == 'TURN_DOWN' and direction == 'DOWN'):
                if prop == 'TEMPERATURE':
                    if value:
                        resp = 'decrease temperature to VALUE'
                    else:
                        resp = 'decrease temperature'
                elif (prop == in ['BREEZE', 'VOLUME']) or (obj == 'FAN'):
                    if value:
                        resp = 'decrase fan to VALUE'
                    else:
                        resp = 'decrease fan'
                elif prop == 'HUMIDITY':
                    if VALUE:
                        resp = 'decrease humidity to VALUE'
                    else:
                        resp = 'decrease humidity'
                elif obj == 'FAN':
                    if value:
                        resp = 'decrease fan to VALUE'
                    else:
                        resp = 'decrease fan'
                elif obj == 'SWING':
                    if value:
                        resp = 'swing down to VALUE'
                    else:
                        resp == 'swing down'
            elif act == 'COOL_ACT':
                if value:
                    resp = 'decrease temperature to VALUE'
                else:
                    resp = 'decrease temperature'
            elif act == 'DRY_ACT':
                if value:
                    resp = 'decrease humidity to VALUE'
                else:
                    resp = 'decrease humidity'
            elif act == 'SWING_ACT':
                if direction == 'UP':
                    if value:
                        resp = 'swing up to VALUE'
                    else:
                        resp = 'swing up'
                elif direction == 'DOWN':
                    if value:
                        resp = 'swing down to VALUE'
                    else:
                        resp = 'swing down'
                elif direction == 'OFF':
                    resp = 'stop swing'
                else:
                    resp = 'start swing'
            elif act == 'SPEED_ACT':
                if direction == 'UP':
                    if value:
                        resp = 'increase fan to VALUE'
                    else:
                        resp = 'increase fan'
                elif direction == 'DOWN':
                    if value:
                        resp = 'decrease fan to VALUE'
                    else:
                        resp = 'decrease fan'
            elif act == 'SET':
                if prop == 'TEMPERATURE':
                    resp = 'set temp to VALUE'
                elif prop == 'HUMIDITY':
                    resp = 'set humidity to VALUE'
                elif prop == 'MODE':
                    resp = 'set mode to VALUE'

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


            if value in ["COLD", "HOT", "DRY" , "HUMID", "STRONG", "FAST", "WEAK", "SLOW"]:
                if (value == "COLD" and neg == False) or (value == "HOT" and neg == True):
                    resp = 'TEMP_UP'
                elif (value == "HOT" and neg == False) or (value == "COLD" and neg == True):
                    resp = 'TEMP_DOWN'
                elif (value == "DRY" and neg == False) or (value == "HUMID" and neg == True):
                    resp = 'HUMIDITY_UP'
                elif (value == "HUMID" and neg == False) or (value == "DRY" and neg == True):
                    resp = 'HUMIDITY_DOWN'
                elif (value in ["STRONG", "FAST"] and neg == False) or (value in ["WEAK", "SLOW"] and neg == True):
                    resp = 'FAN_DOWN'
                elif (value in ["STRONG", "FAST"] and neg == True) or (value in ["WEAK", "SLOW"] and neg == False):
                    resp = 'FAN_UP'

            if prop == 'VOLUME' and (value in ["HIGH"]):
                resp = 'FAN_DOWN'
            elif prop == 'VOLUME' and (value in ["LOW"]):
                resp = 'FAN_UP'
            elif prop == 'TEMPERATURE' and (value in ['HIGH']):
                resp = 'TEMP_DOWN'
            elif prop == 'TEMPERATURE' and (value in ['LOW']):
                resp = 'TEMP_UP'
            elif prop == 'HUMIDITY' and (value in ['LOW']):
                resp = 'HUMIDITY_UP'
            elif prop == 'HUMIDITY' and (value in ['HIGH']):
                resp = 'HUMIDITY_DOWN'
            elif (prop == 'BREEZE' or obj in ['FAN', 'SWING']) and value in ['HIGH']:
                resp = 'SWING_DOWN'
            elif (prop == 'BREEZE' or obj in ["FAN", 'SWING']) and value in ['LOW']:
                resp = 'SWING_UP'

        print(response[resp])

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
