import asyncio
import aiohttp
from itertools import product

# 내가 접속한 브라우저 정보를 알려줌, 로봇이 아닌 사람이 접근했다고 알리는 기능
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

async def fetch_url(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            status_code = response.status
            if status_code == 200:  # 상태 코드가 200일 때만 출력
                print(f"URL: {url}, Status Code: {status_code}")
    except Exception as e:
        print(f"실패! URL: {url}, Exception: {str(e)}, Status Code: {status_code}")

async def main():
    years = ['2020', '2021', '2022', '2023']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    days = [str(i) for i in range(1, 32)]

    # 모든 조합 생성
    combinations = product(years, months, days)

    async with aiohttp.ClientSession() as session:
        tasks = []

        for year, month, day in combinations:
            url1 = f'https://www.who.int/publications/m/item/weekly-update-on-covid-19---{day}-{month}-{year}'
            url2 = f'https://www.who.int/publications/m/item/weekly-epidemiological-update---{day}-{month}-{year}'
            task1 = fetch_url(session, url1)
            tasks.append(task1)
            task2 = fetch_url(session, url2)
            tasks.append(task2)
        
        await asyncio.gather(*tasks)  # 비동기 작업을 병렬로 실행

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
