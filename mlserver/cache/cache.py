class ResponseCache:
    async def insert(self, key: str, value: str):
        """
        Method responsible for inserting value to cache.


        **This method should be overriden to implement your custom cache logic.**
        """
        raise NotImplementedError("insert() method not implemented")

    async def lookup(self, key: str) -> str:
        """
        Method responsible for returning key value in the cache.


        **This method should be overriden to implement your custom cache logic.**
        """
        raise NotImplementedError("lookup() method not implemented")
