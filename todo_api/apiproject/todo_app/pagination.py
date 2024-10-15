from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class TodoListPagination(PageNumberPagination):
    page_size = 5


class TodoLOPagination(LimitOffsetPagination):
    default_limit = 5


class TodoCursorPagination(CursorPagination):
    page_size = 5
    ordering = 'created'