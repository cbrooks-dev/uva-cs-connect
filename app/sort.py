def sort_users(users, method="name"):
    """
    Sorts a list of user dicts by different methods.
    Available methods:
      - "name": alphabetical by last name, then first name
      - "grad_year": lowest → highest graduation year
    """

    if method == "grad_year":
        return sorted(users, key=lambda u: (u.get("grad_year") or 9999,
                                            u.get("last_name", ""),
                                            u.get("first_name", "")))

    # default: alphabetical by last name, then first name
    return sorted(users, key=lambda u: (u.get("last_name", "").lower(),
                                        u.get("first_name", "").lower()))


# sort.py
def sort_events(sort_key):
    if sort_key == "start_asc":
        return "ORDER BY start_datetime ASC"
    elif sort_key == "start_desc":
        return "ORDER BY start_datetime DESC"
    elif sort_key == "alpha_asc":
        return "ORDER BY title ASC"
    else:
        return "ORDER BY start_datetime ASC"  # default


