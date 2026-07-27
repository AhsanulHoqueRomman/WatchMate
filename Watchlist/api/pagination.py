from rest_framework.pagination import PageNumberPagination


class WatchListPagination(PageNumberPagination):
    page_size = 5               # Number of elements or record to show in a single page
    page_query_param = 'p'      # To override the query param name, By default name is ?page=n;
    page_size_query_param = 'size'     # To override the page size settings by client  and give freedom to client. Ex- ?page=n&size=10
    max_page_size = 10           # To control the page size number by client.
    last_page_strings = 'end'       # To go to the last page of any particular view. By default it is 'last'. Ex- ?page=last
    
