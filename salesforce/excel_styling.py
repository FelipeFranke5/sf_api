def get_column_header():
    column_header = {
        'style': {
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
            },
            'font': {
                'name': 'Calibri',
                'size': 10,
                'bold': True,
            },
        },
    }
    return column_header


def get_body():
    body = {
        'style': {
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
            },
            'font': {
                'name': 'Calibri',
                'size': 9,
                'bold': False,
            },
        },
    }
    return body


def get_xlsx_ignore_headers():
    xlsx_ignore_headers = ['notes']
    return xlsx_ignore_headers
