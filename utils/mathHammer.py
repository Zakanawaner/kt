def getWoundsProb(attacker, defender):
    crt = 6 if 'lethal' not in attacker['weapon']['abilities'].keys() else attacker['weapon']['abilities']['lethal']
    normalProb = attacker['weapon']['a'] * (crt - attacker['weapon']['s']) / 6
    crtProb = attacker['weapon']['a'] * (7 - crt) / 6
    return normalProb * attacker['weapon']['n'] + crtProb * attacker['weapon']['c']


def getHitsSaved(defender, hits):
    pass
