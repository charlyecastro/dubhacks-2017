from linguistic import getPOS
from sentiment import getSentiment
from keyphrases import getPhrases
import random

greetings = [ "hi", "hello", "hey", "yo", "greetings" ]
greetings_responses = [ "Hi there." , "Greetings human.", "Hello there.", "Hey." ]
depressed_responses = [ "Do you wanna talk more about that?", "You're gonna be okay", "It's all gonna work out", "I'd love to talk more about that", "I'm here to help you", "It's always darkest before the dawn", "I believe you're capable of anything", "Just keep swimming"]
sad_responses = [ "How can I help?", "What were you looking for?", "Is something upsetting you?", "Why do you think you feel this way?", "You'll be fiiiine", "There's an app for that", "You can always talk to me about it", "Hakuna Matata"]
happy_responses = [ "That's great!", "So, how can I help?", "I'm happy to hear that, anthing I can help with?", "Excellent!", "Fantastic! So how can I help you?", "This is why I do what I do!", ":D"]
ecstatic_responses = [ "I love your spirit!", "I'm happy you're happy!", "Wow! You've really got it figured out", "Marvelous!!", "Your excitement's rubbing off on me!", "You sound overjoyed!!", "YAAAAAASSSSS QUEEEN"]


# Returns JJ if sentence structure is You Are {word}+ JJ {word}+.
def findYouAreJJ(pos):
    foundYou = False
    foundYouAre = False

    for e in pos:
        if e[0].lower() == 'you':
            foundYou = True
        elif e[0].lower() == 'are' and foundYou:
            foundYouAre = True
        elif foundYou and not foundYouAre:
            foundYou = False
        elif foundYouAre and e[1] == 'JJ':
            return e[0]
    return False

# Generates a bot response from a user message
def generateReply(message):
    pos = getPOS(message)
    sentiment = getSentiment(message)
    phrase = getPhrases(message)

    # If user greeted
    if pos[0][0].lower() in greetings:
        return random.choice(greetings_responses)


    # If error occurred getting POS
    if not pos:
        return "I am not functioning at the moment. Perhaps check your API keys."

    # If user said 'You are ... {adjective} ...'
    youAreJJ = findYouAreJJ(pos)   
    if youAreJJ:
        if sentiment >= 0.5:
            return "Thank you, I know I'm "+youAreJJ+"."
        else:
            return "No! I'm not "+youAreJJ+"!"

    # If user said 'I am ... {adjective} ...'
    IAmJJ = findIAmJJ(pos)   
    if IAmJJ:
        if sentiment >= 0.5:
            return "I'm happy for you that you're "+IAmJJ+"."
        else:
            return "Don't be mean on yourself. I'm sure you're not really "+IAmJJ+"!"

    print(sentiment)

    if sentiment <= 0.2:
        return random.choice(depressed_responses)

    elif sentiment <= 0.5:
        return random.choice(sad_responses)

    elif sentiment <= 0.8:
        return random.choice(happy_responses)

    else:
        return random.choice(ecstatic_responses)


# Returns JJ if sentence structure is I Am {word}+ JJ {word}+.
def findIAmJJ(pos):
    foundI = False
    foundIAm = False

    for e in pos:
        if e[0].lower() == 'i':
            foundI = True
        elif e[0].lower() == 'am' and foundI:
            foundIAm = True
        elif foundI and not foundIAm:
            foundI = False
        elif foundIAm and e[1] == 'JJ':
            return e[0]
    return False
