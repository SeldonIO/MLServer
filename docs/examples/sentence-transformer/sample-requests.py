import aiohttp
import asyncio
from time import perf_counter
from random import random

import requests
from time import perf_counter
# inference_request = {
#     "inputs": [
#       {
#           "name": "questions",
#           "datatype": "BYTES",
#           "parameters": {
#             "content_type": "str"
#           },
#           "shape": [2],
#           "data": ["Joanne", "Michael"]
#       }
#     ]
# }
# start_time = perf_counter()
# for i in range(50) :
#   print(f" start request {i}")
#   response = requests.post("http://localhost:8080/v2/models/sentence-transformer/infer", json=inference_request).json()
#   print(f" end request {i}")
# print(response)
# print(f"time taken is {perf_counter() - start_time}")

async def send_request(session):
    inference_request = {
    "inputs": [
        {
            "name": "questions",
            "datatype": "BYTES",
            "parameters": {
                "content_type": "str"
            },
            "shape": [5],
            "data": ["To sorry world an at do spoil along. Incommode he depending do frankness remainder to. Edward day almost active him friend thirty piqued. People as period twenty my extent as. Set was better abroad ham plenty secure had horse", 
                     "Be at miss or each good play home they. It leave taste mr in it fancy. She son lose does fond bred gave lady get. Sir her company conduct expense bed any. Sister depend change off piqued one. Contented continued any happiness instantly objection yet her allowance. Use correct day new brought tedious. By come this been in. Kept easy or sons my it done.",
                     "Attention he extremity unwilling on otherwise. Conviction up partiality as delightful is discovered. Yet jennings resolved disposed exertion you off. Left did fond drew fat head poor. So if he into shot half many long. China fully him every fat was world grave.",
                     "Do in laughter securing smallest sensible no mr hastened. As perhaps proceed in in brandon of limited unknown greatly. Distrusts fulfilled happiness unwilling as explained of difficult. No landlord of peculiar ladyship attended if contempt ecstatic. Loud wish made on is am as hard. Court so avoid in plate hence. Of received mr breeding concerns peculiar securing landlord. Spot to many it four bred soon well to. Or am promotion in no departure abilities. Whatever landlord yourself at by pleasure of children be.",
                     str(random()*1000000)]
        }
    ]
    }
    async with session.post("http://localhost:8080/v2/models/sentence-transformer/infer", json=inference_request) as response:
        return await response.json()

async def main():
    
    start_time = perf_counter()
    print(" start main process")
    # Create an aiohttp ClientSession
    async with aiohttp.ClientSession() as session:
        # Create a list of coroutines representing the concurrent requests
        tasks = [send_request(session) for _ in range(50)]

        # Gather the results from the completed requests
        results = await asyncio.gather(*tasks)
        import pickle
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"time taken is {perf_counter() - start_time}")

# Run the main function

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
