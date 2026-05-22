import re

with open("tinker-atropos/tinker_atropos/trainer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add aiohttp import if not present
if "import aiohttp" not in content:
    content = content.replace("import requests", "import requests\nimport aiohttp")

# Replace _register_trainer
old_register = """    async def _register_trainer(self) -> str:
        \"\"\"Register this trainer with the Atropos API server.\"\"\"
        url = f"{self.atropos_api_url}/register"

        payload = {
            "wandb_project": self.config.wandb_project,
            "wandb_group": self.wandb_group,
            "batch_size": self.config.batch_size,
            "max_token_len": self.config.max_token_trainer_length,
            "starting_step": 0,
            "checkpoint_dir": self.config.checkpoint_dir,
            "save_checkpoint_interval": self.config.save_checkpoint_interval,
            "num_steps": self.num_steps,
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()

        result = response.json()
        return result.get("uuid")"""

new_register = """    async def _register_trainer(self) -> str:
        \"\"\"Register this trainer with the Atropos API server.\"\"\"
        url = f"{self.atropos_api_url}/register"

        payload = {
            "wandb_project": self.config.wandb_project,
            "wandb_group": self.wandb_group,
            "batch_size": self.config.batch_size,
            "max_token_len": self.config.max_token_trainer_length,
            "starting_step": 0,
            "checkpoint_dir": self.config.checkpoint_dir,
            "save_checkpoint_interval": self.config.save_checkpoint_interval,
            "num_steps": self.num_steps,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get("uuid")"""

if old_register in content:
    content = content.replace(old_register, new_register)
else:
    print("WARNING: Could not find old_register block")


# Replace get_batch
old_get_batch = """    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
    def get_batch(self):
        \"\"\"Fetch a batch of rollouts from Atropos API with retry logic.\"\"\"
        data = requests.get(f"{self.atropos_api_url}/batch", timeout=10).json()
        return data"""

new_get_batch = """    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
    async def get_batch(self):
        \"\"\"Fetch a batch of rollouts from Atropos API with retry logic.\"\"\"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.atropos_api_url}/batch", timeout=10) as response:
                response.raise_for_status()
                return await response.json()"""

if old_get_batch in content:
    content = content.replace(old_get_batch, new_get_batch)
else:
    print("WARNING: Could not find old_get_batch block")


# Replace get_data
old_get_data = """    def get_data(self) -> List[tinker.Datum]:
        \"\"\"
        Poll Atropos for a batch of rollouts and convert to Tinker Datums.
        Waits until a batch is available.
        \"\"\"
        import time
        import json

        while True:
            data = self.get_batch()

            if data.get("batch") is not None:
                with open("temp.json", "w", encoding="utf-8") as f:
                    json.dump(data, f)

                datums, group_mean_rewards = self.pad_data_to_good_offset(data)
                self.group_mean_rewards = group_mean_rewards
                return datums
            else:
                time.sleep(1)"""

new_get_data = """    async def get_data(self) -> List[tinker.Datum]:
        \"\"\"
        Poll Atropos for a batch of rollouts and convert to Tinker Datums.
        Waits until a batch is available.
        \"\"\"
        import asyncio
        import json

        while True:
            data = await self.get_batch()

            if data.get("batch") is not None:
                with open("temp.json", "w", encoding="utf-8") as f:
                    json.dump(data, f)

                datums, group_mean_rewards = self.pad_data_to_good_offset(data)
                self.group_mean_rewards = group_mean_rewards
                return datums
            else:
                await asyncio.sleep(1)"""

if old_get_data in content:
    content = content.replace(old_get_data, new_get_data)
else:
    print("WARNING: Could not find old_get_data block")


# Replace train_step get_data call
old_train_step_call = """        # Fetch batch from Atropos
        print("Fetching data from Atropos...")
        data = self.get_data()
        print(f"Got {len(data)} Datum objects")"""

new_train_step_call = """        # Fetch batch from Atropos
        print("Fetching data from Atropos...")
        data = await self.get_data()
        print(f"Got {len(data)} Datum objects")"""

if old_train_step_call in content:
    content = content.replace(old_train_step_call, new_train_step_call)
else:
    print("WARNING: Could not find old_train_step_call block")

with open("tinker-atropos/tinker_atropos/trainer.py", "w", encoding="utf-8") as f:
    f.write(content)
