import os

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage


class MyStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """
        Return a filename that's free on the target storage system and
        available for new content to be written to.
        """
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        # If the filename already exists, add an underscore and a random 7
        # character alphanumeric string (before the file extension, if one
        # exists) to the filename until the generated filename doesn't exist.
        # Truncate original name if required, so the new filename does not
        # exceed the max_length.
        num = 0
        while self.exists(name) or (max_length and len(name) > max_length):
            num += 1
            # file_ext includes the dot.
            name = os.path.join(dir_name, "%s-%s%s" % (file_root, str(num).zfill(2), file_ext))
            if max_length is None:
                continue
            # Truncate file_root if max_length exceeded.
            truncation = len(name) - max_length
            if truncation > 0:
                file_root = file_root[:-truncation]
                # Entire file_root was truncated in attempt to find an available filename.
                if not file_root:
                    raise SuspiciousFileOperation(
                        'Storage can not find an available filename for "%s". '
                        'Please make sure that the corresponding file field '
                        'allows sufficient "max_length".' % name
                    )
                name = os.path.join(dir_name, "%s-%s%s" % (file_root, str(num).zfill(2), file_ext))
        return name
