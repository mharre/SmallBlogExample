from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text',render_kw={'placeholder':'Please write something VERY interesting'}, validators=[DataRequired()])
    submit = SubmitField('BlogPost')
