# coding: utf-8
#
# Author : Alexis Tourneux <alexis.tourneux@gmail.com>

from threading import Thread
import os, time

from trainline import search, Passenger, TGVMAX, _station_to_dict

from datetime import datetime, date as datetime_date, timedelta

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader, select_autoescape

def convert_date_to_string_format(date):

    """This function aims at returning a string properly formatted for the use of trainline module.

       Format should be : 'dd/mm/yyyy hh:mm'

       Examples :

       >>> convert_date_to_string_format(datetime.now())
       '12/09/2019 20:02'
    """

    if date:
        if isinstance(date, datetime):
            day = date.isoformat().split('T')[0].split('-')
            day.reverse()
            return '%s %02d:%02d' % ('/'.join(day), date.hour, date.minute)
        elif isinstance(date, datetime_date):
            return convert_date_to_string_format(datetime(year=date.year, month=date.month, day=date.day))

        else:
            raise Exception("Other format than datetime.datetime are not implemented yet.")

    else:
        return convert_date_to_string_format(datetime.now())

def convert_string_to_date(date_str):

    """This function aims at creating a datetime.datetime object from a string representing a timestamp
       from format 'dd/mm/yyyy hh:mm'.

       >>> convert_string_to_date('12/09/2019 14:56')
       datetime.datetime(year=2019, month=9, day=12, hour=14, minute=56)
    """

    if date_str:
        if isinstance(date_str, str):
            splitted = date_str.split(' ')
            days = splitted[0].split('/')
            time = splitted[1].split(':')

            return datetime(
                year=int(days[2]),
                month=int(days[1]),
                day=int(days[0]),
                hour=int(time[0]),
                minute=int(time[1])
            ).astimezone()

    raise TypeError('Input parameter must be of type str')


class JourneyWish:

    def __init__(self, departure, arrival, from_date, to_date,
                 transportation_mean=None, passengers=None, max_price=None):

        if not departure:
            raise Exception("Departure can not be None.")
        self.departure = departure

        if not arrival:
            raise Exception("Arrival can not be None.")
        self.arrival = arrival

        if not from_date:
            raise Exception("From_date can not be None.")
        elif isinstance(from_date, datetime):
            self.from_date = from_date
        elif isinstance(from_date, str):
            self.from_date = convert_string_to_date(from_date)
        else:
            raise TypeError("From_date should be of type datetime.datetime. Instead found : %s" % type(from_date))

        if not to_date:
            raise Exception("To_date can not be None.")
        elif isinstance(to_date, datetime):
            self.to_date = to_date
        elif isinstance(to_date, str):
            self.to_date = convert_string_to_date(to_date)
        else:
            raise TypeError("To_date should be of type datetime.datetime. Instead found : %s" % type(to_date))

        self.transportation_mean = transportation_mean

        if isinstance(max_price, float) or isinstance(max_price, int):
            self.max_price = max_price
        elif isinstance(max_price, str):
            try:
                self.max_price = float(max_price)
            except ValueError:
                self.max_price = None
        else:
            self.max_price = None

        if isinstance(passengers, Passenger):
            self.passengers = [passengers]
        elif isinstance(passengers, list):
            self.passengers = passengers
        else:
            self.passengers = None

        if len(self.passengers) == 1 and TGVMAX['reference'] in [
            card['reference'] for card in self.passengers[0].cards]:
            self.max_price = 0

        self.best_yet = None
        self.best_match = []

    def search_matching_journeys(self):

        request = self.request_journeys()
        folders = request.folders

        if folders:
            sorted_price = sorted(folders, key= lambda f: f.price)
            best_price = sorted_price[0].price
            best_price_journeys = sorted(
                [folder for folder in folders if folder.price <= best_price],
                key=lambda f: f.departure_date_obj
            )

            return best_price_journeys

    def request_journeys(self):

        return search(
            departure_station=self.departure,
            arrival_station=self.arrival,
            from_date=convert_date_to_string_format(self.from_date),
            to_date=convert_date_to_string_format(self.to_date),
            transportation_mean=self.transportation_mean,
            passengers=self.passengers,
            max_price=self.max_price
        )


class Warner(Thread):

    """This class is aimed at wrapping logical aspects of journeys watchdogs, email sending, etc...
    """

    def __init__(self, wishes) -> None:

        super().__init__()

        if isinstance(wishes, JourneyWish):
            self.wishes = [wishes]
        elif isinstance(wishes, list):
            self.wishes = wishes
        else:
            raise TypeError("Wishes should be of type list. Found %s instead." % type(wishes))

    def start(self) -> None:
        for wish in self.wishes:
            wish.search_matching_journeys()


class EmailSender:

    def __init__(self, receiver, sender, smtp_host, smtp_port=None, smtp_login=None, smtp_password=None):

        if isinstance(receiver, str):
            if ',' in receiver:
                self.receiver = receiver.split(',')
            else:
                self.receiver = [receiver]
        elif isinstance(receiver, list):
            self.receiver = receiver
        else:
            raise TypeError("Receiver should be of type list. Found %s instead." % type(receiver))

        self.sender = sender
        self.smtp_host = smtp_host

        self.smtp_port = smtp_port
        if not self.smtp_port:
            self.smtp_port = 25
        elif not isinstance(smtp_port, int):
            try:
                self.smtp_port = int(smtp_port)
            except ValueError:
                raise TypeError("SMTP port should be a valid int. Found %s instead." % type(smtp_port))

        self.smtp_login = smtp_login
        self.smtp_password = smtp_password

    def send(self, data):

        if self.smtp_port == 587:
            # enables TLS connection
            server = smtplib.SMTP(host=self.smtp_host, port=self.smtp_port)

            server.starttls()
            server.ehlo()
            server.login(self.smtp_login, self.smtp_password)

        elif self.smtp_port == 465:
            # enables SSL connection
            server = smtplib.SMTP_SSL(host=self.smtp_host, port=self.smtp_port)

            server.ehlo()
            server.login(self.smtp_login, "Mayer0404")

        else:
            # Perform basic SMTP connection
            server = smtplib.SMTP(host=self.smtp_host, port=self.smtp_port)

            server.connect(self.smtp_host, self.smtp_port)
            server.helo()

        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'New journeys available !'
        msg['From'] = self.sender
        msg['To'] = ','.join(self.receiver)

        email_template = env.get_template('warn_email.jinja2')

        msg.attach(
            MIMEText(
                email_template.render(folders=data, stations=stations),
                "html"
            )
        )

        server.send_message(msg)
        server.close()


if __name__ == '__main__':

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    STATIONS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "stations_mini.csv")
    stations = _station_to_dict(STATIONS_PATH)

    alexis_passenger = Passenger('05/09/1967')
    alexis_passenger.add_special_card(TGVMAX, 'HC800266305')

    wishes = []

    from_date = datetime(
        year=2019, month=9, day=22, hour=13, minute=0, second=0).astimezone()
    to_date = datetime(
        year=from_date.year, month=from_date.month, day=from_date.day, hour=23, minute=59, second=59).astimezone()
    transportation_mean = 'train'
    wish = JourneyWish(departure="Lille", arrival="Paris", from_date=from_date, to_date=to_date,
                       transportation_mean=transportation_mean, passengers=alexis_passenger)
    wishes.append(wish)

    from_date = datetime(
        year=2019, month=9, day=27, hour=17, minute=0, second=0).astimezone()
    to_date = datetime(
        year=from_date.year, month=from_date.month, day=from_date.day, hour=23, minute=59, second=59).astimezone()
    transportation_mean = 'train'
    wish = JourneyWish(departure="Paris", arrival="Lille", from_date=from_date, to_date=to_date,
                       transportation_mean=transportation_mean, passengers=alexis_passenger)
    wishes.append(wish)

    from_date = datetime(
        year=2019, month=9, day=29, hour=13, minute=0, second=0).astimezone()
    to_date = datetime(
        year=from_date.year, month=from_date.month, day=from_date.day, hour=23, minute=59, second=59).astimezone()
    transportation_mean = 'train'
    wish = JourneyWish(departure="Lille", arrival="Paris", from_date=from_date, to_date=to_date,
                       transportation_mean=transportation_mean, passengers=alexis_passenger)
    wishes.append(wish)

    print(wishes)

    previous_folders = [0]*len(wishes)
    print(previous_folders)

    while True:
        print("Batch at %s" % datetime.now().astimezone().isoformat())
        for i in range(len(wishes)):

            try:
                wish = wishes[i]

                print(
                    ('Starting query with parameters :'
                     '\n\tDeparture : %s\n\tArrival : %s\n\tFrom Date : %s'
                     '\n\tTo Date : %s\n\tTransportation Mean : %s' % (
                         wish.departure, wish.arrival, wish.from_date,
                         wish.to_date, wish.transportation_mean
                     )
                     )
                )

                folders = wish.search_matching_journeys()

                if folders and folders != previous_folders[i]:
                    print("Found folders : %s" % folders)
                    EmailSender(receiver="tourneuxalexis@gmail.com", sender="test@trainwarner.com", smtp_host="smtp.gmail.com",
                                smtp_port=587, smtp_login="trainwarner.info@gmail.com").send(data=folders)
                elif folders == previous_folders[i]:
                    print("No more matching found")
                else:
                    print("Nothing found")

                previous_folders[i] = folders
            except Exception as exception:
                print(exception)

        print("End of batch at %s" % datetime.now().astimezone().isoformat())

        time.sleep(60*10)
