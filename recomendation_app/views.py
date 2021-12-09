import ast
import os

from django.http import JsonResponse
from django.shortcuts import render
# import request
# Create your views here.
from rest_framework import decorators, permissions
from rest_framework.response import Response
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

from recomendation import settings
from recomendation_app.models import *
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from recomendation_app.recommendations import *
import warnings

from recomendation_app.serilizers import PropertySerilizers


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def import_properties(request):
    if request.method == 'POST':
        if not request.data:
            return Response(data='data needed', status=400)
        items = [
            PropertyDetails(
                item_id=data['id'],
                lat=data['lat'],
                lon=data['lon'],
                country_long=data['country_long'],
                location_name=data['location_name'],
                route=data['route'],
                sub_locality_level_1=data['sub_locality_level_1'],
                sub_locality_level_2=data['sub_locality_level_2'],
                sub_locality_level_3=data['sub_locality_level_3'],
                sub_locality_level_4=data['sub_locality_level_4'],
                sub_locality_level_5=data['sub_locality_level_5'],
                administrative_area_level_1=data['administrative_area_level_1'],
                administrative_area_level_2=data['administrative_area_level_2'],
                administrative_area_level_3=data['administrative_area_level_3'],
                administrative_area_level_4=data['administrative_area_level_4'],
                administrative_area_level_5=data['administrative_area_level_5'],
                locality=data['locality'],
                property_name=data['property_name'],
                active_status=data['active_status'],
                searchable_status=data['searchable_status'],
                verification_status=data['verification_status'],
                administration_status=data['administration_status'],
                property_purpose=data['property_purpose'],
                property_long_description=data['property_long_description'],
                water_source=data['water_source'],
                sewage_source=data['sewage_source'],
                zoning=data['zoning'],
                keywords=data['keywords'],
                is_building=data['is_building'],
                has_blocks=data['has_blocks'],
                featured_status=data['featured_status'],
                views=data['views'],
                area=data['area'],
                area_description=data['area_description'],
                lowest_price=data['lowest_price'],
                highest_price=data['highest_price'],
                single_price=data['single_price'],
                negotiation=data['negotiation'],
                is_pets_allowed=data['is_pets_allowed'],
                amenities=data['amenities'],
                rating=data['ratings'],
                unit_count=data['unit_count'],
                property_type=data['property_type'],
                date_created=data['date_created'],
            )
            for data in request.data if not PropertyDetails.objects.filter(id=data['id']).exists()]
        PropertyDetails.objects.bulk_create(items, batch_size=100)
        return Response('done', status='200')
    return Response(data='Method not allowed', status=405)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def add_user(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        if not data:
            return Response(data='data needed', status=400)
        uzer = UsersToRecommend.objects.filter(item_id=data['id']).first()
        if not uzer:
            UsersToRecommend.objects.create(
                item_id=data['id'],
                email=data['email'],
                name=data['name']
            )
        else:
            uzer.email = data['email']
            uzer.name = data['name']
            uzer.save()
        return Response('done', status='200')
    return Response(data='Method not allowed', status=405)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def property_view_interaction(request):
    if request.method == 'POST':
        data = request.data
        if not data:
            return Response(data='data needed', status=400)
        user_id = data['user_id']
        property_id = data['property_id']
        view = data['view']
        # ui = UserInteractions.objects.filter(user__item_id=int(user_id), property__item_id=int(property_id)).first()
        if not UserInteractions.objects.filter(user__item_id=int(user_id), property__item_id=int(property_id)).exists():
            UserInteractions.objects.create(
                user=UsersToRecommend.objects.filter(item_id=int(user_id)).first(),
                property=PropertyDetails.objects.filter(item_id=int(property_id)).first(),
                view=view,
            )

        return Response('done', status='200')
    return Response(data='Method not allowed', status=405)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def add_property(request):
    if request.method == 'POST':
        data = request.data
        if not data:
            return Response(data='data needed', status=400)
        _property = PropertyDetails.objects.filter(item_id=data['id']).first()
        print(data['id'])
        if _property:
            _property.item_id = data['id'],
            _property.lat = data['lat'],
            _property.lon = data['lon'],
            _property.country_long = data['country_long'],
            _property.location_name = data['location_name'],
            _property.route = data['route'],
            _property.sub_locality_level_1 = data['sub_locality_level_1'],
            _property.sub_locality_level_2 = data['sub_locality_level_2'],
            _property.sub_locality_level_3 = data['sub_locality_level_3'],
            _property.sub_locality_level_4 = data['sub_locality_level_4'],
            _property.sub_locality_level_5 = data['sub_locality_level_5'],
            _property.administrative_area_level_1 = data['administrative_area_level_1'],
            _property.administrative_area_level_2 = data['administrative_area_level_2'],
            _property.administrative_area_level_3 = data['administrative_area_level_3'],
            _property.administrative_area_level_4 = data['administrative_area_level_4'],
            _property.administrative_area_level_5 = data['administrative_area_level_5'],
            _property.locality = data['locality'],
            _property.property_name = data['property_name'],
            _property.active_status = data['active_status'],
            _property.searchable_status = data['searchable_status'],
            _property.verification_status = data['verification_status'],
            _property.administration_status = data['administration_status'],
            _property.property_purpose = data['property_purpose'],
            _property.property_long_description = data['property_long_description'],
            _property.water_source = data['water_source'],
            _property.sewage_source = data['sewage_source'],
            _property.zoning = data['zoning'],
            _property.keywords = data['keywords'],
            _property.is_building = data['is_building'],
            _property.has_blocks = data['has_blocks'],
            _property.featured_status = data['featured_status'],
            _property.views = data['views'],
            _property.area = data['area'],
            _property.area_description = data['area_description'],
            _property.lowest_price = data['lowest_price'],
            _property.highest_price = data['highest_price'],
            _property.single_price = data['single_price'],
            _property.negotiation = data['negotiation'],
            _property.is_pets_allowed = data['is_pets_allowed'],
            _property.amenities = data['amenities'],
            _property.rating = data['ratings'],
            _property.unit_count = data['unit_count'],
            _property.property_type = data['property_type'],
            _property.date_created = data['date_created'],
            _property.save()
        else:
            p = PropertyDetails(
                item_id=data['id'],
                lat=data['lat'],
                lon=data['lon'],
                country_long=data['country_long'],
                location_name=data['location_name'],
                route=data['route'],
                sub_locality_level_1=data['sub_locality_level_1'],
                sub_locality_level_2=data['sub_locality_level_2'],
                sub_locality_level_3=data['sub_locality_level_3'],
                sub_locality_level_4=data['sub_locality_level_4'],
                sub_locality_level_5=data['sub_locality_level_5'],
                administrative_area_level_1=data['administrative_area_level_1'],
                administrative_area_level_2=data['administrative_area_level_2'],
                administrative_area_level_3=data['administrative_area_level_3'],
                administrative_area_level_4=data['administrative_area_level_4'],
                administrative_area_level_5=data['administrative_area_level_5'],
                locality=data['locality'],
                property_name=data['property_name'],
                active_status=data['active_status'],
                searchable_status=data['searchable_status'],
                verification_status=data['verification_status'],
                administration_status=data['administration_status'],
                property_purpose=data['property_purpose'],
                property_long_description=data['property_long_description'],
                water_source=data['water_source'],
                sewage_source=data['sewage_source'],
                zoning=data['zoning'],
                keywords=data['keywords'],
                is_building=data['is_building'],
                has_blocks=data['has_blocks'],
                featured_status=data['featured_status'],
                views=data['views'],
                area=data['area'],
                area_description=data['area_description'],
                lowest_price=data['lowest_price'],
                highest_price=data['highest_price'],
                single_price=data['single_price'],
                negotiation=data['negotiation'],
                is_pets_allowed=data['is_pets_allowed'],
                amenities=data['amenities'],
                rating=data['ratings'],
                unit_count=data['unit_count'],
                property_type=data['property_type'],
                date_created=data['date_created'],
            )
            p.save()
        return Response('done', status='200')
    return Response(data='Method not allowed', status=405)


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def get_recommendations(request):
    user_id = request.GET.get('user_id')
    items_req = request.GET.get('items', 10)
    uI = UserInteractions.objects.select_related('property').filter(user__item_id=int(user_id), view=True)
    all_prop = PropertyDetails.objects.all()
    # name_recommendations = get_property_name_recommendation(uI, all_prop, items_req)
    # location_name_recommendations = get_property_location_name_recommendation(uI, all_prop, items_req)
    # administrative_area_level_recommendations = get_property_administrative_area_level_recommendation(uI, all_prop, items_req)
    locality_recommendations = get_property_locality_recommendation(uI, all_prop, items_req)

    return Response({
        'recom_locality': locality_recommendations
        # 'admin_level_locality':administrative_area_level_recommendations
        # 'p_name':name_recommendations,
        # 'locato':location_name_recommendations,
        # 'formated_list': list(set(name_recommendations+location_name_recommendations))
    }, 200)


def test(request):
    # code

    warnings.simplefilter(action='ignore', category=FutureWarning)

    ratings = pd.read_csv(os.path.join(settings.BASE_DIR, 'ratings.csv'))
    ratings.head()
    # print(ratings)

    movies = pd.read_csv(os.path.join(settings.BASE_DIR, 'movies.csv'))
    movies.head()

    n_ratings = len(ratings)
    # print(n_ratings)
    n_movies = len(ratings['movieId'].unique())
    n_users = len(ratings['userId'].unique())

    # print(f"Number of ratings: {n_ratings}")
    # print(f"Number of unique movieId's: {n_movies}")
    # print(f"Number of unique users: {n_users}")
    # print(f"Average ratings per user: {round(n_ratings / n_users, 2)}")
    # print(f"Average ratings per movie: {round(n_ratings / n_movies, 2)}")
    print("======================================================")
    user_freq = ratings[['userId', 'movieId']].groupby('userId').count().reset_index()
    user_freq.columns = ['userId', 'n_ratings']
    user_freq.head()

    # return JsonResponse(user_freq, status=200, safe=False)
    # Find Lowest and Highest rated movies:
    mean_rating = ratings.groupby('movieId')[['rating']].mean()
    # print(mean_rating)
    # Lowest rated movies
    lowest_rated = mean_rating['rating'].idxmin()
    movies.loc[movies['movieId'] == lowest_rated]
    # Highest rated movies
    highest_rated = mean_rating['rating'].idxmax()
    movies.loc[movies['movieId'] == highest_rated]
    # show number of people who rated movies rated movie highest
    ratings[ratings['movieId'] == highest_rated]
    # show number of people who rated movies rated movie lowest
    ratings[ratings['movieId'] == lowest_rated]

    ## the above movies has very low dataset. We will use bayesian average
    movie_stats = ratings.groupby('movieId')[['rating']].agg(['count', 'mean'])
    movie_stats.columns = movie_stats.columns.droplevel()

    # Now, we create user-item matrix using scipy csr matrix
    from scipy.sparse import csr_matrix

    def create_matrix(df):

        N = len(df['userId'].unique())
        M = len(df['movieId'].unique())

        # Map Ids to indices
        user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
        movie_mapper = dict(zip(np.unique(df["movieId"]), list(range(M))))

        # Map indices to IDs
        user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
        movie_inv_mapper = dict(zip(list(range(M)), np.unique(df["movieId"])))

        user_index = [user_mapper[i] for i in df['userId']]
        movie_index = [movie_mapper[i] for i in df['movieId']]

        X = csr_matrix((df["rating"], (movie_index, user_index)), shape=(M, N))

        return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

    X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(ratings)

    from sklearn.neighbors import NearestNeighbors
    """
    Find similar movies using KNN
    """

    def find_similar_movies(movie_id, X, k, metric='cosine', show_distance=False):

        neighbour_ids = []

        movie_ind = movie_mapper[movie_id]
        movie_vec = X[movie_ind]
        k += 1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
        kNN.fit(X)
        movie_vec = movie_vec.reshape(1, -1)
        neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)
        for i in range(0, k):
            n = neighbour.item(i)
            neighbour_ids.append(movie_inv_mapper[n])
        neighbour_ids.pop(0)
        return neighbour_ids

    movie_titles = dict(zip(movies['movieId'], movies['title']))

    movie_id = 3

    similar_ids = find_similar_movies(movie_id, X, k=10)
    movie_title = movie_titles[movie_id]

    print(f"Since you watched {movie_title}")
    for i in similar_ids:
        print(movie_titles[i])
    return Response('yess')


# class MovieDataset:
#     def __init__(self, users, movies, ratings):
#         self.users = users
#         self.ratings = ratings
#         self.movies = movies
#
#     def __len__(self):
#         return len(self.users)
#
#     def __getitem__(self, item):
#         user = self.users[item]
#         movie = self.movies[item]
#         rate = self.ratings[item]
#

# MovieDataset()

def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1
def test2(request):
    all_prop = PropertyDetails.objects.all()
    f_data = PropertySerilizers(all_prop, many=True).data
    properties = pd.DataFrame(f_data)
    new_prop_frame = properties[[
        'id', 'item_id',
        'property_name', 'location_name',
        'property_long_description',
        'administrative_area_level_1','locality',
        'property_purpose',
        'water_source','sewage_source',
        'zoning','keywords',
        'is_building','has_blocks','featured_status',
        'views','area','area_description',
        'lowest_price','highest_price','single_price',
        'negotiation','is_pets_allowed',
        'amenities',
        'rating','property_type','unit_count', 'date_created'
    ]]
    new_prop_frame.dropna(inplace=True)
    new_prop_frame['keywords'] = new_prop_frame['keywords'].apply(collapse)
    new_prop_frame['important_features'] = new_prop_frame['location_name']+new_prop_frame['property_name']+new_prop_frame['administrative_area_level_1']+new_prop_frame['locality']+''.join(str(k) for k in new_prop_frame['keywords'])+new_prop_frame['property_long_description']
    new_head = new_prop_frame.drop(columns=['location_name', 'administrative_area_level_1', 'locality', 'keywords', 'property_long_description'])
    cv = CountVectorizer()
    vector = cv.fit_transform(new_head['important_features']).toarray()
    similarity = cosine_similarity(vector)

    def recommend(movie):
        index = new_head[new_head['property_name'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:6]:
            print(new_head.iloc[i[0]].property_name, new_head.iloc[i[0]].is_building)
    recommend('Building No Blocks')
    # l =new_head[new_head['property_name'] == 'juja'].index[0]
    # prin/t(l)
    # print(new_head.head(4))
    return JsonResponse(data=f_data, status=200, safe=False)



















