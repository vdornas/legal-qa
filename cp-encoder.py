import json
import re
import pickle
import os
import codecs

# vocabulary = {1: 'word'}
vocabulary = {}
answers = {}
answersPretty = []
answercorpus = []
questioncorpus = []
wordcorpus = []
train = []
dev = []

# handle = open('dev', 'rb')
# ttrain = pickle.load(handle)
# print(ttrain)
# quit()


def build_train():
    # list of dict , where each dict has: question (word indices for the question)
    # and answers (answer indices for each of the question ground truth)
    # [{ 'question': [100,10,20], 'answers': [10,10] }]
    train = [{}, {}]
    # answer_dict = build_ans()
   # question_
    # for answer_text in answer_dict:

    # train.append({ 'question':  })


def append_qs(question_text):
    if question_text in questioncorpus:
        questioncorpus.append(question_text)


def build_questions():
    questions = {}
    for idx, question in enumerate(questioncorpus):
        question_tokens = get_vocab_idx(question)


def append_ans(answer_text):
    if answer_text not in answercorpus:
        answercorpus.append(answer_text)


def build_ans():
    # dict object of (answer index <int> -> word indices <list of ints>)
    for idx, answer in enumerate(answercorpus):
        ans_idx = get_vocab_idx(answer)
        # print(ans_idx)
        # print(answer)

        answersPretty.append({'txt': str(answer), 'index': str(idx)})
        answers.update({idx: ans_idx})
        # answers = {idx: ans_idx}
    return answers


def append_vocab(wordlist):
    for word in wordlist.split():
        if word not in wordcorpus:
            wordcorpus.append(word)


def build_vocab():
    for idx, word in enumerate(wordcorpus):
        vocabulary.update({idx: word})
    return vocabulary


def get_vocab_idx(answer_text):
    answer_vec = []

    for answer_word in answer_text.split():
        for idx, vocab_word in enumerate(vocabulary):
            # print(str(vocabulary[idx]) + ' == ' + str(answer_word))
            # if 'Independencia' == 'Independencia':
            #     print('ueeeepa')
            if str(vocabulary[idx]) == str(answer_word):
                #print('found match')
                #quit()
                answer_vec.append(idx)

        # answer_vec.append(next(x for x in vocabulary if x == answer_word))
    #     answer_vec.append(x for x in vocabulary if x == answer_word)
    return answer_vec


def get_answer_idx(answer_bag):
    answer_vec = []
   # print(answersPretty)
    for answer_text in answer_bag:
        for entry in answersPretty:
            # print(entry)
            #print(entry['txt'].encode('utf-8') + ' == ' + answer_text.encode('utf-8'))
            if(entry['txt'] == answer_text):
                #print('found')
                #quit()
                answer_vec.append(int(entry['index']))
        # for idx,answer_sentence in enumerate(answers):
        #     print(str(answer_sentence) + " == " + str(answer_text))
        #     if str(answers[idx] == str(answer_text)):
        #         answer_vec.append(idx)
    # return None
    return answer_vec


def get_answer_idx_except(answer_bag):
    answer_vec = []
   # print(answersPretty)
    for answer_text in answer_bag:
        for entry in answersPretty:
            if(entry['txt'] != answer_text):
                answer_vec.append(int(entry['index']))
    return answer_vec

def append_train(question, set_answers):
    train.append({'question': question, 'answers': answers})

# with open('cp2-base.json', 'r') as csvfile:
with codecs.open('cp-rev4.json', 'rb', 'utf-8') as csvfile:
    codex = json.load(csvfile)
    #print(codex)
    print("First pass.......................")
    # build vocabulary
    for record in codex:
        #print(record)
        #print(record[u'TeorArtigo'].encode('utf-8'))
        vArtigo = record['NumArtigo'].encode('utf-8')
        vTeor = record['TeorArtigo'].encode('utf-8')
        vPergunta = record['Pergunta'].encode('utf-8')

        vArtigoFull = vPergunta + ' ' + vArtigo + ' ' + vTeor
        #vArtigoFull = vArtigo + ' ' + vTeor
        vReferencia = record['Referencia'].encode('utf-8')

       # append_vocab(vArtigoFull + ' ' + vReferencia + ' ' + vPergunta)
        append_vocab(vArtigoFull + ' ' + vPergunta)
        append_ans(vArtigoFull)
        # append_ans(record['Referencia'])
        # append_qs(record['Referencia'])
        # append_ans(record['TeorArtigo'])
    print("Building vocab....................")
    vocab = build_vocab()
    # print(vocab)
    # quit()
    print("Building answers...................")
    answers = build_ans()
    # print(answers)
    # quit()

    # print(answersPretty)
    print("Second pass......................")
    count = 0
    for record in codex:
        # print(record['TeorArtigo'])
        # print(get_answer_idx([record['TeorArtigo']]))

        vArtigo = record['NumArtigo'].encode('utf-8')
        vTeor = record['TeorArtigo'].encode('utf-8')
        vPergunta = record['Pergunta'].encode('utf-8')
        #vArtigoFull = vArtigo + ' ' + vTeor
        vArtigoFull = vPergunta + ' ' + vArtigo + ' ' + vTeor
        #vReferencia = record['Referencia'].encode('utf-8')
        

        train.append({'question': get_vocab_idx(
            vPergunta), 'answers': get_answer_idx([vArtigoFull])})

        ground_truth = get_answer_idx([vArtigoFull])
        false_assertives = get_answer_idx_except([vArtigoFull])
        #print(false_assertives)
        #quit()
        dev.append({'bad': false_assertives, 'question': get_vocab_idx(
            vPergunta), 'good': ground_truth})
        
        count+=1

    #print(dev)
    # print(get_vocab_idx('Independencia'))
    # for record in codex:
    #     append_trainpair({  })

    # answers = build_ans()
    # print(vocab)
    print('saving vocabulary...')
    pickle.dump(vocab, open('vocabulary', 'wb'))

    print('saving answers...')
    pickle.dump(answers, open('answers', 'wb'))

    print('saving train...')
    pickle.dump(train, open('train', 'wb'))

    print('saving dev...')
    pickle.dump(dev, open('dev', 'wb'))

quit()

# with open('cp2-base.json', 'r', encoding='utf-8') as csvfile:
#     codex = json.load(csvfile)
#     # mydict = {}
#     mydict = []
#     vocab = {0: 'oi', 1: 'lla'}
#     print(mydict)
#     for v in codex:
#         p = re.compile('\\w+')

#         print(p.match(v['TeorArtigo']))
#         # mydict.update({'question': v['Referencia'].split(), 'answers': v['TeorArtigo'].split()})
#         # mydict.update({'question': [10,20,40], 'answers': [30,30]})
#         mydict = ([v['TeorArtigo'].split()])
#         print(mydict)
#     # serialize
#     pickle.dump(mydict, open("cp-base.data", 'wb'))
#     # print(mydict)
#     # print(v['Referencia'])
#     # if(v['Referencia'])

# with open('cp-training-question-answer.txt', 'r') as train:
#     # with open('cp2-base.json', 'rb') as f:
#     print(train)

# with open('cp-training-qa-verbose', 'w') as final:
#     print(final)
