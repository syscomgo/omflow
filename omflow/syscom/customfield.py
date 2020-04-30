from django.db import models
import datetime
from django.contrib.auth.models import UserManager


class DateTimeTextField(models.TextField):
    def __init__(self, verbose_name=None, name=None, auto_now=False,
                 auto_now_add=False, **kwargs):
        self.auto_now, self.auto_now_add = auto_now, auto_now_add
        if auto_now or auto_now_add:
            kwargs['editable'] = False
            kwargs['blank'] = True
        super().__init__(verbose_name, name, **kwargs)
    
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.auto_now is not False:
            kwargs["auto_now"] = self.auto_now
        if self.auto_now_add is not False:
            kwargs["auto_now_add"] = self.auto_now_add
        if self.auto_now or self.auto_now_add:
            del kwargs['blank']
            del kwargs['editable']
        return name, path, args, kwargs
    
    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = datetime.datetime.now()
            value = str(value)
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
        
        
class FormatManager(models.Manager):
    def filterformat(self, *args, **kwargs):
        all_list = models.Manager.get_queryset(self)
        search_list = all_list.filter(**kwargs).values(*args)
        for search_item in search_list:
            for field in search_item:
                field_class = search_item[field].__class__.__name__
                if field_class == 'datetime':
                    search_item[field] = str(search_item[field])
                elif field_class == 'UUID':
                    search_item[field] = search_item[field].hex
        return search_list
    
    def getdictformat(self, *args, **kwargs):
        filterformat = self.filterformat(*args, **kwargs)
        result = list(filterformat)[0]
        return result


class UserFormatManager(UserManager):
    def filterformat(self, *args, **kwargs):
        all_list = models.Manager.get_queryset(self)
        search_list = all_list.filter(**kwargs).values(*args)
        for search_item in search_list:
            for field in search_item:
                field_class = search_item[field].__class__.__name__
                if field_class == 'datetime':
                    search_item[field] = str(search_item[field])
                elif field_class == 'UUID':
                    search_item[field] = search_item[field].hex
        return search_list
    