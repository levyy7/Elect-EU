# User Collection with Validation
user_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "email", "password", "admin_rights"],
        "properties": {
            "user_id": {"bsonType": "int"},
            "email": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "password": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "admin_rights": {
                "bsonType": "bool",
                "description": "must be a boolean and is required",
            },
            "BSN": {
                "bsonType": "string",
                "description": "optional social security number",
            },
        },
    }
}


# Vote Options Collection with Validation
vote_option_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["vote_option_id", "election_id", "party_name", "candidates"],
        "properties": {
            "vote_option_id": {"bsonType": "int"},
            "election_id": {"bsonType": "int"},
            "party_name": {"bsonType": "string"},
            "candidates": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "must be an array of candidate names",
            },
            "photo": {
                "bsonType": "string",
                "description": "URL or path to party photo",
            },
        },
    }
}


# Election Collection with Validation
election_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["election_id", "election_date", "vote_options"],
        "properties": {
            "election_id": {"bsonType": "int"},
            "election_date": {"bsonType": "date", "description": "must be an ISODate"},
            "vote_options": {
                "bsonType": "array",
                "items": {"bsonType": "int"},
                "description": "must be an array of vote_option_id references",
            },
        },
    }
}


# Vote Collection with Validation
vote_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "vote_option_id", "timestamp"],
        "properties": {
            "user_id": {"bsonType": "int"},
            "vote_option_id": {"bsonType": "int"},
            "timestamp": {"bsonType": "date", "description": "must be an ISODate"},
        },
    }
}
