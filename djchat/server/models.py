from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from server.validators import validate_icon_image_size, validate_image_file_extension


def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"


def channel_banner_upload_path(instance, filename):
    return f"channel/{instance.id}/channel_banners/{filename}"


def channel_icon_upload_path(instance, filename):
    return f"channel/{instance.id}/channel_icons/{filename}"


class Category(models.Model):
    # Name of the category (required, max length 100 characters)
    name = models.CharField(max_length=100)

    # Optional short description of the category (max 250 characters)
    description = models.CharField(max_length=250, blank=True, null=True)
    # Alternative: use TextField for longer descriptions
    # description = models.TextField(blank=True, null=True)

    # Optional file field for uploading an icon; stored using custom upload path
    icon = models.FileField(upload_to=category_icon_upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to delete the old icon file
        from storage if the icon is being changed.
        """
        if self.id:
            # Fetch the existing instance from the database
            existing = get_object_or_404(Category, id=self.id)
            # If the icon has been changed, delete the old file
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        # Proceed with the normal save operation
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, *args, **kwargs):
        """
        Signal handler that runs before a Category instance is deleted.
        It ensures the associated file (icon) is also deleted from storage.
        """
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(
                        save=False
                    )  # Deletes the file without saving the model again

    def __str__(self):
        # String representation of the category instance
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="channel_owner",
    )
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )
    banner = models.ImageField(
        upload_to=channel_banner_upload_path,
        null=True,
        blank=True,
        validators=[validate_image_file_extension],
    )
    icon = models.ImageField(
        upload_to=channel_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if self.id:
            existing = get_object_or_404(Channel, id=self.id)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(Channel, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Channel")
    def channel_delete_files(sender, instance, *args, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name
