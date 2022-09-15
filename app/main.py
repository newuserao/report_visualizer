from flask import Flask, render_template, redirect, url_for
import os

cwd = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, template_folder=f'{cwd}/')


@app.route('/home')
def datastudio():
    return render_template('datastudio.html')


@app.errorhandler(404)
def handle_bad_request(e):
    return redirect(url_for('datastudio'))


@app.errorhandler(405)
def handle_methodnotallowed_request(e):
    return redirect(url_for('datastudio'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)