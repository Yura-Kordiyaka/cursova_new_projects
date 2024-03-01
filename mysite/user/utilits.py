def validate_password(pwd):
    conds = [
        lambda s: any(x.isupper() for x in s),
        lambda s: any(x.islower() for x in s),
        lambda s: any(x.isdigit() for x in s),
        lambda s: any(x.isspace() for x in s),
        lambda s: len(s) >= 8
    ]

    return all(cond(pwd) for cond in conds)
