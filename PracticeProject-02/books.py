class Book:
    id: int
    tittle: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id, tittle, author, description, rating, publish_date):
        self.id = id
        self.tittle = tittle
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date

BOOKS =[
    Book(1, "Harry Potter", "Siam", "Fantasy Movie", 9, 2030),
    Book(2, "Baybled", "Fahim", "Anime", 8, 2030),
    Book(3, "Pokemon", "Juton", "Animation series", 10, 2029),
    Book(4, "Sinchen", "Habib", "Funny Carton", 7, 2000),
]