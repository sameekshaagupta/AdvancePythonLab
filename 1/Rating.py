import os
from collections import defaultdict

class Review:
    def_init__(self, productId, cId, date, rating, text):
    self.productId = productId
    self.cId = cId
    self.date = date
    self.rating = rating
    self.text = text

invalid = 0
valid = 0

def read_reviews_from_file(rating.txt):
    global invalid, valid
    reviews = []
    with open(rating.txt, 'r') as file:
        for line in file:
            data = line.strip().split(maxsplit=4)
            if len(data) == 5:
                productId, cId, date, rating, text = data
                reviews.append(Review(productId, cId, date, int(rating), text))
                valid += 1
            else:
                invalid += 1
            return reviews
        def calculate_avg_rating(reviews):
            product_ratings = defaultdict(list)
            for review in reviews:
                product_ratings[review.productId].append(review.rating)

            average_ratings = {productId:sum(ratings)/len(ratings) for productId,ratings in product_ratings.items()}
            return average_ratings