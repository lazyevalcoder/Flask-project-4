# Importing necessary modules from flask
from flask import Flask, render_template, request, redirect, url_for
# Importing pandas for data manipulation
import pandas as pd

# Creating a new Flask web server application
app = Flask(__name__)

# Defining the route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    # If the request method is POST
    if request.method == 'POST':
        # Get the username from the form data
        username = request.form['username']
        # Redirect to the upload page with the username as a parameter
        return redirect(url_for('upload', username=username))
    # If the request method is GET, render the home page
    return render_template('home.html')

# Defining the route for the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Get the username from the request arguments
    username = request.args.get('username', None)
    # If the request method is POST
    if request.method == 'POST':
        # If there's no file in the request files
        if 'file' not in request.files:
            return 'No file part'
        # Get the file from the request files
        file = request.files['file']
        # If no file is selected
        if file.filename == '':
            return 'No selected file'
        # If a file is selected
        if file:
            # Read the file into a pandas DataFrame
            df = pd.read_csv(file)
            # Get the top 3 cities by population
            top_cities = df.nlargest(3, 'Population')['City'].tolist()
            # Calculate the average population
            avg_population = df['Population'].mean()
            # Calculate the median population
            median_population = df['Population'].median()
            # Render the result page with the calculated data
            return render_template('result.html', username=username, tables=top_cities, avg_population=avg_population, median_population=median_population)
    # If the request method is GET, render the upload page
    return render_template('upload.html', username=username)

# If the script is run directly (not imported), start the server
if __name__ == '__main__':
    app.run(debug=True)
