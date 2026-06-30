def project_profile(profile, config):
    """
    Project the canonical profile based on runtime configuration.
    Supports field selection and field renaming.
    """

    fields = config.get("fields", [])
    rename = config.get("rename", {})

    projected = {}

    for field in fields:

        if field not in profile:
            continue

        output_name = rename.get(field, field)

        projected[output_name] = profile[field]

    return projected