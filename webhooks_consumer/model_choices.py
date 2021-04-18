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
        factories = {self.TELEGRAM: TelegramMessageFactory, self.SLACK: SlackMessageFactory}
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
    
    CHOICES = (
        (DOGGO , "doggo"),
        (KITTY, "kitty"),
        (PET,"pet"),
        (FOX, "fox"),
        (COMPLIMENT, "compliment"),
        (INSULT, "insult"),
        (TACO, "taco"),
        (BROADCAST, "broadcast_message")
    )
    
    def get_kwargs(self, function_name):
        kwarg_dict = {"broadcast_message": ["sender", "message_text"]}
        return kwarg_dict.get(function_name)



