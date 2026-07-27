from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 5               # Number of elements or record to show in a single page
    # page_query_param = 'p'      # To override the 'page' query param name, By default name is ?page=n;
    page_size_query_param = 'size'     # To override the page size settings by client  and give freedom to client. Ex- ?page=n&size=10
    max_page_size = 10           # To control the max element request in a page s by client.
    # last_page_strings = 'end'       # To go to the last page of any particular view. By default it is 'last'. Ex- ?page=last
    
class WatchListLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5             # Default number of elements to show 
    limit_query_param = 'limit'     # To override the 'limit' query param name, By default name is ?limit=n;
    offset_query_param ='start'     # To override the 'offset' query param name, By default name is ?offset=n;Ex - ?limit=5&offset=10.(Offset means from where to start the data show)
    max_limit = 10                  # To control the max element request in a page s by client.
    
class WatchListCursorPagination(CursorPagination):
    page_size = 5
    cursor_query_param = 'record'      # To override the 'cursor' query param name, By default name is ?cursor=jbdd29hbf28(cursor id);
    ordering = 'created_at'               # To ordering the data in a single page.  Defaults to -created .