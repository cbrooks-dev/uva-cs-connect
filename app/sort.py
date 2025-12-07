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
