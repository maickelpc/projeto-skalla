from rest_framework import routers

class RotasApi():
    rotasApi = routers.DefaultRouter()

    def __init__(self):
        print("teste")
        # self.router.register('profile',ProfileViewSet, 'Profile')
        # self.router.register('user',UserViewSet,'User')
        # self.router.register('fdd/arquivo',ArquivoFddViewSet,'ArquivoFdd')

    def rotas(self):
        return self.router.urls
