import json

# PS i am sorry for the lyrics I just had to do it

class Baby:
    def __init__(self, df=None):
        self.df = df

    def baby(self):
        songie = [
            "Baby, calm down, calm down",
            "Girl, this your body e put in my heart for lockdown, for lockdown, oh lockdown",
            "Girl, you sweet like Fanta ooh, Fanta ooh",
            "If I tell you, say, \"I love you,\" no dey form yanga oh, oh yanga oh",
            "No tell me no, no, no, no, woah, woah, woah, woah",
            "Oh, oh, oh, oh, oh, oh, oh, oh, oh, oh, oh",
            "Baby, come gimme your lo-lo-lo-lo-lo-lo-lo-lo-woah-woah-woah-woah-woah",
            "You got me like, \"woah-woah-woah-woah-woah-woah-woah-woah-woah\"",
            "Shawty come gimme your lo-lo-lo-lo-lo-lo-lo-lo-woah-woah-woah-woah-woah, mhmm",
            "I see this fine girl for my party, she wear yellow",
            "Every other girl they dey do too much but this girl mellow",
            "Naim I dey find situation I go use take tell am hello",
            "Finally I find way to talk to the girl but she no wan follow",
            "Who you come dey form for? (Mhmm)",
            "Why you no wan' conform? (Mhmm)",
            "Then I start to feel her bum-bum, warm (Mhmm)",
            "But she dey gimme small, small woah",
            "I know say she sabi pass that one, one (Mhmm)",
            "But she feeling insecure woah",
            "'Cause her friends go dey gum her like chewing gum (Mhmm)",
            "Go dey gum her like chewing gum, woah, woah, ooh",
            "As I reach my house I say make I rest small (Make a rest small)",
            "As me I wake up na she dey my mind, oh-woah (Na she dey my mind, oh-woah)",
            "Day one, day two-wo, I no fit focus (I no fit focus)",
            "Na so me I call am, say make we link up (I say make we link up)",
            "As I start to dey tell her how I feel, now my heart dey race",
            "Baby girl if you leave me I no go love again",
            "Because e get many girls wey put my heart for pain",
            "Shebi you feel my pain? Yeah, yeah"
        ]

        # Functionality to export to JSON
        self.export_to_json(songie)

    def export_to_json(self, lyrics):
        # Define the filename where the JSON will be saved
        filename = '../data/lyrics.json'
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(lyrics, file, ensure_ascii=False, indent=4)
        print("While I really hope you dont get bored during this process: I had to do this")
        print(f"Buddy you are in for a treat PS if you did not like it I am sorry for this, recruiter gimmi a job mann.")
        
if __name__ == "__main__":
	baby = Baby()
	baby.baby()

  