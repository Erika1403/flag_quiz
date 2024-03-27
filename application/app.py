from flask import Flask, request, render_template
import requests as rq
import random
import os

app = Flask(__name__)
url = "https://restcountries.com/v3.1/all"
code = 0
while code != 200:
    response = rq.get(url)
    code = response.status_code
code = response.status_code
countries = response.json()
countries_full = response.json()
correct_img_path = "static/css/images/icons8/correct"
wrong_img_path = "static/css/images/icons8/wrong"

def pick_flag():
    if len(countries) != 1:
        num = random.randint(0, len(countries))
    else:
        num = 1
    
    info = countries[num]
    
    img_url = info['flags']['png']
    official_name = info['name']['official']
    common_name = info['name']['common']
    del countries[num]
    return img_url, official_name, common_name


def pick_img(path):
    files = []
    if os.path.exists(path):
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                files.append(file_name)
    logo_img = random.choice(files)
    return logo_img

@app.route('/')
def home():
    path = "css/images/icons8/main"
    name1 = "social-text.png"
    name2 = "jelly-character-chooses-one-of-the-suggested-options.png"
    name3 = "3d-casual-life-map.png"
    return render_template('index.html', path=path, name1=name1, name2=name2, name3=name3)

@app.route('/enter_flag')
def enter_flag():
    flag_img, of_name, cm_name = pick_flag()
    return render_template('enter_flag.html', image_url=flag_img, official_name=of_name, common_name=cm_name)
       
@app.route('/check_ans', methods=['POST'])
def check_ans():
    of_ans = request.form['official_cname']
    cm_ans = request.form['common_cname']
    img = request.form['flag_img']
    ans = request.form['answer']
    if ans.lower() == of_ans.lower() or ans.lower() == cm_ans.lower():
        message = "Correct! Well done."
        path = "css/images/icons8/correct"
        fx = "css/audio/QL7TEGT-applause-cheering.mp3"
        logo = pick_img(correct_img_path)
    else: 
        message = "Sorry!\nThe correct answer is "+cm_ans+".\nTry again!"
        path = "css/images/icons8/wrong"
        fx = "css/audio/CF7R4XZ-wrong-answer-tuba.mp3"
        logo = pick_img(wrong_img_path)
    
    return render_template('enter_flag.html', image_url=img, result=message, path = path, name=logo, music=fx)

@app.route('/choose_flag')
def choose_flag():
    mydict = {}
    flag_img, of_name, cm_name = pick_flag()
    mydict[cm_name] = flag_img

    i = len(mydict)
    while i != 4:
        data = random.choice(countries_full)
        key = data['name']['common']
        if mydict.get(key) is None:
            mydict[key] = data['flags']['png']
            i += 1
    items = list(mydict.items())
    random.shuffle(items)
    new_dict = dict(items)
    toShow = True
    
    return render_template('choose_flag.html', country = cm_name, my_dict=new_dict, cor_ans=cm_name, show=toShow, cor_img=flag_img)


@app.route('/check_flag', methods=['POST'])
def check_flag():
    ans = request.form['ctry_flag']
    user_ans = request.form['my_ans']
    img = request.form['img_flag']
    toShow = False

    if ans == user_ans:
        message = "Correct! Good job!"
        path = "css/images/icons8/correct"
        fx = "css/audio/QL7TEGT-applause-cheering.mp3"
        logo = pick_img(correct_img_path)
    else: 
        message = "Sorry! You chose a wrong answer."
        path = "css/images/icons8/wrong"
        fx = "css/audio/CF7R4XZ-wrong-answer-tuba.mp3"
        logo = pick_img(wrong_img_path)

    return render_template('choose_flag.html', country=ans, show=toShow, correct_img=img, result=message, path = path, name=logo, music=fx)

@app.route('/choose_country')
def choose_country():
    flag_img, of_name, cm_name = pick_flag()
    mylist = []
    mylist.append(cm_name)
    toShow = True
    i = len(mylist)
    while i != 6:
        data = random.choice(countries_full)
        key = data['name']['common']
        if key not in mylist:
            mylist.append(key)
            i += 1
    random.shuffle(mylist)
    return render_template('choose_country.html', flag_img=flag_img, list=mylist, cor_ans=cm_name, show=toShow)

@app.route('/check_country', methods=['POST'])
def check_country():
    ans = request.form['choices']
    correct = request.form['cor_answer']
    flag_img = request.form['flag_img']
    toShow = False
    if ans == correct:
        message = "Correct! Good job!"
        path = "css/images/icons8/correct"
        fx = "css/audio/QL7TEGT-applause-cheering.mp3"
        logo = pick_img(correct_img_path)
    else:
        message = "Sorry! You chose a wrong answer."
        path = "css/images/icons8/wrong"
        fx = "css/audio/CF7R4XZ-wrong-answer-tuba.mp3"
        logo = pick_img(wrong_img_path)

    return render_template('choose_country.html', flag_img=flag_img, correct_answer=correct, path = path, name=logo, music=fx, result=message, show=toShow)

if __name__ == '__main__':
    app.run(debug=True)