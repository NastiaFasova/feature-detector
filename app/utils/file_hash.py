"""
File hashing utility for generating secure hash identifiers.
"""
import hashlib

from starlette.requests import Request


class FileHash:

    async def calculate_file_hash(self, content: bytes) -> str:
        hash_obj = hashlib.sha256()
        hash_obj.update(content)
        return hash_obj.hexdigest()

    async def extract_file_hash_from_request(self, request: Request) -> str:
        file_hash = ""
        content_type = request.headers.get("content-type", "")

        if content_type.startswith("multipart/form-data"):
            try:
                form_data = await request.form()
                print('form_data', form_data)

                for field_name, field_value in form_data.items():

                    if hasattr(field_value, 'read') and hasattr(field_value, 'filename'):
                        file_content = await field_value.read()
                        file_hash = hashlib.sha256(file_content).hexdigest()
                        break
            except Exception as e:
                print(f"Error extracting file hash: {e}")
        return file_hash