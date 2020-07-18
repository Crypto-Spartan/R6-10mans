from helper import backend_functions
from helper.custom_forms import InputForm, SubmitForm, HiddenForm
from helper.get_player_rank_data import get_player_rank_data
from flask import Flask, render_template, url_for, redirect, flash, request
import os, sys
import json
from operator import itemgetter

SCRIMDATE = 'Fri 10 July @ 7pm EDT'
ALLOW_SUBMISSIONS = False


# start of flask app
app = Flask(__name__)
SECRET_KEY = os.urandom(64)
app.config['SECRET_KEY'] = SECRET_KEY

@app.template_filter('tojsonobj')
def tojsonobj(string):
  if isinstance(string, str):
    string = string.replace("None", "''")
    string = string.replace("\'", "\"")
    string = json.loads(string)
    return string
  else:
    return string

# main webpages
@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
  global SCRIMDATE
  global ALLOW_SUBMISSIONS

  if ALLOW_SUBMISSIONS:
    
    input_form = InputForm()
    if request.method == 'POST' and input_form.validate_on_submit():
      form_data = {'discord':input_form.discord.data, 'uplay':input_form.uplay.data}
      player_rank_data = get_player_rank_data(form_data['uplay'])
      
      if player_rank_data == 'NOT FOUND':
        return redirect(url_for('not_found', player_entry=form_data))
      
      form_data.update(player_rank_data)

      return redirect(url_for('confirmation_check', player_entry=form_data))
    
    else:
      return render_template('submissions.html', scrimdate=SCRIMDATE, form=input_form)  
  
  else:
    return render_template('deny_submissions.html')


@app.route('/success')
def success():
  return render_template('success.html', player_entry=request.args.get('player_entry'))


@app.route('/confirmation_check', methods=["GET", "POST"])
def confirmation_check():

  if request.method == 'POST':
    submit_form = HiddenForm()
    form_data = {'discord':submit_form.discord.data, 'uplay':submit_form.uplay.data, 'rank_w_mmr':submit_form.rank_w_mmr.data, 'avg_mmr':submit_form.avg_mmr.data,
      'level':submit_form.level.data, 'season':submit_form.season.data, 'picture':submit_form.picture.data, 'rank_img':submit_form.rank_img.data}
    
    #player_csv_entry = dict((itemgetter(*['discord', 'uplay', 'rank_w_mmr', 'avg_mmr', 'level'])(form_data)))
    #backend_functions.player_to_csv(player_entry)
    return redirect(url_for('success', player_entry=form_data))
  else:
    player_entry = tojsonobj(request.args.get('player_entry'))
    #submit_form = SubmitForm(player_entry)
    hidden_form = HiddenForm(discord=player_entry['discord'], uplay=player_entry['uplay'], rank_w_mmr=player_entry['rank_w_mmr'], level=player_entry['level'],
      season=player_entry['season'], picture=player_entry['picture'], rank_img=player_entry['rank_img'])

    return render_template('confirmation_check.html', player_entry=player_entry, form=hidden_form)

  


@app.route('/not_found')
def not_found():
  return render_template('not_found.html', player_entry=request.args.get('player_entry'))


@app.route('/test', methods=["GET", "POST"])
def test():
  global SCRIMDATE
  global ALLOW_SUBMISSIONS

  if ALLOW_SUBMISSIONS:
    
    input_form = InputForm()
    if request.method == 'POST' and input_form.validate_on_submit():
      form_data = {'discord':input_form.discord.data, 'uplay':input_form.uplay.data}
      player_rank_data = get_player_rank_data(form_data['uplay'])
      if player_rank_data == 'NOT FOUND':
        return redirect(url_for('not_found', player_entry=form_data))
      form_data.update(player_rank_data)

      return redirect(url_for('confirmation_check', player_entry=form_data))
    
    else:
      return render_template('submissions_test.html', scrimdate=SCRIMDATE, form=input_form)  
  
  else:
    return render_template('deny_submissions.html')





# run the webserver on localhost, port 8080
if __name__ == '__main__':
  app.run('0.0.0.0', 8080, debug=True)
