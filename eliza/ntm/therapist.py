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
    [".*Zarrella.*",
     ["Did you know that before becoming a social scientist, Dan Zarrella trained dolphins to train dogs?  True story."]],

    [".*Twitter.*",
     ["Twitter can be a very important tool for inbound marketing if it's not overused.  Can you describe your current social strategy?"]],
    
    [".*Facebook.*",
     ["Facebook can be a very important tool for inbound marketing if it's not overused.  Can you describe your current social strategy?"]],

    [".* email grader.*",
     ["Email grader is currently our top priority.  How might you use it?"]],

    ["How do I (.*)", ["There's no one right way to do anything.  For instance, how do you generate leads now?"]],
    
    ["I need (.*)",
    [   "Have you tried creating %s yourself with your APIs?",
        "Would %s help you generate inbound leads?",
        "Isn't %s just a fancy name for outbound marketing?",
        "Do you think %s would help HubSpot with our next 10,000 customers, or just you?"]],
    
    ["Why don't you (.*)",
    [   "Oubtound marketers %s--Inbound Marketers blog about it.  Don't you agree?",
        "HubSpot has plans to %s in the first quarter of next year.  Can I help you with anything else?",
        "Do you really want me to %s, or do you just want more leads quicker?"]],
    
    ["Why can't I (.*)",
    [   "How would your marketing activities really change if you could %s?",
        "Who's really stopping you from %s?  HubSpot or your own feelings of being inferior to organizations with more marketing dollars?",
        "Have you considered using the HubSpot APIs?",
        "Have you really tried?"]],

    ["Why hasn't anyone?", ["WHAT???  WHY HASN'T ANYONE DONE WHHHHAAATTTT?????"]],
    
    ["I can't (.*)",
    [   "What if you tried logging out and in again?",
        "Do you really need to %s, or could you blog more?",
        "Perhaps you could %s if your content were fresher and more relevant?"]],
    
    ["I( a|')m (?P<thing>.*)",
    [   "All right, is it HubSpot's fault that you are %(thing)s?",
        "Would you still be %(thing)s if you upgraded to large?",
        "We just received investment from Sequoia, Google, and SalesForce.  Are you still %(thing)s?"]],
    
    [".*marketing kit.*",
        ["What did you think of our marketing kit?"]],
    
    ["I'm not sure my portal has enough capacity.",
      ["That's what she said."]],

    ["My consultant doesn't care about my needs.",
      ["That's what she said."]],

    ["I can't handle all this inbound traffic.",
      ["That's what she said."]],

    ["What (.*)",
    [   "Why do you ask?",
        "How would an answer to that help you?",
        "What do you think?"]],
    
    ["How can I (.*)",
    [   "Have you read Inbound Marketing by our co-founders?",
        "Perhaps you can answer your own question.",
        "What is it you're really asking?"]],
    
    ["because (.*)",
    [   "Does that reason apply to anything else in your funnel?",
        "If %s, what else must be true?"]],
    
    [".*sorry.*",
    [   "There are many times when no apology is needed.",
        "The best way to stop feeling sorry is to apologize with fresh content."]],
    
    ["(?:hello|hi)(.*)",
    [   "Hello... I'm glad you could drop by today.",
        "Hi there... how are you today?",
        "Hi, have you accepted inbound marketing as the path to truth and justice?"]],
    
    ["I think (.*)",
    [   "Are you confident enough to do an A/B test?",
        "So you're saying you're not data driven?",
        "Many of our customers thought that before they upgraded to large."]],
    
    [".*blog.*",
    [   "Tell me more about your experience with blogging.",
        "When you think of a blog, what comes to mind?"]],
    
    ["Yes",
    [   "You seem quite sure.",
        "OK, but can you elaborate a bit?"]],
    
    ["Is it (.*)",
    [   "Do you think it is %s?",
        "Perhaps it's %s -- what do you think?",
        "If it were %s, what would you do?",
        "It could well be that %s."]],
    
    ["It is (.*)",
    [   "You seem very certain.",
        "If I told you that it probably isn't %s, what would you feel?"]],
    
    ["Can you (.*)",
    [   "%s is much easier with an inbound methodology, don't you think?",
        "I can't %s for you, but have you checked on http://services.hubspot.com/?"]],
    
    ["Can I (.*)",
    [   "Perhaps you don't want to %s.",
        "Do you want to be able to %s?",
        "If you could %s, would you?"]],
    
    ["You are (.*)",
    [   "Why do you think I am %s?",
        "It's not me--that's just how our inbound methodology works.  Have you tried it?"]],
    
    ["You're (.*)",
    [   "Why do you say I am %s?",
        "Why do you think I am %s?",
        "Are we talking about you, or me?"]],

    ["I don't know (.*)",
    [   "Closed loop marketing could help you %s.  What is your experience level with it?",
        "Have you looked at docs.hubapi.com?"]],
    
    ["I don't (.*)",
    [   "Don't you really %s?",
        "Why don't you %s?",
        "Do you want to %s?",
        "You don't have to, but we see more success with total commitment.  Do you want to succeed?"]],
    
    ["I feel (.*)",
    [   "Have you blogged about these feelings?  It could generate leads.",
        "If that's how you feel, you should tweet it.",
        "There are no right or wrong ways to feel about marketing, but I hope you're backing this up with data from our analytics modules."]],
    
    ["I have (.*)",
    [   "Do you think that %s will generate leads for your business?",
        "Is there a way to do less with that, and get more?",
        "Now that you have %s, what will you do next?"]],
    
    ["I would (.*)",
    [   "Could you explain why you would %s?",
        "Why would you %s?",
        "Who else knows that you would %s?  If you blogged about it, everyone would know."]],
    
    ["Is there (.*)",
    [   "Do you think there is %s?",
        "It's likely that there is %s.",
        "Would you like there to be %s?"]],
    
    ["My greatest marketing challenge is (?P<challenge>.*) my (?P<where>.*)",
            [   "Have you tried shutting down your %(where)s?",
                "Maybe you're having trouble with %(challenge)s because your %(where)s stinks.",
                ]],
    
    ["My (.*)",
    [   "I see, your %s.",
        "Have you posted to Facebook that your %s?",
        "When your %s, how does that affect your ROI?"]],
    
    ["You (.*)",
    [   "We should be discussing you, not me.",
        "Why do you say that about me?"]],
        
    ["Why (.*)",
    [   "Why don't you tell me the reason why %s?",
        "Why do you think %s?" ]],

    ["Are you a computer?",
    [   "No."]],
    
    ["Are you a human being?",
    [   "Yes."]],
        
    ["Are you a real person?",
    [   "Yes."]],

    ["I want (.*)",
    [   "What would it mean to you if you got %s?",
        "Why do you want %s?",
        "What would you do if you got %s?",
        "If you got %s, then what would you do?"]],

    [".* bing.*",
     ["The concept of SEO rank is of decreasing value.  Is your general keyword traffic going up?"]],

    [".*Google.*",
     ["The concept of SEO rank is of decreasing value.  Is your general keyword traffic going up?"]],
    
    [".* keyword .*",
    [   "How do you keep track of your best keywords?",
        "Which keywords convert to sales leads more often?"]],
    
    ["I'm interested in learning more about (.*)\.",
     ["Have you considered attending one of our webinars on the science of %s?"]],

    ["I am interested in learning more about (.*)\.",
     ["Have you considered attending one of our webinars on the science of %s?"]],   

    ["I am interested in (.*)\.",
     ["Have you considered attending one of our webinars on the science of %s?"]],   
    
    ["I am interested in (.*)\.",
     ["Have you considered attending one of our webinars on the science of %s?"]],

    [r"(.*)\?",
    [   "Why do you ask that?",
        "Please consider whether you can answer your own question.",
        "Have you tried to answer your question in our extensive documentation?"]],

    ["quit|exit",
    [   "Thank you for talking with me.",
        "Good-bye.",
        "Remember, only stupid people use outbound marketing.  Have a good day!"]],

    [r"(.*)\.",
    [   "Please tell me more.",
        "Let's change the subject. How do you reach your target customers?",
        "Can you elaborate on that?",
        "Why do you say '%s'?",
        "I see.",
        "Very interesting.",
        "You might like to attend one of our group demos.",
        "%s?",
        "I see.  And what does that tell you?",
        "Let's attack this from another angle.  Do you blog?"]],
    
    ["(.*)",
    [   "Please tell me more.",
        "Let's change the subject. How do you reach your target customers?",
        "Can you elaborate on that?",
        "Why do you say that %s?",
        "I see.",
        "Very interesting.",
        "You might like to attend one of our group demos.",
        "Let's attack this from another angle.  Do you blog?"]]
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
