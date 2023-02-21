import random

class Monster():
    def __init__(self,challengerating,creature_type,legendary):
        self.challengerating = challengerating
        self.creature_type = creature_type
        self.archetype = self.get_archetype(creature_type)
        self.proficiencybonus = self.get_proficiency_bonus(challengerating)
        self.abilityscores = self.get_ability_scores(self.archetype,self.challengerating,self.creature_type)
        self.strength = self.abilityscores['strength']
        self.strengthmod = self.abilitymod(self.strength)
        self.dexterity = self.abilityscores['dexterity']
        self.dexteritymod = self.abilitymod(self.dexterity)
        self.constitution = self.abilityscores['constitution']
        self.constitutionmod = self.abilitymod(self.constitution)
        self.intelligence = self.abilityscores['intelligence']
        self.intelligencemod = self.abilitymod(self.intelligence)
        self.wisdom = self.abilityscores['wisdom']
        self.wisdommod = self.abilitymod(self.wisdom)
        self.charisma = self.abilityscores['charisma']
        self.charismamod = self.abilitymod(self.charisma)
        self.size = self.get_size(self.creature_type,self.challengerating)
        self.alignment = self.get_alignment(self.creature_type)
        self.itemuser = self.get_itemuser(self.creature_type)
        self.armor_class = self.get_armor_class(self.itemuser,self.challengerating,self.strength,self.dexteritymod)
        self.speed = self.get_speed(self.creature_type,self.challengerating,self.size)
        self.element = self.get_element(self.creature_type,self.challengerating)
        self.languages = self.get_languages(self.creature_type,self.intelligencemod,self.challengerating)
        self.saving_throws = self.get_proficient_saves(self.archetype,self.creature_type,self.challengerating,self.proficiencybonus,self.strengthmod,self.dexteritymod,self.constitutionmod,self.intelligencemod,self.wisdommod,self.charismamod)
        self.skills = self.get_skills(self.archetype,self.proficiencybonus,self.strengthmod,self.dexteritymod,self.intelligencemod,self.wisdommod,self.charismamod)
        self.senses = self.get_senses(self.creature_type,self.challengerating,self.skills)
        self.resistances = self.get_resistances(self.creature_type,self.element)
        self.traits, self.reactions = self.get_traits(self.creature_type,self.challengerating,self.itemuser,self.speed,self.element,self.size,self.archetype)
        self.actions = self.get_actions(self.archetype,self.challengerating,self.itemuser,self.element,self.creature_type,self.strengthmod,self.dexteritymod,self.constitutionmod,self.intelligencemod,self.wisdommod,self.charismamod,self.size,self.proficiencybonus)
        self.hit_points = self.get_hit_points(self.challengerating,self.constitutionmod,self.archetype,self.speed)
        if legendary == True:
            self.legendary = self.get_legendary_actions(self.speed,self.alignment,self.strengthmod,self.dexteritymod,self.constitutionmod,self.intelligencemod,self.wisdommod,self.charismamod,self.challengerating,self.proficiencybonus,self.archetype)

    # returns a dict where key is name of action
    def get_legendary_actions(self,movement,alignment,strmod,dexmod,conmod,intmod,wismod,chamod,challengerating,proficiencymod,archetype):
        legendary_dc = 8+proficiencymod+max(strmod,dexmod,conmod,intmod,wismod,chamod)
        legendary_dice = max(1,challengerating//3)
        legendary_available = 3
        flying_legendary = [{"Wing Attack (Costs 2 Actions)":"This monster beats its wings. Each creature within 10 feet of this monster must succeed on a DC "+str(legendary_dc)+" Dexterity saving throw or take "+str(legendary_dice)+"d6 bludgeoning damage and be knocked prone. This monster can then fly up to half its flying speed."}]
        evil_legendary = [{"Channel Negative Energy (Costs 2 Actions)":"This monster magically unleashes negative energy. Creatures within 60 feet of this monster, including ones behind barriers and around corners, can't regain hit points until the end of this monster's next turn."},{"Necrotic Burst (Costs 2 Actions)":"This monster emits foul, necrotic. Each creature of its choice in a 10-foot radius must make a DC "+str(legendary_dc)+" Constitution saving throw, taking "+str(legendary_dice)+"d6 cold damage plus "+str(legendary_dice)+"d6 necrotic damage on a failed save, or half as much damage on a successful one."}]
        good_legendary = [{"Radiant Burst (Costs 2 Actions)":"This monster emits magical, divine energy. Each creature of its choice in a 10-foot radius must make a DC "+str(legendary_dc)+" Dexterity saving throw, "+str(legendary_dice)+"d6 fire damage plus "+str(legendary_dice)+"d6 radiant damage on a failed save, or half as much damage on a successful one."}]
        legendary_1cost = [
            {"Use Attack Action":"This monster makes an additional attack."},
            {"Detect":"This monster makes a Wisdom (Perception) check."},
            {"Blinding Dust":"Blinding dust and debris swirls magically around this monster. Each creature within 5 feet of this monster must succeed on a DC "+str(legendary_dc)+" Constitution saving throw or be blinded until the end of the creature's next turn."}
        ]       
        legendary = [
            {"Shimmering Shield (Costs 2 Actions)":"This monster creates a shimmering, magical field around itself or another creature it can see within 60 feet of it. The target gains a +2 bonus to AC until the end of this monster's next turn."},
            {"Heal Self (Costs 3 Actions)":"This monster magically regains "+str(legendary_dice)+"d8 hit points."},
            {"Whirlwind (Costs 2 Actions)":"This monster magically transforms into a whirlwind, moves up to 60 feet, and reverts to its normal form. While in whirlwind form, this monster is immune to all damage, and it can't be grappled, petrified, knocked prone, restrained, or stunned. Equipment worn or carried by this monster remain in its possession"},
            {"Obscuring Cloud (Costs 3 Actions)":"This monster expels an obscuring cloud in a 60-foot radius. The cloud spreads around corners, and that area is heavily obscured to creatures other than this monster. Each creature other than this monster that ends its turn there must succeed on a DC "+str(legendary_dc)+" Constitution saving throw, taking "+str(legendary_dice)+"d10 poison damage on a failed save, or half as much damage on a successful one. A strong wind disperses the cloud, which otherwise disappears at the end of this monster's next turn."},
            {"Blinding Gaze (Costs 3 Actions)":"This monster targets one creature it can see within 30 feet of it. If the target can see it, the target must succeed on a DC "+str(legendary_dc)+" Constitution saving throw or be blinded until magic such as the lesser restoration spell removes the blindness."}
            ]
        legendarylist = []
        if archetype in ["int_user","wis_user","cha_user"]:
            legendarylist += [{"Use Non-Attack Action (costs 2 actions)":"This monster uses one of its actions that isn't an attack."}]
        for i in movement:
            for key in i.keys():
                if key == "fly":
                    legendarylist += flying_legendary
        if "evil" in alignment:
            legendarylist += evil_legendary
        if "good" in alignment:
            legendarylist += good_legendary
        legendary_actions = []
        index_1cost = random.randint(0,len(legendary_1cost)-1)
        selected_1cost = legendary_1cost[index_1cost]
        legendary_actions = [selected_1cost]
        del legendary_1cost[index_1cost]
        legendarylist += legendary+legendary_1cost
        legendary_actions += random.sample(legendarylist,2)
        return(legendary_actions)

    # returns a dict where key is name of action
    def get_actions(self, archetype, challengerating, itemuser, element, creature_type,strmod,dexmod,conmod,intmod,wismod,chamod,size,proficiencybonus):
        strdc = 8 + proficiencybonus + strmod
        dexdc = 8 + proficiencybonus + dexmod
        condc = 8 + proficiencybonus + conmod
        intdc = 8 + proficiencybonus + intmod
        wisdc = 8 + proficiencybonus + wismod
        chadc = 8 + proficiencybonus + chamod
        match archetype:
            case "str_user":
                genericdc = max(1, strdc-2)
            case "dex_user":
                genericdc = max(1, dexdc-2)
            case "int_user":
                genericdc = max(1, intdc-2)
            case "wis_user":
                genericdc = max(1, wisdc-2)
            case "cha_user":
                genericdc = max(1, chadc-2)
        action_list = []
        touch_die_amount = max(2,challengerating//2)
        missile_number = min(8,max(3,challengerating//2))
        missile_die_amount = max(1,challengerating//6)
        ray_number = max(2,challengerating//2)
        ray_die_amount = max(1,challengerating//6)
        aoe_die_amount = max(1,challengerating//3)
        aoe_number_of_times = max(1,challengerating//4)
        utility_number_of_times = max(1,challengerating//6)
        strtohit = proficiencybonus + strmod
        dextohit = proficiencybonus + dexmod
        inttohit = proficiencybonus + intmod
        wistohit = proficiencybonus + wismod
        chatohit = proficiencybonus + chamod
        magictohit = proficiencybonus + max(intmod, wismod, chamod)
        magicdc = proficiencybonus + max(intmod, wismod, chamod)
        amount_dice = max(1,challengerating//3)
        bonus_dice = max(1,challengerating//4)
        utility = [
            {"Enlarge":str(utility_number_of_times)+"/day. For 1 minute, this monster magically increases in size, along with anything it is wearing or carrying. While enlarged, the creature is one size class larger, doubles its damage dice on Strength-based weapon attacks, and makes Strength checks and Strength saving throws with advantage. If this monster lacks the room to become one size class larger, it attains the maximum size possible in the space available."},
            {"Fetid Cloud":str(aoe_number_of_times)+"/day. A 10-foot radius of disgusting green gas extends out from this monster. The gas spreads around corners, and its area is lightly obscured . It lasts for 1 minute or until a strong wind disperses it. Any creature that starts its turn in that area must succeed on a DC "+str(genericdc)+" Constitution saving throw or be poisoned until the start of its next turn . While poisoned in this way, the target can take either an action or a bonus action on its turn, not both, and can't take reactions."},
            {"Leadership":str(utility_number_of_times)+"/day. For 1 minute, this monster can utter a special command or warning whenever an allied creature that it can see within 30 feet of it makes an attack roll or a saving throw. The creature can add a d4 to its roll provided it can hear and understand this monster. A creature can benefit from only one Leadership die at a time. This effect ends if this monster is incapacitated."},
            {"Paralysis Gas":"(Recharge 6). This monster exhales gas in a 30-foot cone. Each creature in that area must succeed on a DC "+str(genericdc)+" Constitution saving throw or be paralyzed for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success."},
            {"Repulsion Breath":"(Recharge 6). This monster exhales repulsion energy in a 30 foot cone. Each creature in that area must succeed on a DC "+str(genericdc)+" Strength saving throw. On a failed save, the creature is pushed 60 feet away from this monster."},
            {"Weakening Gas":"(Recharge 6). This monster exhales gas in a 30-foot cone. Each creature in that area must succeed on a DC "+str(genericdc)+" Strength saving throw or have disadvantage on Strength-based attack rolls, Strength checks, and Strength saving throws for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success."},
            {"Teleport":str(utility_number_of_times)+"/day. This monster magically teleports itself and up to three willing creatures it can see within 5 feet of it, along with any equipment they are wearing or carrying, to a location this monster is familiar with, up to 1 mile away."},
            {"Web":str(utility_number_of_times)+"/day. This monster can innately cast Web, requiring no material components."},
            {"Entangle":str(utility_number_of_times)+"/day. This monster can innately cast Entangle, requiring no material components. The save DC is "+str(genericdc)+"."},
            {"Sleep Gas":"(Recharge 6). This monster exhales gas in a 30-foot cone. Each creature in that area must succeed on a DC "+str(genericdc)+" Constitution saving throw or fall unconscious for 5 minutes. This effect ends for a creature if the creature takes damage or someone uses an action to wake it."},
        ]
        if itemuser == "yes":
            utility += [{"Flying Weapon":"This monster releases one of its weapons to hover magically in an unoccupied space within 5 feet of it. If this monster can see the weapon, this monster can mentally command it as a bonus action to fly up to 50 feet and either make one attack against a target or return to this monster's hands. If the hovering weapon is targeted by any effect, this monster is considered to be holding it. The hovering weapon falls if this monster dies."}]
        magic_utility = [
            {"Create Whirlwind":str(utility_number_of_times)+"/day. A 5-foot-radius, 30-foot-tall cylinder of swirling air magically forms on a point this monster can see within 120 feet of it. The whirlwind lasts as long as this monster maintains concentration (as if concentrating on a spell). Any creature but this monster that enters the whirlwind must succeed on a DC "+str(genericdc)+" Strength saving throw or be restrained by it. This monster can move the whirlwind up to 60 feet as an action, and creatures restrained by the whirlwind move with it. The whirlwind ends if this monster loses sight of it. A creature can use its action to free a creature restrained by the whirlwind, including itself, by succeeding on a DC "+str(genericdc)+" Strength check. If the check succeeds, the creature is no longer restrained and moves to the nearest space outside the whirlwind."},
            {"Darkness Aura":str(utility_number_of_times)+"/day. A 15-foot radius of magical darkness extends out from this monster, moves with it, and spreads around corners. The darkness lasts as long as this monster maintains concentration, up to 10 minutes (as if concentrating on a spell). darkvision can't penetrate this darkness, and no natural light can illuminate it. If any of the darkness overlaps with an area of light created by a spell of 2nd level or lower, the spell creating the light is dispelled."},
            {"Slow":str(utility_number_of_times)+"/day. This monster alters time around up to six creatures of its choice in a 40-foot cube within 60 ft. Each target must succeed on a DC "+str(genericdc)+" Wisdom saving throw against this magic. On a failed save, a target can't use reactions, its speed is halved, and it can't make more than one attack on its turn. In addition, the target can take either an action or a bonus action on its turn, not both. These effects last for 1 minute. A target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success."},
            {"Dispel magic":str(utility_number_of_times)+"/day. This monster chooses one creature, object, or magical effect within 60 feet. Any spell of level "+str(proficiencybonus)+" or lower on the target ends."},
            {"Hold":str(utility_number_of_times)+"/day. This monster chooses up to "+str(proficiencybonus)+" creature(s) within 90 feet. The target(s) must succeed on a DC "+str(genericdc)+" Wisdom saving throw or be paralyzed for one minute. At the end of each of its turns, a target can make another Wisdom saving throw. On a success, the spell ends on that target."},
            {"Blur":str(utility_number_of_times)+"/day. This monster can innately cast Blur, requiring no material components."},
            {"Curse":str(utility_number_of_times)+"/day. This monster can innately cast Curse, requiring no material components."},
            {"Faerie Fire":str(utility_number_of_times)+"/day. This monster can innately cast Faerie Fire, requiring no material components."},
            {"Read Thoughts":"This monster magically reads the surface thoughts of one creature within 60 feet of it. The effect can penetrate barriers, but 3 feet of wood or dirt, 2 feet of stone, 2 inches of metal, or a thin sheet of lead blocks it. While the target is in range, this monster can continue reading its thoughts, as long as the this monster's concentration isn't broken (as if concentrating on a spell). While reading the target's mind, this monster has advantage on Wisdom (Insight) and Charisma (Deception, Intimidation, and Persuasion) checks against the target."},
        ]
        elemental_utility = [
            {"Enlarge":str(utility_number_of_times)+"/day. For 1 minute, this monster magically increases in size, along with anything it is wearing or carrying. While enlarged, the creature is one size class larger, doubles its damage dice on Strength-based weapon attacks, and makes Strength checks and Strength saving throws with advantage. If this monster lacks the room to become one size class larger, it attains the maximum size possible in the space available."},
            {"Teleport":str(utility_number_of_times)+"/day. This monster magically teleports itself and up to three willing creatures it can see within 5 feet of it, along with any equipment they are wearing or carrying, to a location this monster is familiar with, up to 1 mile away."},
            {"Whirling Element":str(aoe_number_of_times)+"/day. A 5-foot-radius, 30-foot-tall cylinder of swirling "+element+" energy magically forms on a point this monster can see within 120 feet of it. The cylinder lasts as long as this monster maintains concentration (as if concentrating on a spell). Any creature but this monster that enters the cylinder must succeed on a DC "+str(genericdc)+" Strength saving throw or be restrained by it. This monster can move the cylinder up to 60 feet as an action, and creatures restrained by the whirlwind move with it. The cylinder ends if this monster loses sight of it. A creature can use its action to free a creature restrained by the whirlwind, including itself, by succeeding on a DC "+str(genericdc)+" Strength check. If the check succeeds, the creature is no longer restrained and moves to the nearest space outside the cylinder. A creature that is restrained by this ability takes "+str(bonus_dice)+"d6 "+element+" damage at the start of its turn turn."},
            {"Slow":str(aoe_number_of_times)+"/day. This monster alters time around up to six creatures of its choice in a 40-foot cube within 60 ft. Each target must succeed on a DC "+str(genericdc)+" Wisdom saving throw against this magic. On a failed save, a target can't use reactions, its speed is halved, and it can't make more than one attack on its turn. In addition, the target can take either an action or a bonus action on its turn, not both. These effects last for 1 minute. A target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success."},
            {"Hold":str(aoe_number_of_times)+"/day. This monster chooses up to "+str(proficiencybonus)+" creature(s) within 90 feet. The target(s) must succeed on a DC "+str(genericdc)+" Wisdom saving throw or be paralyzed for one minute. At the end of each of its turns, a target can make another Wisdom saving throw. On a success, the spell ends on that target. A creature that is held with this ability takes "+str(bonus_dice)+"d6 "+element+" damage at the start of its turn."},
            {"Elemental Fog":"This monster creates a 20-foot-radius sphere of fog centered on a point within 120 feet. The sphere spreads around corners, and its area is heavily obscured. It lasts for the duration or until a wind of moderate or greater speed (at least 10 miles per hour) disperses it. Any creature within the fog takes 1d6 "+element+" damage at the start of its turn."},
            {"Blinding Flash":"(Recharge 6) This monster emits a blinding flash of energy. Each creature that can see it must succeed on a DC "+str(genericdc)+" Constitution saving throw or be blinded until the end of this monster's next turn."},
            {"Stunning Screech":"(Recharge 6) This monster emits a horrific screech. Each hostile creature within 20 feet of it that can hear it must succeed on a DC "+str(genericdc)+" Constitution saving throw or be stunned until the end of this monster's next turn."},
            {"Deafening Roar":"(Recharge 6) This monster emits a horrific roar. Each hostile creature within 20 feet of it that can hear it must succeed on a DC "+str(genericdc)+" Constitution saving throw or be deafened until the end of this monster's next turn."},
        ]
        elementtypes = ["acid", "cold", "fire", "force", "lightning", "necrotic", "poison", "psychic", "radiant", "thunder"]
        elementsaves = {"acid":"Dexterity", "cold":"Constitution", "fire":"Dexterity", "force":"Dexterity", "lightning":"Dexterity", "necrotic":"Constitution", "poison":"Constitution", "psychic":"Wisdom", "radiant":"Dexterity", "thunder":"Constitution"}
        if creature_type == "Elemental":
            elementtypes = [element, element, element, element, element, element, element, element, element, element]
        random.shuffle(elementtypes)
        magic_touch = [
            {elementtypes[0].capitalize()+" Touch":"<i>Melee Spell Attack:</i> +"+str(magictohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(touch_die_amount)+"d6 "+elementtypes[0]+" damage."},
        ]
        magic_ranged = [
            {elementtypes[1].capitalize()+" Missile":"<i>Ranged Spell Attack:</i> range 120 ft. This monster creates "+str(missile_number)+" glowing "+elementtypes[1]+" darts. Each dart hits a creature of this monster's choice that it can see within range. The darts all strike simultaneously, and this monster can direct them to hit one creature or several. <i>Hit:</i> "+str(missile_die_amount)+"d4 "+elementtypes[1]+" damage."},
            {elementtypes[2].capitalize()+" Ray":"<i>Ranged Spell Attack:</i> +"+str(magictohit)+" to hit, range 120 ft. This monster fires "+str(ray_number)+" "+elementtypes[2]+" rays, and can direct the rays at the same target or at different ones. Make a separate attack roll for each ray. <i>Hit:</i> "+str(ray_die_amount)+"d8 "+elementtypes[2]+" damage."},
        ]
        magic_area = [
            {elementtypes[3].capitalize()+" Ball":str(aoe_number_of_times)+"/day. Range 150 ft. A bright streak of "+elementtypes[3]+" flashes from this monster to a point within 150 ft. Each creature in a 20-foot-radius sphere centered on that point must make a DC "+str(magicdc)+" "+elementsaves[elementtypes[3]]+" saving throw, taking "+str(aoe_die_amount)+"d6 "+elementtypes[3]+" damage on a failed save, or half as much damage on a successful one."},
            {elementtypes[4].capitalize()+" Line":str(aoe_number_of_times)+"/day. A burst of "+elementtypes[4]+" forming a line "+str(20+5*challengerating)+" feet long and 5 feet wide blasts out from this monster. Each creature in that line must make a DC "+str(magicdc)+" "+elementsaves[elementtypes[4]]+" saving throw, taking "+str(aoe_die_amount)+"d6 "+elementtypes[4]+" damage on a failed save, or half as much damage on a successful one."},
            {elementtypes[5].capitalize()+" Cone":str(aoe_number_of_times)+"/day. A blast of "+elementtypes[5]+" forming a "+str(max(15 ,min(95,5*challengerating)))+"-foot cone erupts from this monster. Each creature in that cone must make a DC "+str(magicdc)+" "+elementsaves[elementtypes[5]]+" saving throw, taking "+str(aoe_die_amount)+"d6 "+elementtypes[5]+" damage on a failed save, or half as much damage on a successful one."},
        ]
        if itemuser == "yes":
            number_of_actions = max(1,min(challengerating//3,10))
            item_melee_str = [
                {"Longsword":"<i>Melee Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d8 + "+str(strmod)+" slashing damage."},
                {"Warhammer":"<i>Melee Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d8 + "+str(strmod)+" bludgeoning damage."},
                {"Morningstar":"<i>Melee Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d8 + "+str(strmod)+" piercing damage."},
            ]
            item_melee_str_special = [
                {"Greatsword":"<i>Melee Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 2d6 + "+str(strmod)+" slashing damage."},
                {"Maul":"<i>Melee Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 2d6 + "+str(strmod)+" bludgeoning damage."},
            ]
            item_melee_dex = [
                {"Scimitar":"<i>Melee Weapon Attack:</i> +"+str(dextohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d6 + "+str(dexmod)+" slashing damage."},
                {"Shortsword":"<i>Melee Weapon Attack:</i> +"+str(dextohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d6 + "+str(dexmod)+" piercing damage."},
                {"Whip":"<i>Melee Weapon Attack:</i> +"+str(dextohit)+" to hit, reach 10 ft., one target. <i>Hit:</i> 1d4 + "+str(dexmod)+" slashing damage."},
            ]
            item_melee_dex_special = [
                {"Rapier":"<i>Melee Weapon Attack:</i> +"+str(dextohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d8 + "+str(strmod)+" piercing damage."}
            ]
            item_ranged_str = [
                {"Javelin":"Melee or <i>Ranged Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft. or range 30/120 ft., one target. <i>Hit:</i> 1d6 + "+str(strmod)+" piercing damage."},
                {"Spear":"Melee or <i>Ranged Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft. or range 20/60 ft., one target. <i>Hit:</i> 1d6 + "+str(strmod)+" piercing damage."},
            ]
            item_ranged_dex = [
                {"Dart":"<i>Ranged Weapon Attack:</i> +"+str(dextohit)+" to hit, range 20/60 ft., one target. <i>Hit:</i> 1d4 + "+str(dexmod)+" piercing damage."},
                {"Shortbow":"<i>Ranged Weapon Attack:</i> +"+str(dextohit)+" to hit, range 80/320 ft., one target. <i>Hit:</i> 1d6 + "+str(dexmod)+" piercing damage."},
            ]
            item_ranged_dex_special = [
                {"Heavy Crossbow":"<i>Ranged Weapon Attack:</i> +"+str(dextohit)+" to hit, range 100/400 ft., one target. <i>Hit:</i> 1d10 + "+str(dexmod)+" piercing damage."},
                {"Longbow":"<i>Ranged Weapon Attack:</i> +"+str(dextohit)+" to hit, range 150/600 ft., one target. <i>Hit:</i> 1d8 + "+str(dexmod)+" piercing damage."},
            ]
            if creature_type == "Elemental":
                # elementaltohit = max(strtohit,dextohit,chatohit,inttohit,wistohit)
                magic_utility = elemental_utility
                utility = elemental_utility
            if creature_type == "Undead":
                magic_utility += [
                    {"Create Specter":"This monster targets a creature within 10 feet of it that has been dead for no longer than 1 minute and died violently. The target's spirit rises as a specter in the space of its corpse or in the nearest unoccupied space. The specter is under this monster's control. This monster can have no more than seven specters under its control at one time."}
                ]
                magic_utility += [
                    {"Children of the Night":str(utility_number_of_times)+"/day. This monster magically calls 2d4 swarms of bats or rats. While outdoors, this monster can call 3d6 wolves instead. The called creatures arrive in 1d4 rounds, acting as allies of this monster and obeying its spoken commands. The beasts remain for 1 hour, until this monster dies, or until this monster dismisses them as a bonus action."}
                ]
            match archetype:
                case "str_user":
                    if strmod > 3:
                        action_list += random.sample(item_melee_str_special,1)
                        remaining_actions = number_of_actions - len(action_list)
                        str_actions = item_melee_str + item_ranged_str + item_ranged_dex + utility
                        action_list += random.sample(str_actions,max(0,remaining_actions))
                    else:
                        action_list += random.sample(item_melee_str,1)
                        remaining_actions = number_of_actions - len(action_list)
                        str_actions = item_melee_str + item_ranged_str + item_ranged_dex + utility
                        action_list += random.sample(str_actions,max(0,remaining_actions))
                case "dex_user":
                    if dexmod > 3:
                        special_dex = item_melee_dex_special+item_ranged_dex_special
                        action_list += random.sample(special_dex, 1)
                        remaining_actions = number_of_actions - len(action_list)
                        dex_actions = item_melee_dex + item_melee_str + item_ranged_dex + utility
                        action_list += random.sample(dex_actions,max(0,remaining_actions))
                    else:
                        action_list += random.sample(item_melee_dex,1)
                        remaining_actions = number_of_actions - len(action_list)
                        dex_actions = item_melee_dex + item_melee_str + item_ranged_dex + utility
                        action_list += random.sample(dex_actions,max(0,remaining_actions))
                case _:
                    magic_list = magic_ranged + magic_touch
                    action_list += random.sample(magic_list,max(1,min(challengerating//4,2)))
                    remaining_actions = number_of_actions - len(action_list)
                    magic_actions = utility + magic_utility + magic_area
                    action_list += random.sample(magic_actions,max(0,remaining_actions))
            if archetype in ["int_user","cha_user","wis_user"]:
                str_simple = [
                    {"Quarterstaff":"<i>Melee Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d6 + "+str(strmod)+" bludgeoning damage."},
                    {"Mace":"<i>Melee Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d6 + "+str(strmod)+" bludgeoning damage."}
                ]
                dex_simple = [
                    {"Dagger":"<i>Melee Weapon Attack:</i> +"+str(dextohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> 1d4 + "+str(dexmod)+" piercing damage."},
                    {"Shortbow":"<i>Ranged Weapon Attack:</i> +"+str(dextohit)+" to hit, range 80/320 ft., one target. <i>Hit:</i> 1d6 + "+str(dexmod)+" piercing damage."}
                ]                
                if strmod > dexmod:
                    action_list += random.sample(str_simple,1)
                elif dexmod > strmod:
                    action_list += random.sample(dex_simple,1)
                else:
                    combined_list = str_simple + dex_simple
                    action_list += random.sample(combined_list,1)
        elif itemuser == "no":
            size_value = {"Tiny":1,"Small":2,"Medium":3,"Large":4,"Huge":5,"Gargantuan":6}
            die_value = {1:"d4",2:"d4",3:"d6",4:"d8",5:"d10",6:"d10",7:"d12"}
            size_smaller_parser = die_value[max(size_value[size]-1,1)]
            size_current_parser = die_value[size_value[size]]
            size_bigger_parser = die_value[min(size_value[size]+1,7)]
            natural_basic = [
                {"Tail":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage."},
                {"Claw":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" slashing damage."},
                {"Bite":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" piercing damage."},
            ]
            natural_advanced = [
                {"Stinger":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 10 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" piercing damage, and the target must make a DC "+str(genericdc)+" Constitution saving throw, taking "+str(bonus_dice)+"d6 poison damage on a failed save, or half as much damage on a successful one."},
                {"Tentacle":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 10 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage. If the target is smaller than this monster, it is grappled (escape DC "+str(genericdc)+") and restrained until the grapple ends. This monster has "+str(challengerating//3)+" tentacles, each of which can grapple one target."},
                {"Charge":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 5ft., one target. This monster moves up to its speed to a target, then makes an attack if it's in range. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage. If this monster moved more than half its speed, the target must succeed on a DC "+str(genericdc)+" Strength saving throw or be knocked prone. If the target is knocked prone, this monster may make an additional attack against the target."},
                {"Extrude Grease":"(Recharge 6) Slick grease covers the ground in a 10-foot square centered on a point within 60 feet and turns it into difficult terrain for 10 rounds. When the grease appears, each creature standing in its area must succeed on a Dexterity saving throw or fall prone. A creature that enters the area or ends its turn there must also succeed on a Dexterity saving throw or fall prone."},
                {"Acid Spray":"(Recharge 6) This monster spits acid in a line that is 30 feet long and 5 feet wide. Each creature in that line must make a DC "+str(genericdc)+" Dexterity saving throw, taking "+str(bonus_dice)+"d6 acid damage on a failed save, or half as much damage on a successful one."},
                {"Blinding Spittle":"(Recharge 6) This monster spits a chemical glob at a point it can see within 15 feet of it. The glob explodes in a blinding splash of acid. Each creature within 5 feet of the splash must succeed on a DC "+str(genericdc)+" Dexterity saving throw or be blinded until the end of this monster's next turn."},
                {"Spit Poison":"(Recharge 6) This monster spits acid in a 15 foot cone. Each creature in that cone must make a DC "+str(genericdc)+" Constitution saving throw, taking "+str(bonus_dice)+"d6 poison damage on a failed save, or half as much damage on a successful one."},
                {"Stunning Screech":"(Recharge 6) This monster emits a horrific screech. Each hostile creature within 20 feet of it that can hear it must succeed on a DC "+str(genericdc)+" Constitution saving throw or be stunned until the end of this monster's next turn."},
                {"Deafening Roar":"(Recharge 6) This monster emits a horrific roar. Each hostile creature within 20 feet of it that can hear it must succeed on a DC "+str(genericdc)+" Constitution saving throw or be deafened until the end of this monster's next turn."},
            ]
            natural_ranged_str = [
                {"Throw":"<i>Ranged Weapon Attack:</i> +"+str(strtohit)+" to hit, range 20/60 ft., one target. <i>Hit:</i> "+str(amount_dice)+size_smaller_parser+" +"+str(strmod)+" bludgeoning damage."},
            ]
            natural_ranged_dex = [
                {"Spit":"<i>Ranged Weapon Attack:</i> +"+str(dextohit)+" to hit, range 20/60 ft., one target. <i>Hit:</i> "+str(amount_dice)+size_smaller_parser+" +"+str(dexmod)+" acid damage."},
            ]
            number_of_actions = max(1,min(challengerating//3+1,10))
            if creature_type == "Ooze":
                pseudopod = [
                    {"Pseudopod":"<i>Melee Weapon Attack:</i> +"+str(strtohit)+" to hit, reach 5ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(strmod)+" bludgeoning damage plus "+str(bonus_dice)+"d6 acid damage."},
                ]
                action_list += pseudopod
                if size in ["Large","Huge","Gargantuan"]:
                    engulf = [
                        {"Engulf":"This monster moves up to its speed. While doing so, it can enter the spaces of creatures the same size or smaller. Whenever this monster enters a creature's space, the creature must make a DC "+str(genericdc)+" Dexterity saving throw. On a successful save, the creature can choose to be pushed 5 feet back or to the side of this monster. A creature that chooses not to be pushed suffers the consequences of a failed saving throw. On a failed save, this monster enters the creature's space, and the creature takes "+str(bonus_dice)+"d6 elemental damage and is engulfed. The engulfed creature can't breathe, is restrained, and takes "+str(bonus_dice*2)+"d6 elemental damage at the start of each of this monster's turns. When this monster moves, the engulfed creature moves with it. An engulfed creature can try to escape by taking an action to make a DC "+str(genericdc)+" Strength check. On a success, the creature escapes and enters a space of its choice within 5 feet of this monster."},
                    ]
                    action_list += engulf
            elif creature_type == "Dragon":
                dragondc = max(strdc,dexdc,condc,intdc,wisdc,chadc)
                if element in ["poison","cold","necrotic"]:
                    dragonsave = "Constitution"
                else:
                    dragonsave = "Dexterity"
                breath_weapon = [
                    {element.capitalize()+" Breath (line)":"(Recharge 5-6) The dragon exhales "+element+" energy in a line "+str(20+5*challengerating)+" feet long and 5 feet wide. Each creature in that line must make a DC "+str(dragondc)+" "+dragonsave+" saving throw, taking "+str(challengerating+4)+"d8 "+element+" damage on a failed save, or half as much damage on a successful one."},
                    {element.capitalize()+" Breath (cone)":"(Recharge 5-6) The dragon exhales "+element+" energy in a "+str(max(15 ,min(95,5*challengerating)))+" foot cone. Each creature in that area must make a DC "+str(dragondc)+" "+dragonsave+" saving throw, taking "+str(challengerating+4)+"d8 "+element+" damage on a failed save, or half as much damage on a successful one."},
                ]
                action_list += random.sample(breath_weapon,1)
                remaining_actions = number_of_actions - len(action_list)
                if remaining_actions >3:
                    dragon_multi = 1
                    action_list += random.sample(natural_basic,2)
                else:
                    action_list += random.sample(natural_basic,1)
                    dragon_multi = 0
                remaining_actions = number_of_actions - len(action_list)
                frightful_presence = []
                if challengerating > 12:
                    frightful_presence = [
                        {"Frightful Presence":"Each creature of the dragon's choice that is within 120 feet of the dragon and aware of it must succeed on a DC "+str(dragondc)+" Wisdom saving throw or become frightened for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. If a creature's saving throw is successful or the effect ends for it, the creature is immune to the dragon's Frightful Presence for the next 24 hours."}
                    ]
                    action_list += frightful_presence
                remaining_actions = number_of_actions - len(action_list)
                if archetype in ["str_user","dex_user"]:
                    dragon_actions = utility + natural_advanced
                if archetype in ["cha_user"]:
                    dragon_actions = magic_utility + utility
                action_list += random.sample(dragon_actions,max(remaining_actions,0))
            elif creature_type == "Plant":
                plant_basic = [
                    {"Slam":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage."},
                    {"Vine":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" slashing damage."},
                    {"Thorn":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" piercing damage."},
                ]
                plant_advanced = [         
                    {"Nettles":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 10 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" piercing damage, and the target must make a DC "+str(genericdc)+" Constitution saving throw, taking "+str(bonus_dice)+"d6 poison damage on a failed save, or half as much damage on a successful one."},
                    {"Tendril":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 10 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage. If the target is smaller than this monster, it is grappled (escape DC "+str(genericdc)+") and restrained until the grapple ends. This monster has "+str(challengerating//3)+" tendrils, each of which can grapple one target."},
                    {"Charge":"<i>Melee Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, reach 5ft., one target. This monster moves up to its speed to a target, then makes an attack if it's in range. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage. If this monster moved more than half its speed, the target must succeed on a DC "+str(genericdc)+" Strength saving throw or be knocked prone. If the target is knocked prone, this monster may make an additional attack against the target."},
                    {"Extrude Grease":"(Recharge 6) Slick grease covers the ground in a 10-foot square centered on a point within 60 feet and turns it into difficult terrain for 10 rounds. When the grease appears, each creature standing in its area must succeed on a Dexterity saving throw or fall prone. A creature that enters the area or ends its turn there must also succeed on a Dexterity saving throw or fall prone."},
                    {"Acid Spray":"(Recharge 6) This monster spits acid in a line that is 30 feet long and 5 feet wide. Each creature in that line must make a DC "+str(genericdc)+" Dexterity saving throw, taking "+str(bonus_dice)+"d6 acid damage on a failed save, or half as much damage on a successful one."},
                    {"Blinding Resin":"(Recharge 6) This monster spits a chemical glob at a point it can see within 15 feet of it. The glob explodes in a blinding splash of acid. Each creature within 5 feet of the splash must succeed on a DC "+str(genericdc)+" Dexterity saving throw or be blinded until the end of this monster's next turn."},
                    {"Spit Poison":"(Recharge 6) This monster spits acid in a 15 foot cone. Each creature in that cone must make a DC "+str(genericdc)+" Constitution saving throw, taking "+str(bonus_dice)+"d6 poison damage on a failed save, or half as much damage on a successful one."},
                    {"Stunning Screech":"(Recharge 6) This monster emits a horrific screech. Each hostile creature within 20 feet of it that can hear it must succeed on a DC "+str(genericdc)+" Constitution saving throw or be stunned until the end of this monster's next turn."},
                    {"Deafening Roar":"(Recharge 6) This monster emits a horrific screech. Each hostile creature within 20 feet of it that can hear it must succeed on a DC "+str(genericdc)+" Constitution saving throw or be deafened until the end of this monster's next turn."},
                ]
                plant_ranged_str = [          
                    {"Nut Blast":"<i>Ranged Weapon Attack:</i> +"+str(strtohit)+" to hit, range 20/60 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(strmod)+" bludgeoning damage."},
                ]
                plant_ranged_dex = [
                    {"Seed Bullet":"<i>Ranged Weapon Attack:</i> +"+str(dextohit)+" to hit, range 20/60 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(dexmod)+" piercing damage."}
                ]
                action_list += random.sample(plant_basic,max(1, min(2, number_of_actions)))
                remaining_actions = number_of_actions - len(action_list)
                if remaining_actions > 0:
                    if archetype == "str_user":
                        action_list += plant_ranged_str
                    if archetype == "dex_user":
                        action_list += plant_ranged_dex
                    remaining_actions = number_of_actions - len(action_list)
                    action_list += random.sample(plant_advanced,max(0,remaining_actions))
            else:
                if creature_type == "Elemental":
                    elementaltohit = max(strtohit,dextohit,chatohit,inttohit,wistohit)
                    elemental_basic = [
                        {element.capitalize()+" Slam":"<i>Melee Weapon Attack:</i> +"+str(elementaltohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage + "+str(bonus_dice)+"d6 "+element+" damage."},
                        {element.capitalize()+" Slash":"<i>Melee Weapon Attack:</i> +"+str(elementaltohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" slashing damage + "+str(bonus_dice)+"d6 "+element+" damage."},
                        {element.capitalize()+" Spike":"<i>Melee Weapon Attack:</i> +"+str(elementaltohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" piercing damage + "+str(bonus_dice)+"d6 "+element+" damage."},
                    ]
                    elemental_ranged = [
                        {element.capitalize()+" Hurl":"<i>Ranged Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, range 20/60 ft., one target. <i>Hit:</i> "+str(amount_dice)+size_smaller_parser+" +"+str(max(dexmod,strmod))+" "+element+" damage."},
                    ]
                    natural_basic = elemental_basic
                    natural_ranged_dex = elemental_ranged
                    natural_ranged_str = elemental_ranged
                    natural_advanced = elemental_utility
                    magic_utility = elemental_utility
                    utility = elemental_utility
                if creature_type == "Construct":
                    constructtohit = max(strtohit,dextohit,chatohit,inttohit,wistohit)
                    if element == "none":
                        construct_basic = [
                            {"Slam":"<i>Melee Weapon Attack:</i> +"+str(constructtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage."},
                            {"Slash":"<i>Melee Weapon Attack:</i> +"+str(constructtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" slashing damage."},
                            {"Spike":"<i>Melee Weapon Attack:</i> +"+str(constructtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" piercing damage."},
                        ]
                        construct_ranged = [
                            {"Launch":"<i>Ranged Weapon Attack:</i> +"+str(constructtohit)+" to hit, range 20/60 ft., one target. <i>Hit:</i> "+str(amount_dice)+size_smaller_parser+" +"+str(strmod)+" bludgeoning damage."},
                        ]
                    else:
                        construct_basic = [
                            {element.capitalize()+" Slam":"<i>Melee Weapon Attack:</i> +"+str(constructtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" bludgeoning damage + "+str(bonus_dice)+"d6 "+element+" damage."},
                            {element.capitalize()+" Slash":"<i>Melee Weapon Attack:</i> +"+str(constructtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" slashing damage + "+str(bonus_dice)+"d6 "+element+" damage."},
                            {element.capitalize()+" Spike":"<i>Melee Weapon Attack:</i> +"+str(constructtohit)+" to hit, reach 5 ft., one target. <i>Hit:</i> "+str(amount_dice)+random.choice([size_bigger_parser,size_current_parser,size_smaller_parser])+" +"+str(max(dexmod,strmod))+" piercing damage + "+str(bonus_dice)+"d6 "+element+" damage."},
                        ]
                        construct_ranged = [
                            {element.capitalize()+" Hurl":"<i>Ranged Weapon Attack:</i> +"+str(max(dextohit,strtohit))+" to hit, range 20/60 ft., one target. <i>Hit:</i> "+str(amount_dice)+size_smaller_parser+" +"+str(max(dexmod,strmod))+" "+element+" damage."},
                        ]
                    natural_basic = construct_basic
                    natural_ranged_str = construct_ranged
                    natural_ranged_dex = construct_ranged
                    natural_advanced = utility
                match archetype:
                    case "str_user":
                        action_list += random.sample(natural_basic,max(1, min(2, number_of_actions)))
                        remaining_actions = number_of_actions - len(action_list)
                        if remaining_actions > 0:
                            action_list += natural_ranged_str
                        remaining_actions = number_of_actions - len(action_list)
                        if creature_type == "Monstrosity":
                            natural_advanced += utility
                            natural_advanced += magic_utility
                        action_list += random.sample(natural_advanced,max(0,remaining_actions))
                    case "dex_user":
                        action_list += random.sample(natural_basic,max(1, min(2, number_of_actions)))
                        remaining_actions = number_of_actions - len(action_list)
                        if remaining_actions > 0:
                            action_list += natural_ranged_dex
                        remaining_actions = number_of_actions - len(action_list)
                        if creature_type == "Monstrosity":
                            natural_advanced += utility
                            natural_advanced += magic_utility
                        action_list += random.sample(natural_advanced,max(0,remaining_actions))
                    case _:
                        magic_list = magic_ranged + magic_touch
                        action_list += random.sample(magic_list,max(1,min(challengerating//4,2)))
                        remaining_actions = number_of_actions - len(action_list)
                        magic_actions = natural_advanced + magic_utility + magic_area
                        action_list += random.sample(magic_actions,max(0,remaining_actions))
                        action_list += random.sample(natural_basic,1)
        multiattack_blurb = ''
        if creature_type == "Ooze":
            if challengerating > 6:
                multiattack_blurb = "This monster can make "+str(max(2,challengerating//4))+" pseudopod attacks."
        elif creature_type == "Dragon":
            if dragon_multi == 1:
                for k in action_list[1]:
                    action1 = k
                for k in action_list[2]:
                    action2 = k
                if frightful_presence == []:
                    multiattack_blurb = "This monster can make "+str(max(2,challengerating//4))+" "+action1+" attacks, and "+str(max(1,challengerating//6))+" "+action2+" attack(s)."
                else:
                    multiattack_blurb = "The dragon can use its Frightful Presence. Then it can make "+str(max(2,challengerating//4))+" "+action1+" attacks, and "+str(max(1,challengerating//6))+" "+action2+" attack(s)."
            elif challengerating > 4:
                for k in action_list[1]:
                    action1 = k
                multiattack_blurb = "This monster can make "+str(max(2,challengerating//4))+" "+action1+" attacks."
        elif archetype in ["str_user","dex_user"]:
            if len(action_list) > 1:
                for k in action_list[0]:
                    action1 = k
                for k in action_list[1]:
                    action2 = k
                if itemuser == "no":
                    if len(action_list) > 3:
                        for k in action_list[random.randint(3,len(action_list)-1)]:
                            action3 = k
                        multiattack_blurb = "This creature can make "+str(max(2,challengerating//4))+" "+action1+" attacks, and "+str(max(1,challengerating//6))+" "+action2+" attack(s). It can also use "+action3+" (if the action is not on recharge)."
                    else:
                        multiattack_blurb = "This creature can make "+str(max(2,challengerating//4))+" "+action1+" attacks, and "+str(max(1,challengerating//6))+" "+action2+" attack(s)."
                if itemuser == "yes":
                    multiattack_blurb = "This creature may make "+str(max(2,challengerating//4))+" weapon attacks."
        if multiattack_blurb != '':
            action_list.insert(0, {"Multiattack": multiattack_blurb})
        multiattack = []
        melee_attack_list = []
        ranged_attack_list = []
        spell_attack_list = []
        generic_actions = []
        listval = 0
        while listval < len(action_list):
            for actions in action_list:
                for k,v in actions.items():
                    if "Multi" in k:
                        multiattack.append({k:v})
                    elif "Melee Weapon Attack:" in v:
                        melee_attack_list.append({k:v})
                    elif "Ranged Weapon Attack:" in v:
                        ranged_attack_list.append({k:v})
                    elif "Spell Attack:" in v:
                        spell_attack_list.append({k:v})
                    elif "line" in k.lower() or "sphere" in k.lower() or "cone" in k.lower():
                        spell_attack_list.append({k:v})
                    else:
                        generic_actions.append({k:v})
                listval += 1
        sorted_action_list = multiattack + melee_attack_list + ranged_attack_list + spell_attack_list + generic_actions
        return sorted_action_list

    # returns one dict of traits, and one dict of reactions
    def get_traits(self, creature_type, challengerating, itemuser, movement, element, size,archetype):
        total_traits = min(6, max(challengerating // 3,1))
        current_traits = []
        current_reactions = []
        low_traits_available = min(max(challengerating // 3, 1), 2)
        medium_traits_available = min(max(challengerating // 3 - 3, 0), 2)
        high_traits_available = min(max(challengerating // 3 - 4, 0), 1)
        bonus_dice = max(1,challengerating//4)
        if creature_type in ["Ooze"]:
            amorphous = [{"Amorphous": "This monster can move through a space as narrow as 1 inch wide without squeezing."}]
            current_traits += amorphous
            if size in ["Medium","Large","Huge","Gargantuan"]:
                split = [
                    {"Split": "When an Ooze that is Medium or larger is subjected to lightning or slashing damage, it splits into two new Oozes if it has at least 10 hit points. Each new Ooze has hit points equal to half the original Ooze's, rounded down. New Oozes are one size smaller than the original Ooze."},
                ]
                current_reactions += split
            if size in ["Large","Huge","Gargantuan"]:
                ooze_cube = [
                    {"Ooze Cube":"While this monster is large or larger, it takes up its entire space. Other creatures can enter the space, but a creature that does so is subjected to the this monster's Engulf and has disadvantage on the saving throw. Creatures inside the cube can be seen but have total cover. A creature within 5 feet of this monster can take an action to pull a creature or object out of this monster. Doing so requires a successful DC 12 Strength check, and the creature making the attempt takes 3d6 "+element+" damage. This creature can hold only one Large creature or up to four Medium or smaller creatures inside it at a time."},
                ]
                current_traits+= ooze_cube
        if creature_type in ["Elemental"]:
            elemental_traits = [
                {"False Appearance": "While this monster remains motionless, it is indistinguishable from a natural occurence of its type ("+element+")."},
                {element.capitalize()+" Absorption": "Whenever this monster is subjected to "+element+" damage, it takes no damage and instead regains a number of hit points equal to the damage dealt."},
            ]
            elemental_body = [{element.capitalize()+" Body": "This monster can move through a space as narrow as 1 inch wide without squeezing. A creature that touches the elemental or hits it with a melee attack while within 5 feet of it takes 1d10 "+element+" damage. In addition, the elemental can enter a hostile creature's space and stop there."},
            ]
            magic_weapons = [{element.capitalize()+" Weapons":"This monster's weapon attacks are magical. When this monster hits with any weapon, the weapon deals an extra "+str(bonus_dice)+"d6 "+element+" damage (not included in the attack.)"}]
            if itemuser == "yes":
                elemental_traits += magic_weapons
            elif itemuser == "no":
                elemental_traits += elemental_body
            current_traits += random.sample(elemental_traits, low_traits_available- len(current_traits) - len(current_reactions))
        if creature_type in ["Undead"]:
            undead_traits = [
                {"Undead Fortitude": "If damage reduces this monster to 0 hit points, it must make a Constitution saving throw with a DC of 5+ the damage taken, unless the damage is radiant or from a critical hit. On a success, this monster drops to 1 hit point instead."},
                {"Turning Defiance": "The creature and any allies within 30 feet of it have advantage on saving throws against effects that turn undead."},
            ]
            current_traits += random.sample(undead_traits, 1)
        if total_traits - len(current_traits) - len(current_reactions) > 0:
            low_traits = [
                {"Immutable Form": "This monster is immune to any spell or spell effect that would alter its form."},
                {"Mimicry": "This monster can mimic sounds it has heard, including voices. Creatures that hear the sounds can tell they are imitations with a successful Wisdom (Insight) check opposed by this monster's Charisma (Deception) check."},
                {"Adhesive": "This monster adheres to anything that touches it. A creature adhered to this monster that is the same size or smaller is also grappled by it (escape DC 13). Ability checks made to escape this grapple have disadvantage."},
                {"Barbed Hide": "At the start of each of its turns, this monster deals "+str(bonus_dice)+"d10 piercing damage to any creature grappling it."},
                {"Damage Transfer": "While it is grappling, this monster takes only half the damage dealt to it, and the creature being grappled by this monster takes the other half."},
                {"Grappler": "This monster has advantage on attack rolls against any enemy grappled by it."},
                {"Variable Illumination": "This monster sheds bright light in a 0- to 30-foot radius and dim light for an additional number of feet equal to the chosen radius. This monster can alter the radius as a bonus action."},
                {"Pack Tactics": "This monster has advantage on an attack roll against a creature if at least one of this monster's allies is within 5 ft of the creature and the ally isn't incapacitated."},
                {"Spider Climb": "This monster can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check. This monster ignores movement restrictions caused by webbing."},
                {"Standing Leap": "This monster's long jump is up to 20 ft and its high jump is up to 10 ft with or without a running start."},
                {"Stench": "Any creature that starts its turn within 5 ft of this monster must succeed on a DC 12 Constitution saving throw or be poisoned until the start of the creature's next turn. On a successful saving throw, the creature is immune to the stench of all types of this monster for 1 hour."},
            ]
            if creature_type == "Beast" or creature_type == "Swarm":
                limited_low_traits = [
                    {"Amphibious": "This monster can breathe air and water."},
                    {"Keen Senses": "This monster has advantage on Wisdom (Perception) checks that rely on sight, sound, or smell."},
                    {"Camouflage":"This monster has advantage on Dexterity (Stealth) checks."},
                ]
                low_traits += limited_low_traits
            if creature_type in ["Aberration"]:
                low_traits += [
                    {"Gibbering": "This monster babbles incoherently while it can see a creature and isn't incapacitated. Each creature that starts its turn within 20 feet of this monster can hear the gibbering must succeed on a DC 10 Wisdom saving throw. On a failure, the creature can't take reactions until the start of its next turn and rolls a d8 to determine what it does during its turn. On a 1 to 4, the creature does nothing. On a 5 or 6, the creature takes no action or bonus action and uses all its movement to move in a randomly determined direction. On a 7 or 8, it makes a melee attack against a randomly determined creature within its reach or does nothing if it can't make such an attack."},
                    {"Aberrant Ground": "The ground in a 10-foot radius around this monster is difficult terrain. Each creature that starts its turn in that area must succeed on a DC 13 Strength saving throw or have its speed reduced to 0 until the start of its next turn."},
                ]
            elif creature_type not in ["Ooze","Elemental","Construct","Beast","Swarm"]:
                limited_low_traits = [
                    {"Amphibious": "This monster can breathe air and water."},
                    {"Inscrutable": "This monster is immune to any effect that would sense its emotions or read its thoughts, as well as any divination spell that it refuses. Wisdom (Insight) checks made to ascertain this monster's intentions or sincerity have disadvantage."},
                    {"Keen Senses": "This monster has advantage on Wisdom (Perception) checks that rely on sight, sound, or smell."},
                    {"Limited Telepathy": "This monster can magically communicate simple ideas, emotions, and images telepathically with any creature within 100 feet of it that can understand a language."},
                    {"Camouflage":"This monster has advantage on Dexterity (Stealth) checks."},
                    {"Sense Magic": "This monster senses magic within 120 feet of it at will. This trait otherwise works like the detect magic spell but isn't itself magical."},
                ]
                low_traits += limited_low_traits
            else:
                pass
            medium_traits = [
                {"Aggressive": "As a bonus action, this monster can move up to its speed toward a hostile creature that it can see."},
                {"Berserk": "Whenever this monster starts its turn with half hit points or fewer, roll ad6. On a 6, this monster goes berserk. On each of its turns while berserk, this monster attacks the nearest creature it can see. If no creature is near enough to move to and attack, it will instead attack an object, with preference for an object smaller than itself. Once it goes berserk, it continues to do so until it is destroyed or regains all its hit points."},
                {"Reckless": "At the start of its turn, this monster can gain advantage on all melee weapon attack rolls it makes during that turn, but attack rolls against it have advantage until the start of its next turn."},
                {"Nimble Escape": "This monster can take the Disengage or Hide action as a bonus action on each of its turns."},
                {"Relentless": "The first time this monster takes damage that would reduce it to 0 hit points, it is reduced to 1 hit point instead."},
                {"Rampage": "When this monster reduces an enemy to 0 hit points with a melee attack on its turn, this monster can take a bonus action to move up to half its speed and make another attack."},
            ]
            if creature_type == "Beast":
                limited_medium_traits = [
                    {"Two Heads": "This monster has advantage on Wisdom (Perception) checks and on saving throws against being blinded, charmed, deafened, frightened, stunned, and knocked unconscious."},
                ]
                medium_traits += limited_medium_traits
            if creature_type != "Beast" and creature_type != "Swarm":
                limited_medium_traits = [
                    {"Shapechanger": "This monster can use its action to polymorph into a humanoid of the same size or smaller, a monster-humanoid hybrid of the same size, or back into its true form. Its statistics, other than its size, are the same in each form. Any equipment it is wearing or carrying isn't transformed. It reverts to its true form if it dies."},
                    {"Ethereal Jaunt": "As a bonus action, this monster can magically shift from the Material Plane to the Ethereal Plane, or vice versa."},
                    {"Incorporeal Movement": "This monster can move through creatures and objects as if they were difficult terrain. This monster takes 5 (1d10) force damage if this monster ends their turn inside an object."},
                ]
                medium_traits += limited_medium_traits
            if creature_type not in ["Ooze","Elemental","Construct","Beast","Swarm"]:
                limited_medium_traits = [
                {"Two Heads": "This monster has advantage on Wisdom (Perception) checks and on saving throws against being blinded, charmed, deafened, frightened, stunned, and knocked unconscious."},
                {"Tree Stride": "Once per turn, this monster can use 10 ft of its movement to step magically into one living tree within reach, and emerge from a second living tree within 60 ft of the first tree, appearing in an unoccupied space within 5 ft of the second tree. Both trees must be the same size as this creature or bigger."},
                ]
                medium_traits += limited_medium_traits
            if creature_type in ["Monstrosity"]:
                medium_traits += [
                    {"Petrifying Gaze": "If an enemy starts its turn within 30 ft of this monster and the two of them can see each other, this monster can force the creature to make a DC 12 Constitution saving throw if this monster isn't incapacitated. On a failed save, the creature magically begins to turn to stone and is restrained. It must repeat the saving throw at the end of its next turn. On a success, the effect ends. On a failure, the creature is petrified until freed by the greater restoration spell or other magic. If the saving throw fails by 5 or more, the creature is instantly petrified. Unless surprised, a creature can avert its eyes to avoid the saving throw at the start of its turn. If it does so, it can't see this monster until the start of its next turn, when it can avert its eyes again. If it looks at this monster in the meantime, it must immediately make the save. If this monster sees itself reflected within 30 ft of it and in an area of bright light, it is affected by its own gaze."},
                ]
            high_traits = [
                {"Freedom of Movement": "This monster ignores difficult terrain, and magical effects can't reduce its speed or cause it to be restrained. It can spend 5 feet of movement to escape from nonmagical restraints or being grappled."},
                {"Limited Magic Immunity": "This monster can't be affected or detected by spells of 6th level or lower unless it wishes to be. It has advantage on saving throws against all other spells and magical effects."},
                {"Regeneration": "This monster regains 10 hit points at the start of its turn. If this monster takes acid, fire, or any type of damage that it is vulnerable to, this trait doesn't function at the start of this monster's next turn. This monster dies only if it starts its turn with 0 hit points and doesn't regenerate."},
                {"Blood Frenzy": "This monster has advantage on melee attack rolls against any creature that doesn't have all its hit points."},
                {"Legendary Resistance (3/Day)": "If this creature fails a saving throw, it can choose to succeed instead."},
                {"Corrode Metal": "Any nonmagical weapon made of metal that hits this monster corrodes. After dealing damage, the weapon takes a permanent and cumulative -1 penalty to damage rolls. If its penalty drops to -5, the weapon is destroyed. Nonmagical ammunition made of metal that hits this monster is destroyed after dealing damage. This monster can eat through 2-inch-thick, nonmagical metal in 1 round."},
            ]
            limited_high_traits = [
                {"Consume Life": "As a bonus action, this monster can target a creature it can see within 5 feet of it that has 0 hit points and is still alive. The target must succeed on a DC 10 Constitution saving throw against this magic or die. If the target dies, this creature regains 10 (3d6) hit points."},
                {"Invisibility": "This monster is invisible."},
            ]
            if creature_type not in ["Ooze","Elemental","Construct","Beast","Swarm"]:
                high_traits += limited_high_traits
            else:
                pass
            if creature_type in ["Ooze","Elemental","Construct","Swarm"]:
                save_traits = []
            else:
                save_traits = [
                    {"Resilient Ancestry": "This monster has advantage on saving throws against being charmed, and magic can't put this monster to sleep."},
                    {"Resilience": "This monster has advantage on saving throws against poison, spells, and illusions, as well as to resist being charmed or paralyzed."},
                    {"Cunning": "This monster has advantage on Intelligence, Wisdom, and Charisma saving throws against magic."},
                    {"Magic Resistance": "This monster has advantage on saving throws against spells and other magical effects."},
                    {"Steadfast": "This monster can't be frightened while it can see an allied creature within 30 feet of it."},
                    {"Brave": "This monster has advantage on saving throws against being frightened."},
                    {"Sure-footed": "This monster has advantage on Strength and Dexterity saving throws made against effects that would knock it prone."},
                    {"Evasion": "If this monster is subjected to an effect that allows it to make a Dexterity saving throw to take only half damage, this monster instead takes no damage if it succeeds on the saving throw, and only half damage if it fails. "},
                ]
            reactions = [
                {"Parry": "This monster may use a reaction to add 2 to its AC against a melee attack that would hit it."},
                {"Projectile Deflection": "If a projectile is fired or thrown at this monster, this monster can make a Dexterity saving throw. The damage is reduced by that amount."},
                {"Shield": "When a creature makes an attack against one of this monster's allies, this monster grants a +2 bonus to the creature's AC if this monster is within 5 feet of the creature."},
                {"Attack": "This monster makes one attack."},
                {"Move": "This monster may move up to one half its base speed."},
            ]
            if creature_type != "Beast":
                reactions += [{"Teleport": "This monster magically teleports, along with any equipment it is wearing or carrying, up to 30 feet to an unoccupied space it can see."},]
            flying_traits = [{"Flyby": "This monster doesn't provoke an opportunity attack when it flies out of an enemy's reach."}]
            roll = random.randint(0, 100)
            if (roll > 80 and low_traits_available - len(current_traits) - len(current_reactions) > 0):
                current_traits += random.sample(save_traits, min(len(save_traits),1))
            roll = random.randint(0, 100)
            if (roll > 80 and low_traits_available - len(current_traits) - len(current_reactions) > 0):
                current_reactions += random.sample(reactions, 1)
            roll = random.randint(0, 100) + challengerating * 3
            if roll > 50 and low_traits_available - len(current_traits) - len(current_reactions) > 0:
                for i in movement:
                    for key in i.keys():
                        if key == "fly":
                            if roll > 50:
                                current_traits += flying_traits
            current_traits += random.sample(low_traits, max(0,low_traits_available- len(current_traits) - len(current_reactions)))
        if total_traits - len(current_traits) - len(current_reactions) > 0:
            current_traits += random.sample(medium_traits, medium_traits_available)
        if total_traits - len(current_traits) - len(current_reactions) > 0:
            current_traits += random.sample(high_traits, high_traits_available)
        if creature_type in ["Devil"]:
            devil_traits = [
                {"Devil's Sight": "Magical darkness doesn't impede this monster's senses."}
            ]
            current_traits += devil_traits
        if creature_type in ["Celestial"]:
            celestial_traits = [
                {"Divine Awareness": "This monster knows if it hears a lie."}
            ]
            current_traits += celestial_traits
        if creature_type in ["Swarm"]:
            swarm_traits = [
                {"Swarm": "The swarm can occupy another creature's space and vice versa, and the swarm can move through any opening large enough for a tiny creature. The swarm can't regain hit points or gain temporary hit points."},
            ]
            current_traits += swarm_traits
        if challengerating > 6 and itemuser == "yes" and creature_type != "Elemental":
            if archetype in ["str_user","dex_user"]:
                if element == "none":
                    del current_traits[0]
                    brute = [{"Brute":"A melee weapon deals "+str(bonus_dice)+" extra dice of its damage when this monster hits with it (not included in the attack)."}]
                    current_traits += brute
                else:
                    del current_traits[0]
                    magic_weapons = [{element.capitalize()+" Weapons":"This monster's weapon attacks are magical. When this monster hits with any weapon, the weapon deals an extra "+str(bonus_dice)+"d6 "+element+" damage (not included in the attack.)"}]
                    current_traits += magic_weapons
        return current_traits, current_reactions

    # returns a dict where key is header like "Damage Resistance" and value is list of types
    def get_resistances(self, creature_type,element):
        damage_immune = {
            "acid": ["acid"],
            "cold": ["cold"],
            "Construct": ["psychic", "poison"],
            "fire": ["fire"],
            "Demon": ["poison"],
            "Devil": ["fire", "poison"],
            "Elemental": ["poison"],
            "lightning": ["lightning", "thunder"],
            "necrotic": ["necrotic"],
            "poison": ["poison"],
            "thunder": ["thunder", "lightning"],
            "Undead": ["poison"],
        }
        damage_resist = {
            "Aberration": [],
            "Beast": [],
            "Celestial": ["radiant", "non-magical"],
            "Construct": [],
            "Demon": ["cold", "fire", "lightning", "non-magical"],
            "Devil": ["cold", "non-magical"],
            "Dragon": [],
            "Elemental": ["non-magical"],
            "Fey": [],
            "Giant": [],
            "Humanoid": [],
            "Monstrosity": [],
            "Ooze": ["slashing"],
            "Plant": ["bludgeoning", "piercing"],
            "Swarm": ["non-magical"],
            "Undead": ["necrotic"],
        }
        damage_vulnerable = {"Plant": ["fire"], "Undead": ["radiant"]}
        condition_immune = {
            "Aberration": [],
            "Beast": [],
            "Celestial": ["charmed", "frightened", "exhaustion"],
            "Construct": ["charmed", "frightened", "paralyzed", "petrified", "poisoned"],
            "Demon": ["poisoned"],
            "Devil": ["poisoned"],
            "Dragon": [],
            "Elemental": ["charmed","grappled","paralyzed","petrified","poisoned","prone","restrained","unconscious",],
            "Fey": [],
            "Giant": [],
            "Humanoid": [],
            "Monstrosity": [],
            "Ooze": ["blinded", "charmed", "deafened", "frightened", "prone", "exhaustion"],
            "Plant": ["blinded", "deafened", "exhaustion"],
            "Swarm": ["charmed","frightened","grappled","paralyzed","petrified","poisoned","prone","stunned",],
            "Undead": ["charmed", "frightened", "poisoned", "exhaustion"],
        }
        damage_immunities = []
        damage_resistances = []
        damage_vulnerabilities = []
        condition_immunities = []
        if creature_type in ["Ooze","Dragon","Elemental"]:
            if element in damage_immune.keys():
                damage_immunities += damage_immune[element]
        if creature_type in damage_immune.keys():
            damage_immunities += damage_immune[creature_type]
        if creature_type in damage_resist.keys():
            damage_resistances += damage_resist[creature_type]
        if creature_type in damage_vulnerable.keys():
            damage_vulnerabilities += damage_vulnerable[creature_type]
        if creature_type in condition_immune.keys():
            condition_immunities += condition_immune[creature_type]
        output = {}
        if len(damage_resistances) > 0:
            output["Damage Resistances"] = damage_resistances
        if len(damage_vulnerabilities) > 0:
            output["Damage Vulnerabilities"] = damage_vulnerabilities
        if len(damage_immunities) > 0:
            output["Damage Immunities"] = damage_immunities
        if len(condition_immunities) > 0:
            output["Condition Immunities"] = condition_immunities
        return(output)

    # returns a list of dicts with skill name as key
    def get_skills(self, archetype,proficiency_bonus,strmod,dexmod,intmod,wismod,chamod):
        skills = {
            "dex_user": [{"Acrobatics":"+"+str(proficiency_bonus+dexmod)},{"Stealth":"+"+str(proficiency_bonus+dexmod)}],
            "int_user": [{"Arcana":"+"+str(proficiency_bonus+intmod)},{"Investigate":"+"+str(proficiency_bonus+intmod)},],
            "str_user": [{"Athletics":"+"+str(proficiency_bonus+strmod)},{"Perception":"+"+str(proficiency_bonus+wismod)},],
            "cha_user": [{"Intimidation":"+"+str(proficiency_bonus+chamod)},{"Deception":"+"+str(proficiency_bonus+chamod)}],
            "wis_user": [{"Perception":"+"+str(proficiency_bonus+wismod)},{"Insight":"+"+str(proficiency_bonus+wismod)},],
        }
        proficient_skills = skills[archetype]
        return(proficient_skills)

    # returns a list of dicts with save name as key
    def get_proficient_saves(self, archetype, creature_type, challengerating, proficiency_bonus, strmod, dexmod, conmod, intmod, wismod, chamod):
        saves_dict = {
            "str_user":[{"Str":"+"+str(proficiency_bonus+strmod)}],
            "dex_user":[{"Dex":"+"+str(proficiency_bonus+dexmod)}],
            "int_user":[{"Int":"+"+str(proficiency_bonus+intmod)}],
            "wis_user":[{"Wis":"+"+str(proficiency_bonus+wismod)}],
            "cha_user":[{"Cha":"+"+str(proficiency_bonus+chamod)}],
            "Beast":[{"Con":"+"+str(proficiency_bonus+conmod)}],
            "Monstrosity":[{"Con":"+"+str(proficiency_bonus+conmod)}],
            "Undead":[{"Wis":"+"+str(proficiency_bonus+wismod)}],
        }
        saves_list = [
            {"Str":"+"+str(proficiency_bonus+strmod)},
            {"Dex":"+"+str(proficiency_bonus+dexmod)},
            {"Con":"+"+str(proficiency_bonus+conmod)},
            {"Int":"+"+str(proficiency_bonus+intmod)},
            {"Wis":"+"+str(proficiency_bonus+wismod)},
            {"Cha":"+"+str(proficiency_bonus+chamod)}]
        random.shuffle(saves_list)
        proficient_saves = []
        if archetype in saves_dict.keys():
            proficient_saves += saves_dict[archetype]
        if creature_type in saves_dict.keys():
            saves_dict[creature_type]
            proficient_saves += saves_dict[creature_type]
        saves_list = [i for i in saves_list if i not in proficient_saves]
        proficient_saves += random.sample(saves_list,min(len(saves_list),challengerating//8))
        return(proficient_saves)

    # returns list of known languages
    def get_languages(self, creature_type, intelligencemod,challengerating):
        languages={
            "Aberration":["Deep Speech","Common"],
            "Beast":[],"Celestial":["Celestial","Common",],
            "Construct":["Abyssal","Celestial","Draconic","Deep Speech","Infernal","Primordial","Undercommon","Common","Dwarvish","Elvish","Giant","Gnomish","Goblin","Halfling","Orc",],
            "Demon":["Abyssal","Common",],
            "Devil":["Infernal","Common",],
            "Dragon":["Draconic","Common"],
            "Elemental":["Primordial","Common"],
            "Fey":["Sylvan","Common"],
            "Giant":["Common","Giant"],
            "Humanoid":["Abyssal","Celestial","Draconic","Deep Speech","Infernal","Primordial","Undercommon","Common","Dwarvish","Elvish","Giant","Gnomish","Goblin","Halfling","Orc",],
            "Monstrosity":[],
            "Ooze":[],
            "Plant":["Sylvan"],
            "Swarm":[],"Undead":["Infernal","Common","Dwarvish","Elvish","Giant","Gnomish","Goblin","Halfling","Orc",],
        }
        if len(languages[creature_type]) == 0:
            known_languages = ["none"]
        else:
            language_list = languages[creature_type]
            known_languages = random.sample(language_list, max(1, min(len(language_list), intelligencemod)))
        if intelligencemod < -2:
            roll = random.randint(0,100)
            if roll < 20:
                known_languages = ["none"]
            if known_languages != ["none"]:
                known_languages[0] = "Understands but cannot speak "+known_languages[0]
        if creature_type in ["Celestial"]:
            roll = random.randint(0, 100) + challengerating*2
            if roll > 50:
                known_languages = ["all, telepathy 120ft."]
        if creature_type in ["Devil","Demon"]:
            roll = random.randint(0, 100) + challengerating*2
            if roll > 50:
                known_languages += ["telepathy 120ft."]
        return(known_languages)

    # returns empty dict or dict with sense type as key
    def get_senses(self, creature_type, challengerating,skills):
        senses = {
            "Aberration": ["darkvision", "tremorsense"],
            "Beast": ["blindsight", "tremorsense"],
            "Celestial": ["truesight"],
            "Construct": ["blindsight (blind beyond this radius)","darkvision","tremorsense",],
            "Demon": ["blindsight", "darkvision", "truesight"],
            "Devil": ["blindsight", "darkvision", "truesight"],
            "Dragon": ["blindsight", "darkvision", "tremorsense"],
            "Elemental": ["darkvision", "tremorsense"],
            "Fey": ["darkvision", "tremorsense"],
            "Giant": ["tremorsense"],
            "Humanoid": ["blindsight", "darkvision", "tremorsense", "truesight"],
            "Monstrosity": ["blindsight", "darkvision", "tremorsense"],
            "Ooze": ["blindsight (blind beyond this radius)"],
            "Plant": ["blindsight (blind beyond this radius)"],
            "Swarm": ["blindsight", "tremorsense"],
            "Undead": ["blindsight", "blindsight (blind beyond this radius)", "darkvision"],
        }
        distance = 5 * round(((challengerating * 8) / 5))
        distancemax = min(150, distance)
        sense_list = senses[creature_type]
        if creature_type in ["Demon", "Devil"]:
            if challengerating <= 10:
                sense = {"darkvision": distancemax}
            if challengerating > 10:
                sense = {"truesight": distancemax}
        elif creature_type in ["Ooze", "Plant"]:
            sense = {random.choice(sense_list): distancemax}
        else:
            roll = random.randint(0, 100) + challengerating
            if roll > 50:
                sense = {random.choice(sense_list): distancemax}
            else:
                sense = {}
        for k,v in sense.items():
            sense[k] = str(v)+" ft."
        if "blindsight (blind beyond this radius)" in sense.values():
            sense = {
                "blindsight":str(min(60, max(30, 5 * round(((challengerating * 4) / 5)))))+" (blind beyond this radius)"
            }
        for i in skills:
            for k,v in i.items():
                if k == "Perception":
                    if "-" in v:
                        v = v.replace('-','')
                        sense["passive Perception"] = str(10-int(v))
                    else:
                        sense["passive Perception"] = str(10+int(v))
        return(sense)

    # returns lowercase string of element
    def get_element(self, creature_type, challengerating):
        element_type_by_creature = {
            "Aberration": ["none", "force", "necrotic", "poison", "psychic"],
            "Beast": ["none"],
            "Celestial": ["none", "force", "radiant", "thunder"],
            "Construct": ["none","acid","cold","fire","force","lightning","poison","thunder",],
            "Demon": ["none", "fire", "necrotic", "poison", "psychic", "thunder"],
            "Devil": ["none", "fire", "necrotic", "poison", "psychic", "thunder"],
            "Dragon": ["acid", "cold", "fire", "lightning", "poison", "radiant"],
            "Elemental": ["acid","cold","fire","force","lightning","poison","thunder",],
            "Fey": ["none", "force", "lightning", "necrotic", "poison", "psychic"],
            "Giant": ["none", "cold", "fire", "lightning", "radiant", "thunder"],
            "Humanoid": ["none","acid","cold","fire","force","lightning","necrotic","poison","psychic","radiant","thunder",],
            "Monstrosity": ["none", "fire", "necrotic", "poison", "thunder"],
            "Ooze": ["acid", "cold", "fire", "necrotic", "poison"],
            "Plant": ["none", "acid", "poison"],
            "Swarm": ["none"],
            "Undead": ["none","acid","cold","fire","force","lightning","necrotic","poison","psychic",],
        }
        if creature_type in ["Elemental", "Dragon"]:
            element_list = element_type_by_creature[creature_type]
            return(random.choice(element_list))
        elif creature_type == "Ooze":
            element_list = element_type_by_creature[creature_type]
            roll = random.randint(0, 100) + challengerating * 2
            if roll > 50:
                return(random.choice(element_list))
            else:
                return("acid")
        else:
            element_list = element_type_by_creature[creature_type]
            roll = random.randint(0, 100) + challengerating * 2
            if roll > 50:
                return(random.choice(element_list))
            else:
                return("none")

    # returns a list of dicts; each dict key is type of movement
    def get_speed(self, creature_type, challengerating, size):
        base_speed = 30
        match size:
            case "Tiny":
                base_speed = 10
            case "Small":
                base_speed = 20
            case "Medium":
                base_speed = 30
            case "Large":
                base_speed = 35
            case "Huge":
                base_speed = 40
            case "Gargantuan":
                base_speed = 45
        speed_type = {
            "Aberration": [
                {"fly": base_speed * 2},
                {"swim": base_speed},
            ],
            "Beast": [
                {"burrow": base_speed},
                {"climb": base_speed},
                {"fly": base_speed * 2},
                {"swim": base_speed},
            ],
            "Celestial": [
                {"fly": base_speed * 2},
            ],
            "Construct": [
                {"fly": base_speed * 2},
                {"swim": base_speed},
            ],
            "Demon": [
                {"fly": base_speed * 2},
            ],
            "Devil": [
                {"fly": base_speed * 2},
            ],
            "Dragon": [
                {"burrow": base_speed},
                {"fly": base_speed * 2},
                {"swim": base_speed},
            ],
            "Elemental": [],
            "Fey": [
                {"burrow": base_speed},
                {"fly": base_speed * 2},
                {"swim": base_speed},
            ],
            "Giant": [
                {"climb": base_speed},
            ],
            "Humanoid": [
                {"fly": base_speed * 2},
            ],
            "Monstrosity": [
                {"burrow": base_speed},
                {"climb": base_speed},
                {"fly": base_speed * 2},
                {"swim": base_speed},
            ],
            "Ooze": [],
            "Plant": [],
            "Swarm": [
                {"fly": base_speed * 2},
                {"swim": base_speed}
            ],
            "Undead": [
                {"fly": base_speed * 2},
            ],
        }
        walk = [{"walk": base_speed}]
        speed_list = speed_type[creature_type]
        roll = random.randint(0, 100) + challengerating * 2
        if creature_type in ["Beast"]:
            if roll > 80:
                speed_list = walk + random.sample(speed_list, 2)
            elif roll > 30:
                speed_list = walk + random.sample(speed_list, 1)
            else:
                speed_list = walk
        elif creature_type in ["Celestial"]:
            if roll > 30:
                speed_list = walk + random.sample(speed_list, 1)
            else:
                speed_list = walk
        elif creature_type in ["Dragon"]:
            speed_list = walk + random.sample(speed_list, 1)
        elif creature_type in ["Demon", "Devil"]:
            if roll > 30:
                speed_list = walk + random.sample(speed_list, 1)
            else:
                speed_list = walk
        elif creature_type in ["Fey"]:
            if size in ["Tiny","Small"]:
                speed_list = walk + random.sample(speed_list, 1)
            elif roll > 30:
                speed_list = walk + random.sample(speed_list, 1)
            else:
                speed_list = walk
        elif creature_type in ["Humanoid"]:
            if roll > 90:
                speed_list = walk + random.sample(speed_list, 1)
            else:
                speed_list = walk
        elif creature_type in ["Giant"]:
            if roll > 30:
                speed_list = walk + random.sample(speed_list, 1)
            else:
                speed_list = walk
        elif creature_type in ["Monstrosity"]:
            if roll > 80:
                speed_list = walk + random.sample(speed_list, 2)
            elif roll > 30:
                speed_list = walk + random.sample(speed_list, 1)
            else:
                speed_list = walk
        elif creature_type in ["Swarm"]:
            if roll > 50:
                speed_list = walk + random.sample(speed_list, 1)
            else:
                speed_list = walk
        else:
            speed_list = walk
        for items in speed_list:
            for k,v in items.items():
                items[k] = str(v)+" ft."
        return speed_list

    # returns string
    def get_archetype(self,creature_type):
        archetype = {
        "Aberration": ["str_user", "dex_user", "int_user", "cha_user"],
        "Beast": ["str_user", "dex_user"],
        "Celestial": ["str_user", "dex_user", "wis_user", "cha_user"],
        "Construct": ["str_user", "dex_user"],
        "Demon": ["str_user", "dex_user", "cha_user"],
        "Devil": ["str_user", "dex_user", "cha_user"],
        "Dragon": ["str_user", "dex_user", "cha_user"],
        "Elemental": ["str_user", "dex_user", "int_user", "wis_user", "cha_user"],
        "Fey": ["str_user", "dex_user", "wis_user", "cha_user"],
        "Giant": ["str_user", "wis_user", "cha_user"],
        "Humanoid": ["str_user", "dex_user", "int_user", "wis_user", "cha_user"],
        "Monstrosity": ["str_user", "dex_user", "int_user", "wis_user", "cha_user"],
        "Ooze": ["str_user"],
        "Plant": ["str_user", "dex_user"],
        "Swarm": ["str_user", "dex_user"],
        "Undead": ["str_user", "dex_user", "int_user", "wis_user", "cha_user"],
        }
        archetypelist = archetype[creature_type]
        return random.choice(archetypelist)

    # returns int
    def get_proficiency_bonus(self,challengerating):
        return int((challengerating // 4.1) + 2)
    
    # returns dictionary with each ability score name as key
    def get_ability_scores(self,archetype, challengerating, creature_type):
        starting_array = {
            "str_user": {
                "strength": 15,
                "dexterity": 13,
                "constitution": 14,
                "intelligence": 0,
                "wisdom": 0,
                "charisma": 0,
            },
            "dex_user": {
                "strength": 13,
                "dexterity": 15,
                "constitution": 14,
                "intelligence": 0,
                "wisdom": 0,
                "charisma": 0,
            },
            "int_user": {
                "strength": 0,
                "dexterity": 14,
                "constitution": 13,
                "intelligence": 15,
                "wisdom": 0,
                "charisma": 0,
            },
            "wis_user": {
                "strength": 0,
                "dexterity": 14,
                "constitution": 13,
                "intelligence": 0,
                "wisdom": 15,
                "charisma": 0,
            },
            "cha_user": {
                "strength": 0,
                "dexterity": 14,
                "constitution": 13,
                "intelligence": 0,
                "wisdom": 0,
                "charisma": 15,
            },
        }
        available_scores = [8, 10, 12]
        random_available_scores = list(range(len(available_scores)))
        random.shuffle(random_available_scores)
        assigned_abilityscores = [available_scores[i] for i in random_available_scores]

        abilityscores = starting_array[archetype].copy()
        i = 0
        for k, v in abilityscores.items():
            if v == 0:
                abilityscores[k] = assigned_abilityscores[i]
                i += 1
        abilityscores = dict(sorted(abilityscores.items(), key=lambda item: item[1]))
        i = 0
        for k, v in abilityscores.items():
            if i < 3:
                abilityscores[k] = v + (challengerating // 4)
            if i == 3:
                abilityscores[k] = v + (challengerating // 3)
            if i == 4:
                abilityscores[k] = v + (challengerating // 2)
            if i == 5:
                abilityscores[k] = v + (challengerating // 2)
            i += 1
        if creature_type in ["Undead", "Ooze", "Construct", "Elemental"]:
            if archetype not in ["int_user", "cha_user", "wis_user"]:
                abilityscores["intelligence"] = max(abilityscores["intelligence"] - 10, 1)
                abilityscores["charisma"] = max(abilityscores["charisma"] - 10, 1)
                abilityscores["wisdom"] = max(abilityscores["wisdom"] - 10, 3)
        if creature_type in ["Beast", "Monstrosity","Swarm"]:
            if archetype not in ["int_user", "cha_user", "wis_user"]:
                abilityscores["intelligence"] = max(abilityscores["intelligence"] - 11, 1)
                abilityscores["charisma"] = max(abilityscores["charisma"] - 7, 4)
        if creature_type == "Giant":
            roll = random.randint(1,100) + challengerating*2
            abilityscores["strength"] += roll//25
            if abilityscores["strength"] < 18:
                abilityscores["strength"] = 18
            if abilityscores["strength"] > 30:
                abilityscores["strength"] = 30
            roll = random.randint(1,100) + challengerating*2
            abilityscores["constitution"] += roll//25
            if abilityscores["constitution"] < 18:
                abilityscores["constitution"] = 18
            if abilityscores["constitution"] > 30:
                abilityscores["constitution"] = 30
        return abilityscores
    
    # returns int - ex: 14 -> 2; 8 -> -1
    def abilitymod(self, score):
        mod = (int(score / 2)) - 5
        return mod

    # returns int
    def get_hit_points(self, challengerating, conmod,archetype,movement):
        hit_points = round((70 + (challengerating * ((challengerating ** (1/2) ) *2))+(conmod*challengerating) * random.uniform(0.900, 1.100)))
        if archetype in ["int_user","wis_user","cha_user"]:
            hit_points = round(hit_points*.9)
        for i in movement:
            for key in i.keys():
                if key == "fly":
                    hit_points = round(hit_points*.9)
        return hit_points

    # returns string
    def get_size(self, creature_type, challengerating):
        creature_size = {
            "Aberration": ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"],
            "Beast": ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"],
            "Celestial": ["Tiny", "Small", "Medium", "Large"],
            "Construct": ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"],
            "Demon": ["Tiny", "Small", "Medium", "Large", "Huge"],
            "Devil": ["Tiny", "Small", "Medium", "Large", "Huge"],
            "Dragon": ["Small", "Medium", "Large", "Huge", "Gargantuan"],
            "Elemental": ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"],
            "Fey": ["Tiny", "Small", "Medium", "Large"],
            "Giant": ["Large", "Huge", "Gargantuan"],
            "Humanoid": ["Small", "Medium", "Large"],
            "Monstrosity": ["Small", "Medium", "Large", "Huge", "Gargantuan"],
            "Ooze": ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"],
            "Plant": ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"],
            "Swarm": ["Medium", "Large", "Huge", "Gargantuan"],
            "Undead": ["Tiny", "Small", "Medium", "Large", "Huge"],
        }
        # The if statements capture creatures that are generally medium, with some variance
        sizelist = creature_size[creature_type]
        if creature_type in ["Celestial"]:
            size = random.choices(sizelist, weights=[1, 1, 8, 2])
            return("".join(size))
        elif creature_type in ["Humanoid"]:
            size = random.choices(sizelist, weights=[1, 4, 2])
            return("".join(size))
        elif creature_type in ["Fey"]:
            size = random.choices(sizelist, weights=[2, 5, 5, 1])
            return("".join(size))
        # The else statement captures creatures where higher CR generally means bigger size
        else:
            sizelistceiling = (
                min(len(sizelist), max(challengerating - len(sizelist), 2)) - 1
            )
            sizelistfloor = max(sizelistceiling - 2, 0)
            return(sizelist[random.randint(sizelistfloor, sizelistceiling)])

    # returns string
    def get_alignment(self, creature_type):
        alignment = {
            "Aberration": ["True Neutral","Chaotic Neutral","Lawful Evil","Neutral Evil","Chaotic Evil",],
            "Beast": ["Unaligned",],
            "Celestial": ["Lawful Good", "Neutral Good", "Chaotic Good",],
            "Construct": ["Unaligned",],
            "Demon": ["Neutral Evil", "Chaotic Evil",],
            "Devil": ["Lawful Evil", "Neutral Evil",],
            "Dragon": ["Lawful Good","Neutral Good","Chaotic Good","Lawful Neutral","True Neutral","Chaotic Neutral","Lawful Evil","Neutral Evil","Chaotic Evil",],
            "Elemental": ["Lawful Good","Neutral Good","Chaotic Good","Lawful Neutral","True Neutral","Chaotic Neutral","Lawful Evil","Neutral Evil","Chaotic Evil","Unaligned",],
            "Fey": ["Neutral Good","Chaotic Good","True Neutral","Chaotic Neutral","Chaotic Evil",],
            "Giant": ["Lawful Good","Neutral Good","Chaotic Good","Lawful Neutral","True Neutral","Chaotic Neutral","Lawful Evil","Neutral Evil","Chaotic Evil",],
            "Humanoid": ["Lawful Good","Neutral Good","Chaotic Good","Lawful Neutral","True Neutral","Chaotic Neutral","Lawful Evil","Neutral Evil","Chaotic Evil",],
            "Monstrosity": ["Unaligned","Lawful Good","Neutral Good","Chaotic Good","Lawful Neutral","True Neutral","Chaotic Neutral","Lawful Evil","Neutral Evil","Chaotic Evil",],
            "Ooze": ["Unaligned",],
            "Plant": ["Unaligned",],
            "Swarm": ["Unaligned",],
            "Undead": ["Lawful Evil", "Neutral Evil", "Chaotic Evil", "Unaligned",],
        }
        alignment_list = alignment[creature_type]
        return(random.choice(alignment_list).lower())

    # returns string
    def get_itemuser(self, creature_type):
        item_user = {
            "Aberration": ["no"],
            "Beast": ["no"],
            "Celestial": ["no", "yes"],
            "Construct": ["no","yes"],
            "Demon": ["no", "yes"],
            "Devil": ["no", "yes"],
            "Dragon": ["no"],
            "Elemental": ["no","yes"],
            "Fey": ["no"],
            "Giant": ["no", "yes"],
            "Humanoid": ["no","yes","yes","yes"],
            "Monstrosity": ["no"],
            "Ooze": ["no"],
            "Plant": ["no"],
            "Swarm": ["no"],
            "Undead": ["no", "yes"],
        }
        item_list = item_user[creature_type]
        return(random.choice(item_list))

    # returns dict with key as type of armor and value as AC
    def get_armor_class(self, itemuser, challengerating, strength, dexteritymod):
        if itemuser == "no":
            armor_class = 9 + max(1,challengerating // 3) + dexteritymod
            armor = {"natural armor": armor_class}
        if itemuser == "yes":
            if strength < 15 and dexteritymod < 3:
                if challengerating < 3:
                    armor = {"hide armor": 12 + min(dexteritymod, 2)}
                elif challengerating > 2 and challengerating < 5:
                    armor = {"chain shirt": 13 + min(dexteritymod, 2)}
                elif challengerating > 4 and challengerating < 8:
                    armor_names = ["scale mail", "breastplate"]
                    armor = {
                        random.choices(armor_names, weights=[4, 1]): 14
                        + min(dexteritymod, 2)
                    }
                else:
                    armor = {"half plate": 15 + min(dexteritymod, 2)}
            elif strength < 15 and dexteritymod > 2 and dexteritymod < 5:
                if challengerating < 3:
                    armor = {"padded armor": 11 + dexteritymod}
                elif challengerating > 2 and challengerating < 5:
                    armor = {"leather armor": 11 + dexteritymod}
                else:
                    armor = {"studded leather": 12 + dexteritymod}
            elif dexteritymod > 5:
                if challengerating < 3:
                    armor = {"padded armor": 11 + dexteritymod}
                elif challengerating > 2 and challengerating < 5:
                    armor = {"leather armor": 11 + dexteritymod}
                else:
                    armor = {"studded leather": 12 + dexteritymod}
            else:
                if strength < 14 and challengerating < 5:
                    armor = {"ring mail": 14}
                if strength < 15 and challengerating < 10:
                    armor = {"chain mail": 16}
                elif strength < 16 and challengerating < 12:
                    armor = {"splint": 17}
                else:
                    armor = {"plate": 18}
        return(armor)

creature_types = ["Aberration","Beast","Celestial","Construct","Dragon","Elemental","Fey","Demon","Devil","Giant","Humanoid","Monstrosity","Ooze","Plant","Swarm","Undead",]