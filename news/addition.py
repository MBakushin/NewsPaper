"""This file contains values, functions, classes for file models.py"""
article = "AR"
news = "NE"

NOTES = [
    (article, "Статья"),
    (news, "Новость"),
]


class Grade:
    """Class contains two simple methods for models Post and Comment"""
    rating = 0
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
