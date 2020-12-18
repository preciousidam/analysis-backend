import os
import os.path as op
from flask_admin.form.upload import FileUploadField
from wtforms.validators import ValidationError
from flask_admin.babel import gettext

import cloudinary
import cloudinary.uploader as uploader

class CLoudinaryFileUploadField(FileUploadField):
    cloudinary.config(
            cloud_name = os.getenv('CLOUD_NAME'),  
            api_key = os.getenv('CLOUD_API_KEY'),  
            api_secret = os.getenv('CLOUD_API_SECRET')
        )

    def pre_validate(self, form):
        if self._is_uploaded_file(self.data) and not self.is_file_allowed(self.data.filename):
            raise ValidationError(gettext('Invalid file extension'))

        # Handle overwriting existing content
        if not self._is_uploaded_file(self.data):
            return

        if not self._allow_overwrite and 'public_id' in uploader.explicit(f'reports/{self.data.filename}', type='upload'):
            raise ValidationError(gettext('File "%s" already exists.' % self.data.filename))

    def _delete_file(self, filename):
        print(filename)
        uploader.destroy(f'reports/{filename}')
    

    def _save_file(self, data, filename):
        print(data)
        
        file = uploader.upload(data.read(), 
            resource_type = "raw", 
            public_id=f'reports/{filename}', 
            overwrite=self._allow_overwrite
        )
        #data.save(path)
        print(file)

        return file['public_id']