# Flask-Youtube-Scraping-Analysis

Build application using FLASK Framework for scraping metadata and comments from Youtube social media then perform sentiment analysis on comments.

Step by step that has been done:
1. Scraping youtube metadata using beautifulsoup, urllib, json and regex libraries. The output of scraping metadata are:
   - Url = Youtube video url
   - Title = Title of youtube video
   - Upload Date = Youtube video upload time
   - Duration = Youtube video duration
   - Genre = Youtube video genre. Such as Music, blog, horror, documenter, family etc.
   - Views = Total views count of youtube video
   - Likes = Total likes count of youtube video
   - Thumbnail Url = Thumbnail image of youtube video
   - Channel Name = Channel name of youtube video
   - Channel Url = Channel url of youtube video
   - Subscribers = Total subscribers count of youtube channel
   - Is Paid = Is the video paid (Yes/No)
   - Is Unlisted = Is the video unlisted (Yes/No)
   - Is Family = Is the video family friendly (Yes/No)
  
 2. Scraping youtube comments using Ajax based on script tags. The output of scraping youtube comments are:
    - Url = Youtube video url
    - Text = Youtube comment text
    - Time = Youtube comment publish time
    - Votes = Total votes/like count of youtube comment
    - Author = Username who made the comment
    - Photo = Photo of username who made the comment
 
 3. Sentiment analysis was carried out using the Transformers BERT (Bidirectional Encoder Representations from Transformers) method with an accuracy gain of 97.80% for multiclass classification cases (positive, negative, and neutral). 
The steps consist of:
    - Data Acquisition, which done with scraping youtube comments. The dataset used is 10075 comments in Bahasa Indonesia from many url youtube video with topic about "Pemakaian Kawat Gigi/Behel"
    - Data Preprocessing, which done with several steps namely: Casefolding, Cleansing, Tokenizing, Convert Slang Words, Negation Handling, Stemming, Stopwords, and Handling Missing Value
    - Data Labeling, which done with use lexicon based approach. I use reference lexicon dictionary from this repository https://github.com/rifkyahmadsaputra/Sentiment-Analysis-Online-Lectures-in-Indonesia/tree/main/data
    - Data Exploration
    - Prepare model BERT like data splitting, structure of model, initialize value of parameters
    - Training, Validation, Evaluation, and Testing


| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP1.PNG"> Scraping Metadata |<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP2.PNG"> Scraping Comments |<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP3.PNG"> Analyze Comments |
|<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP4.PNG"> Result Scraping Metadata Single Url |<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP5.PNG"> Result Scraping Metadata Multi Url |<img width="1604" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP6.PNG"> Result Scraping Comments Single Url | 
|<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP7.PNG"> Result Scraping Comments Multi Url |<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP8.PNG"> Result Analyze Comments Single Url (1) |<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP9.PNG"> Result Analyze Comments Single Url (2) | <img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP10.PNG">  Result Analyze Comments Single Url (3) |<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP10.PNG"> Result Analyze Comments Single Url (3) |<img width="5000" alt="" src="https://github.com/AnnisaRizki30/BE-Laravel8-Online-Shopping-Web/blob/master/screenshoot/Dashboard.PNG?raw=true"> Result Analyze Comments Single Url (3) |
|<img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP10.PNG"> Result Analyze Comments Single Url (3) | <img width="5000" alt="" src="https://github.com/AnnisaRizki30/Flask-Youtube-Scraping-Analysis/blob/master/Images/FYSSAPP11.PNG"> Result Analyze Comments Multi Url |
