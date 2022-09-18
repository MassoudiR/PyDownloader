from flask import Flask 

app = Flask(__name__,static_url_path='')




## /////// Web site definition
app.config['SITE_NAME'] = "YouDown"  # Web site name
app.config['SITE_ICON'] = "image/icon.png"  # Web site favicon path


app.config['SITE_MODE'] = "Light" # Mode Light or Dark
