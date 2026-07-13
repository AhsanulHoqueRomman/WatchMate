from rest_framework.throttling import UserRateThrottle

class WatchListAVThrottle(UserRateThrottle):
    scope = 'watch-list'
    
class ReviewListCreateThrottle(UserRateThrottle):
    scope = 'review-list'