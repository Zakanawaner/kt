import inspect
import sys
import requests

from bs4 import BeautifulSoup
from database import MathOperative, MathRanged, MathAction, MathPsychic, MathMelee, MathAbility, MathWeaponAbility


# TODO coger las clases que etán definidas y convertirlas en database para guardar directamente en la base de datos

class MathHammer:
    @staticmethod
    def getWoundsProb(attacker, defender):
        abis = [ab.name for ab in attacker.melee[0].SP]
        crt = 6 if 'lethal' not in abis else 5
        normalProb = int(attacker.melee[0].A) * (crt - int(attacker.melee[0].BS)) / 6
        crtProb = int(attacker.melee[0].A) * (7 - crt) / 6
        return normalProb * int(attacker.melee[0].D) + crtProb * int(attacker.melee[0].DC)

    @staticmethod
    def getHitsSaved(defender, hits):
        pass

    @staticmethod
    def fromWahapedia(url, operatives=None):
        if operatives is None:
            operatives = []
        soup = BeautifulSoup(requests.get(url).text)
        obs = inspect.getmembers(sys.modules[__name__])
        for dataSlate in soup.find_all("div", {'class': 'pagebreak'}):
            print(dataSlate.find('h3', {'class': 'pTable_h3'}).text)
            rangedWeapons = []
            meleeWeapons = []
            for wp in dataSlate.find_all('tbody', {'class': 'bkg'}):
                if wp.find('td', {'class': 'wsDataRanged'}):
                    try:
                        try:
                            nm = wp.find('tr', {'class': 'wTable2_short'}).find_all('td')[1].text
                        except AttributeError:
                            nm = ''
                    except IndexError:
                        nm = ''
                    for e in wp.find_all('tr'):
                        if not e.get("class"):
                            f = 0
                            newWp = {
                                'name': nm + e.find_all('td')[1 if nm else 2].text,
                                'a': e.find_all('td')[2 if nm else 3].text,
                                's': e.find_all('td')[3 if nm else 4].text.replace('+', ''),
                                'dn': e.find_all('td')[4 if nm else 5].text.split('/')[0],
                                'dc': e.find_all('td')[4 if nm else 5].text.split('/')[1],
                                'abn': [],
                                'abc': []
                            }
                            if wp.find('td', {'align': 'center', 'class': 'wTable1_long'}):
                                try:
                                    for w in \
                                    wp.find('td', {'align': 'center', 'class': 'wTable1_long'}).text.split('. ')[
                                        0].split(', '):
                                        for ob in obs:
                                            if ob[0].lower() in w.lower().replace(' ', ''):
                                                newWp['abn'].append(ob[1]())
                                                break
                                except IndexError:
                                    pass
                                try:
                                    for w in \
                                    wp.find('td', {'align': 'center', 'class': 'wTable1_long'}).text.split('. ')[
                                        1].split(', '):
                                        for ob in obs:
                                            if ob[0].lower() in w.lower().replace(' ', ''):
                                                newWp['abc'].append(ob[1]())
                                                break
                                except IndexError:
                                    pass
                            # TODO pasar las abilidades a clase de sqlalchemy
                            rangedWeapons.append(MathRanged(name=newWp['name'],
                                                            a=newWp['a'],
                                                            bws=newWp['s'],
                                                            d=newWp['dn'],
                                                            dc=newWp['dc'],
                                                            sp=newWp['abn'],
                                                            critic=newWp['abc']))
                if wp.find('td', {'class': 'wsDataMelee'}):
                    try:
                        try:
                            nm = wp.find('tr', {'class': 'wTable2_short'}).find_all('td')[1].text
                        except AttributeError:
                            nm = ''
                    except IndexError:
                        nm = ''
                    for e in wp.find_all('tr'):
                        if not e.get("class"):
                            f = 0
                            newWp = {
                                'name': nm + e.find_all('td')[1 if nm else 2].text,
                                'a': e.find_all('td')[2 if nm else 3].text,
                                's': e.find_all('td')[3 if nm else 4].text.replace('+', ''),
                                'dn': e.find_all('td')[4 if nm else 5].text.split('/')[0],
                                'dc': e.find_all('td')[4 if nm else 5].text.split('/')[1],
                                'abn': [],
                                'abc': []
                            }
                            if wp.find('td', {'align': 'center', 'class': 'wTable1_long'}):
                                try:
                                    for w in \
                                    wp.find('td', {'align': 'center', 'class': 'wTable1_long'}).text.split('. ')[
                                        0].split(', '):
                                        for ob in obs:
                                            if ob[0].lower() in w.lower().replace(' ', ''):
                                                newWp['abn'].append(ob[1]())
                                                break
                                except IndexError:
                                    pass
                                try:
                                    for w in wp.find('td',
                                                    {'align': 'center', 'class': 'wTable1_long'}).text.split('. ')[1].split(', '):
                                        for ob in obs:
                                            if ob[0].lower() in w.lower().replace(' ', ''):
                                                newWp['abc'].append(ob[1]())
                                                break
                                except IndexError:
                                    pass
                            # TODO pasar las abilidades a clase de sqlalchemy
                            meleeWeapons.append(MathMelee(name=newWp['name'],
                                                          a=newWp['a'],
                                                          bws=newWp['s'],
                                                          d=newWp['dn'],
                                                          dc=newWp['dc'],
                                                          sp=newWp['abn'],
                                                          critic=newWp['abc']))
            abilities = []
            try:
                for a in dataSlate.find('table',
                                        {'class': 'dsAbility_short'}).find_all('tr')[1].find_all('div',
                                                                                                 {'class': 'BreakInsideAvoid'}):
                    abilities.append(MathAbility(
                        name=a.find('b').text,
                        description=a.text.replace(a.find('b').text, '')
                    ))
            except IndexError:
                pass
            actions = []
            try:
                for a in dataSlate.find('table',
                                        {'class': 'dsAbility_short'}).find_all('tr')[3].find_all('div',
                                                                                                 {'class': 'BreakInsideAvoid'}):
                    actions.append(MathAction(
                        name=a.find('b').text.split(' (')[0],
                        cost=a.find('b').text.split(' (')[1][0],
                        description=a.text.replace(a.find('b').text, '')
                    ))
            except IndexError:
                pass
            operatives.append(MathOperative(
                name=dataSlate.find('h3', {'class': 'pTable_h3'}).text,
                m=dataSlate.find('table', {'class': 'pTable_border'}).find_all('td', {'class': 'pCell2'})[0].text,
                apl=dataSlate.find('table', {'class': 'pTable_border'}).find_all('td', {'class': 'pCell2'})[1].text,
                ga=dataSlate.find('table', {'class': 'pTable_border'}).find_all('td', {'class': 'pCell2'})[2].text,
                df=dataSlate.find('table', {'class': 'pTable_border'}).find_all('td', {'class': 'pCell2'})[3].text,
                sv=dataSlate.find('table', {'class': 'pTable_border'}).find_all('td', {'class': 'pCell2'})[4].text,
                wn=dataSlate.find('table', {'class': 'pTable_border'}).find_all('td', {'class': 'pCell2'})[5].text,
                ranged=rangedWeapons,
                melee=meleeWeapons,
                ab=abilities,
                ac=actions,
                kw=dataSlate.find('div', {'class': 'dsKeywords_in'}).text.replace('\n', ''),
                ps=[]  # TODO
            ))
        return operatives


symbols = {
    '▲': 1,
    '⬤': 2,
    '⬛': 4,
    '⬟': 6,
}


class Faction:
    def __init__(self, superfact, name):
        self.superfact = superfact
        self.name = name
        self.operatives = []
        self.abilities = []


class Operative:
    def __init__(self, name, melee, m, apl, ga, df, sv, wn, ranged, ab, ac, kw, ps):
        self.name = name
        self.M = m
        self.APL = apl
        self.GA = ga
        self.DF = df
        self.SV = sv
        self.W = wn
        self.melee = melee
        self.ranged = ranged
        self.abilities = ab
        self.actions = ac
        self.keywords = kw
        self.psychic = ps


class Action:
    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description


class Psychic:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Ability:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class WeaponAbility:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Rng(WeaponAbility):
    def __init__(self, x='⬟'):
        super().__init__('rng x', 'Range. Each time a friendly operative makes a shooting attack with this weapon, '
                                  'only operatives within x are a valid target, x is the distance after the weapon’s '
                                  'Rng, e.g. Rng . All other rules for selecting a valid target still apply.')
        self.range = symbols[x]


class Lethal(WeaponAbility):
    def __init__(self, x='5+'):
        super().__init__('lethal x', 'Range. Each time a friendly operative makes a shooting attack with this weapon, '
                                     'only operatives within x are a valid target, x is the distance after the weapon’s '
                                     'Rng, e.g. Rng . All other rules for selecting a valid target still apply.')
        self.x = int(x[0])


class AP(WeaponAbility):
    def __init__(self, x=1):
        super().__init__('apx', "Each time a friendly operative makes a shooting attack with this weapon, subtract x "
                                "from the Defence of the target for that shooting attack. x is the number after the "
                                "weapon's AP, e.g. AP1. If two different APx special rules would be in effect for a "
                                "shooting attack, they are not cumulative - the attacker selects which one to use.")
        self.x = x


class P(WeaponAbility):
    def __init__(self, x=1):
        super().__init__('px', "Piercing. Each time a friendly operative makes a shooting attack with this weapon, in "
                               "the Roll Attack Dice step of that shooting attack, if you retain any critical hits, the "
                               "weapon gains the APx special rule for that shooting attack, x is the number after the "
                               "weapon’s P, e.g. P1.")
        self.x = x


class Balanced(WeaponAbility):
    def __init__(self):
        super().__init__('balanced', "Each time a friendly operative fights in combat or makes a shooting attack with "
                                     "this weapon, in the Roll Attack Dice stop of that combat or shooting attack, you "
                                     "can re-roll one of your attack dice.")


class Blast(WeaponAbility):
    def __init__(self, x='⬤'):
        super().__init__('blast x', "Each time a friendly operative performs a Shoot action and selects this weapon (or, "
                                    "in the case of profiles, this weapon&#8217;s profile), after making the shooting "
                                    "attack against the target, make a shooting attack with this weapon (using the same "
                                    "profile) against each other operative Visible to and within X of the original "
                                    "target &#8211; each of them is a valid target and cannot be in Cover. X is the "
                                    "distance after the weapon&#8217;s Blast, e.g. Blast . An operative cannot make a "
                                    "shooting attack with this weapon by performing an Overwatch action.")
        self.x = symbols[x]


class Ceaseless(WeaponAbility):
    def __init__(self):
        super().__init__('ceaseless', "Each time a friendly operative fights in combat or makes a shooting attack with "
                                      "this weapon, in the Roll Attack Dice step of that combat or shooting attack, "
                                      "you can re-roll any or all of your attack dice results of 1.")


class Favoured(WeaponAbility):
    def __init__(self):
        super().__init__('favoured of the dark gods', "Once per Turning Point, when it is your turn to use a Strategic "
                                                      "Ploy, if any friendly operatives with this ability are in the "
                                                      "kill zone, you can use a Strategic Ploy without spending any "
                                                      "CPs; that Strategic Ploy must have the same &lt;MARK OF "
                                                      "CHAOS&gt; selectable keyword as one friendly operative with "
                                                      "this ability. For example, if an operative with this ability "
                                                      "has the KHORNE keyword, you could use the Blood for the Blood "
                                                      "God Strategic Ploy. If an operative with this ability has the "
                                                      "UNDIVIDED keyword, you can use the following Strategic Ploys "
                                                      "for this ability instead: Hateful Assault, Malicious Volleys.")


class Fusillade(WeaponAbility):
    def __init__(self):
        super().__init__('fusillade', "Each time a friendly operative performs a Shoot action and selects this weapon, "
                                      "after selecting a valid target, you can select any number of other valid "
                                      "targets within &#11044; of the original target. Distribute your attack dice "
                                      "between the targets you have selected. Make a shooting attack with this weapon "
                                      "(using the same profile) against each of the targets you have selected using "
                                      "the attack dice you have distributed to each of them.")


class Heavy(WeaponAbility):
    def __init__(self):
        super().__init__('heavy', "An Operative cannot perform a Charge, Fall Back or Normal Move action in the same "
                                  "activation in which it performs a Shoot action with this ranged weapon.")


class Hot(WeaponAbility):
    def __init__(self):
        super().__init__('hot', "Each time a friendly operative makes a shooting attack with this weapon, in the Roll "
                                "Attack Dice step of that shooting attack, for each attack dice result of 1 that is "
                                "discarded, that operative suffers 3 mortal wounds.")


class MW(WeaponAbility):
    def __init__(self, x=1):
        super().__init__('mwx', "Each time a friendly operative makes a shooting attack with this weapon, in the Roll "
                                "Attack Dice step of that shooting attack, for each critical hit retained, inflict x "
                                "mortal wounds on the target. x is the number after the weapon's MW, e.g. MW3.")
        self.x = x


class NoCover(WeaponAbility):
    def __init__(self):
        super().__init__('no cover', "Each time a friendly operative makes a shooting attack with this weapon, for "
                                     "that shooting attack, defence dice cannot be automatically retained as a result "
                                     "of Cover (they must be rolled instead).")


class Reap(WeaponAbility):
    def __init__(self, x=1):
        super().__init__('reap x', "Each time a friendly operative fights in combat with this weapon, in the Resolve "
                                   "Successful Hits step of that combat, if you strike with a critical hit, inflict x "
                                   "mortal wounds on each other enemy operative Visible to the friendly operative and "
                                   "within &#9650; of it or the target operative. x is the number after the weapon's "
                                   "Reap, e.g. Reap 1.")
        self.x = x


class Relentless(WeaponAbility):
    def __init__(self):
        super().__init__('relentless', "Each time a friendly operative fights in combat or makes a shooting attack "
                                       "with this weapon, in the Roll Attack Dice step of that combat or shooting "
                                       "attack, you can re-roll any or all of your attack dice.")


class Rending(WeaponAbility):
    def __init__(self):
        super().__init__('Rending', "Each time a friendly operative fights in combat or makes a shooting attack with "
                                    "this weapon, in the Roll Attack Dice step of that combat or shooting attack, if "
                                    "you retain any critical hits you can retain one normal hit as a critical hit.")


class Splash(WeaponAbility):
    def __init__(self, x=1):
        super().__init__('splash x', "Each time a friendly operative makes a shooting attack with this weapon, in the "
                                     "Roll Attack Dice step of that shooting attack, for each critical hit retained, "
                                     "inflict x mortal wounds on the target and each other operative Visible to and "
                                     "within &#11044; of it. x is the number after the weapon's Splash, e.g. Splash 1.")
        self.x = x


class Stun(WeaponAbility):
    def __init__(self):
        super().__init__('stun', "Each time a friendly operative makes a shooting attack with this weapon, in the Roll "
                                 "Attack Dice step of that shooting attack, if you retain any critical hits, subtract "
                                 "1 from the target's APL.<br/>")


class Weapon:
    def __init__(self, name, a, bws, d, dc, sp=None, critic=None):
        if sp is None:
            sp = []
        if critic is None:
            critic = []
        self.name = name
        self.A = a
        self.BS = bws
        self.D = d
        self.DC = dc
        self.SP = sp
        self.critic = critic


class Melee(Weapon):
    def __init__(self, name, a, bws, d, dc, sp, critic):
        super().__init__(name, a, bws, d, dc, sp, critic)
        self.typ = "⚔"


class Ranged(Weapon):
    def __init__(self, name, a, bws, d, dc, sp, critic):
        super().__init__(name, a, bws, d, dc, sp, critic)
        self.typ = "⌖"


class Bolter(Ranged):
    def __init__(self, sp=None, critic=None):
        super().__init__('bolter', 4, 3, 3, 4, sp, critic)


class BoltPistol(Bolter):
    def __init__(self):
        super().__init__(Rng('6'))