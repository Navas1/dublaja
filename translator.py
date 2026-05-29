from deep_translator import GoogleTranslator

def translate_segments(segments: list) -> list:
    """Traduz cada segmento de inglês para português brasileiro."""
    print(f"🌐 Traduzindo {len(segments)} segmentos...")

    translator = GoogleTranslator(source='en', target='pt')
    translated_segments = []

    for idx, seg in enumerate(segments):
        original = seg['text']
        try:
            translated = translator.translate(original)
        except Exception as e:
            print(f"⚠️ Erro segmento {idx}: {e}")
            translated = original

        translated_segments.append({
            'start': seg['start'],
            'end': seg['end'],
            'original': original,
            'translated': translated,
        })

        print(f"  [{idx+1}/{len(segments)}] {original[:40]}... → {translated[:40]}...")

    print(f"✅ {len(translated_segments)} segmentos traduzidos")
    return translated_segments
