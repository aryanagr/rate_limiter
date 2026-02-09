from enum import Enum
from abc import ABC, abstractmethod
from threading import Lock
from datetime import datetime
from time import sleep
from threading import Thread

class RateLimitStrategy(ABC):
    @abstractmethod
    def check_limit(self, api_key:str):
        pass



        

class  FixedWindowAlgo(RateLimitStrategy):
    def __init__(self, api_key:str, max_Request:int):
        self.request = {}
        self.max_request = max_Request
        self.thread = Thread(target=self.reset)
        self.thread.start()
       
        
    
    def check_limit(self, api_key:str):
        # with self.lock:
        current_time =datetime.now()
        if api_key not in self.request:
            self.request[api_key] = 1
            return True
        elif api_key in self.request:
            count = self.request[api_key]
            if(count>=self.max_request):
                return False
            else:
                self.request[api_key] = self.request[api_key] + 1
                return True

    def reset(self):
        self.request = {}
        sleep(20)
        self.reset()

class RateLimiter:
    def __init__(self):
        self.user_config = {}
    
    def set_rate_limit(self, api_key:str,max_Request:int):
        self.user_config[api_key]=FixedWindowAlgo(api_key,max_Request)
        return

    def handle_Request(self, api_key:str):
        if api_key not in self.user_config:
            print("api key not found")
            return False
        else:
            allowed = self.user_config[api_key].check_limit(api_key)
        if allowed:
            print("allowed for api key ", api_key)
        else:
            print("too many request for api key ", api_key)

rateLimiter = RateLimiter()
print("setting rate limit for user_123 to 5")
rateLimiter.set_rate_limit("user_123", 5)
rateLimiter.set_rate_limit("user_456", 1)
for i in range(1, 7):
    print("calling api for user_123")
    print("running request ", i)
    rateLimiter.handle_Request("user_123")
    rateLimiter.handle_Request("user_456")
    sleep(0.1)

sleep(20)
print("trying again after 1 min")
for i in range(1, 7):
    print("calling api for user_123")
    print("running request ", i)
    rateLimiter.handle_Request("user_123")
    rateLimiter.handle_Request("user_456")
    sleep(0.1)
