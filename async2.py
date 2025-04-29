import aiohttp
import asyncio

services = {
    "ipify": "https://api.ipify.org",
    "ip-api": "http://ip-api.com/ip",
}

async def fetch_ip(session, name, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                ip = await response.text()
                return name, ip.strip()
    except Exception as e:
        return name, None

async def get_ip():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_ip(session, name, url) for name, url in services.items()]
        for task in asyncio.as_completed(tasks):
            result = await task
            if result[1] is not None:
                return result
    return None, None

def main():
    ip_service, ip_address = asyncio.run(get_ip())
    if ip_address:
        print(f"Ваш IP-адрес: {ip_address} (Сервис: {ip_service})")
    else:
        print("Не удалось получить IP-адрес.")

if __name__ == "__main__":
    main()
