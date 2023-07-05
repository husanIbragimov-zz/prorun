from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.competition.models import Competition, Category, Participant, CompetitionDetail, TextDetail


class ParticipantAdmin(ImportExportModelAdmin):
    list_display = ('participant', 'competition', 'duration', 'overrun', 'is_active',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    class Meta:
        model = Participant


class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 1


class TextDetailInline(admin.TabularInline):
    model = TextDetail
    extra = 1


class CompetitionDetailAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline, TextDetailInline]
    list_display = ('competition', 'title', 'created_at', 'is_active')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


class CompetitionDetailInline(admin.StackedInline):
    model = CompetitionDetail
    extra = 1


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionDetailInline]
    list_display = ('title', 'category', 'distance', 'status', 'period', 'members', 'free_places', 'time_limit')
    list_filter = ('status',)
    search_fields = ('title', 'category__title')


admin.site.register(CompetitionDetail, CompetitionDetailAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Category)
admin.site.register(Participant, ParticipantAdmin)
