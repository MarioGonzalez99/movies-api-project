# This file should contain records you want created when you run flask db seed.
#
# Example:
# from yourapp.models import User
import os
from api.model.roles import Roles
from api.model.users import Users
from api.model.genres import Genres
from api.model.movies import Movies
from api.service.roles_services import create_rol
from api.service.register_services import create_user
from api.service.genres_services import create_genre
from api.service.movies_services import create_movie

if len(Roles.query.all()) == 0:
    create_rol('admin')
    create_rol('regular')

if Users.query.filter_by(username='admin').first() is None:
    admin_pssw = os.environ.get('ADMIN_PASSWORD') or 'admin'
    create_user(username='admin', password=admin_pssw, rol='admin')

if Users.query.filter_by(username='regular').first() is None:
    regular_pssw = os.environ.get('REGULAR_PASSWORD') or 'regular'
    create_user(username='regular', password=regular_pssw, rol='regular')

if len(Genres.query.all()) == 0:
    create_genre('action')
    create_genre('drama')
    create_genre('comedy')
    create_genre('romance')
    create_genre('horror')
    create_genre('thriller')
    create_genre('fantasy')
    create_genre('sci-fi')

if len(Movies.query.all()) == 0:
    create_movie(
        title='Spider-Man: No Way Home',
        description="Peter Parker is unmasked and no longer able to separate his normal life from the high-stakes of being a super-hero. When he asks for help from Doctor Strange the stakes become even more dangerous, forcing him to discover what it truly means to be Spider-Man.",
        date_released='2021-12-17',
        genre='action',
        budget=200_000_000,
        revenue=1_809_940_686
    )

    create_movie(
        title='The Shawshank Redemption',
        description="Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden.",
        date_released='1994-09-23',
        genre='drama',
        budget=25_000_000,
        revenue=28_341_469
    )

    create_movie(
        title='Interstellar',
        description="The adventures of a group of explorers who make use of a newly discovered wormhole to surpass the limitations on human space travel and conquer the vast distances involved in an interstellar voyage.",
        date_released='2014-11-07',
        genre='sci-fi',
        budget=165_000_000,
        revenue=701_729_206
    )

    create_movie(
        title='The Godfather',
        description="Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family. When organized crime family patriarch, Vito Corleone barely survives an attempt on his life, his youngest son, Michael steps in to take care of the would-be killers, launching a campaign of bloody revenge.",
        date_released='1972-03-15',
        genre='drama',
        budget=6_000_000,
        revenue=245_066_411
    )

    create_movie(
        title='Parasite',
        description="All unemployed, Ki-taek's family takes peculiar interest in the wealthy and glamorous Parks for their livelihood until they get entangled in an unexpected incident.",
        date_released='2019-05-30',
        genre='comedy',
        budget=11_363_000,
        revenue=257_591_776
    )

    create_movie(
        title="Schindler's List",
        description="The true story of how businessman Oskar Schindler saved over a thousand Jewish lives from the Nazis while they worked as slaves in his factory during World War II.",
        date_released='1994-02-04',
        genre='drama',
        budget=22_000_000,
        revenue=321_365_567
    )
