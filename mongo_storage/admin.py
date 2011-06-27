
from django import template
from django.core.exceptions import PermissionDenied
from django.db import router
from django.shortcuts import render_to_response
from django.template.defaultfilters import filesizeformat
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _

from django.contrib.admin.util import get_deleted_objects, model_ngettext
from django.contrib.admin import helpers

__all__ = ('DeleteActionMixin', 'MongoFileAdminMixin')

class DeleteActionMixin(object):
    """
    The regular Django admin's "delete selected models" action calls a
    delete on the model queryset, which bypasses the model's delete method.
    (https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/)

    If you're using the MongoDeleteFileModel in your model, you won't
    be able to delete items in bulk using the 'delete selected...' without
    adding this mixin to your admin. It will delete the django model, but
    leave the file still in django.

    Django Admin is awesome, but some things are not written very extensibly.
    The only thing this method does differently than the normal is it
    moves the delete from 'queryset.delete()' to obj.delete() inside the
    for loop.

    Usage:
    class MyModelAdmin(DeleteActionMixin, admin.ModelAdmin):
        actions = ['delete_selected']
    """

    def delete_selected(self, request, queryset):
        """
        Default action which deletes the selected objects.

        This action first displays a confirmation page whichs shows all the
        deleteable objects, or, if the user has no permission one of the related
        childs (foreignkeys), a "permission denied" message.

        Next, it delets all selected objects and redirects back to the change list.
        """
        opts = self.model._meta
        app_label = opts.app_label

        # Check that the user has delete permission for the actual model
        if not self.has_delete_permission(request):
            raise PermissionDenied

        using = router.db_for_write(self.model)

        # Populate deletable_objects, a data structure of all related objects that
        # will also be deleted.
        deletable_objects, perms_needed, protected = get_deleted_objects(
            queryset, opts, request.user, self.admin_site, using)

        # The user has already confirmed the deletion.
        # Do the deletion and return a None to display the change list view again.
        if request.POST.get('post'):
            if perms_needed:
                raise PermissionDenied
            n = queryset.count()
            if n:
                for obj in queryset:
                    obj_display = force_unicode(obj)
                    self.log_deletion(request, obj, obj_display)
                    obj.delete()
                self.message_user(request, _("Successfully deleted %(count)d %(items)s.") % {
                    "count": n, "items": model_ngettext(self.opts, n)
                })
            # Return None to display the change list page again.
            return None

        if len(queryset) == 1:
            objects_name = force_unicode(opts.verbose_name)
        else:
            objects_name = force_unicode(opts.verbose_name_plural)

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {"name": objects_name}
        else:
            title = _("Are you sure?")

        context = {
            "title": title,
            "objects_name": objects_name,
            "deletable_objects": [deletable_objects],
            'queryset': queryset,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": opts,
            "root_path": self.admin_site.root_path,
            "app_label": app_label,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }

        # Display the confirmation page
        return render_to_response(self.delete_selected_confirmation_template or [
            "admin/%s/%s/delete_selected_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_selected_confirmation.html" % app_label,
            "admin/delete_selected_confirmation.html"
        ], context, context_instance=template.RequestContext(request))
    delete_selected.short_description = "Delete selected %(verbose_name_plural)s"


class MongoFileAdminMixin(object):
    """
    A couple methods that make the files properties more accessible
    to the Admin for use in list_display mode or something similar.

    Usage:
    class MyFileAdmin(MongoFileAdminMixin, admin.ModelAdmin):
        list_display = ['file_name', 'file_size']

    """

    def file_name(self, obj):
        return obj.content.file_name

    def file_size(self, obj):
        return filesizeformat(obj.content.size)
