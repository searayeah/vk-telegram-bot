from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def set_keyboard_1(a):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
            ],
        ]
    )


def set_keyboard_rows_2(a, b):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
            ],
            [
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
            ],
        ]
    )


def set_keyboard_3(a, b, c):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
            ],
            [
                InlineKeyboardButton(c[0], callback_data=str(c[1])),
            ],
        ]
    )


def set_keyboard_4(a, b, c, d):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
            ],
            [
                InlineKeyboardButton(c[0], callback_data=str(c[1])),
                InlineKeyboardButton(d[0], callback_data=str(d[1])),
            ],
        ]
    )


def set_keyboard_5(a, b, c, d, e):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
            ],
            [
                InlineKeyboardButton(c[0], callback_data=str(c[1])),
                InlineKeyboardButton(d[0], callback_data=str(d[1])),
            ],
            [
                InlineKeyboardButton(e[0], callback_data=str(e[1])),
            ],
        ]
    )


def set_keyboard_6(a, b, c, d, e, f):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
            ],
            [
                InlineKeyboardButton(c[0], callback_data=str(c[1])),
                InlineKeyboardButton(d[0], callback_data=str(d[1])),
            ],
            [
                InlineKeyboardButton(e[0], callback_data=str(e[1])),
                InlineKeyboardButton(f[0], callback_data=str(f[1])),
            ],
        ]
    )


def set_keyboard_7(a, b, c, d, e, f, g):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
            ],
            [
                InlineKeyboardButton(c[0], callback_data=str(c[1])),
                InlineKeyboardButton(d[0], callback_data=str(d[1])),
            ],
            [
                InlineKeyboardButton(e[0], callback_data=str(e[1])),
                InlineKeyboardButton(f[0], callback_data=str(f[1])),
            ],
            [
                InlineKeyboardButton(g[0], callback_data=str(g[1])),
            ],
        ]
    )


def set_keyboard_8(
    a,
    b,
    c,
    d,
    e,
    f,
    g,
    h,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
            ],
            [
                InlineKeyboardButton(c[0], callback_data=str(c[1])),
                InlineKeyboardButton(d[0], callback_data=str(d[1])),
            ],
            [
                InlineKeyboardButton(e[0], callback_data=str(e[1])),
                InlineKeyboardButton(f[0], callback_data=str(f[1])),
            ],
            [
                InlineKeyboardButton(g[0], callback_data=str(g[1])),
                InlineKeyboardButton(h[0], callback_data=str(h[1])),
            ],
        ]
    )


def set_keyboard_columns_3(a, b, c):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
                InlineKeyboardButton(c[0], callback_data=str(c[1])),
            ]
        ]
    )


def set_keyboard_rows_3(a, b, c):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(a[0], callback_data=str(a[1])),
            ],
            [
                InlineKeyboardButton(b[0], callback_data=str(b[1])),
            ],
            [
                InlineKeyboardButton(c[0], callback_data=str(c[1])),
            ],
        ]
    )
