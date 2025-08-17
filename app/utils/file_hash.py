import hashlib

class FileHash:

    async def calculate_file_hash(self, content: bytes) -> str:
        hash_obj = hashlib.sha256()
        hash_obj.update(content)
        return hash_obj.hexdigest()