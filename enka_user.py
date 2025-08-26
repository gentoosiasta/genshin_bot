""" Módulo para extrawr información de enka"""
# import asyncio
from enkapy import Enka

client = Enka()

""" Gets the user's general information""" 
async def general_info(uid, update) -> None:
    try:
        await client.load_lang()
        user = await client.fetch_user(uid)
        message_text = f"Nickname: {user.player.nickname}\n"
        message_text += f"Level: {user.player.level}\n"
        message_text += f'Signature: {user.player.signature}\n'
        message_text += f'World level:{user.player.worldLevel}\n'
        message_text += f'Abyss: {user.player.towerFloorIndex}-{user.player.towerLevelIndex}\n'
        message_text += '**************\n'
        message_text += 'List of characters:\n'
        # fetch first character
        for character in user.characters:
            message_text += f'* Character: {character.name}'
            message_text += f' - Level: {character.level}\n'

        await update.message.reply_text(message_text)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
        print(f"Error: {e}")

async def character_info(uid, character_name, update) -> None:
    try:
        await client.load_lang()
        user = await client.fetch_user(uid)
        # message_text = f"Nickname: {user.player.nickname}\n"
        # message_text += f"Level: {user.player.level}\n"
        # message_text += f'Signature: {user.player.signature}\n'
        # message_text += f'World level:{user.player.worldLevel}\n'
        # message_text += f'Abyss: {user.player.towerFloorIndex}-{user.player.towerLevelIndex}\n'
        # message_text += '**************\n'
        # message_text += 'List of characters:\n'
        # # fetch first character
        # for character in user.characters:
        #     message_text += f'* Character: {character.name}'
        #     message_text += f' - Level: {character.level}\n'
        message_text = ''

        for character in user.characters:
            if character.name.lower() == character_name:
                message_text += f'Name: {character.name}\n'
                message_text += f'Ascension: {character.ascension}\n'
                message_text += f'Level: {character.level}\n'
                message_text += f'Exp: {character.experience}\n'
                # message_text += '=============\n'
                # message_text += 'Stats:\n'
                # message_text += f'\t\t\t{character.stats.hp} HP\n'
                # message_text += f'\t\t\t{character.stats.atk} ATK\n'
                # # message_text += f'\t\t\t{character.stats.d} DEF\n'
                # message_text += f'\t\t\t{character.stats.em} EM\n'
                # message_text += f'\t\t\t{character.stats.er} ER\n'
                # message_text += f'\t\t\t{character.stats.cr} CR\n'
                # message_text += f'\t\t\t{character.stats.cd} CD\n'
                message_text += '=============\n'
                message_text += 'Weapon:\n'
                weapon = character.weapon
                message_text += f'\t\t\tName: {weapon.name}\n'
                message_text += f'\t\t\tLevel: {weapon.level}\n'
                message_text += f'\t\t\tRefine: {weapon.refine}\n'
                message_text += f'\t\t\tStar level: {weapon.rank}\n'
                message_text += '=============\n'
                message_text += 'Constellations:\n'
                for constellation in character.constellations:
                    if constellation.activated:
                        message_text += f'\t\t\t{constellation.name} Activated\n'
                message_text += '=============\n'
                message_text += 'Skills:\n'
                for skill in character.skills:
                    if skill.type == 0:
                        message_text += f'\t\t\tNormal skill {skill.name}, level:{skill.level}\n'
                    elif skill.type == 1:
                        message_text += f'\t\t\tElemental skill {skill.name}, level:{skill.level}\n'
                    elif skill.type == 2:
                        message_text += f'\t\t\tElemental burst {skill.name}, level:{skill.level}\n'
                message_text += '=============\n'
                message_text += 'Artifacts:\n'
                for artifact in character.artifacts:
                    message_text += f'\t\t\t{artifact.set_name} {artifact.name}:\n'
                    message_text += f'\t\t\t{artifact.main_stat.prop}:{artifact.main_stat.value}\n'
                    for sub_stats in artifact.sub_stats:
                        message_text += f'\t\t\t\t\t\t{sub_stats.prop}:{sub_stats.value}\n'
        if message_text == '':
            message_text = f'No se encontró el personaje {character_name}\n'
        else:
            await update.message.reply_text(message_text)

    except IndexError:
        await update.message.reply_text(f"No se encontró el personaje {character_name}\n")
        print(f"No se encontró el personaje {character_name}\n")
