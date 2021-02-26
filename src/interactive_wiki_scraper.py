#!/usr/bin/env python
# coding: utf-8

# In[ ]:


N = 20 # num of short and long sentences to find
SHORT = 256 # max length (exclusive) of shorts
LONG = 512 # max length (exclusive) of longs
MIN = 15 # min length (exclusive) of shorts

LINE = '===================================================\n'
LINE_DASH = LINE.replace('=', '-') 
# Prompt which explains user input
def prompt(term):
    print('Enter y/n to approve or delete each ' + term + '.\n' + LINE)
    
# We scrape Wikipedia pages from the Long Pages list using BeautifulSoup
url_long = urllib.urlopen('https://en.wikipedia.org/w/index.php?title=Special:LongPages&limit=500&offset=0')
soup_long = BeautifulSoup(url_long.read())

HEAD = 'https://en.wikipedia.org/wiki/'
links = [] # link string tails; missing HEAD above
lis = soup_long.find("ol").find_all("li")

# Iterate over the "long pages" Wiki page and pull out appropriate articles
for li in lis:
    # The link is in the first href attr of the first a-tag, sandwiched between "title=" and "&action=histor"
    a = li.find_all("a")[0]
    href = a.get("href")
    left_post = "title="
    right_post = "&action=histor"
    
    if href.find(left_post) != -1:
        start = href.find(left_post) + len(left_post)
        end = href.find(right_post) 
        link = href[start:end]
        # Filter out some generally complicated pages
        filter_terms = ['list', 'rounds', 'polling', 'index', 'timeline', 'standings', 'honours', 'results', 'championship', 'racism', 'hell', 'lgbt',
                     'elections', 'islam', 'paleontology', 'cephalopod', 'cigarette', 'script', 'protests', 'nautical', 'botanical', 'tawag', 'football']
        if not any(term in link.lower() for term in filter_terms):
            links.append(link)

indexes = [i for i, _ in enumerate(links)]
short_sentences = []
long_sentences = []
articles = []

prompt('sentence')

# From the pages corresponding to the links we found, scrape at most 5 long and 5 short sentences from each page
# Stop when we have 20 short and 20 long
while len(short_sentences) < N or len(long_sentences) < N:
    # Generate a random article index, then delete the article from the list to pull from
    i = random.randint(0,len(indexes))
    indexes.remove(i)

    # Scrape from the selected article via BeautifulSoup
    tail = links[i]
    url = urllib.urlopen(HEAD + tail)
    soup = BeautifulSoup(url.read())
    
    # Get only the text data; tokenize the content into sentences
    # Since both soup and tokenize are a bit buggy, we end up getting multi-sentence inputs in some cases
    # Clean up the text using regex
    tags = soup.find(id="bodyContent").find(id='mw-content-text').find_all('p')
    body = ''
    for tag in tags:
        text = tag.get_text()
        # Ignore blank p-tags (empty paragraphs)
        if text != '' and text != '\n':
            text = re.sub('\[.+\]|\n|←|→', '', text)
            body += text
    sentences = tokenize.sent_tokenize(body)
    
    # Add at most five sentences from the source list (wiki page) to the target (sentence list)
    # Each sentence has to be approved by the user via input
    def add_sentences(source, target):
        if len(source) > 0 and len(target) < N:
            # Generate n numbers, where n is min(5, # sentences in source, # needed sentences)
            rands = random.sample(range(0, len(source)), min(5, min(len(source), N - len(target))))
            sents = [source[rand] for rand in rands]
            
            # Ask user for approval of each new sentence; do not keep taking from an article if denials occur
            for sent in sents:
                response = input('\"' + sent + '\"\n')
                if response.lower() != 'y':
                    sents.remove(sent)
            
            # Add the kept sentences to the target list, and keep the article name if we use its content
            [target.append(sent) for sent in sents]
            if len(sents) > 0:
                articles.append(tail)
    
    # From this article, build lists of cleaned short and long sentences
    shorts = []
    longs = []
    for sentence in sentences:
        # If there's a quote in the sentence, exclude it
        if '\"' in sentence or '\'' in sentence:
            continue
            
        # Add spaces after periods/commas where needed
        sentence = re.sub(r'(?<=[.,])(?=[^\s\d])', r' ', sentence)
        sentence.replace('U. S. ', 'U.S.') # Fix up most common acronym (U.S.)
        
        # Add a closing parenthesis to the end of the sentence if there's a lonely opening parenthesis & vice versa
        sentence = (sentence + ')' if ('(' in sentence and not ')' in sentence) else sentence)
        sentence = ('(' + sentence if (')' in sentence and not '(' in sentence) else sentence)

        # Determine whether the sentence is short or long
        if len(sentence) >= SHORT and len(sentence) < LONG:
            longs.append(sentence)
        if len(sentence) < SHORT and len(sentence) > MIN:
            shorts.append(sentence)
    
    # Add randomly selected short and long sentences
    add_sentences(shorts, short_sentences)
    add_sentences(longs, long_sentences)
    
    print('\nSOURCE: \"' + tail.replace('_', ' ') + '\"')
    print('COUNT:', len(short_sentences), 'shorts,', len(long_sentences), 'longs')
    print('\n===================================================\n')
    
print('FINISHED! Articles used:')
for article in set(articles):
    print(' - \"' + article.replace('_', ' ') + '\"') 
print()

