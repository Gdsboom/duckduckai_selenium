import time
import asyncio
import random
import pytest
from DuckChat_Tor import DuckChat_Tor
#from pyautogui import *
#import pyautogui
import time
#import keyboard
import random
#import win32api, win32con
#import pyautogui as pag
import sys, random, math
import os
import time
from ctypes import *
import pyperclip
#import pyautogui
import threading
import requests

barrier = threading.Barrier(2)
class Transleta:
    alf = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
    alf = alf.split(" ")
    alf_ru = "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я"
    alf_ru = alf_ru.split(" ")

    def __init__(self,
                 original_file,
                 config_file,
                 translated_file,
                 multiline: False,
                 visual: False,
                 remove_lines_with_0_characters: False,
                 prompts: [],
                 symbols: [],
                 verification = True,
                 proxy='127.0.0.1:9080'):
        self.original_file = original_file
        self.config_file = config_file
        self.config_file_check = self.config_file.replace( ".txt", "Check.txt" )
        self.config_file_check_index = self.config_file.replace(".txt", "CheckIndex.txt")
        self.translated_file = translated_file
        self.translated_file_check = self.translated_file.replace( ".txt", "rr.txt" )
        self.text = ""
        self.kol = set()
        self.buff_all = set()
        self.proxy = proxy
        self.multiline = bool(multiline)
        self.visual = bool(visual)
        self.remove_lines_with_0_characters = bool(remove_lines_with_0_characters)
        self.verification = bool(verification)

        (self.prompt_get_prompt, self.prompt_error_1, self.prompt_error_2, self.prompt_check_1, self.prompt_check_2) \
            = prompts[0], prompts[1], prompts[2], prompts[3], prompts[4]
        self.symbols_NoMultiline, self.symbols_multiline = symbols[0], symbols[1]
        self.original_text = []
        self.prompt = []
        self.buff_kol = []
        self.buff_interval = 0
        self.buff_threading = 1
        self.exit = 0
        """self.brackets = {
            '(', ')',
            '[', ']',
            '{', '}',
            '"', '"',
            "'", "'",
            '「', '」',
            '『', '』'
        }"""
        self.brackets = [
            '(', ')',
            '[', ']',
            '{', '}',
            '"', '"',
            '“', '”',
            "'", "'",
            '「', '」',
            '『', '』'
        ]

        #self.translate()

    def setBuffALL(self):
        self.buff_all = set([-9999999999999])
        #self.kol.append(0)
        self.kol = sorted( self.kol )
        if (self.visual):
            print(self.kol)
            print("Длинна (кол-во) строк: ", len(self.kol), "\n")

    def read_original_file(self, returns = None):
        file_original_2 = []
        with open(self.original_file, encoding='utf-8') as file:
            buff = file.read().splitlines()
        try:
            while True:
                buff.remove('')
                #print(nums)
        except:
             for x in buff:
                 if (returns == None):
                    self.text += x + "\n\n"
                 file_original_2.append(x + "\n\n")

        if (self.visual):
            print(len(self.text))
        if ( returns!= None ):
            return file_original_2
        """with open(self.original_file, encoding='utf-8') as f:
            for i in f:
                for q in i:
                    self.text += str(q)
            #self.text = f.read()
        if ( self.visual ):
            print(len(self.text))
        self.remove_pages()"""

    def remove_pages(self):
        for x in range(500, 0, -1):
            self.text = self.text.replace(f'Page | {x}', '')

    def buff_pass( self, text, buff_i, i ):
        buff_kol = 1
        buff_text = ""
        for q in range(i, len(text)):
            if (buff_i >= q):
                return buff_i, buff_text, buff_kol
            if (text[q] == "\n"):
                buff_kol = sum(1 for k in buff_text if k.isalpha())
                buff_i = q
                return buff_i, buff_text, buff_kol
            buff_text += text[q]
        return buff_i, buff_text, buff_kol

    def __paragraphing(self, file, alf, multiline = None):
        symbols = self.symbols_NoMultiline
        if (self.multiline and multiline == None):
            symbols = self.symbols_multiline
        text = str()
        buff_index = 0
        index = [0]
        refile = []
        #file_original_2 = []
        #file_translate_2 = []
        file_original_2 = file
        '''
        for x in range(len(file)):
            buff_text = ""
            for i in range(len(file[x])):
                if (len(buff_text) != 0 and i + 1 < len(file[x]) and (not (buff_text[-1].lower() in alf) and (file[x][i + 1].lower() != file[x][i + 1] and file[x][i + 1].lower() in alf) and (file[x][i - 1] != ",")) and file[x][i] == " "):
                    buff_text += file[x][i]
                buff_text += file[x][i]
            for i in buff_text.split("  "):
                file_original_2.append(i)
            file_original_2[-1] += "\n\n"'''
        for x in range( len(file_original_2) ):
            buff_index += 1
            buff_kol = sum(1 for i in file_original_2[x].replace("\n", "") if i.isalpha())
            if buff_kol == 0:
                if (text!=""):
                    refile.append(text)
                refile.append( file_original_2[x] )
                index.append(buff_index)
                text = str()
                continue
            if ( x+1<len(file_original_2) and self.multiline == True and len( text  ) + len(file_original_2[x+1]) <= symbols ):
                text += str( file_original_2[x] )
            elif ( x+1<len(file_original_2) and self.multiline == False and len( text  ) + len( file_original_2[x] ) <= symbols ):
                text += str( file_original_2[x] )
            else:
                if ( text!="" ):
                    refile.append( text+" "+str( file_original_2[x] ) )
                index.append(buff_index)
                text = ""
        return refile

    """def process_text(self, text = None, multiline = None):
        symbols = self.symbols_NoMultiline
        if ( self.multiline and multiline == None ):
            symbols = self.symbols_multiline
        if ( text == None ) :
            text = self.text
        '''
        textt = self.__paragraphing( self.read_original_file( returns=1 ), self.alf )
        #textt[x] += "\n\n"
        kol = set()
        buff_x = 0
        for x in textt:
            kol.add( self.text.index( (x.split(" "))[-1] ) + (len(x.split(" ")[-1])) )
        kol = sorted(kol)
        '''
        i = 0
        kol = set()
        kol.add(0)
        shovel = 0
        for x in range(1, len(text)):
            #while (i<=(2_000*x) or a[i-1]!=".") and i<len(a) or scopki==1: # or a[i-1]!="…" or a[i-1]!="!" or a[i-1]!=","
            if ( self.multiline ):
                #while (i <= (symbols * x) or text[i - 1] != ".") and i + 1 < len(text):
                buff_i = -99999999999
                while i<len(text) and ( ( ( i - sorted(kol)[-1] ) <= symbols) or ( shovel==1 ) or (text[i] != "\n") ):

                    buff_i, buff_text, buff_kol = self.buff_pass( text, buff_i, i )

                    if ( not(buff_kol) and len(buff_text)!=0 ):
                        kol.add(i)
                        i += len(buff_text)
                        break
                    
                    elif ( text[i] in self.brackets or text[i] in self.brackets and shovel!=1 ):
                        shovel = 1
                    elif ( text[i] in self.brackets or text[i] in self.brackets ):
                        shovel = 0
                    if ( not( ( i - sorted(kol)[-1] ) <= symbols) and text[i] == "\n" ):
                        break
                    i += 1
            else:
                while (i <= (symbols * x) or not(text[i - 1] in {'.', '。'}) ) and i + 1 < len(text) and (text[i] != "\n"):
                    i += 1
            try:
                while text[i+1]=="\n" or text[i]=="\n":
                    i+=1
            except:
                pass
            if (i < len(text) and text[i] != "\n") or i==len(text):
                #print(i, len(text))
                kol.add(i)
            #i += 1
        kol = sorted(kol)
        return kol
    """
    def process_text(self, text = None, multiline = None):
        symbols = self.symbols_NoMultiline
        if ( self.multiline and multiline == None ):
            symbols = self.symbols_multiline
        if ( text == None ) :
            text = self.text
        """
        textt = self.__paragraphing( self.read_original_file( returns=1 ), self.alf )
        #textt[x] += "\n\n"
        kol = set()
        buff_x = 0
        for x in textt:
            kol.add( self.text.index( (x.split(" "))[-1] ) + (len(x.split(" ")[-1])) )
        kol = sorted(kol)"""
        ''''''
        i = 0
        kol = set()
        kol.add(0)
        shovel = 0
        additional_check_index = 0
        for x in range(1, len(text)):
            #while (i<=(2_000*x) or a[i-1]!=".") and i<len(a) or scopki==1: # or a[i-1]!="…" or a[i-1]!="!" or a[i-1]!=","
            if ( self.multiline ):
                #while (i <= (symbols * x) or text[i - 1] != ".") and i + 1 < len(text):
                buff_i = -99999999999
                while i<len(text) and ( ( ( i - sorted(kol)[-1] ) <= symbols) or ( shovel==1 ) or (text[i] != "\n") ):

                    buff_i, buff_text, buff_kol = self.buff_pass( text, buff_i, i )
                    sdasdasda = text[i]
                    if ( text[i:i+6] == "shade—" ):
                        pass
                    if ( not(buff_kol) and len(buff_text)!=0 ):
                        kol.add(i)
                        i += len(buff_text)
                        break

                    elif ( text[i] in self.brackets[::2] and shovel!=1 and text[i]!="’" ):
                        shovel = 1
                        additional_check_index = self.brackets[::2].index(text[i])
                    elif ( text[i] in self.brackets[1::2] and shovel!=0 and additional_check_index == self.brackets[1::2].index(text[i]) ):
                        shovel = 0
                    if ( not( ( i - sorted(kol)[-1] ) <= symbols) and text[i] == "\n" ):
                        break
                    i += 1
            else:
                while (i <= (symbols * x) or not(text[i - 1] in {'.', '。'}) ) and i + 1 < len(text) and (text[i] != "\n"):
                    i += 1
            try:

                while text[i] == "\n":
                    sadsdasd = text[i-2]
                    sadsdasd1 = text[i - 1]
                    sadsdasd2 = text[i]
                    sadsdasd3 = text[i + 1]
                    i += 1
            except:
                pass
            if (i < len(text) and text[i] != "\n") or i==len(text):
                #print(i, len(text))
                kol.add(i)
            #i += 1
        kol = sorted(kol)
        return kol

    def __read_config_file(self):
        try:
            with open(self.config_file, encoding='utf-8') as file:
                text = ""
                for i in file:
                    for q in i:
                        text += str(q)
                        break
                    break
        except Exception as err:
                print('Ошибка в __read_config_file:\n', err)
                with open(self.config_file, "w+", encoding='utf-8') as file:
                    file.write("")
        with open(self.config_file) as file:
            for x in file:
                self.buff_all.add(int(x))
        self.buff_all = sorted(self.buff_all)[1:]  # Удаляем первый элемент

    def check_punctuation_marks(self, text_original):
        buff_symbol_begin = str()
        buff_symbol_end = str()
        for i in text_original:
            if not ( i.isalpha() ) : #and i!=" "
                buff_symbol_begin += str(i)
            else:
                break
        for i in text_original[::-1]:
            if not ( i.isalpha()) : #and i!=" "
                buff_symbol_end += str(i)
            else:
                break
        return buff_symbol_begin, buff_symbol_end[::-1]

    def checks(self, buff_a, simf):
        try:
            while True:
                buff_a.remove(simf)
        except:
            pass
    def check(self, text, prompt):
        prompt = prompt.replace("\n", "\n\n")
        #for i in range(len(text)):
        try:
            for x in range(10, 2, -1):
                text = text.replace("\n" * x, "\n\n")
        except:
            pass
        #for i in range(len(prompt)):
        try:
            for x in range(10, 2, -1):
                prompt = prompt.replace("\n" * x, "\n\n")
        except:
            pass
        text   = text.split("\n\n")
        #prompt = prompt.replace("\n", "\n\n")
        prompt = prompt.split("\n\n")


        self.checks(text, '\n')
        self.checks(text, ' ')
        self.checks(text, '')
        arr_text = text
        self.checks(prompt, '\n')
        self.checks(prompt, ' ')
        self.checks(prompt, '')
        arr_prompt = prompt

        if ( len( arr_text ) != len( arr_prompt ) ):
            print ( "ERROR check" )
            return 0

        for i in range( len(arr_text) ):
            buff_text = self.check_punctuation_marks( arr_text[i] )
            buff_prompt = self.check_punctuation_marks( arr_prompt[i] )
            if ( buff_prompt[0] != "" ):
                arr_prompt[i] = arr_prompt[i].replace( buff_prompt[0], buff_text[0],1)
            else:
                arr_prompt[i] = buff_text[0] + arr_prompt[i]

            if ( buff_prompt[1] != "" ):
                arr_prompt[i] = arr_prompt[i][::-1]
                arr_prompt[i] = arr_prompt[i].replace(buff_prompt[1][::-1], buff_text[1][::-1],1)
                arr_prompt[i] = arr_prompt[i][::-1]
            else:
                arr_prompt[i] += buff_text[1]
            """
            if ( buff_prompt[0] != "" ):
                arr_prompt[i] = arr_prompt[i].replace( buff_prompt[0], buff_text[0])
            else:
                arr_prompt[i] = buff_text[0] + arr_prompt[i]

            if ( buff_prompt[1] != "" ):
                arr_prompt[i] = arr_prompt[i].replace(buff_prompt[1], buff_text[1])
            else:
                arr_prompt[i] += buff_text[1]
            
            if not( len(buff_text[0]) == len( buff_prompt[0] ) and len(buff_text[1]) == len( buff_prompt[1] ) ):
                arr_prompt[i]= arr_prompt[i].replace( buff_prompt[0], buff_text[0])
                arr_prompt[i] = arr_prompt[i].replace(buff_prompt[1], buff_text[1])
            """


        answer = ""
        for i in arr_prompt:
            answer += i+"\n\n"

        return answer
        """
        if ( self.multiline ):
            buff_text = text.split("\n\n")
            buff_prompt = prompt.split("\n\n")
            for i in range ( len(buff_text) ):

                if (buff_text[i] == buff_text[i].lower()):

                    if (buff_prompt[i].split()[0] != buff_prompt[i].split()[0].lower()):
                        buff_prompt[i] = buff_prompt[i].split()
                        buff_prompt[i][0] = buff_prompt[i][0].lower()
                        buff = ""
                        for x in buff_prompt[i]:
                            buff += x + " "
                        buff_prompt[i] = buff

                if not (buff_text[i][0] in self.alf) and not (buff_text[i][len(buff_text[i]) - 1] in self.alf):

                    if (buff_prompt[i][len(buff_prompt[i]) - 1] in self.alf) and (buff_prompt[i][0] in self.alf):
                        buff_prompt[i] = buff_text[i][0] + buff_prompt[i] + buff_text[i][len(buff_text[i]) - 1]
                    elif ((buff_prompt[i][len(buff_prompt[i]) - 1] in self.alf)):
                        buff_prompt[i] = buff_prompt[i] + buff_text[i][len(buff_text[i]) - 1]
                    elif (buff_prompt[i][0] in self.alf):
                        buff_prompt[i] = buff_text[i][0] + buff_prompt[i]
            
            if ( len(buff_prompt) != 0 ):
                prompt = ""
                for i in buff_prompt:
                    prompt += i+"\n\n"

            return prompt
            

        else:
            if (text == text.lower()):

                if (prompt.split()[0] != prompt.split()[0].lower()):
                    prompt = prompt.split()
                    prompt[0] = prompt[0].lower()
                    buff = ""
                    for x in prompt:
                        buff += x + " "
                    prompt = buff

            if not (text[0] in self.alf) and not (text[len(text) - 1] in self.alf):

                if (prompt[len(prompt) - 1] in self.alf) and (prompt[0] in self.alf):
                    prompt = text[0] + prompt + text[len(text) - 1]
                elif ((prompt[len(prompt) - 1] in self.alf)):
                    prompt = prompt + text[len(text) - 1]
                elif (prompt[0] in self.alf):
                    prompt = text[0] + prompt

                return prompt
        """

    def __get_prompt(self, text, error=1, visual=None):
        if visual==None:
            visual = self.visual
        if (visual):
            print("Проверка:", "\n" + text)

        buff_kol = sum(1 for i in text if i.isalpha())
        if buff_kol == 0:
            return text
        if ( len(text)>15000 ):
            sys.exit("Слишком много текста")
        time.sleep(random.randint(2, 5))
        # text = text.replace("\n\n", "\n")


        buff_x = False
        # prompt = str("Переведи на русский, сделав его более плавным и естественным, даже если считаешь это звуком:" + "\n" + text)
        prompt = str(self.prompt_get_prompt + "\n" + text)
        i = 0
        while not buff_x or not (error):
            try:
                if i > 1 and False:
                    # buff_answer = asyncio.run(self.test("Мне нужен prompt для нейросети, чтобы это слово: " + prompt + " было полность переведено (точнее, чтобы ни одной англиской буквы не было в его составе)." + ("." * (i - 5))))
                    buff_answer = self.test(self.prompt_error_1 + " " + prompt + " " + self.prompt_error_2 + ("." * (i - 2)), browser = "firefox2.exe")
                    prompt = str(buff_answer + ":\n" + text)
                    if (visual):
                        print('\n')
                        print("Новый промпт:", buff_answer)
                elif i > 2:
                    buff_text = text.split("\n\n")
                    for x in range(len(buff_text)):
                        try:
                            if (len(buff_text[x]) == 0 or not (
                                    any(buff_text[x][i].isalpha() for i in range(len(buff_text[x]))))):
                                self.checks(buff_text, buff_text[x])
                        except:
                            break
                    answer = ""
                    for x in buff_text:
                        answer += self.__get_prompt(x,visual=False) #+ "\n\n"
                    pass

                elif i > 3:
                    self.exit = 1
                    barrier.wait()
                    sys.exit()

                if not (i > 2):
                    answer = self.test(prompt, browser = "firefox2.exe", headless = False) #, headless = False
                if (self.verification):
                    error = self.check(text, answer)
                buff_x = True
                i += 1

            except Exception as err:
                print('Ошибка get_prompt:\n', err)
                i += 1
                time.sleep(random.randint(5, 10))
        if (visual and self.verification):
            print("1: ", answer)

        if (self.verification):
            answer = self.check(text, answer)

        if (answer == 0):
            self.__get_prompt(text, answer)

        if (visual and self.verification):
            print("2: ", answer)
            print()

        return answer

    def write_translated_text(self, prompt, config_file = None ):
        if ( config_file == None ):
            config_file = self.config_file
        try:
            with open(config_file, encoding='utf-8') as file:
                text = file.read().splitlines()
                #text = ""
                #for i in file:
                #    for q in i:
                #        text += str(q)
                #        break
                #    break
        except Exception as err:
                print('Ошибка в write_translated_text:\n', err)
                with open(config_file, "w+", encoding='utf-8') as file:
                    file.write("")
        buff_kol = sum(1 for i in prompt if i.isalpha())
        if (self.remove_lines_with_0_characters and buff_kol==0):
            return
        with open(config_file, "a", encoding="utf-8") as file:
            #print(prompt)
            file.write(prompt)
            file.write("\n\n")

    def translate(self):
        #self.setBuffALL()
        #self.read_original_file()
        #self.kol.append( self.process_text() )
        #self.__read_config_file()
        self.read_original_file()
        self.kol = (self.process_text())
        self.setBuffALL()
        self.__read_config_file()

        self.buff_interval = self.kol.index(self.buff_all[-1]) + 1 if self.buff_all else 1
        if self.buff_interval == len(self.kol):
            self.exit = 1
            barrier.wait()
            sys.exit("Завершение программы Translate")
        for x in range( self.buff_interval, len(self.kol) ):
            if ( self.visual ):
                print("x", x)

            """
            if self.prov(self.text, self.kol, x):
                with open(self.translated_file, "a", encoding="utf-8") as file:
                    file.write(self.text[ self.kol[x - 1]:self.kol[x] ])
                    file.write("\n\n")
                print("x", x)
                print()
            else:
            """
            self.original_text.append( self.text[self.kol[x - 1]:self.kol[x]] )
            self.prompt.append( self.__get_prompt( self.text[ self.kol[x - 1]:self.kol[x] ] ) )
            #self.write_translated_text(prompt)
            if ( self.visual ):
                print("x", x)
                print()
                print()
            self.buff_kol.append(self.kol[x])
            if ( self.buff_threading and (self.verification) ):
                barrier.wait()
                self.buff_threading=0
            if ( not(self.verification) ):
                self.write_translated_text(self.prompt[-1], self.translated_file)
                self.update_config_file(self.buff_kol[-1])
            #barrier.wait()
            #time.sleep(random.randint(2, 5))

    def print_text(self):

        self.read_original_file()
        self.kol = (self.process_text())
        self.setBuffALL()
        self.__read_config_file()

        self.buff_interval = self.kol.index(self.buff_all[-1]) + 1 if self.buff_all else 1

        for x in range(self.buff_interval, len(self.kol)):
            print("x", x)
            print( (self.text[self.kol[x - 1]:self.kol[x]]) )
            print( len( self.text[self.kol[x - 1]:self.kol[x]] ) )
            # self.write_translated_text(prompt)
            print("x", x)
            print()
            print( "----------------------------------------------------------------------" )
            print()

    def update_config_file(self, new_index):
        try:
            with open(self.config_file, encoding='utf-8') as file:
                text = file.read().splitlines()
                # text = ""
                # for i in file:
                #    for q in i:
                #        text += str(q)
                #        break
                #    break
        except Exception as err:
                print('Ошибка в update_config_file:\n', err)
                with open(self.config_file, "w+", encoding='utf-8') as file:
                    file.write("")

        with open(self.config_file) as file:
            self.buff_all = {int(x) for x in file}
        self.buff_all.add(new_index)
        with open(self.config_file, 'w') as file:
            for x in sorted(self.buff_all):
                file.write(f"{x}\n")


    def get_Translate(self):
        return self.prompt
    def set_Translate(self, prompt) -> None:
        self.prompt = prompt

    def get_OriginalText(self):
        return self.original_text

    async def DDG(self,model, prompt):
        # global text
        async with DuckChat(self.proxy,model=model) as chat:
            resp = await chat.ask_question(prompt)
            if ( self.visual ):
                print(resp)
            await chat._session.close()
            return resp

    def test(self,prompt, path = "D:/Tor Browser 1/Browser/", headless = False, browser = "firefox1.exe"):
        #if ( model == None ):
        #    model = "gpt-4o-mini"
        #return await self.DDG(model, prompt)
        DT = DuckChat_Tor(path, headless, "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1", browser = browser)
        return DT.GetPrompt(prompt)

"""
    def __del__(self):
        if ( len(self.prompt)>0 ):
            for i in range(0,len(self.prompt)):
                self.write_translated_text( self.prompt[i], self.translated_file )
                #self.update_config_file( self.kol[i+1] )
"""

class Second_Round_Of_Testing(Transleta):
    #def __init__(self, transleta, config_file):
    #    self.transleta = transleta
    #    self.index = 0
    #    self.config_file = config_file

    def _get_prompt(self, original_text, zero_prompt, visual=None):
        if visual==None:
            visual = self.visual
        #print("Проверка В Second_Round_Of_Testing:", text)
        #original_text = original_text.replace( "\n", " " )
        #zero_prompt = zero_prompt.replace("\n", " ")
        buff_kol = sum( 1 for i in original_text if (i.isalpha()) )
        if buff_kol == 0:
            answer = original_text
            if (visual):
                print("3: ", answer)
                print("4: ", answer)
                print()
            return 1
        time.sleep(random.randint(2, 5))
        # text = text.replace("\n\n", "\n")
        # оригинал подходит такой перевод: " перевод "
        buff_x = False
        #prompt = str( original_text + " подходит такой перевод: " + '"' + zero_prompt + '".' + ' Пиши на русском, если перевод соответствует оригиналу или твои изменения лишь в пунктуации, то напиши "подходит". Никогда не пиши "Не подходит.", просто твой исправленный вариант.')
        prompt = str( '"' + original_text + '". ' + self.prompt_check_1 + " " + '"' + zero_prompt + '".' + " " + self.prompt_check_2)
        i=0
        while not buff_x:
            try:
                if not (i > 2):
                    answer = self.test(prompt,"D:/Tor Browser 2/Browser/", True, browser = "firefox3.exe")
                if ( i>2 ):
                    return zero_prompt
                #error = self.check(original_text, answer)
                buff_x = True
                i += 1
            except Exception as err:
                print('Ошибка в проверке:\n', err)
                i += 1
                time.sleep(random.randint(5, 10))
        """i = 0
        while not buff_x:
            try:
                answer = asyncio.run(self.test(prompt))
                buff_x = True
            """
        if (visual):
            print("3: ", answer)
        if ( not( ("Подходит").lower() in answer.lower() ) ):
            answer = self.check(original_text, answer)
        if (answer == 0):
            self._get_prompt(text, answer)
        if (visual):
            print("4: ", answer)
            print()

        return answer

    #(original_text + "\n" + "-+-+-------- " + zero_prompt + "\n" + prompt + "\n\n\n")
    def update_config_file_reprompt(self, original_text, zero_prompt, prompt=None):
        # original_text = original_text.replace("\n", "")
        buff_all = set()
        try:
            with open(self.config_file_check, encoding='utf-8') as file:
                text = ""
                for i in file:
                    for q in i:
                        text += str(q)
                buff_all.add(text)
        except Exception as err:
            print('Ошибка в update_config_file_prompt:\n', err)
            with open(self.config_file_check, "w+", encoding='utf-8') as file:
                file.write("")
        text = ""
        for i in buff_all:
            text += i

        buff_original_text = original_text.split("\n\n")
        if prompt!=None:
            buff_zero_prompt = prompt.split("\n\n")
        else:
            buff_zero_prompt = zero_prompt.split("\n\n")
        text_prompt = ""
        self.checks(buff_original_text, ' ')
        self.checks(buff_original_text, '')
        self.checks(buff_zero_prompt, ' ')
        self.checks(buff_zero_prompt, '')

        if ( len(buff_original_text)!=len(buff_zero_prompt) ):
            print("Ошибка в загрузке текста в файл, не соответсвует оригинальный текст и переработанный:\n")
            print( "Оригинал: " + buff_original_text )
            print("Переработанный: " + buff_zero_prompt)
            print("Закройте программу")
            barrier.wait()


        if prompt!=None:
            #text = text + (original_text + "\n" + "-+-+-------- " + zero_prompt + "\n" + prompt + "\n\n\n")
            for x in range(len(buff_original_text)):
                text += buff_original_text[x] + "\n\n" + buff_zero_prompt[x] + "\n\n"
            text += "\n\n+-+-+-+-+--------------" + zero_prompt + "\n\n\n"

        else:
            while zero_prompt[0] == "\n":
                zero_prompt = zero_prompt.replace("\n","",1)
            for x in range(len(buff_original_text)):
                text += buff_original_text[x] + "\n\n" + buff_zero_prompt[x] + "\n\n"
            text += "\n\n\n"
            #if ( zero_prompt[0] != "\n" ):
            #    text = text + (original_text + "\n\n" + zero_prompt + "\n\n\n")
            #else:
            #    text = text + (original_text + "\n" + zero_prompt + "\n\n\n")
        # buff_all = list(buff_all)

        with open(self.config_file_check, 'w', encoding="utf-8") as file:
            file.write(text + "\n")
            # for x in (buff_all):
            #    file.write(f"{x}\n")

    def update_config_file_prompt(self, original_text, zero_prompt):
        #original_text = original_text.replace("\n", "")
        buff_all = set()
        try:
            with open(self.config_file_check, encoding='utf-8') as file:
                text = ""
                for i in file:
                    for q in i:
                        text += str(q)
                buff_all.add(text)
        except Exception as err:
                print('Ошибка в update_config_file_prompt:\n', err)
                with open(self.config_file_check, "w+", encoding='utf-8') as file:
                    file.write("")
        text = ""
        for i in buff_all:
            text += i
        text = text + (original_text + "\n" + zero_prompt + "\n\n\n")
        #buff_all = list(buff_all)

        with open(self.config_file_check, 'w', encoding="utf-8") as file:
            file.write(text + "\n")
            #for x in (buff_all):
            #    file.write(f"{x}\n")

    def SROTesting(self):

        index = 0
        barrier.wait()
        while index < (len(self.kol) - self.buff_interval):
            if ( self.exit ):
                sys.exit()
            try:
                #self.original_text = []
                #self.prompt = []
                #print( "-------------\n" + "33: Готово" + "-------------\n" )
                prompt = self._get_prompt( self.original_text[index], self.prompt[index] )
                #print("-------------\n" + "44: Готово" + "-------------\n")
                try:
                    if ( (prompt) == 1 ):
                        self.write_translated_text(self.prompt[index], self.translated_file)
                        self.update_config_file(self.buff_kol[index])
                        index += 1
                        #print("-------------\n" + "55: Готово" + "-------------\n")
                        continue
                except:
                    time.sleep(0.01)
                #print( not( ("Подходит").lower() in prompt.lower() ) )
                #print( not( prompt ) )
                #print( self.transleta.prompt[self.index] != prompt )
                if ( not( ("Подходит").lower() in prompt.lower() ) and self.prompt[index] != prompt ):
                    self.update_config_file_reprompt(self.original_text[index], self.prompt[index], prompt)
                    self.prompt[index] = prompt
                else:
                    self.update_config_file_reprompt(self.original_text[index], self.prompt[index])
                if (len(self.prompt) > 0):
                    self.write_translated_text(self.prompt[index], self.translated_file)
                    self.update_config_file(self.buff_kol[index])
                index += 1

                #print("-------------\n" + "66: Готово" + "-------------\n")
                #barrier.wait()
                time.sleep(random.randint(2, 5))
            except Exception as err:
                print('Ошибка в SROTesting:\n', err)
                time.sleep(random.randint(5, 10))

    #def __del__(self):
    #    for i in range( len(self.transleta.prompt) ):
    #        self.transleta.write_translated_text( self.transleta.prompt[i] )
    #    del( self.transleta )

class Already_Done_Second_Round_Of_Testing(Second_Round_Of_Testing):
    """
            for x in range( 1, len(index) ):
                buff_text = ""
                for i in range(index[x - 1], index[x]):
                    buff_text += " " + file_original_2[i]
                refile.append(buff_text)
            refile.append(buff_text)
            return refile"""

    def adjusting_paragraph_breaks(self, file, alf):
        refile = []
        file_original_2 = []
        for x in range(len(file)):
            buff_text = ""
            for i in range(len(file[x])):
                if (len(buff_text) != 0 and i + 1 < len(file[x]) and (not (buff_text[-1].isalpha()) and (file[x][i + 1].lower() != file[x][i + 1] and file[x][i + 1].isalpha()) and (file[x][i - 1] != ",")) and file[x][i] == " "):
                    buff_text += file[x][i]
                buff_text += file[x][i]
            for i in buff_text.split("  "):
                file_original_2.append(i)
            file_original_2[-1] += "\n\n"
        return file_original_2

    def print_asdasd(self, original_file, translated_file):
        for x in range ( len(translated_file) ):
            print( original_file[x], "\n", translated_file[x] )
            print( "-------------------------------------------------------------------------------------------------" )

    def paragraphing(self, file, translated_file, alf, alf_2):
        text = str()
        textt = str()
        buff_index = 0
        index = [0]
        refile = []
        refilet = []
        #file_original_2 = []
        #file_translate_2 = []
        file_original_2 = self.adjusting_paragraph_breaks(file, alf)
        file_translate_2 = self.adjusting_paragraph_breaks(translated_file, alf_2)
        self.print_asdasd( file_original_2, file_translate_2 )
        '''
        for x in range(len(file)):
            buff_text = ""
            for i in range(len(file[x])):
                if (len(buff_text) != 0 and i + 1 < len(file[x]) and (not (buff_text[-1].lower() in alf) and (file[x][i + 1].lower() != file[x][i + 1] and file[x][i + 1].lower() in alf) and (file[x][i - 1] != ",")) and file[x][i] == " "):
                    buff_text += file[x][i]
                buff_text += file[x][i]
            for i in buff_text.split("  "):
                file_original_2.append(i)
            file_original_2[-1] += "\n\n"'''
        if ( len(file_original_2) != len(file_translate_2) ):
            return 0,0
        for x in range( len(file_original_2) ):
            buff_index += 1
            buff_kol = sum(1 for i in file_original_2[x].replace("\n", "") if i.isalpha())
            if buff_kol == 0:
                if (text!=""):
                    refile.append(text)
                refile.append( file_original_2[x] )
                if (textt != ""):
                    refile.append(textt)
                refilet.append(file_translate_2[x])
                #index.append(buff_index - 1)
                index.append(buff_index)
                text = str()
                textt = str()
                continue
            if ( x+1<len(file_original_2) and self.multiline == True and len( text + file_original_2[x+1] ) <= 2000 ):
                text += " "+str( file_original_2[x] )
                textt += " " + str(file_translate_2[x])
            elif ( x+1<len(file_original_2) and self.multiline == False and len( text + file_original_2[x] ) <= 200 ):
                text += " "+str( file_original_2[x] )
                textt += " " + str(file_translate_2[x])
            else:
                if ( text!="" ):
                    refile.append( text+" "+str( file_original_2[x] ) )
                if (textt != ""):
                    refilet.append( textt+" " + str(file_translate_2[x]) )
                index.append(buff_index)
                text = ""
        '''if ( text!="" ):
            refile.append(text)
            index.append(buff_index)'''
        return refile, refilet #self.adjusting_paragraph_breaks( translated_file, index, alf_2 )


    def string_identity_check(self):

        with open(self.original_file, encoding='utf-8') as file:
            buff = file.read().splitlines()
        try:
            while True:
                buff.remove('')
                #print(nums)
        except:
             original_file = buff

        with open( self.translated_file, encoding='utf-8' ) as file:
            buff = file.read().splitlines()
        try:
            while True:
                buff.remove('')
                #print(nums)
        except:
             translated_file = buff

        if ( len( original_file )==len( translated_file ) ):
            return original_file,translated_file
        return 0

    def update_config_file_config_file_check_index(self, index):
        try:
            with open(self.config_file_check_index, encoding='utf-8') as file:
                text = ""
                for i in file:
                    for q in i:
                        text += str(q)
                        break
                    break
        except Exception as err:
                print('Ошибка в update_config_file_config_file_check_index:\n', err)
                with open(self.config_file_check_index, "w+", encoding='utf-8') as file:
                    file.write("")
        with open(self.config_file_check_index, 'w', encoding="utf-8") as file:
            file.write(f"{index}")

    def __read_config_file(self):
        try:
            with open(self.config_file_check_index) as file:
                for x in file:
                    buff_all = int( x.replace( "\n","" ) )
            return buff_all
        except:
            return 0

    def ADSROTesting(self):
        if self.string_identity_check():
            original_file,translated_file = self.string_identity_check()

            original_file,translated_file = self.paragraphing( original_file, translated_file, self.alf, self.alf_ru )

            if ( len( original_file ) != len( translated_file ) ):
                self.print_asdasd( original_file, translated_file)
                return 0

            for i in range ( self.__read_config_file(), len(translated_file) ):
                if (self.visual):
                    print()
                    print( "I:" , i )
                prompt = self._get_prompt(original_file[i], translated_file[i])
                if (prompt == 1):
                    self.write_translated_text(translated_file[i], self.translated_file_check)
                    self.update_config_file_config_file_check_index(i+1)
                    continue
                if (not (("Подходит").lower() in prompt.lower()) and translated_file[i] != prompt):
                    translated_file[i] = prompt
                    self.update_config_file_reprompt(original_file[i], translated_file[i], prompt)
                else:
                    self.update_config_file_prompt(original_file[i], translated_file[i])
                self.write_translated_text( translated_file[i], self.translated_file_check )
                self.update_config_file_config_file_check_index( i+1 )

def file_account(config):
    try:
        with open(config, encoding='utf-8') as file:
            text = file.read().splitlines()
            # text = ""
            # for i in file:
            #    for q in i:
            #        text += str(q)
            #        break
            #    break
        with open(config, encoding='utf-8') as file:
            original_file = ( (file.readline()).replace( "original_file= ", "" ) ).replace("\n","")
            config_file = ( (file.readline()).replace("config_file= ", "") ).replace("\n","")
            translated_file = ( (file.readline()).replace("translated_file= ", "") ).replace("\n","")
            multiline = eval( ( (file.readline()).replace("multiline= ", "") ).replace("\n","") )
            already_done = eval( ( (file.readline()).replace("already_done= ", "") ).replace("\n","") )
            translate = eval(((file.readline()).replace("translate= ", "")).replace("\n", ""))
            symbols_NoMultiline = int(((file.readline()).replace("symbols_NoMultiline= ", "")).replace("\n", ""))
            symbols_multiline = int(((file.readline()).replace("symbols_multiline= ", "")).replace("\n", ""))
            visual = eval( ((file.readline()).replace("visual= ", "")).replace("\n", "") )
            remove_lines_with_0_characters = eval(((file.readline()).replace("remove_lines_with_0_characters= ", "")).replace("\n", ""))
            prompt = ((file.readline()).replace("prompt= ", "")).replace("\n", "")
            prompt_error_1 = ((file.readline()).replace("prompt_error_1= ", "")).replace("\n", "")
            prompt_error_2 = ((file.readline()).replace("prompt_error_2= ", "")).replace("\n", "")
            prompt_check_1 = ((file.readline()).replace("prompt_check_1= ", "")).replace("\n", "")
            prompt_check_2 = ((file.readline()).replace("prompt_check_2= ", "")).replace("\n", "")
    except Exception as err:
        print('Ошибка в file_account:\n', err)
        with open(config, "w+", encoding='utf-8') as file:
            text = ""
            file.write(text)
        with open(config, "w+", encoding='utf-8') as file:
            text += 'original_file=' + " " + '*.txt\n' + 'config_file= *.txt\ntranslated_file= *.txt\nmultiline= True\nalready_done= False\ntranslate= True\nsymbols_NoMultiline= 200\nsymbols_multiline= 1500\n'
            text += "visual=" + " " + "False\n"
            text += "remove_lines_with_0_characters=" + " " + "False\n"
            text += 'prompt=' + " " + 'Переведи на русский, сделав его более плавным и естественным, даже если считаешь это звуком:\n'
            text += 'prompt_error_1=' + " " + 'Мне нужен prompt для нейросети, чтобы это слово:\n' + 'prompt_error_2=' + " " + 'было полность переведено (точнее, чтобы ни одной англиской буквы не было в его составе).\n'
            text += 'prompt_check_1=' + " " + 'подходит такой перевод:\n'
            text += str("prompt_check_2=" + " " + 'Пиши на русском, если перевод соответствует оригиналу или твои изменения лишь в пунктуации, то напиши "подходит". Никогда не пиши "Не подходит.", просто твой исправленный вариант.')
            file.write(text)
            sys.exit()
            '''
            text += 'original_file= .txt\nconfig_file= .txt\ntranslated_file= .txt\nmultiline= True\nalready_done= False\ntranslate= True\nsymbols_NoMultiline= 200\nsymbols_multiline= 1500\n'
            text += "visual= False\n"
            text += 'prompt= Переведи на русский, сделав его более плавным и естественным, даже если считаешь это звуком:\n'
            text += 'prompt_error_1= Мне нужен prompt для нейросети, чтобы это слово: \nprompt_error_2=  было полность переведено (точнее, чтобы ни одной англиской буквы не было в его составе).\n'
            text += 'prompt_check_1=  подходит такой перевод: \n'
            text += str("prompt_check_2=" + ' Пиши на русском, если перевод соответствует оригиналу или твои изменения лишь в пунктуации, то напиши "подходит". Никогда не пиши "Не подходит.", просто твой исправленный вариант.')
            file.write(text)
            sys.exit()
            '''
    return (original_file, config_file, translated_file, multiline, already_done, translate, symbols_NoMultiline, symbols_multiline, visual, remove_lines_with_0_characters, prompt,
            prompt_error_1,
            prompt_error_2,
            prompt_check_1,
            prompt_check_2)





def main():
    #already_done = True #False
    #transl = True
    (original_file, config_file, translated_file, multiline, already_done, transl, symbols_NoMultiline, symbols_multiline, visual, remove_lines_with_0_characters, prompt, prompt_error_1,
     prompt_error_2, prompt_check_1, prompt_check_2) = file_account( "config.txt" )

    prompts = [ prompt, prompt_error_1, prompt_error_2, prompt_check_1, prompt_check_2 ]
    symbols = [ symbols_NoMultiline, symbols_multiline ]

    if ( already_done and transl ):
        translate = Already_Done_Second_Round_Of_Testing( original_file,config_file, translated_file,  multiline = multiline, prompts = prompts, visual = visual, symbols = symbols, remove_lines_with_0_characters=remove_lines_with_0_characters )

        translate.print_text()
        return 0

        translate.ADSROTesting()
        #translate = Transleta("20/20.txt", "20/example.txt", "20/20r.txt", multiline=True)
        #translate.print_text()
    elif ( transl ):
        translate = Second_Round_Of_Testing( original_file, config_file, translated_file, multiline = multiline, prompts = prompts, visual = visual, symbols = symbols, remove_lines_with_0_characters=remove_lines_with_0_characters )
        # SROT=Second_Round_Of_Testing(translate, "19/exampleCheck.txt")
        # translate.translate()
        # SROT.SROTesting()

        #translate.print_text()
        #return 0

        t1 = threading.Thread(target=translate.translate, args=())
        t2 = threading.Thread(target=translate.SROTesting, args=(), daemon = True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        translate = Transleta( original_file, config_file, translated_file, multiline = multiline, prompts = prompts, visual = visual, verification=False, symbols = symbols, remove_lines_with_0_characters=remove_lines_with_0_characters )

        translate.print_text()
        return 0

        t1 = threading.Thread(target=translate.translate, args=())
        t1.start()
        t1.join()



    #print( translate.get_Translate() )
# оригинал подходит такой перевод: " перевод "

if __name__ == "__main__":
    main()


'''
file_original="19/19.txt"
file_config="19/example.txt"
file_translet="19/19r.txt"

f = open(file_original, encoding='utf-8')

a = ""



for i in f:
    a+=str(i)
for x in range(500,0,-1):
    a= a.replace(f'Page | {x}','')

kol = {0}
razr = 0
i=0
scopki = 0
"""
for x in range(50):
    if ( a[x]=="\n"):
        print(a[x-1], a[x+1])
"""

print(len(a))
print( a[91] )
#for x in range (1,1000):
for x in range ( 1,len(a) ):
    #while (i<=(2_000*x) or a[i-1]!=".") and i<len(a) or scopki==1: # or a[i-1]!="…" or a[i-1]!="!" or a[i-1]!=","
    while (i<=(200*x) or a[i-1]!="." ) and i+1 < len(a) and (a[i] != "\n") :
        #print("i=",i)
        asdasfafdaswf = a[i]
        asdasda = a[sorted(kol)[len(kol)-1]:i]
        i+=1
    #asdasdasdfaf = a[i]
    #asdasfafdaswf2131 = a[i]
    #kol1 = sorted(kol)
    #asdasda = a[ kol1[ len(kol1)-2 ]:  kol1[len(kol1)-1]  ]
    if ( i<len(a) and a[i-1]!="\n" ):
        kol.add(i)
    i += 1

print(len(a))

kol = sorted(kol)
print(kol)
print("Длинна: ",len(kol))
asd={-9999999999999}
with open(file_config) as file:
    for x in file:
        asd.add(int(x))
asd = sorted(asd)
asd = asd[1:len(asd)]
if ( len(asd)!=0 ):
    iu = kol.index(asd[-1])
    iu+=1
    print(iu, " ", asd[-1])
else:
    iu=1
f.close()

text = ""

async def DDG(model, prompt):
    #global text
    async with DuckChat(model=model) as chat:
          #global text
          #prompt.replace('\n', '')
          resp = await chat.ask_question(prompt)
          #time.sleep(random.randint(2,5))
          #pyperclip.copy(resp)
          print(resp)
          #text = resp
          await chat._session.close()
          return resp


async def test(bs):
        return await DDG("gpt-4o-mini",bs)

def write_translated_text( bs ):
    with open(file_translet, "a", encoding="utf-8") as file:
        print(bs)
        file.write(asyncio.run(test(bs)))
        file.write("\n\n")
        # print(asyncio.run(test(bs)))
        # file.write(pyperclip.paste())

    print("x", x)
    print()
    print()

def prov ( text, kol,x ):
    alf = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
    alf = alf.split(" ")
    alf_ru = "а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я"
    alf_ru = alf_ru.split(" ")
    buff_kol = 0
    for i in text[kol[x - 1]:kol[x]]:
        if ( i.lower() in alf ):
            buff_kol+=1
    if ( buff_kol==0 ):
        return 1
    return 0


''''''
print()
for x in range (iu,len(kol)):
    print("x", x)
    bs = ""
    if ( prov(a,kol,x) ):
        with open(file_translet, "a", encoding="utf-8") as file:
            # print(asyncio.run(test(bs)))
            # file.write(pyperclip.paste())
            file.write(a[kol[x - 1]:kol[x]])
            file.write("\n\n")
        print("x", x)
        print()
    else:
        """
        try:
            if ( int(a[kol[x - 1]:kol[x]])>0 ):
                with open(file_translet, "a", encoding="utf-8") as file:
                    file.write("\n\n")
                    #print(asyncio.run(test(bs)))
                    #file.write(pyperclip.paste())
                    file.write( a[kol[x - 1]:kol[x]] )
                print("x", x)
                print()
        except:"""
        #for char in ("Переведи на русский, сделав его более плавным и естественным! Если встречаешь ковычки - в переводе они также должны присутствовать! Каждый абзац должен разделятся escape:" + "\n" + a[kol[x - 1]:kol[x]] + "\n" + 'Если встречаешь многократное повторение какого-либо предложения или буквы, или очень длинное слово, то в переводе необходимо это сделать 5 раз и достаточно! Если встречается цифра, то необходимо её перенести как отдельный абзац - это обязательно! В переводе не должно быть вообще ни одного оригинального(англиского) слова!!'):  # Если встречаешь ковычки - в переводе они также должны присутствовать!
        for char in ("Переведи на русский, сделав его более плавным и естественным, даже если считаешь это звуком:" + "\n" + a[kol[x - 1]:kol[x]] + "\n"):
            bs += char

        #print(a[kol[x - 1]:kol[x]])
        #pyperclip.copy(a[kol[x - 1]:kol[x]])
        buff_x = False
        while not(buff_x):
            try:
                write_translated_text(bs)
            except Exception as err:
                print('Ошибка:\n', err)
                time.sleep(random.randint(5, 10))
                continue
            buff_x= True



    #time.sleep(1000)
    asd={-9999999999999}
    with open(file_config) as file:
        for x1 in file:
            asd.add(int(x1))
    file = open(file_config, 'w')
    dsa=""
    asd = sorted(asd)
    asd = asd[1:len(asd)]
    for x1 in asd:
        dsa+=str(x1)+"\n"
    file.write(dsa+(str(kol[x])))
    file.close()
    time.sleep(random.randint(2,5))
'''
