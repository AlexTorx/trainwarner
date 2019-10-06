from anyblok import Declarations
from anyblok.column import Email


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
           * First Name : string that contains user first name
           * Last Name : string that contains user last name
           * Name : function that returns user full name

       Implemented fields are the following :

           * Email address : string that contains user email address

    """

    email = Email(label="Email Address", nullable=False, unique=True)
