from django.db import models

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book_title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='Pending')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_title