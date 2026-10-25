# rule-based признаки

RULES = {
    "experience": {
        "еда": ["кафе", "кофе", "ресторан", "кухн", "меню", "пицц", "обед", "ужин"],
        "культура": ["музей", "искусств", "экспоз", "театр", "спектакл", "концерт"],
        "прогулка": ["парк", "прогул", "набереж", "лес"],
        "развлечения": ["аттракцион", "маркет", "планетар"],
    },
    "atmosphere": {
        "уютное": ["уют", "тих", "спокой"],
        "шумное": ["шум", "многолюд", "жив"],
        "романтичное": ["романт", "вид", "панорам"],
        "деловое": ["бизнес", "ланч", "ноутбук", "работ"],
    },
    "context": {
        "семья": ["дет", "семь", "детск"],
        "друзья": ["друз", "компани", "праздник"],
        "свидание": ["романт", "свидан"],
        "работа": ["ноутбук", "работ", "тих"],
    },
    "budget": {
        "низкий": ["недорог", "дешев", "столов", "студен"],
        "средний": ["средн", "сеть"],
        "высокий": ["дорог", "роскош", "премиум"],
    },
    "time": {
        "утро": ["завтрак", "утр"],
        "день": ["обед", "ланч"],
        "вечер": ["ужин", "вечер", "спектакл"],
    },
}

CAT_EXP = {"cafe": "еда", "restaurant": "еда", "museum": "культура", "park": "прогулка"}


def _tags(text, mapping):
    t = text.lower()
    return [label for label, keys in mapping.items() if any(k in t for k in keys)]


def extract_features(row):
    text = f"{row.get('description', '')} {row.get('reviews', '')} {row.get('name', '')}"
    cat = row.get("category", "")

    exp = _tags(text, RULES["experience"]) or [CAT_EXP.get(cat, "развлечения")]
    atm = _tags(text, RULES["atmosphere"])
    ctx = _tags(text, RULES["context"])
    budget = _tags(text, RULES["budget"]) or (["низкий"] if cat in ("museum", "park") else ["средний"])
    time = _tags(text, RULES["time"]) or (["вечер"] if cat in ("theatre", "restaurant") else ["день"])

    rev = str(row.get("reviews", "")).lower()
    pop = min(1.0, len(rev) / 400)
    if "рейтинг" in rev:
        pop += 0.2
    if any(w in rev for w in ("турист", "очеред", "популяр")):
        pop += 0.3

    return {
        "experience": ", ".join(exp[:2]),
        "atmosphere": ", ".join(atm) if atm else "нейтральное",
        "visit_context": ", ".join(ctx) if ctx else "любой",
        "budget": budget[0],
        "time_of_day": ", ".join(time[:2]),
        "popularity": round(min(1.0, pop), 2),
    }
