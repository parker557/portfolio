# -*- coding: utf-8 -*-
# ==============================================================================
# Copyright (c) 2024 Xavier de Carné de Carnavalet
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ==============================================================================
import binascii
import json

import bcrypt
import pyotp
import qrcode
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort, flash, \
    send_from_directory
from flask_mysqldb import MySQL
from flask_session import Session
from datetime import datetime, timedelta
import yaml
import hmac
import hashlib
import time
import base64
import string
import os
import re

app = Flask(__name__)

# Configure secret key and Flask-Session
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'  # Options: 'filesystem', 'redis', 'memcached', etc.
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True  # To sign session cookies for extra security
app.config['SESSION_FILE_DIR'] = './sessions'  # Needed if using filesystem type

# Load database configuration from db.yaml or configure directly here
db_config = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

mysql = MySQL(app)

# Initialize the Flask-Session
Session(app)


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    sender_id = session['user_id']
    return render_template('chat.html', sender_id=sender_id)


@app.route('/users')
def users():
    if 'user_id' not in session:
        abort(403)

    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, username FROM users")
    user_data = cur.fetchall()
    cur.close()

    filtered_users = [[user[0], user[1]] for user in user_data if user[0] != session['user_id']]
    return {'users': filtered_users}


@app.route('/fetch_messages')
def fetch_messages():
    if 'user_id' not in session:
        abort(403)

    last_message_id = request.args.get('last_message_id', 0, type=int)
    peer_id = request.args.get('peer_id', type=int)

    cur = mysql.connection.cursor()
    query = """SELECT message_id,sender_id,receiver_id,message_text,salt,iv FROM messages 
                   WHERE message_id > %s AND 
                   ((sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s))
                   ORDER BY message_id ASC"""
    cur.execute(query, (last_message_id, peer_id, session['user_id'], session['user_id'], peer_id))

    # Fetch the column names
    column_names = [desc[0] for desc in cur.description]
    # Fetch all rows, and create a list of dictionaries, each representing a message
    messages = [dict(zip(column_names, row)) for row in cur.fetchall()]

    cur.close()
    return jsonify({'messages': messages})


def generate_totp(secret_key, time_step=30, digits=6):
    interval = int(time.time()) // time_step
    msg = int.to_bytes(interval, length=8, byteorder='big')
    hmac_result = hmac.new(base64.b32encode(bytes.fromhex(secret_key)), msg, hashlib.sha1).digest()
    offset = hmac_result[-1] & 0x0F
    truncated_hash = hmac_result[offset:offset + 4]
    binary_code = int.from_bytes(truncated_hash, byteorder='big') & 0x7FFFFFFF
    totp = str(binary_code % 10 ** digits)
    return totp.zfill(digits)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        otp_key = request.form['otpnum']
        cur = mysql.connection.cursor()

        cur.execute("SELECT COUNT(*) FROM login WHERE login_ip = %s AND login_datetime > %s",
                    (request.remote_addr, datetime.now() - timedelta(minutes=5)))

        attempts_count = cur.fetchone()[0]
        if attempts_count >= 5:
            error = 'Too many login attempts. Please try again later.'
            return render_template('login.html', error=error)

        # query salt
        cur.execute("SELECT salt FROM users WHERE username=%s", (username,))
        salt = cur.fetchone()
        if salt is not None:
            salt = salt[0]
            sha3_256 = hashlib.sha3_256()
            sha3_256.update(password.encode('utf-8') + salt.encode('utf-8'))
            hash_password = sha3_256.hexdigest()

            cur.execute("SELECT user_id, password, otp_key FROM users WHERE username=%s", (username,))
            account = cur.fetchone()
            stored_hashed_password = account[1]
            if bcrypt.checkpw(hash_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                # reset the count of login

                totp = pyotp.TOTP(account[2])
                if totp.verify(otp_key):
                    cur.execute("DELETE FROM login WHERE login_ip=%s", (request.remote_addr,))
                    mysql.connection.commit()
                    session['username'] = username
                    session['user_id'] = account[0]
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error='Invalid OTP')

            else:
                # add to sql 'login'
                cur.execute("INSERT INTO login (login_ip, login_datetime) VALUES (%s, %s)",
                            (request.remote_addr, datetime.now()))
                mysql.connection.commit()
                error = 'Invalid Password'
        else:
            # add to sql 'login'
            cur.execute("INSERT INTO login (login_ip, login_datetime) VALUES (%s, %s)",
                        (request.remote_addr, datetime.now()))
            mysql.connection.commit()
            error = 'Invalid Salt'

        return render_template('login.html', error=error)

    return render_template('login.html', error=error)


@app.route('/send_message', methods=['POST'])
def send_message():
    if not request.json or not 'message_text' in request.json:
        abort(400)  # Bad request if the request doesn't contain JSON or lacks 'message_text'
    if 'user_id' not in session:
        abort(403)

    # Extract data from the request
    sender_id = session['user_id']
    receiver_id = request.json['receiver_id']
    message_text = request.json['message_text']
    salt = request.json['salt']
    iv = request.json['iv']

    # Assuming you have a function to save messages
    save_message(sender_id, receiver_id, message_text, salt, iv)

    return jsonify({'status': 'success', 'message': 'Message sent'}), 200


def save_message(sender, receiver, message, salt, iv):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages (sender_id, receiver_id, message_text, salt, iv) VALUES (%s, %s, %s, %s, %s)",
                (sender, receiver, message, salt, iv))
    mysql.connection.commit()
    cur.close()


@app.route('/erase_chat', methods=['POST'])
def erase_chat():
    if 'user_id' not in session:
        abort(403)

    peer_id = request.json['peer_id']
    cur = mysql.connection.cursor()
    query = "DELETE FROM messages WHERE ((sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s))"
    cur.execute(query, (peer_id, session['user_id'], session['user_id'], peer_id))
    mysql.connection.commit()

    # Check if the operation was successful by evaluating affected rows
    if cur.rowcount > 0:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failure'}), 200


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'info')  # Flash a logout success message
    return redirect(url_for('index'))


def check_password(password):
    if len(password) < 8:
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True


def generate_client_recovery_key():
    client_key = ''.join([str(os.urandom(1)[0] % 10) for _ in range(48)])
    return client_key


def generate_server_encryption_key(client_key, salt):
    combined_key = (client_key + salt).encode()
    # Use sha3_256 to hash the combined key
    server_key = hashlib.sha3_256(combined_key).hexdigest()
    return server_key


@app.route('/qr_code')
def serve_qr_code():
    # Retrieve the QR code filename from the user's session
    qr_code_filename = session.get('qr_code_filename')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if qr_code_filename:
        return send_from_directory(f'{script_dir}/otp_qrcode', qr_code_filename)
    else:
        abort(404)  # If no QR code filename is found in the session, return a 404 error


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        # get the register's username and password
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['con_password']

        if password != confirm_password:
            error = 'Password and Confirm Password are not same.'
            return render_template('register.html', error=error)

        if not check_password(password):
            error = 'Password settings not compliant: Passwords must be at least 8 characters long, including uppercase and lowercase letters and numbers.'
            return render_template('register.html', error=error)

        # to find the username exist
        if username_exists(username):
            error = 'user already exist!'
            return render_template('register.html', error=error)
        else:

            salt = binascii.hexlify(os.urandom(16)).decode('utf-8')

            sha3_256 = hashlib.sha3_256()
            sha3_256.update(password.encode('utf-8') + salt.encode('utf-8'))
            hash_password = sha3_256.hexdigest()
            bcrypt_hashed_password = bcrypt.hashpw(hash_password.encode('utf-8'), bcrypt.gensalt())

            # to generate the otp_key
            secret_key = pyotp.random_base32()
            totp = pyotp.TOTP(secret_key)
            uri = totp.provisioning_uri(name=username, issuer_name='Chat App')
            img = qrcode.make(uri)
            qr_code_filename = f"{username}{secret_key}.png"
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.makedirs(os.path.join(script_dir, 'otp_qrcode'), exist_ok=True)
            img.save(os.path.join(script_dir, 'otp_qrcode', f"{qr_code_filename}"))
            session['qr_code_filename'] = qr_code_filename

            # to generate  recovery key and encryption key
            client_recovery_key = generate_client_recovery_key()
            server_encryption_key = generate_server_encryption_key(client_recovery_key, salt)
            session['recovery_key'] = client_recovery_key

            # to sava in db
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (username, password, salt, otp_key, encryption_key) VALUES (%s, %s, %s, %s, %s);",
                (username, bcrypt_hashed_password, salt, secret_key, server_encryption_key))
            mysql.connection.commit()
            cur.close()
            return render_template('register.html', otp_code=secret_key)

    if 'recovery_key' in session:
        recovery_key = session['recovery_key']
        session['recovery_key'] = None
        return render_template('register.html', recovery_key=recovery_key)

    return render_template('register.html', error=error)


def username_exists(username):
    # whether the username exits
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM users WHERE username=%s", (username,))
    account = cur.fetchone()
    if account:
        return True
    return False


def generate_totp_key(length=16):
    # use the urandom to generate the otp_key
    characters = os.urandom(length).hex()
    return characters


@app.route('/register_otp', methods=['POST'])
def register_otp():
    optnum = request.form['optnum']
    username = request.form['username']  # username from front
    password = request.form['password']  # password from front
    totp_key = request.form['totp_key']
    correct_optnum = generate_totp(totp_key)
    if optnum == correct_optnum:
        # back the successful message
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password,optcode) VALUES (%s, %s, %s)",
                    (username, password, totp_key,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'success': True})
    else:
        #  back the unsuccessful message
        return jsonify({'success': False})


@app.route("/saveKey", methods=["POST"])
def saveKey():
    if request.method == 'POST':
        if 'user_id' not in session:
            abort(403)
        formData = json.loads(request.data)
        ECDH_public_key = formData['publicKey']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET ecdh_public_key = %s  WHERE user_id=%s;", (ECDH_public_key, session['user_id']))
        mysql.connection.commit()
    return formData


@app.route("/getSalt", methods=["POST"])
def saveSalt():
    if request.method == 'POST':
        if 'user_id' not in session:
            abort(403)
        formData = json.loads(request.data)
        user_id = formData['user_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT salt FROM key_salt WHERE user_id_1 IN (%s, %s) AND user_id_2 IN (%s, %s)",
                    (user_id, session['user_id'], user_id, session['user_id']))
        existing_salt = cur.fetchone()
        if existing_salt:
            cur.close()
            return existing_salt[0]
        else:
            cur.execute("INSERT INTO key_salt (user_id_1, user_id_2, salt) VALUES (%s, %s, %s)",
                        (session['user_id'], user_id, 1))
            mysql.connection.commit()
            cur.close()
            return "1"
    return formData


@app.route('/get_public_key')
def get_public_key():
    if 'user_id' not in session:
        abort(403)
    user_id = request.args.get('user_id', 0, type=int)
    cur = mysql.connection.cursor()
    cur.execute("SELECT ecdh_public_key FROM users WHERE user_id = %s", (user_id,))
    ECDH_public_key = cur.fetchone()
    if ECDH_public_key:
        ECDH_public_key = ECDH_public_key[0]
    else:
        ECDH_public_key = ''
    cur.close()
    return jsonify(ECDH_public_key)


@app.route("/newSalt", methods=["POST"])
def newSalt():
    if request.method == 'POST':
        if 'user_id' not in session:
            abort(403)
        formData = json.loads(request.data)
        user_id = formData['user_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT salt FROM key_salt WHERE user_id_1 IN (%s, %s) AND user_id_2 IN (%s, %s)",
                    (user_id, session['user_id'], user_id, session['user_id']))
        existing_salt = cur.fetchone()

        if existing_salt:
            new_salt = int(existing_salt[0]) + 1
            cur.execute("UPDATE key_salt SET salt=%s WHERE user_id_1 IN (%s, %s) AND user_id_2 IN (%s, %s)",
                        (new_salt, user_id, session['user_id'], user_id, session['user_id']))
            mysql.connection.commit()
            cur.close()
            return str(new_salt)
        else:
            cur.execute("INSERT INTO key_salt (user_id_1, user_id_2, salt) VALUES (%s, %s, %s)",
                        (session['user_id'], user_id, 1))
            mysql.connection.commit()
            cur.close()
            return "1"
    return formData


if __name__ == '__main__':
    app.run(debug=True)