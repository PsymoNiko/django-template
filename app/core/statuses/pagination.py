# from rest_framework.response import Response
# from rest_framework import status
# from django.utils.translation import gettext_lazy as _
# from django.db.models import Q
# from django.core.paginator import Paginator
# import math
# from unidecode import unidecode
# from backend.exceptions import AbanException
# from django.contrib.contenttypes.models import ContentType
# from users.models import Referral, UserEvent
#
#
# class ListMixinException(AbanException):
#     pass
#
#
# class ListMixin:
#     filterable_fields = []
#     searchable_fields = []
#     sortable_fields = []
#     default_page_count = 10
#
#     OP_MAPPING = {
#         '<': '__lt',
#         '>': '__gt',
#         '<=': '__lte',
#         '>=': '__gte',
#         '=': '',
#         'c': '__contains',
#         '!=': '__not',
#         'in': '__in'
#     }
#
#     def __init__(self) -> None:
#         self._queryset = None
#         self.data = None
#         self._paging = False
#
#     def binary_operate(self, first, second, op):
#         if op == 'and':
#             return first & second
#         if op == 'or':
#             return first | second
#         raise ListMixinException(_("invalid binary operator"))
#
#     def render_iter(self, data):
#         if not isinstance(data, dict):
#             raise ListMixinException(_("invalid Q object"))
#
#         if 'op' not in data and 'rules' not in data:
#             raise ListMixinException(_("invalid Q object"))
#
#         result = Q()
#         rules = data['rules']
#         for cell in rules:
#             result = self.binary_operate(result, self.render(data=cell), data['op'])
#
#         return result
#
#     def render_cell(self, data, allow_field=False):
#         if len(data) != 3:
#             raise ListMixinException(_("invalid Q object cell"))
#
#         field = data[0]
#         op = data[1]
#         value = data[2]
#
#         if field not in self.filterable_fields and not allow_field:
#             raise ListMixinException(_("field must be included in filterable fields"))
#
#         if hasattr(self, 'render_filter_' + field) and callable(getattr(self, 'render_filter_' + field)) is True:
#             render_field = getattr(self, 'render_filter_' + field)(op=op, value=value)
#             return render_field
#
#         if op not in self.OP_MAPPING:
#             raise ListMixinException(_("invalid operator"))
#         if op == '!=':
#             query = {
#                 field: value
#             }
#             return ~Q(**query)
#         query = {
#             field + self.OP_MAPPING[op]: value
#         }
#         return Q(**query)
#
#     def render(self, data):
#         if isinstance(data, dict):
#             return self.render_iter(data=data)
#         if isinstance(data, list):
#             return self.render_cell(data=data)
#
#         raise ListMixinException(_("invalid Q object cell"))
#
#     def filter(self):
#         rendered = self.render(self.data['filter'])
#         self._queryset = self._queryset.filter(rendered)
#
#     def render_search(self):
#         search = self.data['search']
#         search = unidecode(search) if search.isnumeric() else search
#
#         result = Q()
#
#         if search == '':
#             return result
#
#         for field in self.searchable_fields:
#             render_field = Q(**{field + '__icontains': search})
#             if hasattr(self, 'render_search_' + field) and callable(getattr(self, 'render_search_' + field)) is True:
#                 render_field = getattr(self, 'render_search_' + field)(text=search)
#             result = result | render_field
#
#         return result
#
#     def search(self):
#         self._queryset = self._queryset.filter(self.render_search()).distinct()
#
#     def sort(self):
#         if 'field' not in self.data['sort']:
#             raise ListMixinException(_("invalid sort query"))
#
#         if 'type' not in self.data['sort']:
#             raise ListMixinException(_("invalid sort query"))
#
#         type = self.data['sort']['type']
#         field = self.data['sort']['field']
#         if field not in self.sortable_fields:
#             raise ListMixinException(_("field not in sortable fields"))
#
#         self._queryset = self._queryset.order_by(field)
#         if type == 'asc':
#             return
#         if type == 'desc':
#             self._queryset = self._queryset.reverse()
#             return
#         raise ListMixinException(_("invalid sort type"))
#
#     @staticmethod
#     def paginate(queryset, count, page):
#         total_count = queryset.count()
#         paging = Paginator(queryset, count)
#         page_count = math.ceil(total_count / count)
#         page = min(page, page_count)
#         page = max(page, 1)
#         result = paging.page(page).object_list
#         return result, page, len(result), page_count, total_count
#
#     def paging(self, count, page):
#         self._paging = True
#         self._queryset, self.page, self.per_page, self.page_count, self.total_count = self.paginate(
#             queryset=self._queryset, count=count, page=page)
#
#     def _get_queryset(self):
#         self._queryset = super().get_queryset()
#         if self.data is None:
#             return self._queryset
#
#         if 'filter' in self.data:
#             self.filter()
#         if 'search' in self.data and len(self.data['search']):
#             self.search()
#         if 'sort' in self.data:
#             self.sort()
#         return self._queryset
#
#     def get_queryset(self):
#         self._queryset = self._get_queryset()
#         if self.data is None:
#             return self._queryset
#
#         self.paging(count=int(self.data.get('count', self.default_page_count)), page=int(self.data.get('page', 1)))
#         return self._queryset
#
#     def post(self, request, *args, **kwargs):
#         self.data = request.data
#
#         response = self.get(request, *args, **kwargs)
#
#         data = list(response.data)
#         if self._paging:
#             data = {
#                 'data': data,
#                 'page': self.page,
#                 'per_page': self.per_page,
#                 'page_count': self.page_count,
#                 'total': self.total_count
#             }
#
#         return Response(data, status=status.HTTP_200_OK)
#
#     def render_search_phone_number(self, text):
#         text = unidecode(text)
#         if text[0:2] == '09':
#             text = '+98' + text[1:]
#         return Q(**{'phone_number' + '__icontains': text})
#
#     def render_search_user__phone_number(self, text):
#         text = unidecode(text)
#         if text[0:2] == '09':
#             text = '+98' + text[1:]
#         return Q(**{'user__phone_number' + '__icontains': text})
#
#     def render_search_creator_name_code(self, text):
#         user_event_content_type = ContentType.objects.get_for_model(UserEvent)
#         referral_content_type = ContentType.objects.get_for_model(Referral)
#         user_event_query = Q(content_type=user_event_content_type,
#                              object_id__in=UserEvent.objects.filter(
#                                  Q(user__customer__referral__name__icontains=text) | Q(
#                                      user__customer__referral__code__icontains=text)).values('pk'))
#         referral_query = Q(content_type=referral_content_type,
#                            object_id__in=Referral.objects.filter(
#                                Q(name__icontains=text) | Q(code__icontains=text)).values('pk'))
#         return Q() | user_event_query | referral_query
#

from rest_framework.pagination import BasePagination

from rest_framework.pagination import BasePagination

from rest_framework.pagination import PageNumberPagination


# class CustomPagination(PageNumberPagination):
#     page_size_query_param = 'page_size'
#
#     def get_paginated_response(self, data):
#         return {
#             'data': data,
#             'page': self.page.number,
#             'per_page': self.page.paginator.per_page,
#             'page_count': self.page.paginator.num_pages,
#             'total': self.page.paginator.count,
#         }
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    # def get_paginated_response(self, data):
    #     return Response({
    #         'links': {
    #             'next': self.get_next_link(),
    #             'previous': self.get_previous_link()
    #         },
    #         'count': self.page.paginator.count,
    #         'results': data
    #     })

    def get_paginated_response(self, data):
        return {
            'data': data,
            'page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'page_count': self.page.paginator.num_pages,
            'total': self.page.paginator.count,
        }
