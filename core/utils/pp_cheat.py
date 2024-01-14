from playwright.async_api import async_playwright
from core.utils.pp_def import auth, get_fight, class_gender, catch_pokebol, check_place, shines, catches, fights, runners, healing


class DoneCheat(Exception):
    def __init__(self, text):
        self.txt = text


async def main(login, password, proxy, fight, item, item_val, catch, gender, pokebol, shine, f=0):
    async with async_playwright() as p:
        if fight == 'Отсутствует' or fight < 0:
            fight = 200
        elif fight > 1500:
            fight = 1500
        browser = await p.chromium.launch(headless=False, channel='chrome',
                                          executable_path='C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                                          args=['--window-size'], proxy={"server": "per-context"})
        context = await browser.new_context(viewport={'width': 1366, 'height': 668}, proxy={"server": f"{proxy}"})
        page = await context.new_page()
        await auth(browser, page, login, password)
        gender = await class_gender(gender)
        path = await catch_pokebol(pokebol)
        await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this);"]')
        p = await check_place(page)
        while True:
            if await page.is_visible('.BtnAuth'):
                await page.click('.BtnAuth')
                await page.click('//div[@class="Button NoActive" and @onclick="PP.fight.setHunt(this);"]')
            elif await page.is_visible('.Battle'):
                namepok, gendcat = await get_fight(page)
                f, p = await runners(page, namepok, f, p)
                f, p = await shines(page, shine, namepok, f, p)
                f, p = await catches(page, catch, namepok, gender, gendcat, path, f, p)
                f, pp, hp_bar = await fights(page, f)
                await healing(page, pp, hp_bar, p)
                if f >= fight:
                    raise DoneCheat('Программа окончила своё выполнение!')


async def close_page(page):
    await page.close()
