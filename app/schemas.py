# User Collection with Validation
user_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["BSN", "email", "password", "admin_rights"],
        "properties": {
            "BSN": {"bsonType": "int"},
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
        },
    }
}

# Vote Collection with Validation
votes_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["BSN", "vote_option_id"],
        "properties": {
            "BSN": {
                "bsonType": "int",
                "description": "BSN of the user casting the vote",
            },
            "vote_option_id": {
                "bsonType": "int",
                "description": "ID of the selected vote option",
            },
        },
    }
}

# Vote Options Collection with Validation
vote_option_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["vote_option_id", "election_id", "party_name"],
        "properties": {
            "vote_option_id": {
                "bsonType": "int",
                "description": "Auto-incremented ID for the vote option",
            },
            "election_id": {
                "bsonType": "int",
                "description": "ID of the election this vote option belongs to",
            },
            "party_name": {"bsonType": "string", "description": "Name of the party"},
            "photo": {
                "bsonType": "string",
                "description": "URL or path to the party photo",
            },
        },
    }
}

# Candidates Collection with Validation
candidates_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["vote_option_id", "candidate_name"],
        "properties": {
            "vote_option_id": {
                "bsonType": "int",
                "description": "Reference to the vote option",
            },
            "candidate_name": {
                "bsonType": "string",
                "description": "Name of the candidate",
            },
        },
    }
}


# Election Collection with Validation
election_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["election_id", "election_date"],
        "properties": {
            "election_id": {
                "bsonType": "int",
                "description": "Auto-incremented ID for the election",
            },
            "election_date": {
                "bsonType": "date",
                "description": "ISO date of the election",
            },
        },
    }
}
