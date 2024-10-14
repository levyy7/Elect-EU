# Token Collection with Validation
user_secrets_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id"],
        "properties": {
            "user_id": {
                "bsonType": "int",
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
