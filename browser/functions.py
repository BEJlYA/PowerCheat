import asyncio
from data import other


async def auth(browser, page, login, password):
    await page.goto('https://pokepower.ru', timeout=0)
    await page.type('#authLogin', login)
    await page.type('#authPassword', password)
    page.once("dialog", lambda dialog: incr(dialog, browser))
    await page.press('#authPassword', 'Enter')
    await page.click('.BtnAuth', timeout=0)


async def incr(dialog, browser):
    if dialog.message == 'Неверный пароль!' or dialog.message == 'Данный пользователь не найден!':
        await browser.close()


async def target(items, catch):
    targets = {}
    if 'Отсутствует' not in items and 'Отсутствует' in catch:
        itcat = items
    elif 'Отсутствует' in items and 'Отсутствует' not in catch:
        itcat = catch
    elif 'Отсутствует' in items and 'Отсутствует' in catch:
        itcat = ""
    else:
        itcat = items + ', ' + catch
    itcat = itcat.lower().split(', ')
    for o in itcat:
        if ':' in o:
            key, value = o.split(':')
            targets.update({' ' + key: int(value)})
        else:
            targets.update({' ' + o: int(100)})
    return targets


async def class_gender(gender):
    if gender.lower() in other.genderly:
        gender = other.genderly[gender.lower()]
        return gender
    else:
        gender = 'zero'
        return gender


async def catch_pokebol(pokeball):
    if pokeball.lower() in other.id_pokeballs:
        ball_path = f"{other.id_pokeballs[pokeball.lower()]}"
        return ball_path
    else:
        ball_path = "//img[@src='/img/world/items/small/3.png']"
        return ball_path


async def check_place(page):
    await page.click('//div[10]/div[2]/div[1]')
    await page.wait_for_selector('//*[@id="DivModal_Pokemons"]/div[2]/div[@class="PokemonBox"]')
    p = len(await page.locator('//*[@id="DivModal_Pokemons"]/div[2]/child::div[@class="PokemonBox"]').all())
    await page.click('//*[@id="DivModal_Pokemons"]/div[1]/div[2]/i')
    return p


async def create_rooms(page):
    class Room:
        def __init__(self, name):
            self.name = name
            self.exits = {}
            self.drop = None
            self.pokemons = None

        def add_exit(self, direction, room):
            self.exits[direction] = room

        def add_drop(self, item):
            self.drop = item

        def add_pokemon(self, pokemon):
            self.pokemons = pokemon

    location_me, maps, drop, habitat = await get_locate(page)
    with open(f'{maps}', 'r', encoding='cp1251') as map:
        locations = map.readlines()
    rooms = {}
    for location in locations:
        sort = location.strip().split(':')
        name = sort[0]
        if name not in rooms:
            room = Room(name)
            rooms[name] = room
        else:
            room = rooms[name]
        exits = [exit_room.strip() for exit_room in sort[1:]]
        for exit_room in exits:
            if exit_room in rooms:
                room.add_exit(exit_room, rooms[exit_room])
            else:
                new_room = Room(exit_room)
                rooms[exit_room] = new_room
                room.add_exit(exit_room, new_room)
    with open(f'{drop}', 'r', encoding='cp1251') as items_map:
        items_locations = items_map.readlines()
    for item_location in items_locations:
        item = item_location.strip().split(':')[:-1]
        location_name = item_location.strip().split(':')[-1]
        if location_name in rooms:
            rooms[location_name].add_drop(item)
    with open(f'{habitat}', 'r', encoding='cp1251') as pokemons_map:
        pokemons_locations = pokemons_map.readlines()
    for pokemon_location in pokemons_locations:
        pokemons = pokemon_location.strip().split(':')[:-1]
        location_name = pokemon_location.strip().split(':')[-1]
        if location_name in rooms:
            rooms[location_name].add_pokemon(pokemons)
    return rooms, location_me


async def get_path_targets(targets, rooms, location_me):
    for target_name, quantity in dict(sorted(targets.items(), key=lambda x: x[1])).items():
        for location_name, room in rooms.items():
            if room.drop is not None and target_name[1:] in str(room.drop).lower():
                shortest_path = await find_shortest_path(rooms[location_me], room)
                move_path = ([room.name for room in shortest_path])
                move_path.pop(0)
                return move_path
            elif room.pokemons is not None and target_name[1:] in str(room.pokemons).lower():
                shortest_path = await find_shortest_path(rooms[location_me], room)
                move_path = ([room.name for room in shortest_path])
                move_path.pop(0)
                return move_path
            else:
                return


async def move(page, move_path):
    for step in move_path:
        await page.locator(
            f'//div[@class="Name" and text()="Доступные переходы"]/following-sibling::div[@class="Steps"]/div[text()="{step}"]').click(
            timeout=0)


async def heal(page, rooms, location_me, p):
    if not await page.is_visible("//i[@class='fal fa-plus']"):
        await page.click('//div[@class="Button" and @onclick="PP.fight.setHunt(this,1);"]', timeout=0)
        shortest_path = await find_shortest_path(rooms[location_me], rooms['Покецентр'])
        move_path = ([room.name for room in shortest_path])
        move_path.pop(0)
        await move(page, move_path)
        if p >= 6:
            await page.locator("//i[@class='fal fa-plus']").click(timeout=0)
            await drop_pok(page)
        else:
            await page.locator("//i[@class='fal fa-plus']").click(timeout=0)
        move_path = ([room.name for room in shortest_path[::-1]])
        move_path.pop(0)
        await move(page, move_path)
        await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this,1);"]', timeout=0)
    else:
        if p >= 6:
            await page.click('//div[@class="Button" and @onclick="PP.fight.setHunt(this,1);"]', timeout=0)
            await page.locator("//i[@class='fal fa-plus']").click(timeout=0)
            await drop_pok(page)
            await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this,1);"]', timeout=0)
        else:
            await page.locator("//i[@class='fal fa-plus']").click(timeout=0)


async def get_fight(page):
    namepok = await page.locator('//*[@id="battleMap"]/div/div[4]/div[2]/div[2]/div[1]').text_content()
    gendcat = await page.locator('//*[@id="battleMap"]/div/div[4]/div[2]/div[2]/div[2]/i').get_attribute('class')
    return namepok, gendcat


async def runner_shine(page, namepok, f, p):
    await page.locator("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i").click()
    await page.wait_for_timeout(300)
    items = await page.locator("//div[@class='Step tlp-mini-target']/img").all()
    src = []
    for img in items:
        src.append(await img.get_attribute('src'))
    for key in sorted(other.priority, key=other.priority.get):
        if key in src:
            while True:
                if await page.is_visible(f'//div[@class="noty plus"]//span[contains(text(), "{namepok}")]') or\
                        not await page.is_visible('.Battle'):
                    p += 1
                    f += 1
                    return f, p
                elif await page.is_visible(f"//img[@src='{key}']"):
                    await page.locator(f"//img[@src='{key}']").click()
                elif not await page.is_visible(f"//img[@src='{key}']") and await page.is_visible(
                        "//div[@class='UseItemBattle']") or (await get_attr_heal(page))[1] < 40:
                    break
                else:
                    await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i")
                    await page.wait_for_timeout(200)


async def catch_gender(page, targets, namepok, path, f, p):
    while True:
        if await page.is_visible(f'//div[@class="noty plus"]//span[contains(text(), "{namepok}")]') or\
                not await page.is_visible('.Battle'):
            targets.update({namepok.lower()[4:]: int(targets.get(namepok.lower()[4:])) - 1})
            await drop(page, targets)
            p += 1
            f += 1
            return f, p
        elif await page.is_visible(path):
            await page.click(path)
        elif not await page.is_visible(path) and await page.is_visible("//div[@class='UseItemBattle']") or\
                (await get_attr_heal(page))[1] < 40:
            await check_exaut(page)
            return f, p
        else:
            await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i")
            await page.wait_for_timeout(200)


async def catch_all(page, targets, namepok, path, f, p):
    while True:
        if await page.is_visible(f'//div[@class="noty plus"]//span[contains(text(), "{namepok}")]') or\
                not await page.is_visible('.Battle'):
            targets.update({namepok.lower()[4:]: int(targets.get(namepok.lower()[4:])) - 1})
            await drop(page, targets)
            p += 1
            f += 1
            return f, p
        elif await page.is_visible(path):
            await page.click(path)
        elif not await page.is_visible(path) and await page.is_visible("//div[@class='UseItemBattle']") or \
                (await get_attr_heal(page))[1] < 40:
            await check_exaut(page)
            return f, p
        else:
            await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i")
            await page.wait_for_timeout(200)


async def fights(page, namepok, icon_type, type_chart, targets, f, pp=3, hp_bar=41):
    while True:
        if await page.is_visible('//*[@id="battleMap"]/div/div[2]/div[2]//img[@src="/img/load_pika.gif"]'):
            await page.wait_for_timeout(400)
        elif await page.is_visible(
                "//*[@id='battleMap']/div/div[3]/div[3]/div/div/div[2]/span[text()='Нет эффекта от атаки.']"
        ) and await page.is_visible('.Battle'):
            await check_exaut(page)
            return f, pp, hp_bar
        elif await page.is_visible("//*[@class='noty minipok']") or not await page.is_visible('.Battle'):
            await drop(page, targets)
            f += 1
            return f, pp, hp_bar
        else:
            pp, hp_bar = await get_attr_heal(page)
            types = await find_attack(page, icon_type)
            if types is None:
                await check_exaut(page)
                return f, pp, hp_bar
            types_pok = await find_types(namepok)
            max_type = await find_effectiveness(type_chart, types_pok, types)
            if await post_attack(page, max_type, icon_type):
                await page.wait_for_timeout(400)


async def get_attr_heal(page, pp=0):
    atc_pp = await page.locator(
        "//div[@class=' Move']//div[@class='Name MoveCategory1' or @class='Name MoveCategory2']/following::div[1]").all()
    hp_bar = await page.locator('//div[@class="PokemonA"]//div[@class="HpBar __hpW"]').get_attribute('style')
    for text_pp in atc_pp:
        intpp = await text_pp.text_content()
        pp += int(intpp[:intpp.rfind('/')])
    hp_bar = int(hp_bar[7:][:-2])
    return pp, hp_bar


async def find_attack(page, icon_type):
    types = []
    if await page.is_visible(
            "//div[@class='Name MoveCategory1' or @class='Name MoveCategory2']/parent::*/parent::div[@class=' Move']/img"):
        damaging = await page.locator(
            "//div[@class='Name MoveCategory1' or @class='Name MoveCategory2']/parent::*/parent::div[@class=' Move']/img").all()
        for attack in damaging:
            src = await attack.get_attribute('src')
            type_attack = icon_type.get(src)
            types.append(type_attack)
        return types
    else:
        return types


async def find_types(name):
    with open('data/types/pokemons.txt', 'r', encoding="cp1251") as pok_types:
        file_types = pok_types.readlines()
        for poke_type in file_types:
            types_pok = poke_type.strip().split(':')
            if name[5:].lower() in types_pok[0].lower():
                return types_pok[1:]


async def find_effectiveness(type_chart, types_pok, types):
    max_effectiveness = {}
    if len(types_pok) == 2:
        for a in types:
            for i in types_pok:
                e = type_chart.get(a, {}).get(i, 1)
                if a in max_effectiveness:
                    max_effectiveness[a] = (i, e * (max_effectiveness[a][1]))
                else:
                    max_effectiveness[a] = (i, e)
    else:
        for i in types_pok:
            for a in types:
                e = type_chart.get(a, {}).get(i, 1)
                if a in max_effectiveness:
                    if e > max_effectiveness[a][1]:
                        max_effectiveness[a] = (i, e)
                else:
                    max_effectiveness[a] = (i, e)
    max_type = max(max_effectiveness.items(), key=lambda x: x[1][1])
    return max_type[0]


async def post_attack(page, max_type, icon_type):
    rollback_attack = list(icon_type.keys())[list(icon_type.values()).index(max_type)]
    await page.click(
        f"//img[@src='{rollback_attack}']/following-sibling::*/child::div[@class='Name MoveCategory1' or @class='Name MoveCategory2']",
        timeout=0)
    return True


async def check_exaut(page):
    if await page.is_visible("//i[@class='fal fa-flag']"):
        page.once("dialog", lambda dialog: dialog.accept('ОК'))
        await page.wait_for_timeout(200)
        await page.click("//i[@class='fal fa-flag']")
        await page.click(
            "//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[5][@style='display: inline-block;' and @class='buttonFight Button']")
    elif await page.is_visible(
            "//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[5][@style='display: inline-block;' and @class='buttonFight Button']"):
        await page.click(
            "//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[5][@style='display: inline-block;' and @class='buttonFight Button']")


async def drop(page, targets):
    noty_items = await page.locator('//*[@class="noty plus"]/div[3]/child::div[@class="Step"]').all()
    for noty_i in noty_items:
        noty_i_text = await noty_i.text_content()
        try:
            if ' x' in noty_i_text:
                key, value = noty_i_text.lower().split(' x')
                targets.update({key: int(targets.get(key)) - int(value)})
            else:
                targets.update({noty_i_text.lower(): int(targets.get(noty_i_text.lower())) - 1})
        except TypeError:
            pass
    keys_to_remove = [key for key, value in targets.items() if value <= 0]
    for key in keys_to_remove:
        targets.pop(key)
    if ' ' not in targets and targets:
        rooms, location_me = await create_rooms(page)
        move_path = await get_path_targets(targets, rooms, location_me)
        if move_path is not None:
            await move(page, move_path)


async def drop_pok(page):
    await page.click('//div[10]/div[2]/div[1]')
    if await page.is_visible('//*[@id="DivModal_Pokemons"]'):
        pl = await page.locator('//*[@id="DivModal_Pokemons"]/div[2]/child::div[@class="PokemonBox"]').all()
        for pb in pl:
            if await pb.query_selector('//i[@class="fa fa-check Green-Color"]'):
                ball = await pb.query_selector('.Ball')
                await ball.click()
                await page.click('//html/body/div[17]/div[2]/div/div[10]/div/div[2]')
                await page.click('//*[@id="DivModal_Pokemons"]/div[1]/div[2]/i')
                return
        await page.click('.Ball')
        await page.click('//html/body/div[17]/div[2]/div/div[10]/div/div[2]')
        await page.click('//*[@id="DivModal_Pokemons"]/div[1]/div[2]/i')


async def get_locate(page):
    location_me = await page.locator("//div[@class='NameLoc']/div").text_content()
    region = (await page.locator("//div[@class='NameLoc']/div").get_attribute('class'))[:-3]
    if region == 'Name LocationRegionBg1':  # Kanto
        maps = 'data/maps/kanto.txt'
        drop = 'data/drop/kanto.txt'
        habitat = 'data/habitat/kanto.txt'
        return location_me, maps, drop, habitat
    elif region == 'Name LocationRegionBg2':  # Joto
        maps = 'data/maps/joto.txt'
        drop = 'data/drop/joto.txt'
        habitat = 'data/habitat/joto.txt'
        return location_me, maps, drop, habitat
    elif region == 'Name LocationRegionBg7':  # Kalos
        maps = 'data/maps/kalos.txt'
        drop = 'data/drop/kalos.txt'
        habitat = 'data/habitat/kalos.txt'
        return location_me, maps, drop, habitat
    elif region == 'Name LocationRegionBg9':  # Alola
        maps = 'data/maps/alola.txt'
        drop = 'data/drop/alola.txt'
        habitat = 'data/habitat/alola.txt'
        return location_me, maps, drop, habitat
    else:  # Other locations
        maps = 'data/maps/other.txt'
        drop = 'data/drop/other.txt'
        habitat = 'data/habitat/other.txt'
        return location_me, maps, drop, habitat


async def find_shortest_path(start_room, end_room):
    visited = set()
    queue = asyncio.Queue()
    await queue.put((start_room, [start_room]))
    while not queue.empty():
        current_room, path = await queue.get()
        if current_room == end_room:
            return path
        visited.add(current_room)

        for direction, room in current_room.exits.items():
            if room not in visited:
                await queue.put((room, path + [room]))
    return None
