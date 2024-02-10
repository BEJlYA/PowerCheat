from data.other import *
from queue import Queue


async def auth(browser, page, login, password):
    await page.goto('https://pokepower.ru', timeout=0)
    await page.click('.Auth')
    await page.type('#authLogin', login)
    await page.type('#authPassword', password)
    page.once("dialog", lambda dialog: incr(dialog, browser))
    await page.press('#authPassword', 'Enter')
    await page.click('.BtnAuth')


async def incr(dialog, browser):
    if dialog.message == 'Неверный пароль!' or dialog.message == 'Данный пользователь не найден!':
        await browser.close()


async def target(items):
    target_item = {}
    if not items == 'Отсутствует':
        item = items.lower().split(', ')
        for i in item:
            key, value = i.split(':')
            target_item.update({' ' + key: int(value)})
        return target_item
    else:
        return target_item


async def class_gender(gender):
    if gender.lower() in genderly:
        gender = genderly[gender.lower()]
        return gender
    else:
        gender = 'zero'
        return gender


async def catch_pokebol(pokebol):
    if pokebol.lower() in id_pokebols:
        path = f"{id_pokebols[pokebol.lower()]}"
        return path
    else:
        path = "//img[@src='/img/world/items/small/3.png']"
        return path


async def check_place(page):
    await page.click('//div[10]/div[2]/div[1]')
    await page.wait_for_selector('//*[@id="DivModal_Pokemons"]')
    if await page.is_visible('//*[@id="DivModal_Pokemons"]'):
        p = len(await page.query_selector_all('//*[@id="DivModal_Pokemons"]/div[2]/child::div[@class="PokemonBox"]'))
        await page.click('//*[@id="DivModal_Pokemons"]/div[1]/div[2]/i')
        return p


async def get_fight(page):
    namepok = await page.locator('//*[@id="battleMap"]/div/div[4]/div[2]/div[2]/div[1]').text_content()
    gendcat = await page.locator('//*[@id="battleMap"]/div/div[4]/div[2]/div[2]/div[2]/i').get_attribute('class')
    return namepok, gendcat


async def runners(page, namepok, f, p):
    if namepok in runners_list and await page.is_visible("//span[contains(text(),'Можно поймать')]"):
        p = await check_pokebol(page, namepok, p)
        f += 1
        return f, p
    else:
        return f, p


async def shines(page, shine, namepok, f, p):
    if await page.is_visible(
            "//*[@id='battleMap']/div/div[4]/div[1]/div[@class='pok1-color namePokemon Name __name']") and await page.is_visible("//span[contains(text(),'Можно поймать')]") and shine == "Включено":
        p = await check_pokebol(page, namepok, p)
        f += 1
        return f, p
    else:
        return f, p


async def check_pokebol(page, namepok, p):
    await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i")
    items = await page.query_selector_all("//div[@class='Step tlp-mini-target']/img")
    src = []
    for img in items:
        src.append(await img.get_attribute('src'))
    for key in sorted(priority, key=priority.get):
        if key in src:
            if await page.is_visible('.Battle'):
                while not await page.is_visible(f'//*[@class="noty plus"]/div[3]/div[1]/span[@class="pok1-color" and contains(text(),"{namepok}")] or @class="pok0-color" and contains(text(),"{namepok}")]') and await page.is_visible('.Battle'):
                    if await page.is_visible(f"//img[@src='{key}']"):
                        await page.click(f"//img[@src='{key}']")
                    else:
                        await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i")
                        await check_exaut(page)
                p += 1
                return p
            else:
                break
    return p


async def catches(page, catch, namepok, gender, gendcat, path, f, p):
    if namepok.lower()[5:] in catch.lower() and gender == gendcat and await page.is_visible("//span[contains(text(),'Можно поймать')]"):
        while not await page.is_visible(f'//*[@class="noty plus"]/div[3]/div[1]/span[@class="pok0-color" and contains(text(),"{namepok}")]') and await page.is_visible('.Battle'):
            if await page.is_visible(path):
                await page.click(path)
            else:
                await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i")
                await check_exaut(page)
        p += 1
        f += 1
        return f, p
    elif namepok.lower()[5:] in catch.lower() and gender == 'zero' and await page.is_visible("//span[contains(text(),'Можно поймать')]"):
        while not await page.is_visible(f'//*[@class="noty plus"]/div[3]/div[1]/span[@class="pok0-color" and contains(text(),"{namepok}")]') and await page.is_visible('.Battle'):
            if await page.is_visible(path):
                await page.click(path)
            else:
                await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[2]/i")
                await check_exaut(page)
        p += 1
        f += 1
        return f, p
    else:
        return f, p


async def fights(page, target_item, f, pp=2, hp_bar=41):
    if await page.is_visible('.Battle'):
        while not await page.is_visible("//*[@class='noty minipok']"):
            if await page.is_visible("//div[@class=' Move']//div[@class='Name MoveCategory1' or @class='Name MoveCategory2']"):
                pp, hp_bar = await get_attr_heal(page)
                await page.click(
                    "//div[@class=' Move']//div[@class='Name MoveCategory1' or @class='Name MoveCategory2']")
            elif await page.is_visible("//div[@class='MoveBox']/child::div"):
                page.once("dialog", lambda dialog: dialog.accept('ОК'))
                await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[4]")
                await check_exaut(page)
                return f, pp, hp_bar
        await drop(page, target_item)
        f += 1
        return f, pp, hp_bar
    else:
        return f, pp, hp_bar


async def get_attr_heal(page, pp=0):
    atc_pp = await page.query_selector_all(
        "//div[@class=' Move']//div[@class='Name MoveCategory1' or @class='Name MoveCategory2']/following::div[1]")
    hp_bar = await page.locator('//*[@id="battleMap"]/div/div[2]/div[1]/div[9]/div[1]/div[2]').get_attribute('style')
    for text_pp in atc_pp:
        intpp = await text_pp.text_content()
        pp += int(intpp[:intpp.rfind('/')])
    hp_bar = int(hp_bar[7:][:-2])
    return pp, hp_bar


async def check_exaut(page):
    if await page.is_visible("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[5][@style='display: inline-block;']"):
        await page.click("//*[@id='battleMap']/div/div[4]/div[3]/div[3]/div[5][@style='display: inline-block;']")


async def drop(page, target_item):
    if not len(target_item) == 0:
        noty_items = await page.query_selector_all('//*[@class="noty plus"]/div[3]/child::div[@class="Step"]')
        for noty_i in noty_items:
            noty_i_text = await noty_i.text_content()
            if ' x' in noty_i_text:
                key, value = noty_i_text.lower().split(' x')
                target_item.update({key: int(target_item.get(key)) - int(value)})
            else:
                try:
                    target_item.update({noty_i_text: int(target_item.get(noty_i_text)) - 1})
                except TypeError:
                    pass


async def healing(page, pp, hp_bar, p):
    if pp <= 1 or hp_bar <= 40 or p >= 6:
        if not await page.is_visible("//*[@id='window_games']/div/div[3]/div[3]/div[1]/i[@class='fal fa-plus']"):
            await page.click('//div[@class="Button" and @onclick="PP.fight.setHunt(this);"]')
            location_me, region = await get_locate(page)

            class Room:
                def __init__(self, name):
                    self.name = name
                    self.exits = {}

                def add_exit(self, direction, room):
                    self.exits[direction] = room

            with open(f'{region}', 'r', encoding='cp1251') as map:
                locations = map.readlines()
            rooms = {}
            for location in locations:
                sort = location.strip().strip("'").strip(',').strip("',").replace(' : ', ':').replace(': ', ':').split(':')
                name = sort[0].strip()
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

            start_room = rooms[f'{location_me}']
            end_room = rooms['Покецентр']

            shortest_path = find_shortest_path(start_room, end_room)

            n_heal = [room.name for room in shortest_path]
            n_heal.pop(0)
            b_heal = [room.name for room in shortest_path[::-1]]
            b_heal.pop(0)
            for n_step in n_heal:
                n_quits = await page.query_selector_all("//*[@id='window_games']/div/div[2]/div[2]/div")
                for n_quit in n_quits:
                    if await n_quit.text_content() == n_step:
                        await n_quit.click(timeout=0)
                if await page.is_visible("//*[@id='window_games']/div/div[3]/div[3]/div[1]/i[@class='fal fa-plus']") and p >= 6:
                    await drop_pok(page)
                    await page.click("//*[@id='window_games']/div/div[3]/div[3]/div[1]/i[@class='fal fa-plus']", timeout=0)
                    for b_step in b_heal:
                        b_quits = await page.query_selector_all("//*[@id='window_games']/div/div[2]/div[2]/div")
                        for b_quit in b_quits:
                            if await b_quit.text_content() == b_step:
                                await b_quit.click(timeout=0)
                    await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this);"]')
                elif await page.is_visible("//*[@id='window_games']/div/div[3]/div[3]/div[1]/i[@class='fal fa-plus']"):
                    await page.click("//*[@id='window_games']/div/div[3]/div[3]/div[1]/i[@class='fal fa-plus']", timeout=0)
                    for b_step in b_heal:
                        b_quits = await page.query_selector_all("//*[@id='window_games']/div/div[2]/div[2]/div")
                        for b_quit in b_quits:
                            if await b_quit.text_content() == b_step:
                                await b_quit.click(timeout=0)
                    await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this);"]')
        else:
            await page.click("//*[@id='window_games']/div/div[3]/div[3]/div[1]/i[@class='fal fa-plus']", timeout=0)


async def drop_pok(page):
    await page.click('//div[10]/div[2]/div[1]')
    if await page.is_visible('//*[@id="DivModal_Pokemons"]'):
        pl = await page.query_selector_all('//*[@id="DivModal_Pokemons"]/div[2]/child::div[@class="PokemonBox"]')
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
    if not await page.is_visible('.Battle'):
        if await page.is_visible("//*[@id='window_games']/div/div[1]/div/div[3]/div"):
            location_me = await page.locator("//*[@id='window_games']/div/div[1]/div/div[3]/div").text_content()
            region = await page.locator("//*[@id='window_games']/div/div[1]/div/div[3]/div").get_attribute('class')
        else:
            location_me = await page.locator("//*[@id='window_games']/div/div[1]/div/div[2]/div").text_content()
            region = await page.locator("//*[@id='window_games']/div/div[1]/div/div[2]/div").get_attribute('class')
        region = region[:-3]
        if region == 'Name LocationRegionBg1':  # Канто
            region = 'data/map_kanto.txt'
            return location_me, region
        elif region == 'Name LocationRegionBg2':  # Джото
            region = 'data/map_joto.txt'
            return location_me, region
        elif region == 'Name LocationRegionBg7':  # Калос
            region = 'data/map_kalos.txt'
            return location_me, region
        elif region == 'Name LocationRegionBg9':  # Алола
            region = 'data/map_alola.txt'  # алола
            return location_me, region
        else:  # Прочие локи с покецентром
            region = 'core/data/map_other.txt'
            return location_me, region
    else:
        location_me = 'Паллет'
        region = 'data/map_kalos.txt'
        return location_me, region


def find_shortest_path(start_room, end_room):
    visited = set()
    queue = Queue()
    queue.put((start_room, [start_room]))
    while not queue.empty():
        current_room, path = queue.get()
        if current_room == end_room:
            return path
        visited.add(current_room)

        for direction, room in current_room.exits.items():
            if room not in visited:
                queue.put((room, path + [room]))
    return None