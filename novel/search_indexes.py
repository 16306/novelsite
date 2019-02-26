from haystack import indexes
from .models import Nover


class NoverIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Nover

    def index_queryset(self, using=None):
        return self.get_model().objects.all()