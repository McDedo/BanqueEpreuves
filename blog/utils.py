
def get_matiere_icon(nom):
    return {
        "Mathématiques": "📐",
        "Physique-Chimie": "⚛️",
        "Français": "📚",
        "SVT": "🔬",
        "Anglais": "🇬🇧",
        "Histoire-Géographie": "🌍",
        "Philosophie": "🤔",
        "EPS": "🏃",
        "Informatique": "💻",
        "Économie": "💰",
        "Technologie": "🔧",
        "Espagnol": "🗣️",
        "Allemand": "🗣️",
        "Arts Appliqués": "🎨",
    }.get(nom, "📘")
