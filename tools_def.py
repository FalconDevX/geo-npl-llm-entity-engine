tools = [
    {
        "type": "function",
        "function": {
            "name": "search_place_by_name",
            "description": "Wyszukuje kod terytorialny (kod TERYT) dla podanej nazwy miejscowości lub miejsca - stosuj zawsze gdy jest pytanie o jakiekolwiek miejsce.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Nazwa miejscowości, np. Warszawa"}
                },
                "required": ["query"]
            }
        }
    }
]