# vpn-seller
A python telegram bot to sell v2ray vpn accounts.

## General:
* needs a channel to send payment logs.
* needs a channel to send start logs.

ADMIN sends configs to the bot, and bot sells them.

## ADMIN Panel:
* brodcast messages (send a message to all users)
* send message to a user
* statistics (number of users, number of sells, summation of sell)
* add, remove and edit plans (categories)
* send configs for a specific category (plan)
* block / unblock a specific user
* information of a specific user (number of buys, summation of buy, configs) and edit them
* set percentage of money that the user has to pay when he wants to buy a config.
* set some users as hamkar, so can brodcast messages to only hamkars or normal users.
* verify users payment, then accept them or not by one click.

## USER Panel:
* channel lock (has to be joined to specified channel before using the bot) ✅
* visit packages (categories)
* buy config
* wallet and charging it
* get test
* information of account (my configs, my id, etc)
* help
* visit configs data (GB, Exp)
* send message to admin ✅

