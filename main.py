from flask import Flask, Response  ,render_template, request 
import Conf
import apps
from time import sleep
import string , random
app = Conf.app



@app.route('/')
def hello():


    return render_template('Home.html')
    


@app.route('/checkurl', methods=('GET', 'POST'))
def checkurl():
    if request.method == "POST":
        url = request.form.get('url')
        print(url)
        if url != "" :
            
            x=apps.Download(url).Get_Info()
            if x :
                id = (''.join(random.choice(string.ascii_lowercase) for i in range(10)))
                
                return render_template('Box.html' , context=x+(id,))
            else :
                return Response('<div id="errors" hx-swap-oob="true"></div>')
        return Response()

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000, debug=True)