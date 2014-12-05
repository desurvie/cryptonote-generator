import fileinput
import sys
import re
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--config', action='store', dest='config_file',
                    default='config.json',
                    help='Configuration filename. Format: json'
                    )
parser.add_argument('--source', action='store', dest='source',
					default='tmp',
                    help='Working folder containing the base coin source'
                    )
args = parser.parse_args()

json_data=open(args.config_file)
config = json.load(json_data)
json_data.close()

paths = {}

# Make changes in src/CMakeLists.txt
paths['CMakeLists'] = args.source + "/src/CMakeLists.txt"

daemon_name_re = re.compile(r"(set_property\(TARGET daemon PROPERTY OUTPUT_NAME) \"\S+\"\)", re.IGNORECASE)
for line in fileinput.input([paths['CMakeLists']], inplace=True):
	line = daemon_name_re.sub("\\1 \"%s\")" % config['core']['daemon_name'], line)
	# sys.stdout is redirected to the file
	sys.stdout.write(line)


# Make changes in src/cryptonote_config.h
paths['cryptonote_config'] = args.source + "/src/cryptonote_config.h"

CRYPTONOTE_NAME_re = re.compile(r"(const char\s+CRYPTONOTE_NAME\[\]\s+=)\s+\"\w+\"", re.IGNORECASE)
P2P_DEFAULT_PORT_re = re.compile(r"(const int\s+P2P_DEFAULT_PORT\s+=)\s+\d+", re.IGNORECASE)
RPC_DEFAULT_PORT_re = re.compile(r"(const int\s+RPC_DEFAULT_PORT\s+=)\s+\d+", re.IGNORECASE)
P2P_STAT_TRUSTED_PUB_KEY_re = re.compile(r"(const char\s+P2P_STAT_TRUSTED_PUB_KEY\[\]\s+=)\s+\"\w+\"", re.IGNORECASE)
CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX_re = re.compile(r"(const uint64_t\s+CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX\s+=)\s+\d+", re.IGNORECASE)
UPGRADE_HEIGHT_re = re.compile(r"(const uint64_t\s+UPGRADE_HEIGHT\s+=)\s+\d+", re.IGNORECASE)
if 'MONEY_SUPPLY' in config['core']:
	MONEY_SUPPLY_re = re.compile(r"(const uint64_t MONEY_SUPPLY\s+=)\s+[^;]+", re.IGNORECASE)
if 'EMISSION_SPEED_FACTOR' in config['core']:
	EMISSION_SPEED_FACTOR_re =re.compile(r"(const unsigned EMISSION_SPEED_FACTOR\s+=)\s+\d+", re.IGNORECASE)
if 'DIFFICULTY_TARGET' in config['core']:
	DIFFICULTY_TARGET_re = re.compile(r"(const uint64_t DIFFICULTY_TARGET\s+=)\s+\d+", re.IGNORECASE)
if 'COIN' in config['core']:
	COIN_re = re.compile(r"(const uint64_t COIN\s+=\s+UINT64_C\()\d+\)", re.IGNORECASE)
if 'CRYPTONOTE_DISPLAY_DECIMAL_POINT' in config['core']:
	CRYPTONOTE_DISPLAY_DECIMAL_POINT_re = re.compile(r"(const size_t\s+CRYPTONOTE_DISPLAY_DECIMAL_POINT\s+=)\s+\d+", re.IGNORECASE)
if 'MINIMUM_FEE' in config['core']:
	MINIMUM_FEE_re = re.compile(r"(const uint64_t MINIMUM_FEE\s+=\s+UINT64_C\()\d+\)", re.IGNORECASE)
if 'DEFAULT_DUST_THRESHOLD' in config['core']:
	DEFAULT_DUST_THRESHOLD_re = re.compile(r"(const uint64_t DEFAULT_DUST_THRESHOLD\s+=\s+UINT64_C\()\d+\)", re.IGNORECASE)
if 'MAX_BLOCK_SIZE_INITIAL' in config['core']:
	MAX_BLOCK_SIZE_INITIAL_re = re.compile(r"(const size_t\s+MAX_BLOCK_SIZE_INITIAL\s+=)\s+\d+ \* \d+", re.IGNORECASE)

for line in fileinput.input([paths['cryptonote_config']], inplace=True):
	line = CRYPTONOTE_NAME_re.sub("\\1 \"%s\"" % config['core']['CRYPTONOTE_NAME'], line)
	line = P2P_DEFAULT_PORT_re.sub("\\1 %s" % config['core']['P2P_DEFAULT_PORT'], line)
	line = RPC_DEFAULT_PORT_re.sub("\\1 %s" % config['core']['RPC_DEFAULT_PORT'], line)
	line = P2P_STAT_TRUSTED_PUB_KEY_re.sub("\\1 \"%s\"" % config['core']['P2P_STAT_TRUSTED_PUB_KEY'], line)
	line = CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX_re.sub("\\1 %s" % config['core']['CRYPTONOTE_PUBLIC_ADDRESS_BASE58_PREFIX'], line)
	if 'MONEY_SUPPLY' in config['core']:
		line = MONEY_SUPPLY_re.sub("\\1 %s" % config['core']['MONEY_SUPPLY'], line)
	if 'EMISSION_SPEED_FACTOR' in config['core']:
		line = EMISSION_SPEED_FACTOR_re.sub("\\1 %s" % config['core']['EMISSION_SPEED_FACTOR'], line)
	if 'DIFFICULTY_TARGET' in config['core']:
		line = DIFFICULTY_TARGET_re.sub("\\1 %s" % config['core']['DIFFICULTY_TARGET'], line)
	if 'COIN' in config['core']:
		line = COIN_re.sub("\\1 %s)" % config['core']['COIN'], line)
	if 'CRYPTONOTE_DISPLAY_DECIMAL_POINT' in config['core']:
		line = CRYPTONOTE_DISPLAY_DECIMAL_POINT_re.sub("\\1 %s" % config['core']['CRYPTONOTE_DISPLAY_DECIMAL_POINT'], line)
	if 'MINIMUM_FEE' in config['core']:
		line = MINIMUM_FEE_re.sub("\\1 %s)" % config['core']['MINIMUM_FEE'], line)
	if 'DEFAULT_DUST_THRESHOLD' in config['core']:
		line = DEFAULT_DUST_THRESHOLD_re.sub("\\1 %s)" % config['core']['DEFAULT_DUST_THRESHOLD'], line)
	if 'MAX_BLOCK_SIZE_INITIAL' in config['core']:
		line = MAX_BLOCK_SIZE_INITIAL_re.sub("\\1 %s" % config['core']['MAX_BLOCK_SIZE_INITIAL'], line)
	if 'UPGRADE_HEIGHT' in config['core']:
		line = UPGRADE_HEIGHT_re.sub("\\1 %s" % config['core']['UPGRADE_HEIGHT'], line)
	else:
		line = UPGRADE_HEIGHT_re.sub("\\1 %s" % "1", line)

	# sys.stdout is redirected to the file
	sys.stdout.write(line)


SEED_NODES_re = re.compile(r"(const char\* const\s+SEED_NODES\[\] = {)[^;]+(};)", re.DOTALL)
CHECKPOINTS_re = re.compile(r"(const CheckpointData\s+CHECKPOINTS\[\] = {)[^;]+(};)", re.DOTALL)
cryptonote_config_file = open(paths['cryptonote_config'],'r')
cryptonote_config_content = cryptonote_config_file.read()
cryptonote_config_file.close()
cryptonote_config_content = SEED_NODES_re.sub("\\1 %s \\2" % config['core']['SEED_NODES'], cryptonote_config_content)
cryptonote_config_content = CHECKPOINTS_re.sub("\\1 %s \\2" % config['core']['CHECKPOINTS'], cryptonote_config_content)
cryptonote_config_file = open(paths['cryptonote_config'], "w")
cryptonote_config_file.write(cryptonote_config_content)
cryptonote_config_file.close()


# Make changes in src/cryptonote_core/Currency.cpp
paths['Currency'] = args.source + "/src/cryptonote_core/Currency.cpp"
genesisCoinbaseTxHex_re = re.compile(r"(std::string genesisCoinbaseTxHex =) \"\S+\";", re.IGNORECASE)
for line in fileinput.input(paths['Currency'], inplace=True):
	line = genesisCoinbaseTxHex_re.sub("\\1 \"%s\";" % config['core']['genesisCoinbaseTxHex'], line)
	# sys.stdout is redirected to the file
	sys.stdout.write(line)


# Make changes in src/p2p/p2p_networks.h
paths['p2p_networks'] = args.source + "/src/p2p/p2p_networks.h"

BYTECOIN_NETWORK_re = re.compile(r"(const static boost::uuids::uuid BYTECOIN_NETWORK =) { {[^;]+} };", re.IGNORECASE)
for line in fileinput.input(paths['p2p_networks'], inplace=True):
	line = BYTECOIN_NETWORK_re.sub("\\1 { { %s} };" % config['core']['BYTECOIN_NETWORK'], line)
	# sys.stdout is redirected to the file
	sys.stdout.write(line)
