from django.db import models
import uuid

# Create your models here.

class Genre(models.Model):
    """도서 장르"""
    name = models.CharField(max_length = 200, help_text='도서의 장르를 입력하시오. (예: SF)')

    def __str__(self):
        return self.name
    

class Book(models.Model):
    """도서 마스터 정보"""
    title = models.CharField(max_length = 200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length = 1000, help_text = '간단한 도서의 설명을 넣어주세요.')
    isbn = models.CharField('ISBN', max_length = 13, help_text='13글자의 <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>을 넣으십시오.')

    genre = models.ManyToManyField(Genre, help_text='도서의 장르를 고르십시오')
    language = models.ForeignKey('Language', on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """출간 개별 도서의 정보"""
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, help_text='특정 도서의 고유번호')
    book = models.ForeignKey('Book', on_delete = models.SET_NULL, null = True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null = True, blank = True)

    LOAN_STATUS = (
        ('m', '수선중'),
        ('o', '대출중'),
        ('a', '대여가능'),
        ('r', '예약됨'),
    )

    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text = '도서 대출가능여부',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null = True, blank = True)
    date_of_death = models.DateField('Died', null = True, blank = True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

class Language(models.Model):
    name = models.CharField(max_length = 200, help_text = '도서의 언어')

    def __str__(self):
        return self.name
