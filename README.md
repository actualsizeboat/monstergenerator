# About 5e Monster Generator
This repo has the code for the 5e Monster Generator found at ionme.dev.

By comparing various values (HP, armor class, damage per round, number of traits, number of actions, etc.) of SRD monsters at different challenge ratings, a new monster can be procedurally created. In this readme, I will provide a brief overview of the generation process.

This tool is intended for advanced game masters - it might throw some wacky or unbalanced stuff at you. Don't entirely trust my challenge rating estimates. This software is provided without warranty. I am not responsible for any dismemberment, failed death saving throws, total party kills, or apocalyptic scenarios that may arise from using this software.

###### Legal Info
This work includes material taken from the System Reference Document 5.1 (“SRD 5.1”) by Wizards of the Coast LLC and available at https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License available at https://creativecommons.org/licenses/by/4.0/legalcode.

The web interface provided at ionme.dev for using this tool, and any other ionme.dev assets that are not part of this repository are the intellectual property of ionme.dev.

The python code included in this project (except where the above apply) is completely free for you to use.

# How it works

## Generating Attributes

1. The basic characteristics of the Monster are determined by the end user.
  - These basic characteristics are: challenge rating, creature type, and whether or not the creature has legendary actions.
  - Challenge rating supports integer values, and has been sanity tested up to challenge rating 25. Higher numbers shouldn't break the code, but you might see really weird stuff.

2. Based on the creature type, the Monster is assigned an archetype.
  - The list of archetypes follows: strength user, dexterity user, intelligence user, charisma user, wisdom user
  - Basically: Martial, martial, caster, caster, caster
  - For thematic reasons, certain creature types may only be generated with certain archetypes. For example, a Beast may be a strength user or a dexterity user; while a Monstrosity may be any archetype.
 
3. Based on the assigned archetype, an ability score array is generated.
  - This ability score array is influenced by the overall challenge rating, as well as the creature's type.

4. The Monster's size is determined.
  - For creatures that tend to have less variance in size (e.g. Humanoids, Celestials, Fey), the size is chosen from a weighted list of valid sizes.
  - For other creatures, size is taken as a function of challenge rating and creature type. For example, a low challenge rating Beast will be more likely to generate as Small or Medium while a higher challenge rating Beast will be more likely to generate as a larger size class.

5. The Monster's alignment is determined based on the creature type.
  - Examples: a Celestial will be any Good alignment; a Fey will be any non-lawful alignment; a Beast will be unaligned.

6. Based on the creature type, a value called "itemuser" is populated with either "yes" or "no".
- Examples: Beasts will never use weapons or armor, so itemuser will be "no". Humanoids are wildly diverse, with some using natural weapons (claws, bites, etc.) and others using manufactured weapons (swords, bows, so on).

7. The Monster's armor class is determined.
  - If the creature is not an item user, the armor class is based on target challenge rating.
  - If the creature is an item user, its ability scores are analyzed to determine the best piece of armor for it to wear.

8. The Monster's movement types and speed are determined.
  - This is based on creature type and size, and additional movement types (ex: fly, burrow) are weighted by challenge rating.

9. The Monster's element is determined.
  - This is largely important for Oozes, Elementals, and Dragons. This is mainly used to determine their damage types and resistances.

10. The Monster's languages are determined.
  - This is a function of the creature's intelligence and creature type.

11. The Monster's saving throws are determined.
  - Initial saves are based on archetype and creature type.
  - Additional saves are pulled at random from the remaining ability scores, as a function of challenge rating.

12. The Monster's proficient skills are determined based on its archetype.
  - The list of skills is arbitrarily small - effectively, it's only skills that I think may be useful in combat.

13. The Monster's senses are determined based on its creature type.

14. The Monster's resistances and vulnerabilities are determined based on its creature type and, when applicable, element.
  - Ex: Oozes are always immune to being knocked prone. Elementals are always immune to their element type.

## Generating Traits, Reactions, and Actions.
This is where stuff gets ~~complicated~~ fun.

15. The Monster's traits are generated.
  - The list of possible traits is pulled from all monsters in the SRD. Some traits that I felt were too specific have been left out, and some traits have had their text changed to be more "general".
  - For thematic reasons, some traits have been restricted by creature type. For example, a Beast will not generate with Limited Telepathy or Sense Magic.
  - For balance, traits have been arbitrarily assigned a value of High, Medium, or Low. At challenge rating 1, a Monster will have one trait chosen from the Low list. At challenge rating 20, a Monster will have the following: three Low traits, two Medium traits, one High trait.
  - Monsters will always have a minimum of one trait at challenge rating 1, and a maximum of 6 traits at challenge rating 20 (in addition to thematic creature-specific traits).
  - Creature types with thematic creature-specific traits (ex: Devil's Sight, Divine Awareness, Swarm) will get those in addition to the traits above.
  - Creature types with mechanical creature-specific traits (ex: Oozes, Elementals) will select from those lists before selecting from the Low, Medium, and High lists.
  - For balance purposes, item users above challenge rating 6 will always have one trait replaced with Brute or Magic Weapons.

16. The Monster may have a reaction generated.
  - For thematic reasons, Oozes above Large size will always have Split as a reaction.
  - Otherwise, a Monster has a 20% chance to have one of its Low traits replaced with a reaction.

17. The Monster's Actions are generated.
  - For thematic reasons, monster actions are split into many lists. Examples: magic attacks, weapon attacks, natural attacks, utility, magic utility, etc.
  - Monsters will always have a minimum of one action at challenge rating 1, and a maximum of 6 actions at challenge rating 20 (in addition to thematic creature-specific actions).
  - Casters may roll with an additional action in the form of a simple weapon or a natural weapon.
  - Attack actions are generated first. This means that lower challenge rating Monsters may or may not have additional actions.
  - Attack action generation is based on the following: item user, size (for non item users), archetype, creature type.
  - After attack actions are generated, additional actions are generated. Action lists are made available based on the Monster's archetype, creature type, and whether or not it uses items.
  - Natural attacks determine the amount of dice (example: Xd6) based on the Monster's challenge rating.
  - Natural attacks determine the type of dice (example: 6dX) based on the Monster's size, and may randomly be stepped up or down by one size class.
  - Weapon attacks do not scale by size because that's not part of the 5e SRD. A giant may roll with a 1d4 dagger.
  - Some actions with a DC are determined by the Monster's main ability score.
  - Most actions with a DC are determined as above, but lowered by 2.
  - If the Monster is in one of the martial archetypes and has multiple attack actions, Multiattack is added to the top of the Monster's action list.
  - This is only a surface-level view of action generation. The actual code handles many thematic cases.

## Generating Hit Points

18. Hit points are generated based on the creature's Constitution modifier, archetype, and movement.
  - To avoid assigning and rolling hit dice, the actual hit point generation is arbitrary. It seems to mostly check out based on comparisons to SRD monsters.
  - Casters and Monsters with fly speeds have their hit points arbitrarily lowered to adjust for difficulty in hitting the monsters or tanking the damage per round.

## Generating Legendary Actions

19. If Legendary Actions are selected at the time of Monster generation, three Legendary Actions will be generated.
  - The first Legendary Action will always be a one-cost Legendary Action.
  - Good-alignment creatures and evil-alignment creatures each have on additional Legendary Action available to select from.
  - Due to the way Actions are generated, low challenge rating monsters may generate the Legendary Action "Use Non-Attack Action" without any non-attack actions to choose from.

## After Generation

As the monster is generated, python class attributes for its instance are populated with all of the characteristics described above. Each function in the generation code is documented with the type of data that will be returned.

