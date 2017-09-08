operators = {
    'OR': {
        'prec': 1,
        'assoc': 'left',
        'arity': 2,
    },

    'AND': {
        'prec': 2,
        'assoc': 'left',
        'arity': 2
    },

    'NOT': {
        'prec': 3,
        'assoc': 'right',
        'arity': 1,
    }
}