# 6.00x Problem Set 6
#
# Part 2 - RECURSION

#
# Problem 3: Recursive String Reversal
#
def reverseString(aStr):
    """
    Given a string, recursively returns a reversed copy of the string.
    For example, if the string is 'abc', the function returns 'cba'.
    The only string operations you are allowed to use are indexing,
    slicing, and concatenation.
    
    aStr: a string
    returns: a reversed string
    """
    if len(aStr) == 1:
        return aStr[0]
    return aStr[-1]+reverseString(aStr[:-1])
print reverseString('abcdef')    
print reverseString('abc')
# Problem 4: X-ian
#
def x_ian(x, word):
    """
    Given a string x, returns True if all the letters in x are
    contained in word in the same order as they appear in x.

    >>> x_ian('eric', 'meritocracy')
    True
    >>> x_ian('eric', 'cerium')
    False
    >>> x_ian('john', 'mahjong')
    False
    
    x: a string
    word: a string
    returns: True if word is x_ian, False otherwise
    """
    letter = x[0]
    if not letter in word:
        return False
    elif len(x) == 1:
        return x in word        
    return x_ian(x[1:], word[word.index(letter)+1:])        
print x_ian('eric', 'meritocracy') 
print x_ian('eric', 'cerium') 
print x_ian('john', 'mahjong')     
#
# Problem 5: Typewriter
#
def insertNewlines(text, lineLength):
    """
    Given text and a desired line length, wrap the text as a typewriter would.
    Insert a newline character ("\n") after each word that reaches or exceeds
    the desired line length.

    text: a string containing the text to wrap.
    line_length: the number of characters to include on a line before wrapping
        the next word.
    returns: a string, with newline characters inserted appropriately. 
    """
    if len(text) < lineLength:
        return text
    return text[:lineLength] + '\n' + insertNewlines(text[lineLength:], lineLength)
    
print insertNewlines('my name is basant soni and my favourite movie is braveheart', 3)    