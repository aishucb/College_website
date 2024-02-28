from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson import ObjectId
import os


uri = "mongodb+srv://holygraceiedc:CIpx5ne5mmBaHYsT@collegewebsite.2ax8qbs.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.get_database("collegewebsite")


app = Flask(__name__)
UPLOAD_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'UPLOAD_FOLDER')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PATH
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key for your application

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def hello_world():
    collection = db['news']
    documents = collection.find({})
    # Assuming 'documents' is a PyMongo cursor
# Sort documents by '_id' in descending order to get the latest documents first
    documents.sort([('_id', -1)])

# Extract the last six documents
    last_six_documents = documents.limit(6)

# Create news_data list for the last six documents

    news_data = [
    {
        'newsDate': document.get('newsDate', 'Unknown'),
        'newsTitle': document.get('newsTitle', 'Unknown'),
        'newsDescription': document.get('newsDescription', 'Unknown'),
        'newsPicture': document.get('newsPicture', 'Unknown'),
        '_id': str(document.get('_id'))
    }
    for document in last_six_documents
]

    return render_template('index.html',news_data=news_data)

@app.route('/my_link')
def my_link():
    return render_template('management.html')

@app.route('/union')
def union():
    return render_template('union.html')

@app.route('/contactus')
def contactus():
    return render_template('contact.html')

@app.route('/facilites')
def facilites():
    return render_template('facilites.html')

@app.route('/civil')
def civil():
    return render_template('civil.html')

@app.route('/mech')
def mech():
    return render_template('mech.html')

@app.route('/cse')
def cse():
    return render_template('cse.html')

@app.route('/eee')
def eee():
    return render_template('eee.html')

@app.route('/wissen')
def wissen():
    return render_template('wissen.html')

@app.route('/iedc')
def iedc():
    return render_template('iedc.html')

@app.route('/studentcorner')
def studentcorner():
    return render_template('studentscorner.html')

@app.route('/placement')
def placement():
    return render_template('placement.html')

@app.route('/abouthg')
def abouthg():
    return render_template('abouthg.html')

@app.route('/whyhgae')
def whyhgae():
    return render_template('whyhgae.html')

@app.route('/aboutprincipal')
def aboutprincipal():
    return render_template('aboutprincipal.html')

@app.route('/secretary')
def secretary():
    return render_template('director.html')

@app.route('/chairman')
def chairman():
    return render_template('chairman.html')

users_collection = db['users']  # Create a 'users' collection for storing user data


class User(UserMixin):
    def __init__(self, username, password, email):
        self.id = username
        self.password = password
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({'_id': user_id})
    if user_data:
        return User(username=user_data['_id'], password=user_data['password'], email=user_data['email'])
    return None


# Render loading page
@app.route('/admin')
def loading():
    return render_template('loading.html')



def check_password(saved_password, provided_password):
    return check_password_hash(saved_password, provided_password)



# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = users_collection.find_one({'_id': username})

        if user_data and check_password(user_data['password'], password):
            user = User(username=username, password=user_data['password'], email=user_data['email'])
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username is already taken
        if users_collection.find_one({'_id': username}):
            flash('Username is already taken. Please choose a different one.', 'danger')
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            user_data = {
                '_id': username,
                'password': hashed_password,
                'email': email
            }
            users_collection.insert_one(user_data)
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# Protected route (requires login)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboardd.html')






# Render main dashboard page
@app.route('/index')
def index():
    return render_template('dashboardd.html')


# Render news add page
@app.route('/news_add')
def newsadd():
    return render_template('newspage.html')


# Fetch news data to show on news page
@app.route('/news')
def news():
    collection = db['news']
    documents = collection.find({})
    news_data = [
        {
            'newsDate': document.get('newsDate', 'Unknown'),
            'newsTitle': document.get('newsTitle', 'Unknown'),
            'newsDescription': document.get('newsDescription', 'Unknown'),
            'newsPicture': document.get('newsPicture', 'Unknown'),
            '_id': str(document.get('_id'))
        }
        for document in documents
    ]
    return render_template('news.html', news_data=news_data)


# Form to add news
@app.route('/add_call_news', methods=['GET', 'POST'])
def add_call_news():
    collection = db['news']
    if request.method == 'POST':
        newsTitle = request.form['newsTitle']
        newsDate = request.form['newsDate']
        newsPicture = request.files['newsPicture']
        newsDescription = request.form['newsDescription']

        if newsPicture and newsPicture.filename != '':
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], newsPicture.filename)
            newsPicture.save(image_filename)

        data_to_insert = {
            'newsTitle': newsTitle,
            'newsDate': newsDate,
            'newsPicture': newsPicture.filename,
            'newsDescription': newsDescription,
        }
        collection.insert_one(data_to_insert)

        return redirect('/index')

    return render_template('form2.html')


# Update news route
@app.route('/update_news/<news_id>', methods=['GET', 'POST'])
def update_news(news_id):
    collection = db['news']
    news = collection.find_one({'_id': ObjectId(news_id)})

    if request.method == 'POST':
        # Update the fields based on the form data
        news['newsTitle'] = request.form['newsTitle']
        news['newsDate'] = request.form['newsDate']
        news['newsDescription'] = request.form['newsDescription']

        # Check if 'newsPicture' is in the form files and not empty
        if 'newsPicture' in request.files and request.files['newsPicture'].filename != '':
            newsPicture = request.files['newsPicture']
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], newsPicture.filename)
            newsPicture.save(image_filename)
            news['newsPicture'] = newsPicture.filename

        # Save the updated document back to the database
        collection.update_one({'_id': ObjectId(news_id)}, {'$set': news})

        return redirect(url_for('news'))

    return render_template('update_news.html', news=news)



# Delete news route
@app.route('/delete_news/<news_id>')
def delete_news(news_id):
    collection = db['news']
    collection.delete_one({'_id': ObjectId(news_id)})
    return redirect(url_for('news'))


# Render event add page
@app.route('/event_add')
def eventadd():
    return render_template('eventpage.html')


# Fetch event data to show on events page
@app.route('/events')
def events():
    collection = db['events']
    documents = collection.find({})
    event_data = [
        {
            'eventDate': document.get('eventDate', 'Unknown'),
            'eventTitle': document.get('eventTitle', 'Unknown'),
            'eventDescription': document.get('eventDescription', 'Unknown'),
            'eventPicture': document.get('eventPicture', 'Unknown'),
            '_id': str(document.get('_id'))
        }
        for document in documents
    ]
    return render_template('events.html', event_data=event_data)


# Form to add events
@app.route('/add_call_events', methods=['GET', 'POST'])
def add_call_events():
    collection = db['events']
    if request.method == 'POST':
        eventTitle = request.form['eventTitle']
        eventDate = request.form['eventDate']
        eventPicture = request.files['eventPicture']
        eventDescription = request.form['eventDescription']

        if eventPicture and eventPicture.filename != '':
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], eventPicture.filename)
            eventPicture.save(image_filename)

        data_to_insert = {
            'eventTitle': eventTitle,
            'eventDate': eventDate,
            'eventPicture': eventPicture.filename,
            'eventDescription': eventDescription,
        }
        collection.insert_one(data_to_insert)

        return redirect('/index')

    return render_template('form2.html')


# Update event route
@app.route('/update_event/<event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    collection = db['events']
    event = collection.find_one({'_id': ObjectId(event_id)})

    if request.method == 'POST':
        # Update the fields based on the form data
        event['eventTitle'] = request.form['eventTitle']
        event['eventDate'] = request.form['eventDate']
        event['eventDescription'] = request.form['eventDescription']

        # Check if 'eventPicture' is in the form files and not empty
        if 'eventPicture' in request.files and request.files['eventPicture'].filename != '':
            eventPicture = request.files['eventPicture']
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], eventPicture.filename)
            eventPicture.save(image_filename)
            event['eventPicture'] = eventPicture.filename

        # Save the updated document back to the database
        collection.update_one({'_id': ObjectId(event_id)}, {'$set': event})

        return redirect(url_for('events'))

    return render_template('update_event.html', event=event)



# Delete event route
@app.route('/delete_event/<event_id>')
def delete_event(event_id):
    collection = db['events']
    collection.delete_one({'_id': ObjectId(event_id)})
    return redirect(url_for('events'))






if __name__ == '__main__':
    app.run(debug=True)