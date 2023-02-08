from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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


def set_keyboard_1(x, callback_x):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
            ],
        ]
    )


def set_keyboard_row_3(
    x,
    y,
    z,
    callback_x,
    callback_y,
    callback_z,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
                InlineKeyboardButton(y, callback_data=str(callback_y)),
                InlineKeyboardButton(z, callback_data=str(callback_z)),
            ]
        ]
    )


def set_keyboard_column_3(
    x,
    y,
    z,
    callback_x,
    callback_y,
    callback_z,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
            ],
            [
                InlineKeyboardButton(y, callback_data=str(callback_y)),
            ],
            [
                InlineKeyboardButton(z, callback_data=str(callback_z)),
            ],
        ]
    )


def set_keyboard_triangle_3(
    x,
    y,
    z,
    callback_x,
    callback_y,
    callback_z,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
                InlineKeyboardButton(y, callback_data=str(callback_y)),
            ],
            [
                InlineKeyboardButton(z, callback_data=str(callback_z)),
            ],
        ]
    )


def set_keyboard_square_4(
    x,
    y,
    z,
    t,
    callback_x,
    callback_y,
    callback_z,
    callback_t,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
                InlineKeyboardButton(y, callback_data=str(callback_y)),
            ],
            [
                InlineKeyboardButton(z, callback_data=str(callback_z)),
                InlineKeyboardButton(t, callback_data=str(callback_t)),
            ],
        ]
    )


def set_keyboard_square_5(
    x,
    y,
    z,
    t,
    s,
    callback_x,
    callback_y,
    callback_z,
    callback_t,
    callback_s,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(x, callback_data=str(callback_x)),
                InlineKeyboardButton(y, callback_data=str(callback_y)),
            ],
            [
                InlineKeyboardButton(z, callback_data=str(callback_z)),
                InlineKeyboardButton(t, callback_data=str(callback_t)),
            ],
            [
                InlineKeyboardButton(s, callback_data=str(callback_s)),
            ],
        ]
    )
