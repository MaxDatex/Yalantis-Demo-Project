from datetime import datetime


def validate_args(args, method='post'):
    # strip data
    for arg in args:
        if type(args[arg]) == str:
            args[arg] = ' '.join(args[arg].split())

    # validate title
    if method == 'put' and args.get('title') and not args['title']:
        return False, 'Bad title!'
    if not args.get('title') or not args['title']:
        return False, 'Bad title!'

    # validate date
    start_date = args.get('start_date')
    end_date = args.get('end_date')
    if start_date is not None:
        if not _validate_date_format(start_date):
            return False, 'Bad date format.(YYYY-MM-DD)'
    if end_date is not None:
        if not _validate_date_format(end_date):
            return False, 'Bad date format.(YYYY-MM-DD)'

    return True, args


def _validate_date_format(date_string):
    format = "%Y-%m-%d"
    try:
        datetime.strptime(date_string, format)
    except ValueError:
        return False
    return True
