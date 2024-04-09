import re 





# discord emojis






spinner = "<a:Spinning_wheel:1183400343011328011>"
middle_finger = "<a:MiddleFinger:1183357057387208724>"
sus_laugh = "<a:emoji702183399:1192068572869050383>"
searching = "<a:Searching:1192799729835323483> "



#discord character emojis





sanji = "<:Sanji:1183358095049625681>"
zoro = "<a:Zoro:1183409621281554564>"
nami = "<a:nami:1183358353515225088>"
robin = "<a:Robinn:1183364094678544505>"
chopper = "<a:ChopperStar:1183358589990092871>"
luffy = "<a:luffy:1183409233362944072>"
naruto = "<a:naruto:1183410266004787210>"
sakura = "<:Sakura:1183410705047748721>"
sasuke = "<a:sasuke:1183412476780499014>"
whitebeard = "<a:whitebeard:1183415954185670697>"
hinata ="<a:HinataSmile:1183419108360978514>"
kakashi = "<a:kakashi:1183419393040994354>"
madara = "<a:MadaraLaugh:1183420070639194205>"
itachi = "<a:itachi:1183439244576952351>"
izumi = "<:izumi:1183440020187660308>"
ace = "<a:acefire:1183440669625298946>"
brook = "<a:brook:1183441302071808132>"
obito = "<a:obito:1183442432667431003>"
rin = "<a:rin:1183449538321723422> "



emoji_pattern = re.compile(r"<(a?):(\w+):(\d+)>")

def emoji_to_url(emoji_string):
 match = emoji_pattern.match(emoji_string)
 if match:
    extension = ".gif" if match.group(1) else ".png"
    return f"https://cdn.discordapp.com/emojis/{match.group(3)}{extension}"
 return None

#name_url = emoji_to_url(name)
zoro_url = emoji_to_url(zoro)
sanji_url = emoji_to_url(sanji)
nami_url = emoji_to_url(nami)
middle_finger_url = emoji_to_url(middle_finger)
chopper_url = emoji_to_url(chopper)
robin_url = emoji_to_url(robin)
luffy_url = emoji_to_url(luffy)
naruto_url = emoji_to_url(naruto)
sakura_url = emoji_to_url(sakura)
sasuke_url = emoji_to_url(sasuke)
whitebeard_url = emoji_to_url(whitebeard)
hinata_url = emoji_to_url(hinata)
kakashi_url = emoji_to_url(kakashi)
madara_url = emoji_to_url(madara)
itachi_url = emoji_to_url(itachi)
izumi_url = emoji_to_url(izumi)
ace_url = emoji_to_url(ace)
brook_url = emoji_to_url(brook)
obito_url = emoji_to_url(obito)
rin_url = emoji_to_url(rin)