import re
from typing import Optional, List
from deep_translator import MyMemoryTranslator, GoogleTranslator

class TranslatorService:
    _instance = None
    _cache = {}

    def __init__(self):
        self.mymemory = MyMemoryTranslator(source='en-US', target='vi-VN')

    @classmethod
    def get_instance(cls) -> "TranslatorService":
        if cls._instance is None:
            cls._instance = TranslatorService()
        return cls._instance

    def _split_into_chunks(self, text: str, max_chunk_size: int = 400) -> List[str]:
        if len(text) <= max_chunk_size:
            return [text]

        paragraphs = text.split("\n")
        chunks = []

        for p in paragraphs:
            if not p.strip():
                chunks.append("")
                continue

            if len(p) <= max_chunk_size:
                chunks.append(p)
            else:
                sentences = re.split(r"(?<=[.!?;\n])\s+", p)
                current = ""
                for s in sentences:
                    if not s:
                        continue
                    if len(current) + len(s) + 1 <= max_chunk_size:
                        current = (current + " " + s).strip() if current else s
                    else:
                        if current:
                            chunks.append(current)
                        if len(s) > max_chunk_size:
                            words = s.split(" ")
                            sub_cur = ""
                            for w in words:
                                if len(sub_cur) + len(w) + 1 <= max_chunk_size:
                                    sub_cur = (sub_cur + " " + w).strip() if sub_cur else w
                                else:
                                    if sub_cur:
                                        chunks.append(sub_cur)
                                    sub_cur = w
                            if sub_cur:
                                chunks.append(sub_cur)
                            current = ""
                        else:
                            current = s
                if current:
                    chunks.append(current)

        return chunks

    def translate_en_to_vi(self, text: str) -> str:
        if not text or not text.strip():
            return text

        cache_key = text.strip()
        if cache_key in self._cache:
            return self._cache[cache_key]

        chunks = self._split_into_chunks(text, max_chunk_size=400)
        translated_chunks = []

        for chunk in chunks:
            if not chunk or not chunk.strip():
                translated_chunks.append("")
                continue

            translated = None
            try:
                translated = self.mymemory.translate(chunk)
            except Exception:
                pass

            if not translated:
                try:
                    translated = GoogleTranslator(source='auto', target='vi').translate(chunk)
                except Exception:
                    pass

            if not translated:
                translated = chunk

            translated_chunks.append(translated)

        result = "\n".join(translated_chunks) if "\n" in text else " ".join(translated_chunks)
        if len(self._cache) > 300:
            self._cache.clear()
        self._cache[cache_key] = result
        return result

def translate_en_to_vi(text: str) -> str:
    return TranslatorService.get_instance().translate_en_to_vi(text)
