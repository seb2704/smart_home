# This is a sample Python script.
import streamlit as st
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def get_state_from_db():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="example",
            host="db"
        )
        cursor = connection.cursor()
        #select state with the newest date
        cursor.execute("SELECT activated FROM alarm_state order by date desc limit 1")
        result = cursor.fetchone()
        return result[0] if result else False
    except Exception as e:
        st.write(f"Error fetching state from database: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()


# Initialize state with a state form postgres database if it exists
if 'state' not in st.session_state:

    st.session_state.state = get_state_from_db()


def get_alarm_from_db():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="example",
            host="db"
        )
        cursor = connection.cursor()
        #select state with the newest date
        cursor.execute("SELECT alarm FROM alarm_state order by date desc limit 1")
        result = cursor.fetchone()
        return result[0] if result else False
    except Exception as e:
        st.write(f"Error fetching state from database: {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()



if 'alarm' not in st.session_state:

    st.session_state.alarm = get_alarm_from_db()

# Function to toggle state
def toggle_state():
    st.session_state.state = not st.session_state.state

button_label = 'Alarm off' if st.session_state.state else 'Alarm on'
st.button(button_label, on_click=toggle_state)
def shutdown_alarm(password):
    correct_password = "your_password"  # Replace with your actual password
    if password == correct_password:
        st.session_state.alarm = False
        st.write("Alarm shut down")
    else:
        st.write("Incorrect password")
st.write(f"Current state: {st.session_state.state}")


password = st.text_input("Enter password to shutdown alarm", type="password")
st.button('Shutdown Alarm', on_click=lambda: shutdown_alarm(password))
def check_gpio():
    if read_gpio():  # Replace 17 with your GPIO pin number
        door_open = True
    else:
        door_open = False
    if door_open and st.session_state.state:
        st.session_state.alarm = True
        st.write("Alarm activated")

    #write door_open, the alarm activated state, the time and the alarm state to the database
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="example",
            host="db"
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO alarm_state (door_open, alarm, date, activated) VALUES (%s, %s, now(), %s)", (door_open, st.session_state.alarm, st.session_state.state))
        connection.commit()
    except Exception as e:
        st.write(f"Error inserting state into database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def read_gpio():
    # Replace this with your GPIO reading TODO!!!
    return True


# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_gpio, 'interval', seconds=1)
scheduler.start()

# Ensure the scheduler is shut down properly when the app stops
import atexit
atexit.register(lambda: scheduler.shutdown())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
