from django.db import models


def upload_path(instance, filename):
    return '/'.join(['user_images', filename])

# 사용자 이미지 저장
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_img = models.ImageField(blank=True, upload_to=upload_path)
    # user_img_url = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    user_email = models.EmailField(blank=True)

    def __str__(self):
        return f'[{self.user_id}]'


# 결과물 이미지 저장
class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    result_img_path = models.CharField(max_length=250)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    result_emotion = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.result_id}]'
