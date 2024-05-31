from data import other
from browser import functions
from playwright.async_api import async_playwright


class ExCheat(Exception):
    def __init__(self, text):
        self.txt = text


async def main(login, password, proxy, fight, items, catch, gender, pokeball, shine, state, f=0):
    async with async_playwright() as pw:
        if fight == 'Отсутствует' or fight < 0:
            fight = 200
        elif fight > 1500:
            fight = 1500
        browser = await pw.chromium.launch(headless=False, channel='chrome',
                                           executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                                           args=['--window-size'])
        context = await browser.new_context(viewport={'width': 1366, 'height': 668})
        page = await context.new_page()
        await state.update_data(p_browser=browser)
        await functions.auth(browser, page, login, password)
        targets = await functions.target(items, catch)
        gender = await functions.class_gender(gender)
        pokeball_path = await functions.catch_pokebol(pokeball)
        p = await functions.check_place(page)
        if ' ' not in targets and not await page.is_visible('.Battle'):
            rooms, location_me = await functions.create_rooms(page)
            move_path = await functions.get_path_targets(targets, rooms, location_me)
            if move_path is not None:
                await functions.move(page, move_path)
        await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this,1);"]')
        while True:
            if await page.is_visible('.BtnAuth'):
                await page.click('.BtnAuth')
                await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this,1);"]')
            elif await page.is_visible('.Battle'):
                namepok, gendcat = await functions.get_fight(page)
                if namepok in other.runners_list and await page.is_visible("//span[contains(text(),'Можно поймать')]"):
                    f, p = await functions.runner_shine(page, namepok, f, p)  # Catches runners
                elif await page.is_visible(
                        "//div[@class='PokemonB']//div[@class='pok1-color namePokemon Name __name']") and await page.is_visible(
                        "//span[contains(text(),'Можно поймать')]") and shine == "Включено":
                    f, p = await functions.runner_shine(page, namepok, f, p)  # Catches shines
                elif namepok.lower()[4:] in targets and gender == gendcat and await page.is_visible(
                        "//span[contains(text(),'Можно поймать')]") and p < 6:
                    f, p = await functions.catch_gender(page, targets, namepok, pokeball_path, f, p)  # Catches one select gender pokemons
                elif namepok.lower()[4:] in targets and gender == 'zero' and await page.is_visible(
                        "//span[contains(text(),'Можно поймать')]") and p < 6:
                    f, p = await functions.catch_all(page, targets, namepok, pokeball_path, f, p)  # Catches all genders pokemons
                elif namepok not in other.runners_list or not await page.is_visible(
                        "//div[@class='PokemonB']//div[@class='pok1-color namePokemon Name __name']") and not await page.is_visible(
                        "//span[contains(text(),'Можно поймать')]") or not namepok.lower()[4:] in targets and not gender == gendcat or not namepok.lower()[4:] in targets and not gender == 'zero':
                    f, pp, hp_bar = await functions.fights(page, namepok, other.icon_type, other.type_chart, targets, f)
                    if pp <= 3 or hp_bar <= 40 or p >= 6:
                        rooms, location_me = await functions.create_rooms(page)
                        await functions.heal(page, rooms, location_me, p)
                    if f >= fight or all(int(value) <= 0 for value in targets.values()):
                        raise ExCheat('Бот окончил своё выполнение!')
            elif not page.url == 'https://pokepower.ru/world':
                raise ExCheat('Произведен вход с другого устройства!')
            elif 'https://pokepower.ru/world?ver=' in page.url:
                raise ExCheat('Игра была обновлена!')
