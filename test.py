# import requests

# test_dict = {
#   "adult": False,
#   "backdrop_path": "/hZkgoQYus5vegHoetLkCJzb17zJ.jpg",
#   "belongs_to_collection": "",
#   "budget": 63000000,
#   "genres": [
#     {
#       "id": 18,
#       "name": "Drama"
#     },
#     {
#       "id": 53,
#       "name": "Thriller"
#     },
#     {
#       "id": 35,
#       "name": "Comedy"
#     }
#   ],
#   "homepage": "http://www.foxmovies.com/movies/fight-club",
#   "id": 550,
#   "imdb_id": "tt0137523",
#   "original_language": "en",
#   "original_title": "Fight Club",
#   "overview": "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an out-of-control spiral toward oblivion.",
#   "popularity": 61.416,
#   "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
#   "production_companies": [
#     {
#       "id": 508,
#       "logo_path": "/7cxRWzi4LsVm4Utfpr1hfARNurT.png",
#       "name": "Regency Enterprises",
#       "origin_country": "US"
#     },
#     {
#       "id": 711,
#       "logo_path": "/tEiIH5QesdheJmDAqQwvtN60727.png",
#       "name": "Fox 2000 Pictures",
#       "origin_country": "US"
#     },
#     {
#       "id": 20555,
#       "logo_path": "/hD8yEGUBlHOcfHYbujp71vD8gZp.png",
#       "name": "Taurus Film",
#       "origin_country": "DE"
#     },
#     {
#       "id": 54051,
#       "logo_path": "",
#       "name": "Atman Entertainment",
#       "origin_country": ""
#     },
#     {
#       "id": 54052,
#       "logo_path": "",
#       "name": "Knickerbocker Films",
#       "origin_country": "US"
#     },
#     {
#       "id": 4700,
#       "logo_path": "/A32wmjrs9Psf4zw0uaixF0GXfxq.png",
#       "name": "The Linson Company",
#       "origin_country": "US"
#     },
#     {
#       "id": 25,
#       "logo_path": "/qZCc1lty5FzX30aOCVRBLzaVmcp.png",
#       "name": "20th Century Fox",
#       "origin_country": "US"
#     }
#   ],
#   "production_countries": [
#     {
#       "iso_3166_1": "US",
#       "name": "United States of America"
#     }
#   ],
#   "release_date": "1999-10-15",
#   "revenue": 100853753,
#   "runtime": 139,
#   "spoken_languages": [
#     {
#       "english_name": "English",
#       "iso_639_1": "en",
#       "name": "English"
#     }
#   ],
#   "status": "Released",
#   "tagline": "Mischief. Mayhem. Soap.",
#   "title": "Fight Club",
#   "video": False,
#   "vote_average": 8.433,
#   "vote_count": 26280
# }


# API_KEY = "f84bd283f269ae39390fd22e875d5941"
# movie = "Oppenheimer"
# movie_id = 872585

# api_url  = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
# headers = {
#         "accept": "application/json",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDM2MjcxM2YxNDJiODQ0OGFiNjIwMTM1ZDMzZjA1MSIsIm5iZiI6MTcyNTU1NDY0Mi41OTA0MTYsInN1YiI6IjY2ZDlkOTVhMWUwMzA1MTZjYTJhMDc5YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mb1f0BGvBzEl7CeV1LXIxGvapbAVZ7CIyUm3_b724HY"
#             }
# response = requests.get(api_url, headers=headers)
# print(response.text)

values = [i for i in range(1, 100)]
def is_even(val):
    if val % 2 == 0:
        return True
    else:
        return False


list_of_even = list(filter(is_even, values))
print(list_of_even)

