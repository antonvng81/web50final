from django.db.models import Q

def Q_search_title(search_str):
    search_list = search_str.split()
    q = Q()
    for s in search_list:
        q |= Q(title__icontains=s)
    return q

def Q_search_location(search_str):
    search_list = search_str.split()
    q = Q()
    for s in search_list:
        q |= Q(location__icontains=s)
    return q    


def Q_search_cv_text(search_str):
    search_list = search_str.split()
    q = Q()
    for s in search_list:
        q |= Q(cv__text__icontains=s)
    return q
