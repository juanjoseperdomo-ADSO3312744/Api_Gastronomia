"""
Punto de entrada estándar para el servidor ASGI (Uvicorn).
Permite ejecutar directamente: uvicorn app.main:app --reload
"""
from app.j_main import j_app

# Alias estándar para uvicorn
app = j_app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
