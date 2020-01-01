# Sentiment_Analysis
LSTM and GRU based Approach to classify the sentiments of the IMDb movie reviews

The project makes use of the Different approaches namely randomforest,LSTM or GRU to perform the sentimental analysis of the IMDb Dataset and hence analyse which Technique fits the most.

It includes the use of different techniques such as (Porter stemming, Stop words) for pre-processing of data and training the model using  Long short-term memory(LSTM) or Gated recurrent unit(GRU) with an training accuracy of 92.6.
The model also uses the stored data in the corresponding csv file to predict the sentiment of a random review collected from web.

  Dataset for training the data can be found at [Training Data](https://drive.google.com/file/d/1O72Wo3BKxfytcqwE27_EL4ofHn99tcps/view?usp=sharing).The files also include a trained model by selecting (porter steeming for preprocessing and GRU based approach to tain the model) is **_RNN GRU modelPorter Stemming.h5_**. Below is the detailed description about how the model was trained, preprocessing that was done on data and its predictions on [Testing Data](https://drive.google.com/file/d/1-uMKaMsp6QY8NdsMXxmh1dTl6hlfgtAk/view?usp=sharing) and its accuracy in predicting the sentiment analysis of new reviews from web.
  
  ### Dataset 
  There are Two datasets - 
  1.labeledTrainData
  2.testData
  
  LabeledTrainData has 25000 rows containing 3 columns - id, Sentiment, review.
  TestData has 25000 rows containing only 2 columns - id, and reviews. We have to predict the sentiments of these reviews.
   
  ### Prerequisites
  re,numpy,pickle,pandas,nltk,keras,sklearn
  Install these Dependencies First.
  
  ### Training the model and Testing it
  please follow the LSTM_and_GRU.py to train the model on the TrainingData
  while training the data select either one of the data preprocessing methods ie Porter Stemming, Stop Wrods.
  then select which RNN Architecture to use ie LSTM or GRU
  Then you will finally find 2 files such as Predicted RNN GRU modelPorter Stemming.csv(if you select porter stemming for preprocessing and GRU for Training) and RNN GRU modelPorter Stemming.h5(if you select porter stemming for preprocessing and GRU for Training) the Predicted RNN GRU modelPorter Stemming.csv is the csv file obtained from the testing data with the analyzed sentiment column of the tweet added to it where the value is 1(for positive review) and 0(for negative review)
  ### Testing the model against new reviews from web 
  please run predictYourReview.py file 
  select either one of the data preprocessing methods ie Porter Stemming, Stop Wrods.
  then select which RNN Architecture to use ie LSTM or GRU so that the system loads the necessary file.
  Now write your own review and decide is it positive(1) or negative(0) review.
  
## Author

**[KOLLI VENKATA MADHUKAR ](https://www.linkedin.com/in/madhukar-kolli-2a512916b/)**

## Acknowledgments
### References
- [Sentiment Analysis on Movie Reviews Recurrent Neural Network Architectures](https://cs224d.stanford.edu/reports/TimmarajuAditya.pdf)
- [Text sentiment analysis based on long short-term memory](https://ieeexplore.ieee.org/document/7778967)


