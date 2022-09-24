from operator import sub
from flask import Flask, render_template, request, session, send_from_directory, g
from werkzeug.utils import secure_filename
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

import metadata_scrape 
from downloader_comment import YoutubeCommentDownloader, SORT_BY_RECENT
from preprocessing_text import text_preprocessing
import visualization

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import csv
import sys
import time
import datetime
import os
# import uuid
# secret_key = uuid.uuid4().hex
# print(secret_key)

app = Flask(__name__)


# Define folder to save uploaded files to process further
UPLOAD_FOLDER = os.path.join(app.instance_path, 'uploads')

# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define folder to save result of scraping metadata
RESULT_META_FOLDER = os.path.join(app.root_path, 'result-meta')
if not os.path.exists(RESULT_META_FOLDER):
    os.makedirs(RESULT_META_FOLDER)

# Configure result of scraping metadata file path flask
app.config['RESULT_META_FOLDER'] = RESULT_META_FOLDER

# Define folder to save result of scraping comments
RESULT_COMMENT_FOLDER = os.path.join(app.root_path, 'result-comment')
if not os.path.exists(RESULT_COMMENT_FOLDER):
    os.makedirs(RESULT_COMMENT_FOLDER)

# Configure result of scraping comment file path flask
app.config['RESULT_COMMENT_FOLDER'] = RESULT_COMMENT_FOLDER

# Define folder to save result of analyze comments
RESULT_ANALYZE_FOLDER = os.path.join(app.root_path, 'result-analyze')
if not os.path.exists(RESULT_ANALYZE_FOLDER):
    os.makedirs(RESULT_ANALYZE_FOLDER)

# Configure result of analyze comment file path flask
app.config['RESULT_ANALYZE_FOLDER'] = RESULT_ANALYZE_FOLDER

# Define secret key to enable session
app.secret_key = '233769295e7a4c17a806b38d3aae2c62'


##------------------ Code Setup Model Bert -----------------##
pretrained= "liandarizkia/SA01-IndoBert"
model = AutoModelForSequenceClassification.from_pretrained(pretrained)
tokenizer = AutoTokenizer.from_pretrained(pretrained)

sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

label_index = {'LABEL_0': 'negative', 'LABEL_1': 'positive', 'LABEL_2': 'neutral'}

# Function for return probability score from sentiment analysis result
def probability(score):
  return f'{score * 100:.2f}%'

##------------------ End Code Setup Model Bert -----------------##


##------------------ Code For Delete File Based On Age of File -----------------##

def del_older_files(req_path):
  N=5
  if not os.path.exists(req_path):
    print("Please provide valid path")
    sys.exit(1)
  if os.path.isfile(req_path):
    print("Please provide dictionary path")
    sys.exit(2)
  today=datetime.datetime.now()
  for each_file in os.listdir(req_path):
    each_file_path=os.path.join(req_path,each_file)
    if os.path.isfile(each_file_path):
      file_cre_date=datetime.datetime.fromtimestamp(os.path.getctime(each_file_path))
      dif_days=(today-file_cre_date).days
      if dif_days > N:
        os.remove(each_file_path)
        print(each_file_path,dif_days)


# Run function in each predefined folder
del_older_files(RESULT_META_FOLDER)
del_older_files(RESULT_COMMENT_FOLDER)
del_older_files(RESULT_ANALYZE_FOLDER)

##------------------ End Code For Delete File Based On Age of File -----------------##


current_date = datetime.datetime.now()
format_name = str(current_date.day)+str(current_date.month)+str(current_date.year)


##------------------ MAIN CODE -------------------------## 
@app.route('/', methods=['GET'])
def index():
	return render_template('metadata.html')

@app.route('/comments', methods=['GET'])
def comments():
	return render_template('comment.html')

@app.route('/analyze', methods=['GET'])
def analyze():
	return render_template('analyze.html')


@app.route('/scrape-metadata-single',methods=['GET','POST'])
def metadata_single_url():
	global url_video, title, date_published, channel_name, genre 
	global subscribers, likes_num, views_count, duration, thumbnail_url
	global tags, description
	if request.method == 'POST':
		try:
			raw_url = request.form['raw_url']
			result = metadata_scrape.scrape_video_data(raw_url)
			url_video = result['url']
			title = result['title']
			date_published = result['upload_date']
			channel_name = result['channel_name']
			genre = result['genre']
			subscribers = result['subscribers']
			likes_num = result['likes']
			views_count = result['views']
			duration = result['duration']
			tags = result['tags']
			description = result['description']
			thumbnail_url = result['thumbnail_url']

		except Exception as e:
			print('Error:', str(e))

	return render_template('metadata.html',
							url_video=url_video, 
							title=title,
							date_published=date_published,
							channel_name=channel_name,
							genre=genre,
							subscribers=subscribers,
							likes_num=likes_num,
							views_count=views_count,
							duration=duration,
							thumbnail_url=thumbnail_url,
							tags=tags,
							description=description,
							)



@app.route('/scrape-metadata-multi',methods=['GET','POST'])
def metadata_multi_url():
	global metadata_df
	if request.method == 'POST':
		try:
			uploaded_df = request.files['file']
			data_filename = secure_filename(uploaded_df.filename)
			uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
			session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
			filepath = session['uploaded_data_file_path']

			dict_data = []
			with open(filepath) as file:
				csv_file = csv.DictReader(file)
				for row in csv_file:
					dict_data.append(row)

			metadata_df = pd.DataFrame()
			for video_link in dict_data:
				result = metadata_scrape.scrape_video_data(video_link['Urls'])
				print(result)
				metadata_df = metadata_df.append(result, ignore_index=True)
				fname_metadata = f'youtube_metadata_{format_name}.csv'
				session['fname_metadata'] = fname_metadata 
				metadata_df.to_csv(os.path.join(app.config['RESULT_META_FOLDER'], fname_metadata), encoding='utf-8', index=False)
		
		except Exception as e:
				print('Error:', str(e))

	return render_template('metadata_multi.html', column_names=metadata_df.columns.values, row_data=list(metadata_df.values.tolist()), zip=zip)
	


@app.route("/download-metadata")
def download_metadata():
	if 'fname_metadata' in session:
		csvFileName = session['fname_metadata']
	
	return send_from_directory(os.path.join(app.config['RESULT_META_FOLDER']), path=csvFileName, as_attachment=True)



@app.route('/scrape-comments-single',methods=['GET','POST'])
def comment_single_url():
	global dict_data
	if request.method == 'POST':
		try:
			raw_url = request.form['raw_url']
			youtube_url = raw_url
			limit = int(request.form['number_comments'])
			print('Downloading Youtube comments for', youtube_url)
			downloader = YoutubeCommentDownloader()
			generator = (downloader.get_comments_from_url(youtube_url))
			count = 0

			dict_data = []
			for comment in generator:
				dict_data.append(comment)
				count += 1
				sys.stdout.write('Downloaded %d comment(s)\r' % count)
				sys.stdout.flush()
				if limit and count >= limit:
					break
			print(dict_data)

		except Exception as e:
			print('Error:', str(e))
	
	return render_template('comment.html', result=dict_data)
	


@app.route('/scrape-comments-multi',methods=['GET','POST'])
def comment_multi_url():
	global comment_df_multi
	if request.method == 'POST':
		uploaded_df = request.files['file']
		data_filename = secure_filename(uploaded_df.filename)
		uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
		session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
		filepath = session['uploaded_data_file_path']

		dict_data = []
		with open(filepath) as file:
			csv_file = csv.DictReader(file)
			for row in csv_file:
				dict_data.append(row)

		comment_df_multi = pd.DataFrame()
		for video_link in dict_data:
			try:
				youtube_url = video_link['Urls']
				limit = int(request.form['number_comments'])
				print('Downloading Youtube comments for', youtube_url)
				downloader = YoutubeCommentDownloader()
				generator = (downloader.get_comments_from_url(youtube_url))
				count = 0

				start_time = time.time()
				for comment in generator:
					comment['channel_name'] = video_link['Channel_Name']
					comment_df_multi = comment_df_multi.append(comment, ignore_index=True)
					count += 1
					sys.stdout.write('Downloaded %d comment(s)\r' % count)
					sys.stdout.flush()
					if limit and count >= limit:
						break

				comment_df_multi = comment_df_multi[['urls', 'channel_name', 'author', 'text', 'time', 'votes', 'photo']]
				print("DataFrame Shape: ",comment_df_multi.shape,"\nYoutube Comment DataFrame: ")
				print(comment_df_multi)
				print('\n[{:.2f} seconds] Done!'.format(time.time() - start_time))

				fname_comment = f'youtube_comment_{format_name}.csv'
				session['fname_comment'] = fname_comment 
				comment_df_multi.to_csv(os.path.join(app.config['RESULT_COMMENT_FOLDER'], fname_comment), encoding='utf-8', index=False)

			except Exception as e:
				print('Error:', str(e))
	
	return render_template('comment_multi.html', column_names=comment_df_multi.columns.values, row_data=list(comment_df_multi.values.tolist()), zip=zip)



@app.route("/download-comments")
def download_comment():
	if 'fname_comment' in session:
		csvFileName = session['fname_comment']

	return send_from_directory(os.path.join(app.config['RESULT_COMMENT_FOLDER']), path=csvFileName , as_attachment=True)



@app.route('/analyze-single-url',methods=['GET','POST'])
def analyze_single_url():
	global dict_data, vis_positive, vis_negative, vis_neutral
	global df_analyze_single, vis_bar, vis_pie
	if request.method == 'POST':
		try:
			raw_url = request.form['raw_url']
			youtube_url = raw_url
			limit = int(request.form['number_comments'])
			print('Downloading Youtube comments for', youtube_url)
			downloader = YoutubeCommentDownloader()
			generator = (downloader.get_comments_from_url(youtube_url))
			count = 0

			dict_data = []

			for comment in generator:
				comment['text_clean'] = text_preprocessing(comment['text'])
				prediction = sentiment_analysis(comment['text_clean'])
				status = label_index[prediction[0]['label']]
				score = probability(prediction[0]['score'])
				comment['sentiment'] = status
				comment['polarity'] = score
				dict_data.append(comment)
				count += 1
				sys.stdout.write('Downloaded %d comment(s)\r' % count)
				sys.stdout.flush()
				if limit and count >= limit:
					break
				
			df_analyze_single = pd.DataFrame.from_dict(dict_data)
	
			df_wc_pos = df_analyze_single[df_analyze_single['sentiment'] == 'positive']
			df_wc_neg = df_analyze_single[df_analyze_single['sentiment'] == 'negative']
			df_wc_neu = df_analyze_single[df_analyze_single['sentiment'] == 'neutral']
			
			pos_string = []
			for t in df_wc_pos.text_clean:
				pos_string.append(t)
			pos_string = pd.Series(pos_string).str.cat(sep=' ')

			neg_string = []
			for t in df_wc_neg.text_clean:
				neg_string.append(t)
			neg_string = pd.Series(neg_string).str.cat(sep=' ')

			neu_string = []
			for t in df_wc_neu.text_clean:
				neu_string.append(t)
			neu_string = pd.Series(neu_string).str.cat(sep=' ')

			vis_positive = visualization.render_word_cloud(pos_string)
			vis_negative = visualization.render_word_cloud(neg_string)
			vis_neutral = visualization.render_word_cloud(neu_string)
			
			vis_bar = visualization.bar_graph(df_analyze_single)
			vis_pie = visualization.pie_graph(df_analyze_single)

			analyze_comment_single = f'youtube_comment_analyze_{format_name}.csv'
			session['analyze_comment_single'] = analyze_comment_single 
			df_analyze_single.to_csv(os.path.join(app.config['RESULT_ANALYZE_FOLDER'], analyze_comment_single), encoding='utf-8', index=False)

		except Exception as e:
			print('Error:', str(e))
	
	return render_template('analyze.html', 
							result=dict_data, 
							res_1=vis_positive,
							res_2=vis_negative,
							res_3=vis_neutral,
							bar_graph=vis_bar,
							pie_graph=vis_pie
						  )



@app.route("/download-analyze-comments-single")
def download_analyze_comment_single():
	if 'analyze_comment_single' in session:
		csvFileName = session['analyze_comment_single']

	return send_from_directory(os.path.join(app.config['RESULT_ANALYZE_FOLDER']), path=csvFileName , as_attachment=True)



@app.route('/analyze-multi-url', methods=['GET','POST'])
def analyze_multi_url():
	global df_analyze_multi
	if request.method == 'POST':
		uploaded_df = request.files['file']
		data_filename = secure_filename(uploaded_df.filename)
		uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
		session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)
		filepath = session['uploaded_data_file_path']

		dict_data = []
		with open(filepath) as file:
			csv_file = csv.DictReader(file)
			for row in csv_file:
				dict_data.append(row)

		df_analyze_multi = pd.DataFrame()
		for video_link in dict_data:
			try:
				youtube_url = video_link['Urls']
				limit = int(request.form['number_comments'])
				print('Downloading Youtube comments for', youtube_url)
				downloader = YoutubeCommentDownloader()
				generator = (downloader.get_comments_from_url(youtube_url))
				count = 0
				
				start_time = time.time()
				for comment in generator:
					comment['channel_name'] = video_link['Channel_Name']
					comment['text_clean'] = text_preprocessing(comment['text'])
					prediction = sentiment_analysis(comment['text_clean'])
					status = label_index[prediction[0]['label']]
					score = probability(prediction[0]['score'])
					comment['sentiment'] = status
					comment['polarity'] = score

					df_analyze_multi = df_analyze_multi.append(comment, ignore_index=True)

					count += 1
					sys.stdout.write('Downloaded %d comment(s)\r' % count)
					sys.stdout.flush()
					if limit and count >= limit:
						break

				df_analyze_multi = df_analyze_multi[['urls', 'channel_name', 'author', 'text', 'time', 'votes', 'sentiment', 'polarity', 'photo']]

				print("DataFrame Shape: ",df_analyze_multi.shape,"\nYoutube Comment DataFrame: ")
				print(df_analyze_multi)
				print('\n[{:.2f} seconds] Done!'.format(time.time() - start_time))
			
				
				analyze_comment_multi = f'youtube_comment_analyze_{format_name}.csv'
				session['analyze_comment_multi'] = analyze_comment_multi 
				df_analyze_multi.to_csv(os.path.join(app.config['RESULT_ANALYZE_FOLDER'], analyze_comment_multi), encoding='utf-8', index=False)

			except Exception as e:
				print('Error:', str(e))
	
	return render_template('analyze_multi.html', column_names=df_analyze_multi.columns.values, row_data=list(df_analyze_multi.values.tolist()), zip=zip)
			


@app.route("/download-analyze-comments-multi")
def download_analyze_comment_multi():
	if 'analyze_comment_multi' in session:
		csvFileName = session['analyze_comment_multi']
	
	return send_from_directory(os.path.join(app.config['RESULT_COMMENT_FOLDER']), path=csvFileName , as_attachment=True)

##------------------ END MAIN CODE --------------------------## 


if __name__ == '__main__':
	app.run(debug=True)
    
    
    
    
    
    
    
