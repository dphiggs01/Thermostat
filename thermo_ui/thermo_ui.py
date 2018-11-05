from forms import LoginForm, SetpointForm, AwayForm
from flask import Flask, request, session, redirect, url_for, render_template, flash
from rest_call import RestServiceCall
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py


# Retieve data from 'static' directory. Used most typically for rendering images.
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/')
@app.route('/index')
def index():
    rest_service_call = RestServiceCall()
    ui_data = rest_service_call.get_thermostat_data(refresh=True)
    logging.debug("ui_data [{}]".format(ui_data))
    form = SetpointForm()
    form.set_point.data = ui_data['set_point']
    form.temperature.data = ui_data['temperature']
    if ui_data['set_point'] is not "NA":
        form.time.data = ui_data['time']
        form.battery.data = ui_data['battery']

    return render_template('index.html', ui_data=ui_data, form=form)


@app.route('/schedule')
def schedule():
    return render_template('schedule.html', ui_data={})


@app.route('/away', methods=['GET', 'POST'])
def away():
    if request.method == 'GET':
        rest_service_call = RestServiceCall()
        ui_data = rest_service_call.get_thermostat_data(refresh=True)
        form = AwayForm()
        form.away.data = not ui_data['away']
        return render_template('away.html', ui_data=ui_data, form=form)

    if request.method == 'POST':
        try:
            rest_service_call = RestServiceCall()
            form_away = request.form['away']
            logging.debug("call set away schedule to [{}]".format(form_away))
            rest_service_call.set_thermostat_away(form_away)
            logging.debug("call set away schedule")
        except ValueError:
            flash('Away feature not activated.')

        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        if request.form['user_name'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))

    return render_template('login.html',
                           title='Sign In',
                           ui_data={},
                           form=form,
                           error=error)


@app.route('/adjust_setpoint', methods=['GET', 'POST'])
def adjust_setpoint():
    if request.method == 'GET':
        return redirect(url_for('index'))

    if request.method == 'POST':
        rest_service_call = RestServiceCall()
        try:
            set_point = int(request.form['set_point'])
            rest_service_call.set_thermostat_data(set_point)
            logging.debug("setpoint.........")
        except ValueError:
            flash('Adjust temperature not available at this time.')

    form = SetpointForm()
    form.set_point.data = request.form['set_point']
    form.temperature.data = request.form['temperature']
    form.battery.data = request.form['battery']
    form.time.data = request.form['time']

    ui_data = {'set_point': request.form['set_point'],
               'temperature': request.form['temperature'],
               'battery': request.form['battery'],
               'time': request.form['time']
               }
    return render_template('index.html', ui_data=ui_data, form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='password',
    WTF_CSRF_ENABLED=True,
))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    # app.run(host='0.0.0.0')
