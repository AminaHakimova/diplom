from django.db import models


class Like(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE,
                               related_name='likes_user',
                               verbose_name='Автор')
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                             related_name='likes_post', verbose_name='Пост')

    def __str__(self):
        return f"{self.post.title} -- {self.author.username}"

    class Meta:
        db_table = 'likes'
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайки'
