from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, NumberRange, ValidationError, StopValidation


def LevelValidator(form, field):
  if form.rank.data == 'unranked' and not field.data:
    raise ValidationError()
  elif not field.data:
    # clear out processing errors
    field.errors[:] = []
    # Stop further validators running
    raise StopValidation()
  

class InputForm(FlaskForm):
  discord = StringField('Discord Username (in 0utli3r\'s discord)', [DataRequired()])
  uplay = StringField('Uplay Username - Enter excact characters', [DataRequired()])
  #rank = SelectField('Rank', choices=[(None, 'Select One'), ('unranked', 'Unranked'), ('diamond', 'Diamond'), ('plat1', 'Plat 1'), ('plat2', 'Plat 2'), ('plat3', 'Plat 3'), ('gold1', 'Gold 1'), ('gold2', 'Gold 2'), ('gold3', 'Gold 3'), ('silver1', 'Silver 1'), ('silver2', 'Silver 2'), ('silver3', 'Silver 3'), ('silver4', 'Silver 4'), ('silver5', 'Silver 5'), ('bronze1', 'Bronze 1'), ('bronze2', 'Bronze 2'), ('bronze3', 'Bronze 3'), ('bronze4', 'Bronze 4'), ('bronze5', 'Bronze 5'), ('copper1', 'Copper 1'), ('copper2', 'Copper 2'), ('copper3', 'Copper 3'), ('copper4', 'Copper 4'), ('copper5', 'Copper 5')])
  #level = IntegerField('If Unranked, what is your level?', [LevelValidator, NumberRange(min=1,max=999)])

  submit = SubmitField('Submit')


class HiddenForm(FlaskForm):
  discord = HiddenField('', [DataRequired()])
  uplay = HiddenField('', [DataRequired()])
  rank_w_mmr = HiddenField('', [DataRequired()])
  avg_mmr = HiddenField('', [DataRequired()])
  level = HiddenField('', [DataRequired()])
  season = HiddenField('', [DataRequired()])
  picture = HiddenField('', [DataRequired()])
  rank_img = HiddenField('', [DataRequired()])
  submit = SubmitField('Submit')


class SubmitForm(FlaskForm):
  def __init__(self, player_entry=None, *args, **kwargs):
    super(SubmitForm, self).__init__(*args, **kwargs)
    self.discord = player_entry['discord']
    self.uplay = player_entry['uplay']
    self.rank_w_mmr = player_entry['rank_w_mmr']
    self.level = player_entry['level']
    self.season = player_entry['season']
    self.picture = player_entry['picture']
    self.rank_img = player_entry['rank_img']
    self.submit = SubmitField('Submit')
    #print(player_entry)
    #form_data = {'discord':discord, 'uplay':uplay, 'rank_w_mmr':rank_w_mmr, 'level':level, 'season':season, 'picture':picture, 'rank_img':rank_img}
    #self.discord = player_entry['discord']
    #self.
    

  #fld1 = HiddenField("Field 1")
  #fld2 = StringField("Field 2")
  

  #discord = StringField('', [DataRequired()])
  #uplay = StringField('', [DataRequired()])
  #rank_w_mmr = StringField('', [DataRequired()])
  #level = IntegerField('', [DataRequired()])
  #season = StringField('', [DataRequired()])

  #picture = StringField('', [DataRequired()])
  #rank_img = StringField('', [DataRequired()])

  
  
