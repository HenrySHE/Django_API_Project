from rest_framework.pagination import LimitOffsetPagination

class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    # Set the max limit value to 8
    # 重写方法为8
    max_limit=8