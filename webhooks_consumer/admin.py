simple_admins = [
    "Bot",
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
