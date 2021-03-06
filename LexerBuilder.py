import re
import copy


class LexerBuilder():
    __keywords = {}

    __REGULAR_EXPRESSIONS = {}

    __text = ""

    __matched_value = None

    __copied = None

    __token_counter = -1

    __REGEX_IDENTIFIER = re.compile("^[a-zA-Z_$][a-zA-Z_$0-9]*$")

    __REGEX_INTEGER_LITERAL = re.compile(
        "[+-]?[0-9]+")

    __REGEX_FLOAT_LITERAL = re.compile(r"[+-]?[0-9]+\.[0-9]+")

    __BINARY_OPERATORS = ['*', '/', '+',
                          '-', '%', '<', '>', '&', '|', '^', '~']

    __COMPARISON_OPERATORS = ['=', '!', '<', '>']

    __LOGICAL_OPERATORS = ['&', '|', '!']

    __TOKENS = []

    __keyword = ""

    __can_i_add_quotes = False

    __token_identifier = None

    __token_float = None

    __token_integer = None

    __token_string = None

    __token_binary_operator = None

    __token_assignment_operator = None

    __token_comparison_operator = None

    __token_logical_operator = None

    __token_comma = None

    __token_dot = None

    __token_semicolon = None

    __token_colon = None

    __token_bracket = None

    __token_curly_bracket = None

    __token_square_bracket = None

    __comment_char = '\0'

    __end_comment_char = '\0'

    def __init__(self, text):
        self.set_text(text)

    def __matched(self, to_match):
        for key in self.__REGULAR_EXPRESSIONS:
            value = self.__REGULAR_EXPRESSIONS[key]
            if key.match(to_match):
                return value
        return None

    def set_on_identifier(self, token_identifier):
        self.__token_identifier = token_identifier

    def set_on_float_literal(self, token_float):
        self.__token_float = token_float

    def set_on_integer_literal(self, token_integer):
        self.__token_integer = token_integer

    def set_on_string_literal(self, token_string):
        self.__token_string = token_string

    def set_on_binary_operator(self, token_binary_operator):
        self.__token_binary_operator = token_binary_operator

    def set_on_assignment_operator(self, token_assignment_operator):
        self.__token_assignment_operator = token_assignment_operator

    def set_on_comparison_operator(self, token_comparison_operator):
        self.__token_comparison_operator = token_comparison_operator

    def set_on_logical_operator(self, token_logical_operator):
        self.__token_logical_operator = token_logical_operator

    def set_on_comma(self, token_comma):
        self.__token_comma = token_comma
        self.__token_comma.set_text(".")

    def set_on_dot(self, token_dot):
        self.__token_dot = token_dot
        self.__token_dot.set_text(",")

    def set_on_semicolon(self, token_semicolon):
        self.__token_semicolon = token_semicolon
        self.__token_semicolon.set_text(";")

    def set_on_colon(self, token_colon):
        self.__token_colon = token_colon
        self.__token_colon.set_text(":")

    def set_on_bracket(self, token_bracket):
        self.__token_bracket = token_bracket

    def set_on_curly_bracket(self, token_curly_bracket):
        self.__token_curly_bracket = token_curly_bracket

    def set_on_square_bracket(self, token_square_bracket):
        self.__token_square_bracket = token_square_bracket

    def set_comment_char(self, comment_char, end_comment_char):
        self.__comment_char = comment_char
        self.__end_comment_char = end_comment_char

    def add_quotes_to_string_literal(self, __can_i_add_quotes):
        self.__can_i_add_quotes = __can_i_add_quotes

    def set_text(self, text):
        self.__text = text + " "

    def set_keyword(self, keyword, token):
        self.__keywords[keyword] = token

    def set_regex(self, regex, token):
        self.__REGULAR_EXPRESSIONS[re.compile(regex)] = token

    @staticmethod
    def get_identifier_regex():
        return "^[a-zA-Z_$][a-zA-Z_$0-9]*$"

    def remove_keyword(self, keyword):
        if keyword in self.__keywords:
            del self.__keywords[keyword]

    def remove_regex(self, regex):
        compiled_regex = re.compile(regex)
        if compiled_regex in self.__REGULAR_EXPRESSIONS:
            del self.__REGULAR_EXPRESSIONS[compiled_regex]

    def __check(self):
        keyword_to_string = self.__keyword[:self.__keyword.__len__() - 1]
        self.__matched_value = self.__matched(keyword_to_string)
        if keyword_to_string in self.__keywords:
            self.__copied = copy.copy(self.__keywords[keyword_to_string])
            self.__copied.set_text(keyword_to_string)
            self.__TOKENS.append(self.__copied)
        elif self.__matched_value!= None:
            self.__copied = copy.copy(self.__matched_value)
            self.__copied.set_text(keyword_to_string)
            self.__TOKENS.append(self.__copied)
        elif self.__token_float!= None and self.__is_float_literal(keyword_to_string):
            self.__copied = copy.copy(self.__token_float)
            self.__copied.set_text(keyword_to_string)
            self.__TOKENS.append(self.__copied)
        elif self.__token_integer!= None and self.__is_integer_literal(keyword_to_string):
            self.__copied = copy.copy(self.__token_integer)
            self.__copied.set_text(keyword_to_string)
            self.__TOKENS.append(self.__copied)
        elif self.__token_identifier!= None and self.__is_identifier(keyword_to_string):
            self.__copied = copy.copy(self.__token_identifier)
            self.__copied.set_text(keyword_to_string)
            self.__TOKENS.append(self.__copied)

    def __is_integer_literal(self, string):
        return self.__REGEX_INTEGER_LITERAL.match(string)

    def __is_float_literal(self, string):
        return self.__REGEX_FLOAT_LITERAL.match(string)

    def __is_identifier(self, string):
        return self.__REGEX_IDENTIFIER.match(string)

    def get_all_tokens(self):
        self.__TOKENS = []
        self.__keyword = ""
        is_in_string = False
        is_in_comment = False
        write_next_escape_char = False
        i = 0
        while i < self.__text.__len__():
            this_char = self.__text[i]
            if is_in_comment:
                if this_char==self.__end_comment_char:
                    is_in_comment = False
                i += 1
                continue
            if is_in_string:
                if write_next_escape_char:
                    self.__keyword += this_char
                    write_next_escape_char = False
                elif this_char=='\\':
                    write_next_escape_char = True
                elif this_char=='\"':
                    self.__copied = copy.copy(self.__token_string)
                    self.__copied.set_text(self.__keyword)
                    if self.__can_i_add_quotes:
                        self.__copied.set_text(
                            "\"" + self.__copied.get___text() + "\"")
                    self.__TOKENS.append(self.__copied)
                    is_in_string = False
                    self.__keyword = ""
                else:
                    self.__keyword += this_char
                i += 1
                continue
            self.__keyword += this_char
            if this_char!= '\0' and this_char==self.__comment_char:
                is_in_comment = True
            elif self.__token_string!= None and this_char=='\"':
                is_in_string = True
                self.__keyword = ""
            elif str(this_char).isspace():
                self.__check()
                self.__keyword = ""
            elif self.__token_comma!= None and this_char==',':
                self.__check()
                self.__TOKENS.append(self.__token_comma)
                self.__keyword = ""
            elif self.__token_dot!= None and this_char=='.':
                if i > 0:
                    if not str(self.__text[i - 1]).isdigit:
                        self.__check()
                        self.__TOKENS.append(self.__token_dot)
                        self.__keyword = ""
            elif self.__token_semicolon!= None and this_char==';':
                self.__check()
                self.__TOKENS.append(self.__token_semicolon)
                self.__keyword = ""
            elif self.__token_colon!= None and this_char==':':
                self.__check()
                self.__TOKENS.append(self.__token_colon)
                self.__keyword = ""
            elif self.__token_bracket!= None and (this_char=='(' or this_char==')'):
                self.__check()
                self.__copied = copy.copy(self.__token_bracket)
                self.__copied.set_text(str(this_char))
                self.__TOKENS.append(self.__copied)
                self.__keyword = ""
            elif self.__token_curly_bracket!= None and (this_char=='{' or this_char=='}'):
                self.__check()
                self.__copied = copy.copy(self.__token_curly_bracket)
                self.__copied.set_text(str(this_char))
                self.__TOKENS.append(self.__copied)
                self.__keyword = ""
            elif self.__token_square_bracket!= None and (this_char=='[' or this_char==']'):
                self.__check()
                self.__copied = copy.copy(self.__token_square_bracket)
                self.__copied.set_text(str(this_char))
                self.__TOKENS.append(self.__copied)
                self.__keyword = ""
            elif self.__token_comparison_operator!= None and this_char in self.__COMPARISON_OPERATORS and (
                    (i <= self.__text.__len__() - 2) and (
                    self.__text[i + 1]=='=' or (this_char=='<' or this_char=='>') and (
                    self.__text[i + 1]!= '<' and self.__text[i + 1]!= '>'))):
                self.__check()
                self.__copied = copy.copy(self.__token_comparison_operator)
                if this_char=='<' or this_char=='>' and self.__text[i + 1]!= '=':
                    self.__copied.set_text(str(this_char))
                else:
                    self.__copied.set_text(str(this_char + "="))
                    i += 1
                self.__TOKENS.append(self.__copied)
                self.__keyword = ""
            elif self.__token_logical_operator!= None and this_char in self.__LOGICAL_OPERATORS:
                if (this_char=='&' or this_char=='|') and (
                        i <= self.__text.__len__() - 2 and self.__text[i + 1]==this_char):
                    self.__copied = copy.copy(self.__token_logical_operator)
                    self.__copied.set_text(self.__text[i:i + 2])
                    i += 1
                elif this_char=='!' and (i==self.__text.__len__() - 1 or (
                        i <= self.__text.__len__() - 2 and self.__text[i + 1]!= '=')):
                    self.__copied = copy.copy(self.__token_logical_operator)
                    self.__copied.set_text("!")
                self.__TOKENS.append(self.__copied)
                self.__keyword = ""
            elif (
                    self.__token_binary_operator!= None or self.__token_assignment_operator!= None) and \
                    this_char in self.__BINARY_OPERATORS or this_char=='=':
                self.__check()
                is_assignment_operator = False
                if self.__token_assignment_operator!= None:
                    if i <= self.__text.__len__() - 3 and (
                            self.__text[i:i + 3] == "<<=" or self.__text[i:i + 3] == ">>="):
                        self.__copied = copy.copy(
                            self.__token_assignment_operator)
                        self.__copied.set_text(self.__text[i:i + 3])
                        is_assignment_operator = True
                        i += 2
                    elif i <= self.__text.__len__() - 2 and this_char in self.__BINARY_OPERATORS and \
                            self.__text[i + 1]=='=':
                        self.__copied = copy.copy(
                            self.__token_assignment_operator)
                        self.__copied.set_text(self.__text[i:i + 2])
                        is_assignment_operator = True
                        i += 1
                    elif this_char=='=':
                        self.__copied = copy.copy(
                            self.__token_assignment_operator)
                        self.__copied.set_text(str(this_char))
                        is_assignment_operator = True
                if not is_assignment_operator and self.__token_binary_operator!= None:
                    if i <= self.__text.__len__() - 3 and self.__text[i:i + 3] == ">>>":
                        self.__copied = copy.copy(self.__token_binary_operator)
                        self.__copied.set_text(self.__text[i:i + 3])
                        i += 2
                    elif i <= self.__text.__len__() - 2 and (
                            self.__text[i:i + 2] == "<<" or self.__text[i:i + 2] == ">>"):
                        self.__copied = copy.copy(self.__token_binary_operator)
                        self.__copied.set_text(self.__text[i:i + 2])
                        i += 1
                    elif this_char in self.__BINARY_OPERATORS:
                        self.__copied = copy.copy(self.__token_binary_operator)
                        self.__copied.set_text(str(this_char))

                self.__TOKENS.append(self.__copied)
                self.__keyword = ""
            i += 1
        return self.__TOKENS

    def get_next_token(self):
        self.get_all_tokens()
        if self.__TOKENS!= None and self.__token_counter + 1 < self.__TOKENS.__len__():
            self.__token_counter += 1
            return self.__TOKENS[self.__token_counter]
        return None

    def get_current_token(self):
        if self.__token_counter >= 0:
            return self.__TOKENS[self.__token_counter]
        return None

    def has_next_token(self):
        if self.__token_counter+1==self.__TOKENS.__len__():
            return False
        return True
