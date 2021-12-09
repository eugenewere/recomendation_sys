from statistics import mode

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from recomendation_app.models import *


def get_property_name_recommendation(uI, all_prop, items_req):
    viewed_properties = [i.property.property_name for i in uI if i]
    is_build = [i.property.is_building for i in uI if i]
    cm = CountVectorizer().fit_transform([p.property_name for p in all_prop])
    cs = cosine_similarity(cm)
    vector = SearchVector('property_name')
    query = SearchQuery(' '.join(viewed_properties).replace(',', '').replace('-', '').replace(' ', ' | '), search_type='raw')
    scores = []
    for i in PropertyDetails.objects.annotate(search=vector).filter(search=query, is_building=mode(is_build)).exclude(id__in=[i.id for i in uI if i]):
        try:
            scores.append(list(enumerate(cs[i.id])))
        except Exception:
            pass

    liked = []
    try:
        sorted_scores = sorted(scores[0], key=lambda x: x[1], reverse=True)
        sorted_scores = sorted_scores

        for item in sorted_scores[:items_req]:
            prop = PropertyDetails.objects.filter(id=item[0]).first()
            if prop:
                liked.append(prop.item_id)
    except Exception:
        pass
    return liked


def get_property_location_name_recommendation(uI, all_prop, items_req):
    viewed_properties = [i.property.location_name for i in uI if i]
    is_build = [i.property.is_building for i in uI if i]
    # print(viewed_properties)
    cm = CountVectorizer().fit_transform([p.location_name for p in all_prop])
    cs = cosine_similarity(cm)
    # print(' '.join(viewed_properties).replace(',', '').replace('-', '').replace(' ', ' | '))
    vector = SearchVector('location_name')
    item_name = ' '.join(viewed_properties) \
        .replace(',', '') \
        .replace('-', '').replace('Unnamed', ' ').replace(' ', ' | ')
    query = SearchQuery(item_name, search_type='raw')
    scores = []
    for i in PropertyDetails.objects.annotate(search=vector).filter(search=query, is_building=mode(is_build)).exclude(id__in=[i.id for i in uI if i]):
        try:
            scores.append(list(enumerate(cs[i.id])))
        except Exception:
            pass
    liked = []
    try:
        sorted_scores = sorted(scores[0], key=lambda x: x[1], reverse=True)
        sorted_scores = sorted_scores
        for item in sorted_scores[:items_req]:
            prop = PropertyDetails.objects.filter(id=item[0]).first()
            if prop:
                liked.append(prop.item_id)
    except Exception:
        pass
    return liked


def get_property_administrative_area_level_recommendation(uI, all_prop, items_req):
    viewed_properties = [i.property.administrative_area_level_1 for i in uI if i]
    is_build = [i.property.is_building for i in uI if i]
    print(viewed_properties)
    print(','.join(viewed_properties).replace(',', ' '))
    # print()
    cm = CountVectorizer().fit_transform([i.administrative_area_level_1 for i in all_prop])
    cs = cosine_similarity(cm)
    vector = SearchVector('administrative_area_level_1', 'administrative_area_level_2', 'administrative_area_level_3', 'administrative_area_level_4', 'administrative_area_level_5')
    item_name = ','.join(viewed_properties).replace(',', ' | ')
    # print(item_name)
    query = SearchQuery(item_name, search_type='websearch')
    scores = []
    for i in PropertyDetails.objects.annotate(search=vector).filter(search=query, is_building=mode(is_build)).exclude(id__in=[i.id for i in uI if i]):
        try:
            scores.append(list(enumerate(cs[i.id])))
        except Exception:
            pass
    liked = []
    try:
        sorted_scores = sorted(scores[0], key=lambda x: x[1], reverse=True)
        sorted_scores = sorted_scores
        for item in sorted_scores[:items_req]:
            prop = PropertyDetails.objects.filter(id=item[0]).first()
            if prop:
                liked.append(prop.item_id)
    except Exception:
        pass
    return liked


def get_property_locality_recommendation(uI, all_prop, items_req):
    viewed_properties = [i.property.locality.replace(' ', '_') for i in uI if i]
    is_build = [i.property.is_building for i in uI if i]
    print(viewed_properties)
    print(','.join(viewed_properties).replace(',', ' '))
    # print([i.locality for i in all_prop if i.locality ])
    items_all=[i.locality for i in all_prop ]
    cm = CountVectorizer().fit_transform(items_all)
    count_vector = cm.fit_transform(items_all)
    print(count_vector)
    cs = cosine_similarity(cm)
    # print(cs)
    # vector = SearchVector('locality')
    # item_name = ','.join(viewed_properties).replace(',', ' | ')
    # print(item_name)
    # query = SearchQuery(item_name, search_type='raw')
    scores = []
    for i in PropertyDetails.objects.filter(locality__in=viewed_properties, is_building=mode(is_build)).exclude(id__in=[i.id for i in uI if i]):
        print(i.locality)
        try:
            scores.append(list(enumerate(cs[i.id])))
        except Exception:
            pass
    liked = []
    try:
        sorted_scores = sorted(scores[0], key=lambda x: x[1], reverse=True)
        sorted_scores = sorted_scores
        for item in sorted_scores[:items_req]:
            prop = PropertyDetails.objects.filter(id=item[0]).first()
            if prop:
                liked.append(prop.item_id)
    except Exception:
        pass
    print(liked)
    return liked
