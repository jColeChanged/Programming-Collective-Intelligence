"""
A Pop-3 Mail Filter

Python comes with a library called poplib for downloading email messages.
Write a script that downloads email messages from a server and attempts to
classify them. What are the different properties of an email message and how
 might you build a feature extraction function to take advantage of these?
 """
import poplib
from email import parser
import re


pop = poplib.POP3_SSL('pop.gmail.com')
pop.user('jColeChanged@gmail.com')
pop.pass_('passwordwithheld")

messages = [pop.retr(i) for i in range(1, len(pop.list()[1]) + 1)]
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
#Parse message intom an email object:
messages = [parser.Parser().parsestr(mssg) for mssg in messages]
pop_conn.quit()


def get_words(doc):
    splitter = re.compile("\\W*")
    words = [s.lower() for s in splitter.split(doc) 
                if len(s) > 2 and len(s) < 20]

    return dict([(w, 1) for w in words])

def get_email_features(email):
    keys = email.keys()
    features = {}
    for key in keys:
        features.update(get_words(email[key]))
    return features
