def get_real_page(page, buttons_on_page, cnt):
    if page < 1:
        return 1

    max_page = (cnt + buttons_on_page - 1) // buttons_on_page
    max_page = max(max_page, 1)
    if page > max_page:
        return max_page
    return page