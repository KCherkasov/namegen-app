# -*- coding: utf-8 -*-

from charlist.character.helpers import *
from charlist.character.skill import Skill
from charlist.character.stat import Stat
from charlist.character.talent import Talent
from charlist.character.trait import Trait

SKILL_POINTS_PER_UPG = 10

UNTRAINED_SKILL = -20

SKILL_UPGRADES_CAP = 4

CURRENT_ID = 0
CAP_ID = 1
SPENT_ID = 1


class CharacterModel(object):
    def __init__(self, cid: int, squad_id: int, name: str, hw_id: str,
                 bg_id: str, role_id: str, div_id: str,
                 ea_id: List[str], wounds: List[int],
                 fatigue: List[int], xp: List[int], fate: List[int],
                 insanity: int, corruption: int, pr: int,
                 apts: List[str], stats: Dict[str, Stat],
                 skills: Dict[str, Skill], talents: Dict[str, Talent],
                 traits: Dict[str, Trait], psy: List[str], equipment: List,
                 disorders: List[str], malignancies: List[str],
                 mutations: List[str]):
        self.__cid = cid
        self.__squad_id = squad_id
        self.__name = name
        self.__hw_id = hw_id
        self.__bg_id = bg_id
        self.__role_id = role_id
        self.__div_id = div_id
        self.__ea_id = ea_id
        self.__wounds = wounds
        self.__fatigue = fatigue
        self.__xp = xp
        self.__fate = fate
        self.__insanity = insanity
        self.__corruption = corruption
        self.__pr = pr
        self.__apts = apts
        self.__stats = stats
        self.__skills = skills
        self.__talents = talents
        self.__traits = traits
        self.__psy = psy
        self.__equipment = equipment
        self.__disorders = disorders
        self.__malignancies = malignancies
        self.__mutations = mutations

    def id(self):
        return self.__cid

    def squad_id(self):
        return self.__squad_id

    def name(self):
        return self.__name

    def hw_id(self):
        return self.__hw_id

    def bg_id(self):
        return self.__bg_id

    def role_id(self):
        return self.__role_id

    def div_id(self):
        return self.__div_id

    def ea_id(self):
        return self.__ea_id

    def wounds(self):
        return self.__wounds

    def wounds_cap(self):
        return self.__wounds[CAP_ID]

    def wounds_current(self):
        return self.__wounds[CURRENT_ID]

    def damage(self, dmg: int):
        if dmg > 0:
            self.__wounds[CURRENT_ID] -= dmg
            return True
        else:
            return False

    def heal(self, hld: int):
        if hld > 0:
            self.__wounds[CURRENT_ID] += hld
            if self.__wounds[CURRENT_ID] > self.__wounds[CAP_ID]:
                self.__wounds[CURRENT_ID] = self.__wounds[CAP_ID]
            return True
        else:
            return False

    def fatigue(self):
        return self.__fatigue

    def fatigue_cap(self):
        return self.__fatigue[CAP_ID]

    def fatigue_current(self):
        return self.__fatigue[CURRENT_ID]

    def add_fatigue(self, amount: int):
        if amount > 0:
            self.__fatigue[CURRENT_ID] += amount
            return True
        else:
            return False

    def remove_fatigue(self, amount: int):
        if amount > 0:
            self.__fatigue[CURRENT_ID] -= amount
            return True
        else:
            return False

    def xp(self):
        return self.__xp

    def xp_current(self):
        return self.__xp[CURRENT_ID]

    def xp_spent(self):
        return self.__xp[SPENT_ID]

    def spend_xp(self, amount: int):
        if amount > self.__xp[CURRENT_ID]:
            return False
        else:
            self.__xp[CURRENT_ID] -= amount
            self.__xp[SPENT_ID] += amount
            return True

    def get_xp(self, amount: int):
        if amount > 0:
            self.__xp[CURRENT_ID] += amount
            return True
        else:
            return False

    def xp_total(self):
        return self.__xp[CURRENT_ID] + self.__xp[SPENT_ID]

    def fate(self):
        return self.__fate

    def fate_current(self):
        return self.__fate[CURRENT_ID]

    def fate_cap(self):
        return self.__fate[CAP_ID]

    def spend_fate(self):
        if self.__fate[CURRENT_ID] > 0:
            self.__fate[CURRENT_ID] -= 1
            return True
        else:
            return False

    def burn_fate(self):
        if self.__fate[CAP_ID] > 0:
            self.__fate[CAP_ID] -= 1
            if self.__fate[CURRENT_ID] > self.__fate[CAP_ID]:
                self.__fate[CAP_ID] = self.__fate[CURRENT_ID]
            return True
        else:
            return False

    def restore_fate(self):
        self.__fate[CURRENT_ID] = self.__fate[CAP_ID]

    def insanity(self):
        return self.__insanity

    def insanity_bonus(self):
        return self.__insanity // 10

    def insanity_residue(self):
        return self.__insanity % 10

    def gain_insanity(self, amount: int):
        if amount > 0:
            self.__insanity += amount

    def remove_insanity(self, amount: int):
        if amount > 0:
            self.__insanity -= amount
            if self.__insanity < 0:
                self.__insanity = 0

    def corruption(self):
        return self.__corruption

    def corruption_bonus(self):
        return self.__corruption // 10

    def corruption_residue(self):
        return self.__corruption % 10

    def gain_corruption(self, amount: int):
        if amount > 0:
            self.__corruption += amount

    def pr(self):
        return self.__pr

    def gain_pr(self):
        self.__pr += 1

    def aptitudes(self):
        return self.__apts

    def add_apt(self, apt: str):
        if (apt != '') and not (apt in self.__apts):
            self.__apts.append(apt)

    def stats(self):
        return self.__stats

    def upgrade_stat(self, stat: str):
        if stat in self.__stats.keys():
            if self.__stats.get(stat).is_upgradeable():
                self.__stats.get(stat).upgrade()

    def improve_stat(self, stat: str, amount: int):
        if (stat in self.__stats.keys()) and (amount > 0):
            self.__stats.get(stat).improve(amount)

    def damage_stat(self, stat: str, amount: int):
        if (stat in self.__stats.keys()) and (amount > 0):
            self.__stats.get(stat).damage(amount)

    def skills(self):
        return self.__skills

    def improve_skill(self, sk_tag: str):
        if sk_tag in self.__skills.keys():
            if self.__skills.get(sk_tag).upgradeable():
                self.__skills.get(sk_tag).upgrade()

    def improve_skill_subtag(self, sk_tag: str, sk_subtag: str, facade: Facade):
        if sk_tag in self.__skills.keys():
            if self.__skills.get(sk_tag).upgradeable_subtag(sk_subtag):
                self.__skills.get(sk_tag).upgrade_subtag(sk_subtag)
        elif sk_tag in facade.skill_descriptions().keys() \
                and facade.skill_descriptions().get(sk_tag).is_specialist():
            skill = Skill(sk_tag, {sk_subtag: 1})
            self.__skills[sk_tag] = skill

    def get_skill_diff(self, sk_tag: str, stat: str):
        if (sk_tag not in self.__skills.keys()) or (stat not in self.__stats.keys()):
            return None
        diff = self.__stats.get(stat).value() + self.__skills.get(sk_tag).get_adv_bonus()
        return diff

    def get_subskill_diff(self, sk_tag: str, subskill: str, stat: str):
        if (sk_tag not in self.__skills.keys()) \
                or (subskill not in self.__skills.get(sk_tag).advances().keys()) \
                or (stat not in self.__stats.keys()):
            return None
        diff = self.__stats.get(stat).value() + self.__skills.get(sk_tag).get_adv_bonus_subtag(subskill)
        return diff

    def talents(self):
        return self.__talents

    def gain_talent(self, tl_tag: str, facade: Facade):
        if tl_tag in facade.talent_descriptions().keys():
            if not facade.talent_descriptions().get(tl_tag).is_specialist():
                if tl_tag not in self.__talents.keys():
                    talent = Talent(tl_tag, 1)
                    self.__talents[tl_tag] = talent
                elif facade.talent_descriptions().get(tl_tag).is_stackable():
                    self.__talents.get(tl_tag).take(facade)

    def gain_talent_subtag(self, tl_tag: str, tl_subtag: str, facade: Facade):
        if tl_tag in facade.talent_descriptions().keys():
            if facade.talent_descriptions().get(tl_tag).is_specialist():
                if tl_tag in self.__talents.keys():
                    self.__talents.get(tl_tag).take_subtag(facade, tl_subtag)
                else:
                    talent = Talent(tl_tag, {tl_subtag: 1})
                    self.__talents[tl_tag] = talent

    def traits(self):
        return self.__traits

    def gain_trait(self, tr_tag: str, facade: Facade):
        if tr_tag in facade.trait_descriptions().keys():
            if tr_tag in self.__traits.keys():
                self.__traits.get(tr_tag).take(facade)
            else:
                trait = Trait(tr_tag, 1)
                self.__traits[tr_tag] = trait

    def gain_trait_subtag(self, tr_tag: str, tr_subtag: str, facade: Facade):
        if tr_tag in facade.trait_descriptions().keys():
            if facade.trait_descriptions().get(tr_tag).is_specialist():
                if tr_tag in self.__traits.keys():
                    self.__traits.get(tr_tag).take_subtag(facade, tr_subtag)
                else:
                    trait = Trait(tr_tag, {tr_subtag: 1})
                    self.__traits[tr_tag] = trait

    def psy_powers(self):
        return self.__psy

    def equipment(self):
        return self.__equipment

    def disorders(self):
        return self.__disorders

    def malignances(self):
        return self.__malignancies

    def mutations(self):
        return self.__mutations

    # TODO - add psy powers!!!

    # TODO - add maligns and mutations
    def make_hookups(self, facade: Facade):
        hookups = dict()
        hw_name = dict()
        for lang in ['ru', 'en']:
            hw_name[lang] = facade.homeworlds().get(self.__hw_id).get_bonus().get_name(lang)
        map_hints(hookups, facade.homeworlds().get(self.__hw_id).get_bonus().get_hints(), hw_name, facade)
        bg_name = dict()
        for lang in ['ru', 'en']:
            bg_name[lang] = facade.backgrounds().get(self.__bg_id).get_bonus().get_name(lang)
        map_hints(hookups, facade.backgrounds().get(self.__bg_id).get_bonus().get_hints(), bg_name, facade)
        role_name = dict()
        for lang in ['ru', 'en']:
            role_name[lang] = facade.roles().get(self.__role_id).get_bonus().get_name(lang)
        map_hints(hookups, facade.roles().get(self.__role_id).get_bonus().get_hints(), role_name, facade)
        div_name = dict()
        for lang in ['ru', 'en']:
            div_name[lang] = facade.divinations().get(self.__div_id).get_name(lang)
        map_hints(hookups, facade.divinations().get(self.__div_id).get_hints(), div_name, facade)
        for tl_tag in self.__talents.keys():
            tmp_name = dict()
            for lang in ['ru', 'en']:
                tmp_name[lang] = facade.talent_descriptions().get(tl_tag).get_name(lang)
            map_hints(hookups, facade.talent_descriptions().get(tl_tag).get_hints(), tmp_name, facade)
        for tr_tag in self.__traits.keys():
            tmp_name = dict()
            for lang in ['ru', 'en']:
                tmp_name[lang] = facade.trait_descriptions().get(tr_tag).get_name(lang)
            map_hints(hookups, facade.trait_descriptions().get(tr_tag).get_hints(), tmp_name, facade)
        # for disorder in self.__disorders:
        #     tmp_name = dict()
        #     for lang in ['ru', 'en']:
        #         tmp_name[lang] = facade.disorders().get(disorder).get_name(lang)
        #     map_hints(hookups, facade.disorders().get(disorder).get_hints(), tmp_name, facade)
        # for malign in self.__malignancies:
        #     tmp_name = dict()
        #     for lang in ['ru', 'en']:
        #         tmp_name[lang] = facade.malignancies().get(malign).get_name(lang)
        #     map_hints(hookups, facade.malignancies().get(malign).get_hints(), tmp_name, facade)
        # for mutation in self.__mutations:
        #     tmp_name = dict()
        #     for lang in ['ru', 'en']:
        #         tmp_name[lang] = facade.mutations().get(mutation).get_name(lang)
        #     map_hints(hookups, facade.mutations().get(mutation).get_hints(), tmp_name, facade)
        return hookups
