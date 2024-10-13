# Token Collection with Validation
token_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["email"],
        "properties": {
            "email": {
                "bsonType": "string",
                "description": "Email of the user associated with this token",
            },
            "authentication_token": {
                "bsonType": "string",
                "description": "Authentication token for 2FA",
            },
            "bearer_token": {
                "bsonType": "string",
                "description": "Bearer token for API authentication",
            },
        },
    }
}

