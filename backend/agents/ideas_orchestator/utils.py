import os
import random
from cloud.cloud_constants import api_keys



def get_random_service_key():
        """Return (service, key) for one random API key."""
        # flatten into a list of (service, key)
        all_pairs = [(service, key) for service, keys in api_keys.items() for key in keys]
        if not all_pairs:
            raise ValueError("No API keys loaded.")
        api_key = random.choice(all_pairs)
        service, key = api_key

        if service == "groq":
            os.environ["GROQ_API_KEY"] = key
        if service == "sambanova":
            os.environ["SAMBANOVA_API_KEY"] = key
        if service == "cerebras":
            os.environ["CEREBRAS_API_KEY"] = key
        if service == "googleaistudio":
            os.environ["GOOGLE_API_KEY"] = key

        return api_key


