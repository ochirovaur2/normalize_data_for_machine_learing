# encoding: utf-8
import pymorphy2
import re
import json
from city_names import city_names
from stop_words import stop_words



morph = pymorphy2.MorphAnalyzer()


data = json.load(open('./data/input/issues_with_comments_2020-09-01_2020-09-02.json', encoding='utf8'))

tickets = data['data']


#turn cities in one word city\
    
city_names = city_names.lower()
city_names_arr = city_names.split(" ")

# stopwords
stop_words = stop_words.lower()

stop_words_arr = stop_words.split(" ")

def sentence_to_normalized_words(sentence):
    global stop_words_arr
    global city_names_arr
    
    morph = pymorphy2.MorphAnalyzer()
    sentence = sentence.lower() 
    arr = sentence.split(" ")
    num_i = 0
    for word in arr:     
        if word.find("им") != -1 or word.find("ку") != -1:

            washed_word = re.findall(r'им[\w\d-]+', word)
            if len(washed_word) > 0:
                
                is_contract = re.findall('\d',washed_word[0])
                if len(is_contract) > 0:
                    
                   
                    arr[num_i] = "contract"
                    

            washed_word = re.findall(r'ку[\w\d-]+', word)
            if len(washed_word) > 0:
                
                is_contract = re.findall('\d',washed_word[0])
                if len(is_contract) > 0:
                    
                    
                    arr[num_i] = "contract"
                    

        if word.find('сч-') != -1:

            is_contract = re.findall('\d',word)
            if len(is_contract) > 0:
                
                arr[num_i] = "kreditcontrol"
                
        num_i +=1

    normalized_words = [morph.parse(w)[0].normal_form for w in arr]
    sentence = " ".join(normalized_words)
    sentence = re.sub(r'\d{8,10}', 'order', sentence)
    sentence = re.sub(r'{[a-zA-Z0-9_.+-:#]+}', "", sentence)
    sentence = re.sub(r'<[a-zA-Z0-9_.+-:#]+>', "", sentence)
    sentence = re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', "email", sentence)
    sentence = re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?','URL', sentence)
    sentence = re.sub(r'www','', sentence)
    sentence = re.sub(r'[\n\r .,()":?!]+', ' ', sentence) 
    sentence = sentence.strip()
    sentence_arr = re.findall(r'[\w\d-]+', sentence)
    sentence = ' '.join(sentence_arr)
    arr = sentence.split(" ")
    num_i = 0
    for word in arr:
        if word in city_names_arr:
            
            arr[num_i] = "city"
            
        if word in stop_words_arr:
            try:
                arr.remove(word)
            except:
                continue
        
    
            
        
    sentence = " ".join(arr)
    arr = sentence.split()
    sentence = " ".join(arr)
    return sentence
    

nz_summarys = []
nz_descriptions = []
nz_input_tickets = []
cnames = []

out = open('out.txt', 'w', encoding='utf8')
print('Normalizing...')
for i,ticket in enumerate(tickets):
    print(i)
    if i%1000 == 0: 
        print(f'#{i}/{len(tickets)}')
    description = ticket['description'] or ''
    summary = ticket['summary'] or ''
    temp_str = f'{str(sentence_to_normalized_words(summary))} {str(sentence_to_normalized_words(description))}'
    nz_input_tickets.append(temp_str)
    temp_str = ""
    
    
    cnames.append(ticket['cname'])
    

data_prepared = {'nz_input_tickets': nz_input_tickets,'cnames': cnames}
fname = './data/output/data_prepared.json'

print(f'Saving prepared data into: {fname}')
json.dump(data_prepared, open(fname, 'w', encoding='utf8'), indent=4, ensure_ascii=False)