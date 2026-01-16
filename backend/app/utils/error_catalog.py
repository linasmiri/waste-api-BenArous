"""Create error_catalog.py with ErrorCatalog class:
Define ERRORS dictionary with these error codes:
- AUTH_001: {"code": 401, "message": "Invalid credentials"}
- AUTH_002: {"code": 401, "message": "Unauthorized access"}
- USER_001: {"code": 400, "message": "User already exists"}
- USER_002: {"code": 404, "message": "User not found"}
- BATCH_001: {"code": 400, "message": "Invalid batch data"}
- BATCH_002: {"code": 400, "message": "Invalid material type"}
- BATCH_003: {"code": 404, "message": "Batch not found"}
- HOTSPOT_001: {"code": 400, "message": "Invalid hotspot coordinates"}
- HOTSPOT_002: {"code": 404, "message": "Hotspot not found"}
- ROUTE_001: {"code": 400, "message": "Insufficient hotspots for routing"}
- VALIDATION_001: {"code": 422, "message": "Data validation failed"}

Add static method get_error(error_code) that returns error dict or default {"code": 500, "message": "Unknown error"}.
"""

class ErrorCatalog:
    """Error catalog for all API errors"""
    
    ERRORS = {
        "AUTH_001": {
            "code": 401,
            "message": "Invalid credentials"
        },
        "AUTH_002": {
            "code": 401,
            "message": "Unauthorized access"
        },
        "USER_001": {
            "code": 400,
            "message": "User already exists"
        },
        "USER_002": {
            "code": 404,
            "message": "User not found"
        },
        "BATCH_001": {
            "code": 400,
            "message": "Invalid batch data"
        },
        "BATCH_002": {
            "code": 400,
            "message": "Invalid material type"
        },
        "BATCH_003": {
            "code": 404,
            "message": "Batch not found"
        },
        "HOTSPOT_001": {
            "code": 400,
            "message": "Invalid hotspot coordinates"
        },
        "HOTSPOT_002": {
            "code": 404,
            "message": "Hotspot not found"
        },
        "ROUTE_001": {
            "code": 400,
            "message": "Insufficient hotspots for routing"
        },
        "VALIDATION_001": {
            "code": 422,
            "message": "Data validation failed"
        }
    }
    
    @staticmethod
    def get_error(error_code: str) -> dict:
        """
        Get error details by error code.
        
        Args:
            error_code: The error code to look up
            
        Returns:
            dict: Error details with 'code' and 'message' keys.
                  Returns default 500 error if code not found.
        """
        return ErrorCatalog.ERRORS.get(
            error_code,
            {"code": 500, "message": "Unknown error"}
        )
