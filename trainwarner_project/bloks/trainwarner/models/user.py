from anyblok import Declarations
from anyblok.column import String


register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Model)
class User(Mixin.TrackModel):

    """This model ovverrides Model.User from anyblok_pyramid. It is intented
       for representing a trainwarner user.

       Inherited fields are the following :

           * login : String representing login used for authenticating users.
           For this field, the email address will be used.

       Implemented fields are the following :

           These first fields overrides already existing fields :
           * First Name : nullable string that contains user first name
           * Last Name : nullable string that contains user last name
    """

    first_name = String(label="First Name", nullable=True)
    last_name = String(label="Last Name", nullable=True)
