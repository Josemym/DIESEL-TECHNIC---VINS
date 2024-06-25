import asyncio
import random
from time import perf_counter
import aiohttp
import pandas as pd
from app.services.dataframe import get_dataframe

URL_ROOT = 'https://partnerportal.dieseltechnic.com/api/search/partSearch'
HEADERS = {
    "Accept":"application/json",
    "content-type":"application/json",
    "Host":"partnerportal.dieseltechnic.com",
    "Origin":"https://partnerportal.dieseltechnic.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
}


semaphore = asyncio.Semaphore(10)


async def make_request(async_session: aiohttp.ClientSession, codart: str):
    # Semaphore for limiting concurrent requests to 8
    async with semaphore:
        # Asynchronous GET request
        data_json = {
            "countryID":"DE",
            "languageID":"es-ES",
            "searchTerm":codart,
            "token":""
            }
        async with async_session.post(url=URL_ROOT,json=data_json, headers = HEADERS, ssl=False) as response:            
            # avoid overpowering the URL right away by having this happen first
            content_product = ''  
            if response.status == 200:                               
                try:
                    content = await response.json()
                    content_product = content['products']
                except:
                    pass                
            await asyncio.sleep(random.randint(1,2)) 
            if len(content_product) > 0:
                for cross in content_product:
                    try:
                        result_cross = cross['crossReferences']    
                    except:
                        result_cross = ''
                        
                    # initializing K key 
                    K = "referenceNo"
                    
                    # creating a pandas dataframe from the list of dictionaries
                    df = pd.DataFrame(result_cross)
                    
                    # selecting the dictionaries with an empty string value in the K key
                    res = df[df[K] == codart].to_dict('records')
                    
                    # printing the result
                    if len(res) > 0:
                        get_dataframe(codart, cross['sku'], cross['name'])
                    else:
                        get_dataframe(codart,'-','-')
                    
            else:
                get_dataframe(codart,'-','-')
            
            #get_dataframe(list_codart,list_codfab,list_description)
            


async def makes_all_requests(urls: list[str]):
    # Stores all tasks that will later be used on `asyncio.gather`
    async with aiohttp.ClientSession() as async_session:
        tasks = []
        for codart in urls:
            # Creates asyncio.Task that will return a future
            task = asyncio.create_task(
                coro=make_request(
                    async_session=async_session,
                    codart=codart,
                )
            )

            tasks.append(task)

        # Tasks are ran with asyncio.gather
        # By setting `return_exceptions` to False, we will raise Exceptions within
        #   their asyncio task instance and everything will stop, by putting True, it
        #   will raise when `result()` is called on the future.
        await asyncio.gather(*tasks, return_exceptions=False)



