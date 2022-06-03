from datetime import datetime


def logAccess(endPoint, user, request):
    today = datetime.today().strftime('%Y-%m-%d')
    hour = datetime.today().strftime('%H:%M:%S')
    name = user.username if not user.is_anonymous else 'anonymous'
    with open('log/{}.txt'.format(today), 'a') as lg:
        lg.write(hour + '\t\t' + request.remote_addr + '\t\t' + request.method + '\t\t' + endPoint + '\t\t' + name + '\n')
        lg.close()
