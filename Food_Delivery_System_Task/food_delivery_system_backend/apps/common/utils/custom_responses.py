from rest_framework.response import Response

def success_response(message: str, status_code, data=None) -> Response:
    """
    Returns a customized Response.
    
    Args:
        message (str): standard success message
        data (dict, list, or None): serilizer payload
        status_code (int): HTTP status code
    Return:
        DRF Response with modified response data structure
    """
    
    payload = {
        "success": True,
        "message": message,
        "data": data,
        "status_code": status_code
    }
    
    return Response(payload, status=status_code)

def error_response(error: str, status_code) -> Response:
    """
    Returns a customized Response.
    
    Args:
        error (str): standard error message
        status_code (int): HTTP status code
    Return:
        DRF Response with modified response data structure
    """
    
    payload = {
        "success": False,
        "error": error,
        "status_code": status_code
    }
    
    return Response(payload, status=status_code)
    