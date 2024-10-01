forest_map = {
    'Campsite': {
        'description': "You are at the campsite, where your adventure begins. To your north are the dark woods which you have to escape. There is a half torn paper lying on the ground. ", 
        'exits': {
            'north': 'Dark Woods'
            }, 
        'clue': "Carry light to find your way.", 
        'items': ['Match', "Lantern"]
        },
    'Dark Woods': {
        'description': "You are in the dark woods. Strange noises are all around. There is something written on the tree.", 
        'exits': {
            'south': 'Campsite', 
            'east': 'Old Cabin',
            'west': 'Small Hut', 
            'north': 'Riverbank', 
            }, 
        'clue1': "The wind whispers of an old cabin to the east.",
        'clue2': "Looks like there is something shining in the bushes.",
        'clue3': "There is a strange nest on the tree on which this was written, 'The wind whispers of an old cabin to the east.'",
        'clue4': "There is a path behind the bushes.",

        'items': ["key","jewel"]
        },
    'Small Hut':{
        'description': "A small wooden hut, Looks like there is something in the hut. ",
        'exits':{
            'east':'Dark Woods'
        },
        'item': ['Shovel', 'jewel']
    },    
    'Old Cabin': {
        'description': "An old, abandoned cabin. It looks like no one has been here for years. Its locked! Looks like it needs a key to open.", 
        'exits': {
            'west': 'Dark Woods'
            },  
        'clue': "Something seems out of place near the fireplace.",
        'items': ['rare piece of a key.']
        },
    'Riverbank': {
        'description': "A fast-flowing river blocks your path. You can't cross without something to float on.", 
        'exits': {
            'east': 'Dark Woods', 
            }, 
        'items': ['raft'],
        'clue': 'There is a wooden object on the bank. Its half under the ground. Maybe be you can dig the ground a bit and get it out. '
        },
    'Witch’s Hut': {
        'description': "You stand before a creepy hut in the woods. The witch offers you a challenge.", 
        'exits': { 
            'north': 'Hidden Cave'
            },  
        },
    'Hidden Cave': {
        'description': "Looks like its a hidden cave.", 
        'exits': {
            'south': 'Witch’s Hut',
            'north': 'Tunnel(Escape)'
            },  
        'items': ['ancient box'],
        'clue0':'A tree seems to be blocking some entrance. You can use the axe to cut down the tree.',
        'clue1':'There is something written on the wall.',
        'clue2': "There is a strange wall hanging in the cave." 
        },

    'Tunnel': {
        'description': "There is light at the end of this tunnel. It is the escape point"
    }    
}