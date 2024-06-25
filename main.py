from time import perf_counter
from app.lists.list_vin import  list_vin
from app.lists.list_art import list_art
#from app.services.requests import makes_all_requests
from app.services.requests_dt import makes_all_requests
import asyncio



if __name__ == "__main__":
    urls = list_art

    print("---Starting---")

    start_time = perf_counter()

    asyncio.run(makes_all_requests(urls=urls))

    end_time = perf_counter()
    total_time = end_time - start_time
    print(f"\n---Finished in: {total_time:02f} seconds---")