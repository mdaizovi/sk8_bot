from django.contrib.auth.models import Group

from .models import InputSource, OutputChannel


simple_admins = [
    "BotAction", "BotOutput"
]
import_str = "from django.contrib import admin\nfrom .models import {}".format(
    ", ".join([m for m in simple_admins])
)
if import_str[-1] == ",":
    import_str = import_str[:-1]
exec(import_str)

for s in simple_admins:
    exec(
        "@admin.register({})\nclass {}Admin(admin.ModelAdmin):\n\tpass".format(s, s, s)
    )


admin.site.unregister(Group)


@admin.register(InputSource)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "enviro")
    list_filter = ("enviro", "platform")


@admin.register(OutputChannel)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "enviro")
    list_filter = ("enviro", "platform")
