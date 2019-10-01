from anyblok import Declarations
from anyblok.column import String, DateTime, Boolean, Date
from anyblok.relationship import Many2One, Many2Many

from datetime import datetime, date, timezone


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Model)
class JourneyWish(Mixin.UuidColumn, Mixin.TrackModel, Mixin.WorkFlow):

    """This model has Model.JourneyWish as a namespace. It is intented for
       storing journey wishes that represents travels intentions.

       For instance, an intention may be caracterized by start date, with an
       a time frame delimited by earlier and latest departure times,
       departure and arrival stations, passengers, maximum price, etc...

       Implemented fields are the following :

           * Departure station : Many2One relationship with Model.Station
           * Arrival station : Many2One relationship with Model.Station
           * Start date : DateTime representing earlier time after which train
           may leave the departure station
           * End date : DateTime representing latest time after which train may
           leave departure station.
           * Passengers : Many2Many relationship to Model.Passenger
           * Transportation mean : String, containing type of transport
           required by user (train, coach, etc...)
           * Active : boolean that stores if wish has to be processed
           * Activation date : Date, represent the moment when the wish could
           start being processed"""

    departure = Many2One(label="Departure Station",
                         model=Model.Station,
                         nullable=True,
                         one2many="departures"
                         )

    arrival = Many2One(label="Arrival Station",
                       model=Model.Station,
                       nullable=True,
                       one2many="arrivals"
                       )

    from_date = DateTime(label="Earlier Departure Date", nullable=True)
    end_date = DateTime(label="Latest Departure Date", nullable=True)
    activation_date = Date(label="Activation Date",
                           nullable=True,
                           default=date.today
                           )

    passengers = Many2Many(model=Model.Passenger,
                           join_table="join_passengers_by_wishes",
                           remote_columns="uuid", local_columns="uuid",
                           m2m_remote_columns="p_uuid",
                           m2m_local_columns="w_uuid",
                           many2many="wishes"
                           )

    transportation_mean = String(label="Transportation Mean",
                                 default="any",
                                 nullable=True
                                 )

    active = Boolean(label="Active Wish", nullable=True)

    @classmethod
    def get_workflow_definition(cls):

        """This method is aimed at defining workflow used for model
           Model.JourneyWish"""

        return {
            'draft': {
                'default': True,
                'allowed_to': ['running', 'pending'],
                'apply_change': 'deactivate'
                },
            'running': {
                'allowed_to': ['cancelled', 'expired'],
                'apply_change': 'activate'
                },
            'pending': {
                'allowed_to': ['cancelled', 'expired', 'running'],
                'apply_change': 'deactivate'
                },
            'expired': {
                'apply_change': 'deactivate'
                },
            'cancelled': {
                'apply_change': 'deactivate'
                }
            }

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def check_state(self):

        """This method is aimed at being used in order to automatically set
           workflow state, depending on record attributes."""

        if self.state == 'pending':
            # If wish is pending, check is activation_date is set
            if self.activation_date and self.activation_date <= date.today():
                self.state_to('running')

        elif self.state == 'running':
            # If wish is already running, check that from_date is not in the
            # past

            try:
                now = datetime.now().astimezone()
            except ValueError:
                # Python3.5 and below do not support astimezone on 'naive'
                # dates provided by datetime.now()
                now = datetime.now(timezone.utc).astimezone()

            if self.from_date and self.from_date < now:
                self.state_to('expired')
