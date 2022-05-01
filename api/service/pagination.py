from api.service.users_services import get_users, get_all_users_count, get_users_count
from api.service.movies_services import get_movies, get_all_movies_count, get_movies_count, get_liked_movies, get_all_liked_movies_count, get_liked_movies_count


def pagination(query_params, cls):
    page = query_params['page']
    per_page = query_params['per_page']
    sort = query_params.setdefault('sort', None)
    q = query_params.setdefault('q', None)

    if cls.__name__ == 'Users':
        if sort is None:
            sort = 'user_id'

        if q is None:
            total_results = get_all_users_count()
        else:
            total_results = get_users_count(q)

        results = get_users(page, per_page, sort, q)
    elif cls.__name__ == 'Movies':
        if sort is None:
            sort = 'movie_id'

        if q is None:
            total_results = get_all_movies_count()
        else:
            total_results = get_movies_count(q)

        results = get_movies(page, per_page, sort, q)

    total_pages = -(total_results // -per_page)  # Perform ceil division
    return {
        'results': results,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_results': total_results
    }


def pagination_liked_movies(query_params, user_id):
    page = query_params['page']
    per_page = query_params['per_page']
    sort = query_params.setdefault('sort', None)
    q = query_params.setdefault('q', None)

    if sort is None:
        sort = 'movie_id'

    if q is None:
        total_results = get_all_liked_movies_count(user_id)
    else:
        total_results = get_liked_movies_count(user_id, q)

    results = get_liked_movies(page, per_page, sort, q, user_id)

    total_pages = -(total_results // -per_page)  # Perform ceil division

    return {
        'results': results,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_results': total_results
    }
