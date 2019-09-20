from anyblok import Declarations
from anyblok.column import String, DateTime
from anyblok.relationship import Many2One, Many2Many

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Model)
class JourneyWish(Mixin.UuidColumn, Mixin.TrackModel, Mixin.Workflow):

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
           required by user (train, coach, etc...)"""

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
