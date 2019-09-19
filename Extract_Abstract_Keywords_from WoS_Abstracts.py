###WRITTEN BY DERYC T. PAINTER
###SEPT. 19, 2019

###KEYWORD EXTRACTION METHOD MODIFIED FROM...
###HACOHEN-KERNER, YAAKOV "AUTOMATIC EXTRACTION OF KEYWORDS FROM ABSTRACTS"
###INTERNATIONAL CONFERENCE ON KNOWLEDGE-BASED AND INTELLIGENT INFORMATION AND ENGINEERING SYSTEMS
###SPRINGER, BERLIN, HEIDELBERG, 2003


from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

infile = input('Enter the name of the Web of Science file (i.e. /Users/savedrecs.txt): ')
kwfile = input('Enter the name of the file you wish to create containing the keywords (i.e. /Users/keywordfile.txt): ')
sensativity = input('Enter the minimum level of keyness you wish to extract (i.e. 1.0): ')


#STOP WORDS WITH USEFUL ADDITIONS FOR SCIENTIFIC ANALYSIS
#THE NEW STOPWORDS CAN BE COMMENTED OUT SHOULD YOU NOT HAVE NEED FOR THEM
stop_words = set(stopwords.words('english'))
newStopWords = ['THE','ARE','OF','IN','THIS','IT','HAS','TO','ON',\
                'AND','FOR','A','AS','WE','BOTH','OR','WELL','BETWEEN',\
                'WERE','HOWEVER','ALTHOUGH','USING','THESE','THEIR','RECENTLY'\
                'BASIS','RESULT','OUTCOME','SELECT','SHOWN','FOUND','WITHIN',\
                'WOULD','AMONG','MAY',]
for number in range(0,2020):
    newStopWords.append(str(number))
for x in newStopWords:
    stop_words.add(x.lower())
  
tokenizer = RegexpTokenizer(r'\w+')

lemmatizer = WordNetLemmatizer()

def ngrams(input, n):  #REMOVES STOPWORDS AND CREATES NGRAMS

    word_tokens = tokenizer.tokenize(str(input).lower().strip())
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    unfiltered_sentence = []
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            unfiltered_sentence.append(w)
    for word in unfiltered_sentence:
        filtered_sentence.append(lemmatizer.lemmatize(word))
    output = {}
    for i in range(len(filtered_sentence)-n+1):
        g = ' '.join(filtered_sentence[i:i+n])
        output.setdefault(g, 0)
        output[g] += 1
    return output

def keywords(input):  #ADJUSTS THE FREQUENCY MINIMUM FOR KEYWORDS
    
    keyword = []
    for i in sorted(input, key=input.get, reverse=True):
        try:
            input[i] = input[i] / sentenceCount
            if input[i] >= float(sensativity):
                keyword.append((i,input[i]))
        except ZeroDivisionError:
            print('{} did not contain an abstract.'.format(title))
            break
    return keyword



with open(infile,'r',encoding='UTF-8-sig') as f:

    for line in f:  #PROCESS WEB OF SCIENCE RECORDS INTO NGRAMS
        
        title = line.lower().strip().split('\t')[8]
        abstract = str(line.strip().split('\t')[21])
        text = title+' '+abstract

        authorKWs = line.lower().strip().split('\t')[19]
        keyWordPlus = line.lower().strip().split('\t')[20]
        
        sentenceCount = text.count('. ')
        unigrams = ngrams(text,1)
        bigrams = ngrams(text,2)
        trigrams = ngrams(text,3)

        wordCount = len(unigrams)

        
        for key in unigrams.keys():  #RANK NGRAMS BASED ON FREQUENCY
            for item in bigrams.keys():
                if key.lower() in item.lower():
                    bigrams[item] = bigrams[item] + (unigrams[key]/4)
        for key in unigrams.keys():
            for item in trigrams.keys():
                if key.lower() in item.lower():
                    trigrams[item] = trigrams[item] + (unigrams[key]/8)
        for key in bigrams.keys():
            for item in trigrams.keys():
                if key.lower() in item.lower():
                    trigrams[item] = trigrams[item] + ((2*bigrams[key])/6)
        xgrams = dict(unigrams, **bigrams, **trigrams)
        
        PubKWs = keywords(xgrams)

        try:  #PRINTS RESULTS AND IGNORES RECORDS WITHOUT ABSTRACT
            for j,k in PubKWs:
                print(title,'\t',j,'\t',k,file=kwfile)
        except TypeError:
            print('{} did not contain an abstract.'.format(title),file=kwfile)
            next
        if len(PubKWs) > 0:
            print('{} has {} words in {} sentences.'.format(title,wordCount,sentenceCount),file=kwfile)




