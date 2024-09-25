"""
Elder Coxson
"""

from datetime import datetime
import os
import time
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'csdm/holly/holly')))


import dotenv
from mysql.connector.cursor import MySQLCursor
import holly
import mysql.connector

dotenv.load_dotenv()


ZONE_CHATS = [
    # '4133470603409493',
    # '2419609848082592', #should be zone 1, double-check
    # '4954822721225549',
    # '5865277466887042',
    # '1363317190447129',
    # '5936540856451995',
    # '4145470815511596',
    # '24976215742026849',
    '26732959939628175' #Elder DAvis
]


def process_message(
    msg: holly.ParsedHollyMessage,
    client: holly.HollyClient,
):
    # make sure there's a message
    if len(msg.content) < 1:
        return
    
    please_add = 0
    #determin number to add based on emoji in the chat
    # Program will quit if wrong emoji used
    if msg.content[0] == '⚾':
        please_add = 1
    elif msg.content[0] == '🌊':
        please_add = 4
    else:
        return

    mydb = mysql.connector.connect(
        host='localhost',
        user=os.environ['DATABASE_USERNAME'],
        password=os.environ['DATABASE_PASSWORD'],
        database='zone_1_game_data',
    )
    mydb.autocommit = True
    cursor: MySQLCursor = mydb.cursor()

    cursor.execute(
        'SELECT area FROM missionaries WHERE name = %s', (msg.sender,)
    )
    area = cursor.fetchone()
    if area:
        area = area[0]
    else:
        client.send(
            holly.HollyMessage(
                content="I don't know which area you're in...",
                chat_id=msg.chat_id,
            )
        )
        return
    print(area)
    cursor.execute(
        'SELECT name,score,adds FROM areas WHERE id = %s', (area,)
    )
    result = cursor.fetchone()

    if result:
        area_name = result[0]
        score = result[1]
        adds = result[2]
        score += please_add
        if please_add >= 4:
            adds += 1
        cursor.execute(
            'UPDATE areas SET score = %s, adds = %s WHERE id = %s',
            (score, adds, area),
        )
        if score % 4 == 0 or please_add >= 4:
            if datetime.now().hour > 6 and datetime.now().hour < 21:
                for c in ZONE_CHATS:
                    client.send(
                        holly.HollyMessage(
                            content=f'{area_name} just scored!!', chat_id=c
                        )
                    )
            if msg.chat_id not in ZONE_CHATS:
                client.send(
                    holly.HollyMessage(
                        content=f'{area_name} just scored!!',
                        chat_id=msg.chat_id,
                    )
                )


def main():
    """Main function"""

    parser = holly.HollyParser()

    while True:
        try:
            client = holly.HollyClient()
            print('Connected to Holly')
            while True:
                raw_msg = client.recv()
                print(raw_msg)
                process_message(raw_msg.parse(parser), client)
        except holly.HollyError as e:
            print(f'Error: {e}')

        print('Disconnected from Holly socket')
        time.sleep(30)


if __name__ == '__main__':
    main()
