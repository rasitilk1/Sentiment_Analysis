# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:38:58 2019

@author: madhu
"""
import re
import pickle
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.metrics import confusion_matrix

from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, Dropout, Conv1D, MaxPool1D, GRU, LSTM, Dense

def reviewWords(review, method):
    data_train_Exclude_tags = re.sub(r'<[^<>]+>', " ", review)      # Excluding the html tags
    data_train_num = re.sub(r'[0-9]+', 'number', data_train_Exclude_tags)  # Converting numbers to "NUMBER"
    data_train_lower = data_train_num.lower()              # Converting to lower case.
    data_train_no_punctuation = re.sub(r"[^a-zA-Z]", " ", data_train_lower )
    
    if method == "Porter Stemming":
        #print("Processing dataset with porter stemming...")
        stemmedWords = [ps.stem(word) for word in re.findall(r"\w+", data_train_no_punctuation)]
        return(" ".join(stemmedWords))
        
    if method == "Stop Words":
        #print("Processing dataset with stop words...")
        data_train_split = data_train_no_punctuation.split()            # Splitting into individual words.
        stopWords = set(stopwords.words("english") )
        meaningful_words = [w for w in data_train_split if not w in stopWords]     # Removing stop words.
        return( " ".join( meaningful_words )) 
        
    if method == "Nothing":
        #print("Processing dataset without porter stemming and stop words...")
        return data_train_no_punctuation
    
def training_Validation_Data(cleanWords, data_train):
    
    X = cleanWords
    y = data_train["sentiment"]
    
    test_start_index = int(data_train.shape[0] * .8)
    
    x_train = X[0:test_start_index]
    y_train = y[0:test_start_index]
    x_val = X[test_start_index:]
    y_val = y[test_start_index:]

    return x_train, y_train, x_val, y_val

# Reading the Data
data_train = pd.read_csv(r"C:\Users\madhu\Desktop\sentiment analysis\labeledTrainData.tsv", delimiter = "\t")
data_test = pd.read_csv(r"C:\Users\madhu\Desktop\sentiment analysis\testData.tsv", delimiter = "\t")

# Input the value, whether you want to include porter stemming, stopwords.
print("Input 'Porter Stemming' for porter stemming, 'Stop Words' for stop words, or anywords for Neither of them: ")
preprocessingInput = input("Do you want to include porter stemming or stop word?\n")

print(preprocessingInput)
type(preprocessingInput)
if preprocessingInput == "Porter Stemming":
    print(1)
    method = "Porter Stemming"
    ps = PorterStemmer()        # instantiating a class instance.
    
elif preprocessingInput == "Stop Words":
    method = "Stop Words"
    

print(method)
# Input the value, whether you want to run the model on LSTM RNN or GRU RNN.
print("Input 'LSTM' for LSTM RNN, 'GRU' for GRU RNN ")
modelInput= input("Do you want to compile the model using LSTM RNN or GRU RNN?\n")

if modelInput == "LSTM":
    lstm = True
else:
    lstm = False
    
# Let's process all the reviews together of train data.

cleanWords = []
for i in range(data_train['review'].size):
    cleanWords.append( reviewWords( data_train["review"][i], method ))
print("---Review Processing Done!---\n")

# Splitting the data into tran and validation
x_train, y_train, x_val, y_val = training_Validation_Data(cleanWords, data_train)

# There is a data leakage in test set.
data_test["sentiment"] = data_test["id"].map(lambda x: 1 if int(x.strip('"').split("_")[1]) >= 5 else 0)
y_test = data_test["sentiment"]

# Processing text dataset reviews.
testcleanWords = []
for i in range(data_train['review'].size):
    testcleanWords.append( reviewWords( data_test["review"][i], method ))
print("---Test Review Processing Done!---\n")

# Generate the text sequence for RNN model
np.random.seed(1000)
num_most_freq_words_to_include = 5000
MAX_REVIEW_LENGTH_FOR_KERAS_RNN = 500           # Input for keras.
embedding_vector_length = 32

all_review_list = x_train + x_val

tokenizer = Tokenizer(num_words = num_most_freq_words_to_include)
tokenizer.fit_on_texts(all_review_list)

#tokenisingtrain data
train_reviews_tokenized = tokenizer.texts_to_sequences(x_train)      
x_train = pad_sequences(train_reviews_tokenized, maxlen = MAX_REVIEW_LENGTH_FOR_KERAS_RNN)          # 20,000 x 500

#tokenising validation data
val_review_tokenized = tokenizer.texts_to_sequences(x_val)
x_val = pad_sequences(val_review_tokenized, maxlen = MAX_REVIEW_LENGTH_FOR_KERAS_RNN)  

#tokenising Test data
test_review_tokenized = tokenizer.texts_to_sequences(testcleanWords)
x_test = pad_sequences(test_review_tokenized, maxlen = MAX_REVIEW_LENGTH_FOR_KERAS_RNN)

# Save the tokenizer, so that we can use this tokenizer whenever we need to predict any reviews.
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
def RNNModel(lstm = False):
    model = Sequential()
    model.add(Embedding(input_dim = num_most_freq_words_to_include, 
                                output_dim = embedding_vector_length,
                                input_length = MAX_REVIEW_LENGTH_FOR_KERAS_RNN))
    
    model.add(Dropout(0.2))
    model.add(Conv1D(filters = 32, kernel_size = 3, padding = 'same', activation = 'relu'))
    model.add(MaxPool1D(pool_size = 2))
    if lstm == True:
        model.add(LSTM(100))
    else:
        model.add(GRU(100))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation = 'sigmoid'))             
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
    
    return model

themodel = RNNModel(lstm)
themodel.summary()
themodel.fit(x_train, y_train, batch_size=64, epochs=3, validation_data=[x_val, y_val])

# Creating file name for saving the model.
if lstm == True:
    modelSelected = "LSTM"
else:
    modelSelected = "GRU"
fileName = "RNN " + modelSelected + " model" + method + ".h5"

# Saving the model for future reference.
themodel.save(fileName)
# Prediction.
ytest_prediction = themodel.predict(x_test)

from sklearn.metrics import  roc_auc_score
print("The roc AUC socre for GRU(using porter stemming) model is : %.4f." %roc_auc_score(y_test, ytest_prediction)) 

# Creating csv file for 
# Changing the shape of ytest_prediction to 1-Dimensional
ytest_prediction = np.array(ytest_prediction).reshape((25000, ))
for i in range(len(ytest_prediction)):
    ytest_prediction[i] = round(ytest_prediction[i])
ytest_prediction = ytest_prediction.astype(int)

# Copy the predicted values to pandas dataframe with an id column, and a sentiment column.
output = pd.DataFrame(data = {"id": data_test["id"], "sentiment": ytest_prediction} )

outputName = "Predicted RNN " + modelSelected + " model" + method + ".csv"
output.to_csv(outputName, index = False, quoting = 3 )

cm = confusion_matrix(y_test, ytest_prediction)
print(cm)