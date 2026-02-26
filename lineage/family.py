from .models import Person


def build_descendants_tree(person, depth=5):
    """
    Recursively builds a descendants-only tree.
    """

    if depth == 0:
        return None

    return {
        "id": person.id,
        "name": str(person),
        "gender": person.gender,
        "age": person.get_age(),
        "status": person.status,
        "children": [
            build_descendants_tree(child, depth - 1)
            for child in person.get_children()
        ]
    }


def get_family_tree(person_id, depth=5):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
        return None

    return build_descendants_tree(person, depth)
