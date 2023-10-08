from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resource import ParticipantResource
from apps.competition.api.v1.qrcode import check_qrcode
from apps.competition.models import Competition, Category, Participant, CompetitionTexts, CompetitionMaps, HistoryImage


class CompetitionTextsInline(admin.TabularInline):
    model = CompetitionTexts
    extra = 1


class CompetitionMapsInline(admin.TabularInline):
    model = CompetitionMaps
    extra = 1
    
class HistoryImageInline(admin.TabularInline):
    model = HistoryImage
    extra = 1


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionMapsInline, CompetitionTextsInline, HistoryImageInline]
    list_display = ('title', 'category', 'distance', 'status', 'period', 'members')
    filter_horizontal = ('partners',)


class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 1


class CompetitionMapsAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]
    list_display = ('competition', 'title', 'set_position')


class ParticipantAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ParticipantResource]
    list_display = ('user', 'competition')
    search_fields = ('competition__title', 'choice__title', 'user__first_name', 'user__last_name')
    list_filter = ('competition', 'choice',)
    actions = ['generate_qrcodes']

    def generate_qrcodes(self, request, queryset):
        for participant in queryset:
            check_qrcode(participant)
        self.message_user(request, f"QR codes generated successfully. {queryset.count()} participants.")

    generate_qrcodes.short_description = "Generate QR codes for selected participants"


admin.site.register(CompetitionMaps, CompetitionMapsAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Category)
admin.site.register(Participant, ParticipantAdmin)
