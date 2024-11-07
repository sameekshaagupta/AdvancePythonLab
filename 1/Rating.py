import os
from collections import defaultdict

class Review:
    def __init__(self, productId, cId, date, rating, text):
        self.productId = productId
        self.cId = cId
        self.date = date
        self.rating = rating
        self.text = text

valid = 0
invalid = 0

def read_reviews_from_file(filename):
    global invalid, valid
    reviews = []
    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split(maxsplit=4)
            if len(data) == 5:
                productId, cId, date, rating, text = data
                reviews.append(Review(productId, cId, date, int(rating), text))
                valid += 1
            else:
                invalid += 1
    return reviews

def calculate_average_ratings(reviews):
    product_ratings = defaultdict(list)
    for review in reviews:
        product_ratings[review.productId].append(review.rating)

    average_ratings = {productId: sum(ratings) / len(ratings) for productId, ratings in product_ratings.items()}
    return average_ratings

folder_path = 'sample_data'
all_reviews = []

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        all_reviews.extend(read_reviews_from_file(file_path))

average_ratings = calculate_average_ratings(all_reviews)

#task 1
print("Average Ratings for All Products:")
for productId, avg_rating in average_ratings.items():
    print(f'Product ID: {productId}, Average Rating: {avg_rating:.2f}')


def get_second_element(item):
    return item[1]


sorted_products = sorted(average_ratings.items(), key=get_second_element, reverse=True)


top_products = sorted_products[:3]

#task 2
print("\nTop 3 Products with Highest Average Ratings:")
for productId, avg_rating in top_products:
    print(f'Product ID: {productId}, Average Rating: {avg_rating:.2f}')
# task 3
print(f'\nValid Reviews: {valid}')
print(f'Invalid Reviews: {invalid}')

# task 4
# Create and write summary to summary.txt
with open('summary.txt', 'w') as summary_file:
    summary_file.write(f'Total Reviews Processed: {valid + invalid}\n')
    summary_file.write(f'Valid Reviews: {valid}\n')
    summary_file.write(f'Invalid Reviews: {invalid}\n\n')
    summary_file.write('Top 3 Products with Highest Average Ratings:\n')
    for productId, avg_rating in top_products:
        summary_file.write(f'Product ID: {productId}, Average Rating: {avg_rating:.2f}\n')

print("\nSummary written to summary.txt")
