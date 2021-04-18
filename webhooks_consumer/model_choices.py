from .factory import SlackMessageFactory, TelegramMessageFactory

class PlatformChoices:
    TELEGRAM = "TLGRM"
    SLACK = "SLCK"
    
    CHOICES = (
        (TELEGRAM, "Telegram"),
        (SLACK, "Slack"),
    )

    @staticmethod
    def get_factory(abbrv):
        factories = {"TLGRM": TelegramMessageFactory,"SLCK": SlackMessageFactory}
        return factories.get(abbrv)
    
class FunctionChoices:
    DOGGO = "doggo"
    KITTY = "kitty"
    PET = "pet"
    FOX = "fox"
    COMPLIMENT = "compliment"
    INSULT = "insult"
    TACO = "taco"
    BROADCAST = "broadcast_message"
    DUCK = "duck"
    BUNNY = "bunny" # doesn't work without js
    SLOTH = "sloth" # doesn't work without js

    CHOICES = (
        (DOGGO , "doggo"),
        (KITTY, "kitty"),
        (PET,"pet"),
        (FOX, "fox"),
        (COMPLIMENT, "compliment"),
        (INSULT, "insult"),
        (TACO, "taco"),
        (BROADCAST, "broadcast_message"),
        (DUCK, "duck"),
        (SLOTH, "sloth")
    )
    
    def get_kwargs(self, function_name):
        kwarg_dict = {"broadcast_message": ["sender", "message_text"]}
        return kwarg_dict.get(function_name)



