from browser.functions import *
from data.other import icon_type, type_chart
from playwright.async_api import async_playwright


class ExCheat(Exception):
    def __init__(self, text):
        self.txt = text


async def main(login, password, proxy, fight, items, catch, gender, pokebol, shine, state, f=0):
    async with async_playwright() as pw:
        if fight == 'Отсутствует' or fight < 0:
            fight = 200
        elif fight > 1500:
            fight = 1500
        browser = await pw.chromium.launch(headless=False, channel='chrome',
                                           executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                                           args=['--window-size'], proxy={"server": "per-context"})
        context = await browser.new_context(viewport={'width': 1366, 'height': 668}, proxy={"server": f"{proxy}"})
        page = await context.new_page()
        await state.update_data(p_browser=browser)
        await auth(browser, page, login, password)
        targets = await target(items, catch)
        gender = await class_gender(gender)
        path = await catch_pokebol(pokebol)
        await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this,1);"]')
        p = await check_place(page)
        while True:
            if await page.is_visible('.BtnAuth'):
                await page.click('.BtnAuth')
                await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this,1);"]')
            elif await page.is_visible('.Battle'):
                namepok, gendcat = await get_fight(page)
                if namepok in runners_list and await page.is_visible("//span[contains(text(),'Можно поймать')]"):
                    f, p = await runner_shine(page, namepok, f, p)  # Runner
                elif await page.is_visible(
                        "//div[@class='PokemonB']//div[@class='pok1-color namePokemon Name __name']") and await page.is_visible(
                        "//span[contains(text(),'Можно поймать')]") and shine == "Включено":
                    f, p = await runner_shine(page, namepok, f, p)  # Shine
                elif namepok.lower()[4:] in targets and gender == gendcat and await page.is_visible(
                        "//span[contains(text(),'Можно поймать')]") and p < 6:
                    f, p = await catch_gender(page, targets, namepok, path, f, p)
                elif namepok.lower()[4:] in targets and gender == 'zero' and await page.is_visible(
                        "//span[contains(text(),'Можно поймать')]") and p < 6:
                    f, p = await catch_all(page, targets, namepok, path, f, p)
                elif namepok not in runners_list or not await page.is_visible(
                        "//div[@class='PokemonB']//div[@class='pok1-color namePokemon Name __name']") and not await page.is_visible(
                        "//span[contains(text(),'Можно поймать')]") or not namepok.lower()[4:] in targets and not gender == gendcat or not namepok.lower()[4:] in targets and not gender == 'zero':
                    f, pp, hp_bar = await fights(page, namepok, icon_type, type_chart, targets, f)
                    p = await healing(page, pp, hp_bar, p)
                    if f >= fight or all(int(value) <= 0 for value in targets.values()):
                        raise ExCheat('Бот окончил своё выполнение!')
            elif not page.url == 'https://pokepower.ru/world':
                raise ExCheat('Произведен вход с другого устройства!')
