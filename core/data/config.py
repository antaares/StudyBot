from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  

ADMINS_ = env.list("ADMINS") 
ADMINS = [int(admin) for admin in ADMINS_] 

API_KEY = env.str("API_KEY")
