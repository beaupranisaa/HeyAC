import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tree import Tree
from .utils import *
from textblob import TextBlob

class HeyAC:
    def __init__(self, grammar_path='grammars/grammar_combined.txt'):
        self.lemmatizer = WordNetLemmatizer()
        self.grammar = nltk.CFG.fromstring(open(grammar_path, "r"))
        self.parser = nltk.RecursiveDescentParser(self.grammar)

    def _response_str(self, key, var):

        print('[KEY]',key)
        print()

        RESPONSE = "[RESPONSE]"
        
        if type(var) == list:
            no_var = len(var)
        else:
            no_var = 0

        if no_var == 0:
            response = { 
                    "TEMP_UP":f"{RESPONSE} Increasing the temperature.",
                    "TEMP_DOWN":f"{RESPONSE} Decreasing the temperature.",
                    "HUMIDITY_UP":f"{RESPONSE} Humidifying the room.",
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
        elif no_var == 1:
            response = {
                    "TEMP_UP":f"{RESPONSE} Increasing the temperature to {var[0]}.",
                    "TEMP_DOWN":f"{RESPONSE} Decreasing the temperature to {var[0]}.",
                    "HUMIDITY_UP":f"{RESPONSE} Humidifying the room to {var[0]}.",
                    "HUMIDITY_DOWN":f"{RESPONSE} Drying the room to {var[0]}.",
                    'FAN_UP':f'{RESPONSE} Increasing the air volume to {var[0]}.',
                    'FAN_DOWN':f'{RESPONSE} Decreasing the air volume to {var[0]}.',
                    'SWING_DOWN':f'{RESPONSE} Swinging downwards to {var[0]}.',
                    'SWING_UP':f'{RESPONSE} Swinging upwards to {var[0]}.',
                    'TURN_ON':f'{RESPONSE} Starting ac at {var[0]}',
                    'TURN_OFF':f'{RESPONSE} Stopping ac at {var[0]}.',
                    'SET_MODE':f'{RESPONSE} Set mode to {var[0]}.',
                    'SET_TEMP':f'{RESPONSE} Set temperature to {var[0]}.',
                    'SET_FAN':f'{RESPONSE} Set fan speed to {var[0]}.',
                    'SET_HUMIDITY':f'{RESPONSE} Set humidity to {var[0]}.',
                    }

        elif no_var == 2:
            response = {
                    "TEMP_UP":f"{RESPONSE} Increasing the temperature to {var[1]}.",
                    "TEMP_DOWN":f"{RESPONSE} Decreasing the temperature to {var[1]}.",
                    "HUMIDITY_UP":f"{RESPONSE} Humidifying the room to {var[1]}.",
                    "HUMIDITY_DOWN":f"{RESPONSE} Drying the room to {var[1]}.",
                    'FAN_UP':f'{RESPONSE} Increasing the air volume to {var[1]}.',
                    'FAN_DOWN':f'{RESPONSE} Decreasing the air volume to {var[1]}.',
                    'SWING_DOWN':f'{RESPONSE} Swinging downwards to {var[1]}.',
                    'SWING_UP':f'{RESPONSE} Swinging upwards to {var[1]}.',
                    'TURN_ON':f'{RESPONSE} Starting ac from {var[0]} to {var[1]}.',
                    'SET_MODE':f'{RESPONSE} Set mode to {var[1]}.',
                    'SET_TEMP':f'{RESPONSE} Set temperature to {var[1]}.',
                    'SET_HUMIDITY':f'{RESPONSE} Set humidity to {var[1]}.',
                    }

        try:
            resp = response[key]
        except:
            resp = '[ERROR] What do you mean?'
        return resp

    def classify(self, text):
        '''
        Classifies the intent from the pruned text
        '''
        harvest = self.prune(text)

        key = None
        var = None

        if harvest['ACT'] is not None:
            print("[DIRECT COMMAND]")

            act = harvest['ACT']
            print('[ACT]',act)

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
            
            if act == 'ACTIVATE' or (act == 'TURN_ACT' and direction == 'ON'):
                if obj in ['AC','FAN']:
                    key = 'TURN_ON'
                elif obj == 'SWING':
                    key = 'SWING_START'
                elif value:
                    key = 'SET_MODE'
            elif act == 'STOP' or (act == 'TURN_ACT' and direction == 'OFF'):
                if obj in ['AC','FAN']:
                    key = 'TURN_OFF'
                elif obj == 'SWING':
                    key = 'SWING_STOP'
            elif act == 'INCREASE' or (act == 'TURN_ACT' and direction == 'UP'):
                if prop == 'TEMPERATURE':
                    key = 'TEMP_UP'
                elif (prop in ['BREEZE', 'VOLUME']) or (obj in ['FAN','AC','ENVIRONMENT']):
                    key = 'FAN_UP'
                elif prop == 'HUMIDITY':
                    key = 'HUMIDITY_UP'
                elif obj == 'SWING':
                    key = "SWING_UP"
            elif act == 'DECREASE' or (act == 'TURN_ACT' and direction == 'DOWN'):
                if prop == 'TEMPERATURE':
                    key = 'TEMP_DOWN'
                elif (prop in ['BREEZE', 'VOLUME']) or (obj in ['FAN','AC','ENVIRONMENT']):
                    key = 'FAN_DOWN'
                elif prop == 'HUMIDITY':
                    key = 'HUMIDITY_DOWN'
                elif obj == 'FAN':
                    key = 'FAN_DOWN'
                elif obj == 'SWING':
                    key = 'SWING_DOWN'
            elif act == 'COOL_ACT':
                key = 'TEMP_DOWN'
            elif act == 'DRY_ACT':
                key = 'HUMIDITY_DOWN'
            elif act == 'SWING_ACT':
                if direction == 'UP':
                    key = 'SWING_UP'
                elif direction == 'DOWN':
                    key = 'SWING_DOWN'
                elif direction == 'OFF':
                    key = 'SWING_STOP'
                else:
                    key = 'SWING_START'
            elif act == 'SPEED_ACT':
                if direction == 'UP':
                    key = 'FAN_UP'
                elif direction == 'DOWN':
                    key = 'FAN_DOWN'
            elif act == 'SET':
                if prop == 'TEMPERATURE':
                    key = 'SET_TEMP'
                elif prop == 'HUMIDITY':
                    key = 'SET_HUMIDITY'
                elif prop == 'VOLUME' or obj == 'FAN':
                    key = 'SET_FAN'
                elif prop == 'MODE':
                    key = 'SET_MODE'
                elif type(value) == list and len(value) > 0:
                    key = 'SET_MODE'

                elif value == 'HOT':
                    key = 'TEMP_UP'
                elif value == 'COLD':
                    key = 'TEMP_DOWN'
                elif value == 'DRY':
                    key = 'HUMIDITY_DOWN'
                elif value == 'HUMID':
                    key = 'HUMIDITY_UP'
                elif value == 'LOW':
                    if prop == 'TEMPERATURE':
                        key = 'TEMP_DOWN'
                    elif prop == 'VOLUME':
                        key = 'FAN_DOWN'
                    elif prop == 'HUMIDITY':
                        key = 'HUMIDITY_DOWN'
                    elif prop == 'BREEZE':
                        key = 'FAN_DOWN'
                    elif obj  == 'FAN':
                        key = 'FAN_DOWN'
                    elif obj == 'ENVIRONMENT':
                        key = 'TEMP_DOWN'
                    elif obj == 'AC':
                        key = 'TEMP_DOWN'
                    elif obj == 'SWING':
                        key = 'SWING_DOWN'
                elif value == 'HIGH':
                    if prop == 'TEMPERATURE':
                        key = 'TEMP_UP'
                    elif prop == 'VOLUME':
                        key = 'FAN_UP'
                    elif prop == 'HUMIDITY':
                        key = 'HUMIDITY_UP'
                    elif prop == 'BREEZE':
                        key = 'FAN_UP'
                    elif obj  == 'FAN':
                        key = 'FAN_UP'
                    elif obj == 'ENVIRONMENT':
                        key = 'TEMP_UP'
                    elif obj == 'AC':
                        key = 'TEMP_UP'
                    elif obj == 'SWING':
                        key = 'SWING_UP'

            if type(value) == list:
                var = []
                for val in harvest['VALUE']:
                    if val['MODES']:
                        var.append(val['MODES'])
                    else:
                        co = val['CO']
                        if val['UNIT']:
                            unit = val['UNIT']
                        else:
                            unit = ''
                        co_unit = ' '.join([co,unit])
                        var.append(co_unit)
                print(self._response_str(key, var))
            else:
                print(self._response_str(key, None))
        else:
            print("[INDIRECT COMMAND]")
            if len(harvest['VALUE']) > 0:
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

            if (value == "COLD" and neg == False) or (value == "HOT" and neg == True):
                key = 'TEMP_UP'
            elif (value == "HOT" and neg == False) or (value == "COLD" and neg == True):
                key = 'TEMP_DOWN'
            elif (value == "DRY" and neg == False) or (value == "HUMID" and neg == True):
                key = 'HUMIDITY_UP'
            elif (value == "HUMID" and neg == False) or (value == "DRY" and neg == True):
                key = 'HUMIDITY_DOWN'
            elif (value in ["STRONG", "FAST"] and neg == False) or (value in ["WEAK", "SLOW"] and neg == True):
                key = 'FAN_DOWN'
            elif (value in ["STRONG", "FAST"] and neg == True) or (value in ["WEAK", "SLOW"] and neg == False):
                key = 'FAN_UP'

            elif prop == 'VOLUME' and (value in ["HIGH"]) and neg == False:
                key = 'FAN_DOWN'
            elif prop == 'VOLUME' and (value in ["LOW"] and neg == False):
                key = 'FAN_UP'
            elif prop == 'TEMPERATURE' and (value in ['HIGH'] and neg == False):
                key = 'TEMP_DOWN'
            elif prop == 'TEMPERATURE' and (value in ['LOW'] and neg == False):
                key = 'TEMP_UP'
            elif prop == 'HUMIDITY' and (value in ['LOW'] and neg == False):
                key = 'HUMIDITY_UP'
            elif prop == 'HUMIDITY' and (value in ['HIGH'] and neg == False):
                key = 'HUMIDITY_DOWN'
            elif (prop == 'BREEZE' or obj in ['FAN', 'SWING']) and value in ['HIGH'] and neg == False:
                key = 'SWING_DOWN'
            elif (prop == 'BREEZE' or obj in ["FAN", 'SWING']) and value in ['LOW'] and neg == False:
                key = 'SWING_UP'
            elif (obj in ["FAN", "AC", "ENVIRONMENT"]) and value in ["RUNNING", "WORKING"] and neg == False:
                key = 'TURN_OFF'
            elif value == "SWINGING" and neg == False:
                key = 'SWING_STOP'
            elif (obj == "SWING" and value in ["MOVING", "RUNNING", "WORKING"] and neg == False):
                key = "SWING_STOP"

            elif prop == 'VOLUME' and (value in ["HIGH"]) and neg == True:
                key = 'FAN_UP'
            elif prop == 'VOLUME' and (value in ["LOW"] and neg == True):
                key = 'FAN_DOWN'
            elif prop == 'TEMPERATURE' and (value in ['HIGH'] and neg == True):
                key = 'TEMP_UP'
            elif prop == 'TEMPERATURE' and (value in ['LOW'] and neg == True):
                key = 'TEMP_DOWN'
            elif prop == 'HUMIDITY' and (value in ['LOW'] and neg == True):
                key = 'HUMIDITY_DOWN'
            elif prop == 'HUMIDITY' and (value in ['HIGH'] and neg == True):
                key = 'HUMIDITY_UP'
            elif (prop == 'BREEZE' or obj in ['FAN', 'SWING']) and value in ['HIGH'] and neg == True:
                key = 'SWING_UP'
            elif (prop == 'BREEZE' or obj in ["FAN", 'SWING']) and value in ['LOW'] and neg == True:
                key = 'SWING_DOWN'
            elif (obj in ["FAN", "AC", "ENVIRONMENT"]) and value in ["RUNNING", "WORKING"] and neg == True:
                key = 'TURN_ON'
            elif value == "SWINGING" and neg == True:
                key = 'SWING_START'
            elif (obj == "SWING" and value in ["MOVING", "RUNNING", "WORKING"] and neg == True):
                key = "SWING_START"

            print(self._response_str(key, None))

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
                'VALUE':[],
                'ACT':None,  
                'DIR':None,
                'VBG':None,
                'MODES':None,
                }
        
        if len(parse_trees) > 1:
            print('[WARNING] More than a single parse detected')

        parse_tree = parse_trees[0]

        for sub_tree in parse_tree.subtrees():
            label = sub_tree.label()
            if label in harvest.keys():
                if label == 'VALUE':
                    if len(list(sub_tree)) == 1 and list(sub_tree)[0].label() not in ['CO','MODES']:
                        harvest[label] = list(sub_tree)[0].label()
                    else:
                        value_harvest = {
                                'CO':None,
                                'UNIT':None,
                                'MODES':None,
                                }
                        for st in list(sub_tree):
                            v_label = st.label()
                            if v_label in value_harvest.keys():
                                try:
                                    value_harvest[v_label] = list(st)[0].label()
                                except:
                                    value_harvest[v_label] = list(st)[0].upper()
                        harvest[label].append(value_harvest)
                    continue
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
