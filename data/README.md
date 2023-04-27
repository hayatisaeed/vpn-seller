# DataBase Structures

## users-info.json

This database keeps: chat_id: {number of baught configs, number of commissions, user_credit, sale_credit}

## servers.json
This database keeps:  
    server_domain: {panel_link, user_name, password}

## user-configs.json
This database keeps:
    chat_id: {config_id: config_uuid}
    
## messages.json
keeps ids of messages which should be copied to users.

## packages.json
the packages in which the admin has set.

## configs.json
message_id of configs available or sold. admin sends them to the bot and should not delete them from chat.

## users.json
determines wheter the user is hamkar or not. and determines the percentage of price that bot has to get from the user when user wants to buy a config. and also accepted the rules and joined channel or not.