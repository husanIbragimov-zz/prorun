from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.competition.models import Competition, Category, Participant, CompetitionTexts, CompetitionMaps


class CompetitionTextsInline(admin.TabularInline):
    model = CompetitionTexts
    extra = 1


class CompetitionMapsInline(admin.TabularInline):
    model = CompetitionMaps
    extra = 1


class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionMapsInline, CompetitionTextsInline]
    list_display = ('title', 'category', 'distance', 'status', 'period', 'members')


class ParticipantAdmin(ImportExportModelAdmin):
    list_display = ('user', 'competition', 'choice', 'personal_id', 'duration', 'is_active',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)



class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 1


class CompetitionMapsAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]
    list_display = ('competition', 'title')


#
# class CompetitionTextsInline(admin.TabularInline):
#     model = CompetitionTexts
#     extra = 1
#
#
# class CompetitionDetailAdmin(admin.ModelAdmin):
#     inlines = [ParticipantInline, CompetitionTextsInline]
#     list_display = ('competition', 'title', 'created_at')
#     date_hierarchy = 'created_at'
#     readonly_fields = ('created_at',)
#
#
# class CompetitionMapsInline(admin.StackedInline):
#     model = CompetitionMaps
#     extra = 1


# class CompetitionAdmin(admin.ModelAdmin):
#     inlines = [CompetitionMapsInline]
#     list_display = ('title', 'category', 'distance', 'status', 'period', 'members')
#     list_filter = ('status',)
#     search_fields = ('title', 'category__title')


admin.site.register(CompetitionMaps, CompetitionMapsAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Category)
admin.site.register(Participant, ParticipantAdmin)
