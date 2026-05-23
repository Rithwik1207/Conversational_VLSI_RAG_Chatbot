DEBUG_MODE = True


def debug_log(title, value=None):

    if not DEBUG_MODE:
        return

    print("\n" + "=" * 50)

    print(f"[DEBUG] {title}")

    if value is not None:

        print(value)

    print("=" * 50)