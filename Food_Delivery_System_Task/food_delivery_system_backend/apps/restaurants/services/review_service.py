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
        
    def create_review(self) -> dict:
        """
        Creates new view

        Returns:
            dict: returns review data in ReturnDict object
        """
        serializer = self.obj.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return serializer.data
    
    def retrieve_review(self) -> dict:
        """
        Retrieve review by id

        Returns:
            dict: returns review data in ReturnDict object
        """
        review = self.obj.get_object()
        serializer = self.obj.get_serializer(review)
        
        return serializer.data
    
    def list_review(self) -> list:
        """
        Retrieves list of reviews
        
        Returns:
            list: returns list of dictionaries containing review data
        """
        queryset = self.obj.filter_queryset(self.obj.get_queryset())
        page = self.obj.paginate_queryset(queryset)
        if page is not None:
            serializer = self.obj.get_serializer(page, many=True)
            return self.obj.get_paginated_response(serializer.data).data

        serializer = self.obj.get_serializer(queryset, many=True)
        return serializer.data
    
    def update_review(self, partial_flag) -> dict:
        """
        updaes review by id id either partially or whole review
        
        Args:
            partial_flag (bool): retrun true if update to be performed is partially else false
        Returns:
            dict: returns review data in ReturnDict object
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
        