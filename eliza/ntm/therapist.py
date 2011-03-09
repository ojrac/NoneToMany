#----------------------------------------------------------------------
#   therapist.py
#
#   a cheezy little Eliza knock-off by Joe Strout <joe@strout.net>
#   with some updates by Jeff Epler <jepler@inetnebr.com>
#   last revised: 3/17/97
#----------------------------------------------------------------------

import string
import re
import random

#----------------------------------------------------------------------
# translate: take a string, replace any words found in dict.keys()
#   with the corresponding dict.values()
#----------------------------------------------------------------------
def translate(word, mapping):
    words = string.split(string.lower(word))
    for i in range(0,len(words)):
        if words[i] in mapping.keys():
            words[i] = mapping[words[i]]
    return string.join(words)

#----------------------------------------------------------------------
#   respond: take a string, a set of regexps, and a corresponding
#       set of response lists; find a match, and return a randomly
#       chosen response from the corresponding list.
#----------------------------------------------------------------------
def respond(question, patterns, formats):
    """Test a question against a set of patterns, and apply the first
    matching substitution
    """
    for pattern, substitution in zip(patterns, formats):
        match = pattern.match(question)
        if not match:
            continue

        return make_response(question, match, substitution)

def make_response(question, match, substitution_set):
    """Compose and return a response for the given match object,
    from a list of possible replies
    """
    substitution = random.choice(substitution_set)
    if "%" not in substitution:
        return substitution
    elif "%(" in substitution:
        # use the fancy dict style format
        
        items = match.groupdict()
    else:
        items = match.groups()

    items = fix_pronouns(items)

    return substitution % items

def fix_pronouns(items):
    """Changes the perspective of a dict or tuple of words from user input"""
    if type(items) != dict:
        return tuple([translate(i, G_REFLECTIONS) for i in items])

    for k, v in items.items():
        items[k] = translate(v, G_REFLECTIONS)

    return items

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#       into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
G_REFLECTIONS = {
    "am"    : "are",
    "was"   : "were",
    "i"     : "you",
    "i'd"   : "you would",
    "i've"  : "you have",
    "i'll"  : "you will",
    "my"    : "your",
    "are"   : "am",
    "you've": "I have",
    "you'll": "I will",
    "your"  : "my",
    "yours" : "mine",
    "you"   : "me",
    "me"    : "you" }

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#   two-element list; the first is a regexp, and the second is a
#   list of possible responses, with standard format strings
#----------------------------------------------------------------------
gPats = [
    ["I need (.*)",
    [   "Why do you need %s?",
        "Would it really help you to get %s?",
        "Are you sure you need %s?"]],
    
    ["Why don't you (.*)",
    [   "Do you really think I don't %s?",
        "Perhaps eventually I will %s.",
        "Do you really want me to %s?"]],
    
    ["Why can't I (.*)",
    [   "Do you think you should be able to %s?",
        "If you could %s, what would you do?",
        "I don't know -- why can't you %s?",
        "Have you really tried?"]],
    
    ["I can't (.*)",
    [   "How do you know you can't %s?",
        "Perhaps you could %s if you tried.",
        "What would it take for you to %s?"]],
    
    ["I am (.*)",
    [   "Did you come to me because you are %s?",
        "How long have you been %s?",
        "How do you feel about being %s?"]],
    
    ["I'm (.*)",
    [   "How does being %s make you feel?",
        "Do you enjoy being %s?",
        "Why do you tell me you're %s?",
        "Why do you think you're %s?"]],
    
    ["Are you (.*)",
    [   "Why does it matter whether I am %s?",
        "Would you prefer it if I were not %s?",
        "Perhaps you believe I am %s.",
        "I may be %s -- what do you think?"]],
    
    ["What (.*)",
    [   "Why do you ask?",
        "How would an answer to that help you?",
        "What do you think?"]],
    
    ["How (.*)",
    [   "How do you suppose?",
        "Perhaps you can answer your own question.",
        "What is it you're really asking?"]],
    
    ["because (.*)",
    [   "Is that the real reason?",
        "What other reasons come to mind?",
        "Does that reason apply to anything else?",
        "If %s, what else must be true?"]],
    
    ["(.*) sorry (.*)",
    [   "There are many times when no apology is needed.",
        "What feelings do you have when you apologize?"]],
    
    ["(?:hello|hi)(.*)",
    [   "Hello... I'm glad you could drop by today.",
        "Hi there... how are you today?",
        "Hello, how are you feeling today?"]],
    
    ["I think (.*)",
    [   "Do you doubt %s?",
        "Do you really think so?",
        "But you're not sure %s?"]],
    
    ["(.*) friend(.*)",
    [   "Tell me more about your friends.",
        "When you think of a friend, what comes to mind?",
        "Why don't you tell me about a childhood friend?"]],
    
    ["Yes",
    [   "You seem quite sure.",
        "OK, but can you elaborate a bit?"]],
    
    ["(.*) computer(.*)",
    [   "Are you really talking about me?",
        "Does it seem strange to talk to a computer?",
        "How do computers make you feel?",
        "Do you feel threatened by computers?"]],
    
    ["Is it (.*)",
    [   "Do you think it is %s?",
        "Perhaps it's %s -- what do you think?",
        "If it were %s, what would you do?",
        "It could well be that %s."]],
    
    ["It is (.*)",
    [   "You seem very certain.",
        "If I told you that it probably isn't %s, what would you feel?"]],
    
    ["Can you (.*)",
    [   "What makes you think I can't %s?",
        "If I could %s, then what?",
        "Why do you ask if I can %s?"]],
    
    ["Can I (.*)",
    [   "Perhaps you don't want to %s.",
        "Do you want to be able to %s?",
        "If you could %s, would you?"]],
    
    ["You are (.*)",
    [   "Why do you think I am %s?",
        "Does it please you to think that I'm %s?",
        "Perhaps you would like me to be %s.",
        "Perhaps you're really talking about yourself?"]],
    
    ["You're (.*)",
    [   "Why do you say I am %s?",
        "Why do you think I am %s?",
        "Are we talking about you, or me?"]],
    
    ["I don't (.*)",
    [   "Don't you really %s?",
        "Why don't you %s?",
        "Do you want to %s?"]],
    
    ["I feel (.*)",
    [   "Good, tell me more about these feelings.",
        "Do you often feel %s?",
        "When do you usually feel %s?",
        "When you feel %s, what do you do?"]],
    
    ["I have (.*)",
    [   "Why do you tell me that you've %s?",
        "Have you really %s?",
        "Now that you have %s, what will you do next?"]],
    
    ["I would (.*)",
    [   "Could you explain why you would %s?",
        "Why would you %s?",
        "Who else knows that you would %s?"]],
    
    ["Is there (.*)",
    [   "Do you think there is %s?",
        "It's likely that there is %s.",
        "Would you like there to be %s?"]],
    
    ["My (.*)",
    [   "I see, your %s.",
        "Why do you say that your %s?",
        "When your %s, how do you feel?"]],
    
    ["You (.*)",
    [   "We should be discussing you, not me.",
        "Why do you say that about me?",
        "Why do you care whether I %s?"]],
        
    ["Why (.*)",
    [   "Why don't you tell me the reason why %s?",
        "Why do you think %s?" ]],
        
    ["I want (.*)",
    [   "What would it mean to you if you got %s?",
        "Why do you want %s?",
        "What would you do if you got %s?",
        "If you got %s, then what would you do?"]],
    
    ["(.*) mother(.*)",
    [   "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?",
        "How does this relate to your feelings today?",
        "Good family relations are important."]],
    
    ["(.*) father(.*)",
    [   "Tell me more about your father.",
        "How did your father make you feel?",
        "How do you feel about your father?",
        "Does your relationship with your father relate to your feelings today?",
        "Do you have trouble showing affection with your family?"]],

    ["(.*) child(.*)",
    [   "Did you have close friends as a child?",
        "What is your favorite childhood memory?",
        "Do you remember any dreams or nightmares from childhood?",
        "Did the other children sometimes tease you?",
        "How do you think your childhood experiences relate to your feelings today?"]],
        
    ["(.*)\?",
    [   "Why do you ask that?",
        "Please consider whether you can answer your own question.",
        "Perhaps the answer lies within yourself?",
        "Why don't you tell me?"]],
    
    ["quit",
    [   "Thank you for talking with me.",
        "Good-bye.",
        "Thank you, that will be $150.  Have a good day!"]],
    
    ["(.*)",
    [   "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?",
        "Why do you say that %s?",
        "I see.",
        "Very interesting.",
        "%s.",
        "I see.  And what does that tell you?",
        "How does that make you feel?",
        "How do you feel when you say that?"]]
    ]

#----------------------------------------------------------------------
#   Main program
#----------------------------------------------------------------------

G_KEYS = map(lambda x:re.compile(x[0], re.I),gPats)
G_VALUES = map(lambda x:x[1],gPats)

END_PUNCTUATION_RE = re.compile('[\.!?]+$')
def strip_punctuation(question):
    return END_PUNCTUATION_RE.sub('', question)

def answer(question):
    question = strip_punctuation(question)
    return respond(question, G_KEYS, G_VALUES)
    
def main():
    print "Therapist\n---------"
    print "Talk to the program by typing in plain English, using normal upper-"
    print 'and lower-case letters and punctuation.  Enter "quit" when done.'
    print '='*72
    print "Hello.  How are you feeling today?"
    s = ""
    while s != "quit":
        try: s = raw_input("> ")
        except EOFError:
            s = "quit"
        print answer(s)

if __name__ == "__main__":
    main()
