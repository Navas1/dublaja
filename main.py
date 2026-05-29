import sys
import uvicorn
from api import app

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Modo CLI direto
        url = input("🔗 Cole o link do YouTube: ").strip()
        if not url:
            print("❌ Nenhum link informado")
            return
        from pipeline import run_pipeline
        result = run_pipeline(url)
        print(f"\n🎉 Pronto! Arquivo: {result['output_path']}")
    else:
        # Modo API (padrão)
        print("\n🎧 DUBLAJÁ - Servidor Iniciado")
        print("📡 Acesse: http://localhost:8000")
        print("📡 Docs:   http://localhost:8000/docs")
        print("=" * 40)
        uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
