from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.competition.models import Competition, Category, Participant, CompetitionTexts, CompetitionMaps
from apps.competition.api.v1.qrcode import generate_qrcode
import qrcode


class CompetitionTextsInline(admin.TabularInline):
    model = CompetitionTexts
    extra = 1


class CompetitionMapsInline(admin.TabularInline):
    model = CompetitionMaps
    extra = 1


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionMapsInline, CompetitionTextsInline]
    list_display = ('title', 'category', 'distance', 'status', 'period', 'members')
    filter_horizontal = ('partners',)


# class ParticipantAdmin(ImportExportModelAdmin):
#     list_display = ('user', 'competition', 'choice', 'personal_id', 'duration', 'is_active',)
#     date_hierarchy = 'created_at'
#     readonly_fields = ('created_at',)



class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 1


class CompetitionMapsAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]
    list_display = ('competition', 'title', 'set_position')


class ParticipantAdmin(ImportExportModelAdmin):
    list_display = ('user', 'competition')
    search_fields = ('competition__title', 'choice__title', 'user__first_name', 'user__last_name')
    list_filter = ('choice',)
    actions = ['generate_qrcodes']

    def generate_qrcodes(self, request, queryset):
        for participant in queryset:
            if not participant.qr_code:
                qr_img = qrcode.make(f"{participant.user.first_name} {participant.user.last_name}")
                qr_code_path = f"qr-img-{participant.id}.jpg"
                qr_img.save(qr_code_path)
                participant.qr_code = qr_code_path
                participant.save()
                self.message_user(request, f"Generated QR code for {participant.user.id}")
            else:
                self.message_user(request, f"QR code already generated for {participant.user.id}")

    generate_qrcodes.short_description = "Generate QR codes for selected participants"




admin.site.register(CompetitionMaps, CompetitionMapsAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Category)
admin.site.register(Participant, ParticipantAdmin)
