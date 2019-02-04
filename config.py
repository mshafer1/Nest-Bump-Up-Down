# to have the utilities just work on all thermostats in residence, set affect_all to true
affect_all = True

# if not using affect_all, provide the name of the thermostat - Example: 'Example Name (####)'
device_name = ''

# distance to move the target from the current temperature
step = 2

# if operating in dual mode, keep the heat and ac at least this far apart
gap = 4

# provide sanity boundaries for absolute max heat and min cool.
max = 80
min = 60

# see https://github.com/nestlabs/nest-python and https://developers.nest.com/guides/get-started 
#  for details on getting client_id and client_secret
client_id = '' 
client_secret = ''

access_token_cache_file = 'nest.json'
