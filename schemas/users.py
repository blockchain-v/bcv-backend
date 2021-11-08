userschema = {
    "collMod": "users",
    "validator": {
        "bsonType": "object",
        "required": ["address", "signedAddress"],
        "properties": {
            "address": {
                "bsonType": "string",
                "unique": True,
                "description": "must be a string and is required"
            },
            "signedAddress": {
                "bsonType": "string",
                "description": "must be a string and is required"
            }
        }
    }
}
