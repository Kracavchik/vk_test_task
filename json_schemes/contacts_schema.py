contacts_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "pattern": r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",
            "minLength": 6,
            "maxLength": 127
        },
        "first_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 127
        },
        "last_name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 127
        },
        "phone": {
            "type": "string",
            "pattern": r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
        },
        "country": {
            "type": "string",
            "maxLength": 64
        },
        "city": {
            "type": "string",
            "maxLength": 64
        },
        "address": {
            "type": "string",
            "maxLength": 256
        },
    }
}
