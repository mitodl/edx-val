"""
Admin file for django app edxval.
"""
from django import forms
from django.contrib import admin

from .models import (CourseVideo, EncodedVideo, Profile, TranscriptPreference,
                     Video, VideoImage, VideoTranscript)


class ProfileAdmin(admin.ModelAdmin):  # pylint: disable=C0111
    list_display = ('id', 'profile_name')
    list_display_links = ('id', 'profile_name')
    admin_order_field = 'profile_name'


class EncodedVideoInline(admin.TabularInline):  # pylint: disable=C0111
    model = EncodedVideo


class CourseVideoInline(admin.TabularInline):  # pylint: disable=C0111
    model = CourseVideo
    extra = 0
    verbose_name = "Course"
    verbose_name_plural = "Courses"


class VideoAdmin(admin.ModelAdmin):  # pylint: disable=C0111
    list_display = (
        'id', 'edx_video_id', 'client_video_id', 'duration', 'created', 'status'
    )
    list_display_links = ('id', 'edx_video_id')
    search_fields = ('id', 'edx_video_id', 'client_video_id')
    list_per_page = 50
    admin_order_field = 'edx_video_id'
    inlines = [CourseVideoInline, EncodedVideoInline]


class VideoImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('course_video', )
    list_display = ('get_course_video', 'image', 'generated_images')

    def get_course_video(self, obj):
        return u'"{course_id}" -- "{edx_video_id}" '.format(
            course_id=obj.course_video.course_id,
            edx_video_id=obj.course_video.video.edx_video_id
        )

    get_course_video.admin_order_field = 'course_video'
    get_course_video.short_description = 'Course Video'

    model = VideoImage

    verbose_name = 'Video Image'
    verbose_name_plural = 'Video Images'


class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'get_video_id', 'is_hidden')

    def get_video_id(self, obj):
        return obj.video.edx_video_id

    get_video_id.admin_order_field = 'video'
    get_video_id.short_description = 'edX Video Id'

    model = CourseVideo
    verbose_name = 'Course Video'
    verbose_name_plural = 'Course Videos'


class VideoTranscriptAdmin(admin.ModelAdmin):
    list_display = ('video_id', 'language_code', 'provider', 'file_format')

    model = VideoTranscript


class TranscriptPreferenceAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'provider', 'video_source_language', 'preferred_languages')

    model = TranscriptPreference


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(VideoTranscript, VideoTranscriptAdmin)
admin.site.register(TranscriptPreference, TranscriptPreferenceAdmin)
admin.site.register(VideoImage, VideoImageAdmin)
admin.site.register(CourseVideo, CourseVideoAdmin)
