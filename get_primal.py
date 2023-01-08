import asyncio
import aiohttp

from re import findall
from imbox import Imbox
from web3.auto import w3
from loguru import logger
from aiohttp import ClientSession
from random import choice, randint
from string import ascii_lowercase


HEADERS = {
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5cmp5Y29jdmx1b2NkZ2xpeXZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njc0MDY3NzksImV4cCI6MTk4Mjk4Mjc3OX0.SLAgTxtgawJoxTXXtxfI85Q3Xz-ecBI9XkjZyKvl794',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5cmp5Y29jdmx1b2NkZ2xpeXZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njc0MDY3NzksImV4cCI6MTk4Mjk4Mjc3OX0.SLAgTxtgawJoxTXXtxfI85Q3Xz-ecBI9XkjZyKvl794'}


async def get_imap(provider: str, login: str, password: str):
    return Imbox(
        provider,
        username=login,
        password=password,
        ssl=True,
        ssl_context=None,
        starttls=None)


async def get_code_email(email: str, password: str):
    imbox = await get_imap('imap.rambler.ru', email, password)
    return await recv_message(imbox, 0, 'Inbox')


async def recv_message(imbox: Imbox, count: int, folder: str):
    for _, message in imbox.messages(folder=folder)[::-1]:
        if message.sent_from[0]["email"] == "noreply@m1.getprimal.com":
            return findall(r"\d{6}", message.body["plain"][0])[0]
    while count < 60:
        count += 1
        await asyncio.sleep(1)
        return await recv_message(imbox, count, folder)
    while count < 65:
        count += 1
        await asyncio.sleep(1)
        return await recv_message(imbox, count, 'Spam')
    raise Exception()


async def send_email(client: ClientSession, email: str, captcha: str):
    try:
        response = await client.post('https://byrjycocvluocdgliyvg.supabase.co/auth/v1/otp',
                                     json={
                                         "email": email,
                                         "data": {},
                                         "create_user": True,
                                         "gotrue_meta_security": {'captcha_token': captcha}
                                     })
        data = await response.text()
        if data != "{}":
            logger.error(data)
            raise Exception()
    except:
        raise Exception()


async def verify(client: ClientSession, email: str, code: str):
    try:
        response = await client.post('https://byrjycocvluocdgliyvg.supabase.co/auth/v1/verify',
                                     json={
                                         "email": email,
                                         "token": code,
                                         "type": "signup",
                                         "gotrue_meta_security": {}
                                     })
        access_token = (await response.json())['access_token']
        return access_token
    except:
        raise Exception()


async def add_referral(client: ClientSession, access_token: str):
    try:
        await client.post('https://byrjycocvluocdgliyvg.supabase.co/rest/v1/rpc/set_referred_by',
                          json={
                              "code": ref
                          })
    except:
        raise Exception()


async def set_username(client: ClientSession, access_token: str):
    try:
        username = ''.join([choice(ascii_lowercase)
                            for _ in range(randint(7, 14))])
        await client.post('https://byrjycocvluocdgliyvg.supabase.co/rest/v1/rpc/set_username',
                          json={
                              "username": username
                          })
    except:
        raise Exception()


async def set_wallet(client: ClientSession, access_token: str, address: str):
    try:
        await client.post('https://byrjycocvluocdgliyvg.supabase.co/rest/v1/rpc/set_wallet',
                          json={
                              "eth_address": address
                          })
    except:
        raise Exception()


async def sending_captcha(client: ClientSession):
    try:
        response = await client.get(f'http://185.189.167.221:3005/in.php?userkey={user_key}&host=https://byrjycocvluocdgliyvg.supabase.co/auth/v1/otp&sitekey=c4344dc0-0182-431f-903c-d8f53065d81d')
        data = await response.text()
        if 'ERROR' in data:
            return(await sending_captcha(client))
        id = data[3:]
        return(await solving_captcha(client, id))
    except:
        raise Exception()


async def solving_captcha(client: ClientSession, id: str):
    for i in range(100):
        try:
            response = await client.get(f'http://185.189.167.221:3005/res.php?userkey={user_key}&id={id}')
            data = await response.text()
            if 'ERROR' in data:
                logger.error(print(data))
                raise Exception()
            elif 'OK' in data:
                return(data[3:])
            return(await solving_captcha(client, id))
        except:
            raise Exception()
    raise Exception()


def create_wallet():
    account = w3.eth.account.create()
    return(str(account.address), str(account.privateKey.hex()))


async def worker(q: asyncio.Queue):
    while True:
        try:
            async with aiohttp.ClientSession(
                headers=HEADERS
            ) as client:

                emails = await q.get()
                email, password = emails.split(":")

                address, private_key = create_wallet()

                logger.info('Solving captcha')
                captcha = await sending_captcha(client)

                logger.info('Send email')
                await send_email(client, email.lower(), captcha)

                logger.info('Get code email')
                code = await get_code_email(email, password)

                logger.info('Verify')
                access_token = await verify(client, email, code)

                client.headers.update({
                    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ5cmp5Y29jdmx1b2NkZ2xpeXZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njc0MDY3NzksImV4cCI6MTk4Mjk4Mjc3OX0.SLAgTxtgawJoxTXXtxfI85Q3Xz-ecBI9XkjZyKvl794',
                    'authorization': 'Bearer ' + access_token
                })

                logger.info('Add referral')
                await add_referral(client, access_token)

                logger.info('Add username')
                await set_username(client, access_token)

                logger.info('Add wallet')
                await set_wallet(client, access_token, address)

        except Exception:
            logger.error("Error\n")
            with open('error.txt', 'a', encoding='utf-8') as f:
                f.write(f'{email}:{password}\n')
        else:
            with open('register.txt', 'a', encoding='utf-8') as file:
                file.write(f'{email}:{password}:{address}:{private_key}\n')
            logger.success('Successfully\n')

        await asyncio.sleep(delay)


async def main():
    emails = open("emails.txt", "r+").read().strip().split("\n")

    q = asyncio.Queue()

    for account in list(emails):
        q.put_nowait(account)

    tasks = [asyncio.create_task(worker(q)) for _ in range(threads)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print("Bot Primal @flamingoat\n")

    user_key = input('Captcha key: ')
    ref = input('Referral code: ')
    delay = int(input('Delay(sec): '))
    threads = int(input('Threads: '))

    asyncio.run(main())