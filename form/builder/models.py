from django.db import models


class Form(models.Model):
    name = models.CharField(max_length=191)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    TEXT = 'text'
    LONG_TEXT = 'long-text'
    ATTACHMENT = 'attachment'
    QUESTION_CHOICE = (
        (TEXT, 'Text'),
        (LONG_TEXT, 'Long Text'),
        (ATTACHMENT, 'Attachment'),
    )
    text = models.CharField(max_length=191)
    choice = models.CharField(max_length=191, choices=QUESTION_CHOICE, default=TEXT)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.form.name

    @property
    def name(self):
        return self.form.name

    @property
    def slug(self):
        return self.form.slug


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
