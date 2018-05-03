from django.db.models import Manager, Count
from django.db.models.functions import Length
from taggit.managers import _TaggableManager

class AnswerManager(Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(upvotes_num=Count('upvotes')).order_by('-upvotes_num')

class _CustomTagManager(_TaggableManager):
    def most_common_public(self):
        return self.get_queryset().annotate(
                num_times=Count(self.through.tag_relname())
            ).order_by('-num_times')
