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
        factories = {"TLGRM": TelegramMessageFactory,
                     "SLCK": SlackMessageFactory}
        return factories.get(abbrv)


class EnvChoices:
    DEVELOPMENT = "D"
    PRODUCTION = "P"

    CHOICES = (
        (DEVELOPMENT, "Development"),
        (PRODUCTION, "Production"),
    )


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
    SLOTH = "sloth"
    BOOTIE = "bootie"  # example for showing newbies how to write a simple input/output

    CHOICES = (
        (DOGGO, "doggo"),
        (KITTY, "kitty"),
        (PET, "pet"),
        (FOX, "fox"),
        (COMPLIMENT, "compliment"),
        (INSULT, "insult"),
        (TACO, "taco"),
        (BROADCAST, "broadcast_message"),
        (DUCK, "duck"),
        (SLOTH, "sloth"),
        (BOOTIE, "bootie")
    )

    def get_kwargs(self, function_name):
        kwarg_dict = {"broadcast_message": ["sender", "message_text"]}
        return kwarg_dict.get(function_name)
