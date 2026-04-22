class ReviewService:
    """
    Handles logic for reviews.
    
    This service manages create, update, retrieve, delete and list operations
    on reviews.
    """
    def __init__(self, view_object, request_object):
        """
        Initializes service class object with view and request object
        """
        
        self.obj = view_object
        self.request = request_object
        
    def create_review(self):
        """
        Creates new view
        """
        serializer = self.obj.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return serializer.data
    
    def retrieve_review(self):
        """
        Retrieve review by id
        """
        review = self.obj.get_object()
        serializer = self.obj.get_serializer(review)
        
        return serializer.data
    
    def list_review(self):
        """
        Retrieves list of reviews
        """
        queryset = self.obj.filter_queryset(self.obj.get_queryset())
        page = self.obj.paginate_queryset(queryset)
        if page is not None:
            serializer = self.obj.get_serializer(page, many=True)
            return self.obj.get_paginated_response(serializer.data).data

        serializer = self.obj.get_serializer(queryset, many=True)
        return serializer.data
    
    def update_review(self, partial_flag):
        """
        updaes review by id id either partially or whole review
        """
        review = self.obj.get_object()
        serializer = self.obj.get_serializer(
            review,
            data=self.request.data,
            partial=partial_flag
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return serializer.data
        