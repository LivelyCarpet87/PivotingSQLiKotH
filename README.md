# PivotingSQLiKotH
 A SQL injection king of the hill that requires teams to pivot and coordinate their attacks.

# Customization

## Credentials
Credentials and keys for the server can be found in the creds.py file.

## Other Default Values

The rest of the game data can be found in the data.py file. This server will use values from this file IF AND ONLY IF the server save file serverData.json does not exist.

## Adding Players

Team members can be added via the url /adminPanel once the server is launched, added by altering the serverData.json BEFORE STARTING THE SERVER, or by using the Load Data section of the /adminPanel. More admin panel documentation below.

## Local File Inclusion Simulation

The Local File Inclusion simulated file directory can be found under the LFI folder. The server will traverse this directory when simulating a LFI vulnerability. Please don't touch the /etc/* files unless you know how the code works to prevent breaking the simulated LFI vulnerabilities.

# Admin Panel

This page can be found at `/adminPanel` and is not listed in the links. The server does NOT use SSL by default, so MAKE SURE THAT YOUR CONNECTION CANNOT BE SNIFFED or that your players are incapable of sniffing with apps like Wireshark.

## Adding/Removing Members

These two forms allows the admin to add or remove players. The admin can input the player's username, password and name (reserved for future use, and to aid identifying players). The players can log in with their given credentials once added. Adding a player repeatedly will overwrite previous additions. Player removal will remove their data.

## Leak

This form will leak the password and possibly the username of the node whose ID was given on the forums page. The leak cannot be undone and will be done subtly in a stack trace. This is useful for overturning node possession indirectly.

## Data

This returns the current version of ALL server data in compact JSON form. DO NOT SHOW IT TO GAME PARTICIPANTS. IT CONTAINS ALL USER PASSWORDS, NODE PASSWORDS, JWT SIGNING KEY, AND ADMIN PANEL PASSWORD.

## Log

Returns the most verbose log file. it is useful for remote debugging.

## Launch Game

This form launches or disables all competitive elements of the game. Users will be able to attack devices their team does not possess, and the score bot will begin to tally points. This is False by default and its state will be toggled each time it is submitted.

## Load Data

This is the quickest way to break the game. BE CAREFUL.  The server will parse the data it received as JSON. It will look for variables given in data.py, and replace the values of each variable with the value it finds in the given JSON data. It is the only way to modify JWT Key, points, scorebotInterval, modifierDivider, and products listing. It can be used to batch load users. BUT IT CAN QUICKLY CORRUPT THE SERVER DATA AND RUIN THE SAVE STATE.
