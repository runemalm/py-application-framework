class Service:

    def run(self):
        """Run the service synchronously. Override this method in subclasses."""
        raise Exception("No sync() method has been implemented.")

    async def run_async(self):
        """Run the service asynchronously. Override this method in subclasses."""
        raise Exception("No async() method has been implemented.")
